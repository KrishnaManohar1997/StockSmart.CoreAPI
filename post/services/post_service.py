import string
from datetime import datetime
from decimal import Decimal
from enum import Enum
from random import choice
from uuid import uuid4

import structlog
from django.core.exceptions import ValidationError

from common.constants import exclude_ticker_target_list
from common.helper import uuid_to_str_list_converter
from common.helper.datetime_helper import DateTimeHelper
from mentions.services import MentionService, TickerMentionService
from post.models import Post
from post.repositories import PostRepository
from post.serializers import CreatePostSerializer
from smallcase.services.smallcase_service import SmallcaseService
from stock.services import StockService
from ticker.services.ticker_service import TickerService
from user.services import UserService

logger = structlog.getLogger("django.server")


class PostService:
    stock_service = StockService()
    smallcase_service = SmallcaseService()
    mention_service = MentionService()
    ticker_mention_service = TickerMentionService()
    user_service = UserService()
    post_repo = PostRepository()
    ticker_service = TickerService()
    explore_filter = None

    def __init__(self):
        self.explore_filter = {
            "recent": self.get_recent_post_feed,
            "popular": self.get_popular_post_feed,
            "engaged": self.get_most_engaged_post_feed,
            "targets": self.get_target_post_feed,
            "verified": self.get_verified_post_feed,
            "stocks": self.get_stock_post_feed,
            "smallcases": self.get_smallcase_post_feed,
        }

    # Currently Unused
    def generate_post_url(self, username, post_content, mentioned_tickers: list = None):
        URL_ALLOWED_CHARS = ["-", ".", "_", "~"] + list(
            string.ascii_letters + string.digits
        )
        if not post_content:
            return
        seo_content_url = ticker_url = ""
        words = post_content.split(" ")
        seo_content_url = "-".join(words[:4])
        if mentioned_tickers:
            ticker_url = "-".join(mentioned_tickers[:3]) + "-discussion"
            seo_content_url += "-" + ticker_url
        # Sanitizes the URL by removing Special Characters
        seo_content_url = "".join(x for x in seo_content_url if x in URL_ALLOWED_CHARS)
        if len(seo_content_url) > 72:
            seo_content_url = seo_content_url[: seo_content_url.rfind("-")]
        seo_content_url = seo_content_url.strip("-").replace("--", "-")[:30]
        return f"{username}_{seo_content_url}_{uuid4().hex[-8:]}"

    def generate_post_url_id(self):
        return "".join(choice((str.upper, str.lower))(c) for c in uuid4().hex)[
            : choice(range(28, 33))
        ]

    def __get_post_mentioned_tickers(self, mentioned_ticker_symbols):
        ticker_queryset = self.stock_service.get_stocks_by_symbols(
            mentioned_ticker_symbols
        )
        ticker_ids = ticker_queryset.values_list("id", flat=True)
        if len(mentioned_ticker_symbols) != len(ticker_ids):
            raise ValidationError("Invalid Stock Symbol", code=400)
        return ticker_ids, ticker_queryset

    def __get_post_mentioned_smallcases(self, mentioned_smallcase_symbols):
        smallcase_queryset = self.smallcase_service.get_smallcases_by_symbols(
            mentioned_smallcase_symbols
        )
        ticker_ids = smallcase_queryset.values_list("id", flat=True)
        if len(mentioned_smallcase_symbols) != len(ticker_ids):
            raise ValidationError("Invalid Smallcase Symbol", code=400)
        return ticker_ids, smallcase_queryset

    def __get_mentions_json(self, ticker_ids, user_ids, smallcase_ids):
        ticker_ids = uuid_to_str_list_converter(ticker_ids)
        user_ids = uuid_to_str_list_converter(user_ids)
        smallcase_ids = uuid_to_str_list_converter(smallcase_ids)
        return {
            "ticker_ids": ticker_ids,
            "user_ids": user_ids,
            "smallcase_ids": smallcase_ids,
        }

    def __validate_max_post_mentions(
        self, ticker_symbols, smallcase_symbols, mentioned_user_ids
    ):
        MAX_TICKER_MENTION_COUNT = 10
        MAX_USER_MENTION_COUNT = 5

        if MAX_TICKER_MENTION_COUNT < len(ticker_symbols) + len(smallcase_symbols):
            raise ValidationError(
                f"Ticker mentions cannot be more than {MAX_TICKER_MENTION_COUNT}"
            )

        if MAX_USER_MENTION_COUNT <= len(mentioned_user_ids):
            raise ValidationError(
                f"Cannot mention more than {MAX_USER_MENTION_COUNT} Users in a Post"
            )

    def __parse_target_price(self, target_price: str):
        target_price = Decimal(str(target_price))
        if (
            not target_price > 0
            or not target_price.as_tuple().exponent >= -2  # More than two Decimals
            or not int(float(target_price % 1) * 100) % 5
            == 0  # Decimal exactly divisible by 0.05
        ):
            raise ValidationError("Invalid Target price")
        return float(target_price)

    def __validate_ticker_target(self, request):
        # Removing target related fields
        # When the Ticker is not a Stock
        if request.data.get("source", {}).get("ticker_type", "") != "Stock":
            request.data.pop("target_price", None)
            request.data.pop("signal_expire_at", None)
            return

        target_price = request.data.get("target_price", None)
        target_date = request.data.get("signal_expire_at", None)

        # If None of the Target Fields are filled
        # Skip any other Validation
        if not any([target_price, target_date]):
            return

        if request.data["source"]["symbol"] in exclude_ticker_target_list:
            raise ValidationError("Sorry, we don't support targets on this Ticker")

        # If any one of the Value is Empty
        if any(x is None for x in [target_price, target_date]):
            raise ValidationError("Invalid Target Request")

        if not request.data.get("signal_type"):
            raise ValidationError("Specify Bullish/Bearish on Target")

        # Parsing Target Price and validation
        target_price = self.__parse_target_price(target_price)

        today_date = DateTimeHelper.get_asia_calcutta_date()
        formatted_target_date = datetime.strptime(target_date, "%d-%m-%Y").date()
        target_days_count = (formatted_target_date - today_date).days
        if target_days_count < 1 or target_days_count > 31:
            raise ValidationError("Invalid Target Expiry Date")

        request.data["signal_expire_at"] = formatted_target_date
        request.data["target_price"] = target_price

    def parse_mentioned_symbols(self, request_data):
        ticker_symbols = list(set(request_data.get("ticker_symbol_mentions", [])))
        smallcase_symbols = list(set(request_data.get("smallcase_symbol_mentions", [])))
        mentioned_user_ids = list(set(request_data.get("user_id_mentions", [])))
        return ticker_symbols, smallcase_symbols, mentioned_user_ids

    def create_post_from_request(self, request):
        source = request.data.get("source", None)
        if not source:
            logger.error("Missing Source attribute", request_data=request.data)
            raise ValidationError("Invalid Request")

        ticker_symbol, ticker_type = source.get("symbol"), source.get("tickerType")

        # Raises Validation Error if the Ticker is Invalid
        self.ticker_service.get_ticker_by_symbol(ticker_symbol, ticker_type)

        # Ingest Source data if Ticker Details are Valid
        request.data["source"] = {"ticker_type": ticker_type, "symbol": ticker_symbol}

        (
            ticker_symbols,
            smallcase_symbols,
            mentioned_user_ids,
        ) = self.parse_mentioned_symbols(request.data)

        if not ticker_symbols and not smallcase_symbols:
            raise ValidationError("At least a ticker should be tagged")

        # Source Ticker should be present in mentioned Tickers
        if not (ticker_symbol in ticker_symbols or ticker_symbol in smallcase_symbols):
            raise ValidationError("Invalid Request")

        self.__validate_max_post_mentions(
            ticker_symbols, smallcase_symbols, mentioned_user_ids
        )

        self.__validate_ticker_target(request)
        ticker_ids, stock_queryset, smallcase_ids, smallcase_queryset = [], [], [], []
        if ticker_symbols:
            ticker_ids, stock_queryset = self.__get_post_mentioned_tickers(
                ticker_symbols
            )
        if smallcase_symbols:
            smallcase_ids, smallcase_queryset = self.__get_post_mentioned_smallcases(
                smallcase_symbols
            )

        user_id_list, user_queryset = [], []
        if mentioned_user_ids:
            user_queryset = self.user_service.get_non_blocked_users_by_ids(
                mentioned_user_ids, request.user.id
            )
            user_id_list = list(user_queryset.values_list("id", flat=True))

        request.data["url"] = self.generate_post_url_id()
        request.data["created_by_user"] = request.user.id
        request.data["mentions"] = self.__get_mentions_json(
            ticker_ids, user_id_list, smallcase_ids
        )
        create_post_serializer = CreatePostSerializer(data=request.data)
        if not create_post_serializer.is_valid():
            return False, create_post_serializer
        post = create_post_serializer.save()
        self.mention_service.create_post_mentions(
            post, [*stock_queryset, *smallcase_queryset], user_queryset
        )
        return True, post

    def get_posts_by_filter(self, request):
        blocked_by_user_ids = self.user_service.get_blocked_by_user_ids(request.user.id)
        feed_type = request.query_params.get("type", "recent").lower()
        return self.explore_filter.get(feed_type)(blocked_by_user_ids)

    def get_recent_post_feed(self, blocked_by_user_ids=None):
        return self.post_repo.get_recent_post_feed(blocked_by_user_ids)

    def get_popular_post_feed(self, blocked_by_user_ids=None):
        return self.post_repo.get_popular_post_feed(blocked_by_user_ids)

    def get_most_engaged_post_feed(self, blocked_by_user_ids=None):
        return self.post_repo.get_most_engaged_post_feed(blocked_by_user_ids)

    def get_target_post_feed(self, blocked_by_user_ids=None):
        return self.post_repo.get_target_post_feed(blocked_by_user_ids)

    def get_verified_post_feed(self, blocked_by_user_ids=None):
        return self.post_repo.get_verified_post_feed(blocked_by_user_ids)

    def get_stock_post_feed(self, blocked_by_user_ids=None):
        return self.post_repo.get_stock_post_feed(blocked_by_user_ids)

    def get_smallcase_post_feed(self, blocked_by_user_ids=None):
        return self.post_repo.get_smallcase_post_feed(blocked_by_user_ids)

    def get_ticker_post_feed(self, requesting_user_id: str, ticker_symbol: str):
        ticker = self.stock_service.get_stock_by_symbol(ticker_symbol)
        if not ticker:
            raise ValidationError("Invalid Stock Ticker", code=404)
        blocked_by_user_ids = self.user_service.get_blocked_by_user_ids(
            requesting_user_id
        )
        return self.stock_service.get_stock_mention_posts(ticker, blocked_by_user_ids)

    def get_post_by_id_or_none(self, post_id: str):
        try:
            return self.post_repo.get_post_by_id(post_id)
        except Post.DoesNotExist:
            return None

    def update_post_reaction_count(self, post: Post, is_reaction_added: bool):
        self.post_repo.update_post_reaction_count(post, is_reaction_added)

    def update_comment_count(self, post: Post, is_comment_added: bool = True):
        self.post_repo.update_comment_count(post, is_comment_added)

    def get_post_by_url(self, post_url: str, requesting_user_id: str):
        blocked_by_user_ids = self.user_service.get_blocked_by_user_ids(
            requesting_user_id
        )
        return self.post_repo.get_post_by_url(post_url, blocked_by_user_ids)

    def delete_post(self, post) -> bool:
        return self.post_repo.delete_post(post)

    def get_posts_by_ids(self, post_ids):
        return self.post_repo.get_posts_by_ids(post_ids)
