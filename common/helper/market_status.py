from datetime import datetime, time, timedelta, timezone

import pytz
from django.conf import settings

from common.helper.datetime_helper import DateTimeHelper

TICKER_REFRESH_FREQUENCY = settings.TICKER_REFRESH_FREQUENCY

MARKET_HOLIDAY_CALENDAR = {
    "26-Jan-2022": "Republic Day",
    "01-Mar-2022": "Mahashivratri",
    "18-Mar-2022": "Holi",
    "14-Apr-2022": "Dr.Baba Saheb Ambedkar Jayanti/Mahavir Jayanti",
    "15-Apr-2022": "Good Friday",
    "03-May-2022": "Id-Ul-Fitr (Ramzan ID)",
    "09-Aug-2022": "Moharram",
    "15-Aug-2022": "Independence Day",
    "31-Aug-2022": "Ganesh Chaturthi",
    "05-Oct-2022": "Dussehra",
    "24-Oct-2022": "Diwali * Laxmi Pujan",
    "26-Oct-2022": "Diwali-Balipratipada",
    "08-Nov-2022": "Gurunanak Jayanti",
}

MARKET_OPEN_TIME = "09:15:00.00"
MARKET_END_TIME = "16:00:00.00"

tz = pytz.timezone("Asia/Calcutta")


def get_next_market_open_time():
    """Returns Next Market Open Time in Seconds"""
    cdt = DateTimeHelper.get_asia_calcutta_time_now()

    # If Market Doesn't open today
    # We will give the next Market Open Time on next day
    if will_market_open_today() is False:
        tom_time = cdt + timedelta(days=1)
        tom_market_open_date_time = datetime(
            tom_time.year,
            tom_time.month,
            tom_time.day,
            9,
            15,
            tzinfo=tz,
        )
        return (tom_market_open_date_time - cdt).total_seconds()

    # If Market is Open already
    # Frequency in seconds for refresh is returned
    if is_market_open():
        # 5 Seconds if market is Open
        return TICKER_REFRESH_FREQUENCY

    # Market Opens today in a Future Date Time
    market_open_date_time = get_today_market_open_time()
    return (market_open_date_time - cdt).total_seconds()


def get_today_market_open_time(as_utc: bool = False):
    cdt = DateTimeHelper.get_asia_calcutta_time_now()
    mkt_open_time = tz.localize(datetime(cdt.year, cdt.month, cdt.day, 9, 15))
    if as_utc:
        return mkt_open_time.astimezone(timezone.utc)
    return mkt_open_time


def get_today_market_close_time(as_utc: bool = False):
    cdt = DateTimeHelper.get_asia_calcutta_time_now()
    mkt_close_time = tz.localize(datetime(cdt.year, cdt.month, cdt.day, 15, 30))
    if as_utc:
        return mkt_close_time.astimezone(timezone.utc)
    return mkt_close_time


def get_yesterday_market_open_time(as_utc: bool = False):
    yesterday_market_open_time = get_today_market_open_time() - timedelta(days=1)
    if as_utc:
        return yesterday_market_open_time.astimezone(timezone.utc)
    return yesterday_market_open_time


def get_yesterday_market_close_time(as_utc: bool = False):
    yesterday_market_close_time = get_today_market_close_time() - timedelta(days=1)
    if as_utc:
        return yesterday_market_close_time.astimezone(timezone.utc)
    return yesterday_market_close_time


def get_yesterday_market_times(as_utc: bool = False):
    return get_yesterday_market_open_time(as_utc), get_yesterday_market_close_time(
        as_utc
    )


def get_market_open_time():
    return (
        datetime.strptime(MARKET_OPEN_TIME, "%H:%M:%S.%f")
        .replace(tzinfo=pytz.timezone("Asia/Calcutta"))
        .time()
    )


def get_market_close_time():
    return (
        datetime.strptime(MARKET_END_TIME, "%H:%M:%S.%f")
        .replace(tzinfo=pytz.timezone("Asia/Calcutta"))
        .time()
    )


def will_market_open_today():
    current_date_time = DateTimeHelper.get_asia_calcutta_time_now()
    return not any(
        [
            current_date_time.weekday() > 4,
            current_date_time.strftime("%d-%b-%Y") in MARKET_HOLIDAY_CALENDAR.keys(),
            current_date_time.time() > time(16, 00),
        ]
    )


def is_market_open():
    current_date_time = DateTimeHelper.get_asia_calcutta_time_now()
    if will_market_open_today() is False:
        return False
    if time(9, 15) <= current_date_time.time() <= time(16, 00):
        return True
    return False


def is_market_open_on_day(date_obj: datetime):
    # date_obj in Asia/Calcutta Timezone
    return not any(
        [
            date_obj.weekday() > 4,
            date_obj.strftime("%d-%b-%Y") in MARKET_HOLIDAY_CALENDAR.keys(),
        ]
    )
