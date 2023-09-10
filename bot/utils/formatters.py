from engine.exceptions import NegativeTimeError


class TimeFormatter:
    @staticmethod
    def format_time(seconds: int) -> str:
        if seconds < 0:
            raise NegativeTimeError

        hours = seconds // (60 * 60)
        minutes = (seconds % (60 * 60)) // 60
        seconds = seconds % 60

        if hours == 0:
            if minutes == 0:
                time_str = f"{seconds:02d}"
            else:
                time_str = f"{minutes:02d}:{seconds:02d}"
        else:
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        return time_str
