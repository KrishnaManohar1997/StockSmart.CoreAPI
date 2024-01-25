# ! RULES
# This Job is executed Everday @ 4:30 PM
# This worker helps in validating Each Post's Target
# It compares the price with the LTP of Ticker


import structlog

from common.constants.leaderboard_rewards import leaderboard_rewards
from common.helper.datetime_helper import DateTimeHelper
from post.models import Leaderboard, Post
from post.services import LeaderboardService
from stock.services import StockService
from stocksmart.celery import app
from user.tasks.user_success_rate_updater import user_success_rate_updater
from notification.services import NotificationService
from .notify_leaderboard_users import notify_leaderboard_users

logger = structlog.getLogger("django.server")

LEADERBOARD_MAX_USERS = 5
LEADERBOARD_REWARDMAP = leaderboard_rewards


def is_bullish_target_achieved(target, low, high):
    return (low <= target <= high) or (target < low)


def is_bearish_target_achieved(target, low, high):
    return (low <= target <= high) or (target > high)


def update_user_targets(user_target_dict, post, new_target_change):
    user_id = post.created_by_user_id
    user_target = user_target_dict.get(user_id)
    if not user_target:
        # Insert User target for first time
        user_target_dict[user_id] = {
            "price_change": new_target_change,
            "post_id": post.id,
            "date": post.signal_expire_at,
        }
        return

    # If a User's target is already present
    # Update based on his new Target Change
    if user_target["price_change"] < new_target_change:
        user_target_dict[user_id] = {
            "price_change": new_target_change,
            "post_id": post.id,
            "date": post.signal_expire_at,
        }


def sort_nested_dictionary_by_key(data, key: str, sort_by="desc", level=1):
    sorted_data = sorted(data.items(), key=lambda x: x[level][key])
    if sort_by == "desc":
        sorted_data.reverse()
    return sorted_data


def get_leaderboard_instance(user_id, post_data, signal_type):
    return Leaderboard(
        user_id=user_id,
        post_id=post_data["post_id"],
        percentage_change=post_data["price_change"],
        position=post_data["position"],
        date=post_data["date"],
        signal_type=signal_type,
        reward=LEADERBOARD_REWARDMAP.get(post_data["position"], 0),
    )


def update_leaderboard_users(bullish_target_dict, bearish_target_dict):
    top_bulls = sort_nested_dictionary_by_key(bullish_target_dict, key="price_change")
    top_bears = sort_nested_dictionary_by_key(bearish_target_dict, key="price_change")
    leaderboard_objs = []
    for position, (bull_user_id, post_data) in enumerate(
        top_bulls[:LEADERBOARD_MAX_USERS], 1
    ):
        post_data["position"] = position
        leaderboard_objs.append(
            get_leaderboard_instance(bull_user_id, post_data, Post.SignalType.BULLISH)
        )
    for position, (bear_user_id, post_data) in enumerate(
        top_bears[:LEADERBOARD_MAX_USERS], 1
    ):
        post_data["position"] = position
        leaderboard_objs.append(
            get_leaderboard_instance(bear_user_id, post_data, Post.SignalType.BEARISH)
        )
    leaderboard_service = LeaderboardService()
    leaderboard_service.bulk_create_items(leaderboard_objs)
    leaderboard_service.update_leaderboard_users_data_day(
        DateTimeHelper.get_asia_calcutta_time_now().date(), True, ttl=86400
    )
    logger.info("Leader Board Users are updated")


class PostTargetChecker:
    @staticmethod
    def process_targets(posts):
        bullish_target_dict, bearish_target_dict = {}, {}
        stock_symbols = list(posts.values_list("source__symbol", flat=True))
        symbol_stock_obj_map = {
            s.symbol: s
            for s in list(StockService().get_stocks_by_symbols(stock_symbols))
        }
        updated_post_objs = []

        for post in posts:
            ticker = symbol_stock_obj_map.get(post.source.get("symbol"))

            if post.signal_type == Post.SignalType.BULLISH:

                post.ticker_mkt_price_at_target = ticker.high
                target_price_percentage = (
                    (ticker.high - post.ticker_mkt_price_at_post)
                    / post.ticker_mkt_price_at_post
                ) * 100

                if (
                    not post.target_price > post.ticker_mkt_price_at_post
                    or not is_bullish_target_achieved(
                        post.target_price, ticker.low, ticker.high
                    )
                    or target_price_percentage < 1.0
                ):
                    post.is_target_reached = False
                    updated_post_objs.append(post)
                    continue
                post.is_target_reached = True
                update_user_targets(
                    bullish_target_dict,
                    post,
                    target_price_percentage,
                )

            else:
                # BEARISH CONDITION

                post.ticker_mkt_price_at_target = ticker.low
                target_price_percentage = (
                    (post.ticker_mkt_price_at_post - ticker.low) / ticker.low
                ) * 100

                if (
                    not post.target_price < post.ticker_mkt_price_at_post
                    or not is_bearish_target_achieved(
                        post.target_price, ticker.low, ticker.high
                    )
                    or target_price_percentage < 1.0
                ):
                    post.is_target_reached = False
                    updated_post_objs.append(post)
                    continue

                post.is_target_reached = True
                update_user_targets(
                    bearish_target_dict,
                    post,
                    target_price_percentage,
                )

            # Adds Every Target Reached Post Object
            # Non Target Met are added at Failed Stage
            updated_post_objs.append(post)
        update_leaderboard_users(bullish_target_dict, bearish_target_dict)
        Post.objects.bulk_update(
            updated_post_objs, ["is_target_reached", "ticker_mkt_price_at_target"]
        )

    @staticmethod
    def start():
        today_start, _ = DateTimeHelper.get_today_start_and_end()

        posts = Post.objects.filter(
            signal_expire_at=today_start.date(),
            source__ticker_type="Stock",
        )
        PostTargetChecker.process_targets(posts)

        user_success_rate_updater.delay(
            list(posts.values_list("created_by_user_id", flat=True))
        )

        NotificationService.send_post_target_notification.delay(
            list(posts.values_list("id", flat=True))
        )


@app.task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 3, "countdown": 5})
def post_target_processor():
    logger.info("Posts target validation Job Started")
    try:
        PostTargetChecker.start()
        logger.info("Posts target validation Job Processed Successfully")
        notify_leaderboard_users.delay()
    except Exception as error:
        logger.error(f"Posts target validation Job Failed --> {error}")
        # Propagate the Error Back for Retrying
        raise Exception("Retrying the Failed Job")
