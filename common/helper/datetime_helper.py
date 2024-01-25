from datetime import datetime, timedelta, timezone

import pytz


class DateTimeHelper:

    CALCUTTA_TZ = pytz.timezone("Asia/Calcutta")
    UTC_TZ = pytz.timezone("UTC")

    @staticmethod
    def get_asia_calcutta_time_now() -> datetime:
        """Generates a DateTime to get current Asia/Calcutta Time

        Returns:
            datetime: Current Datetime in Asia Calcutta Timezone
        """
        return datetime.now(DateTimeHelper.CALCUTTA_TZ)

    @staticmethod
    def get_asia_calcutta_date():
        return DateTimeHelper.get_asia_calcutta_time_now().date()

    @staticmethod
    def __get_days_start_and_end(datetime_obj):
        today = datetime_obj
        start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end = (
            start + timedelta(1) - timedelta(microseconds=1000)
        )  # Removing 1 MS to stay in prev date
        return start, end

    @staticmethod
    def get_today_start_and_end():
        today = datetime.now(tz=DateTimeHelper.CALCUTTA_TZ)
        return DateTimeHelper.__get_days_start_and_end(today)

    @staticmethod
    def get_prev_day_start_and_end():
        today = datetime.now(tz=DateTimeHelper.CALCUTTA_TZ) - timedelta(days=1)
        return DateTimeHelper.__get_days_start_and_end(today)

    @staticmethod
    def get_epoch_seconds_from_datetime(datetime_obj):
        return round(datetime_obj.timestamp())

    @staticmethod
    def get_epoch_milliseconds_from_datetime(datetime_obj):
        return round(datetime_obj.timestamp() * 1000)

    @staticmethod
    def get_utc_timezone_date(datetime_obj):
        return datetime_obj.astimezone(timezone.utc)

    @staticmethod
    def get_utc_datetime():
        return datetime.now(tz=DateTimeHelper.UTC_TZ)
