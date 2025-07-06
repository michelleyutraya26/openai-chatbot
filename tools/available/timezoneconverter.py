from typing import List
from datetime import datetime
import pytz
from tools.base import BaseTool, ToolParameter

class TimezoneConverter(BaseTool):
    """Tool that converts time from one timezone to another"""

    @property
    def name(self) -> str:
        return "convert_timezone"

    @property
    def description(self) -> str:  # ✅ Fix here
        return "Convert a datetime from one timezone to another"

    @property
    def parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="datetime",
                type="string",
                description="The datetime to convert in YYYY-MM-DD HH:MM format.",
                required=True
            ),
            ToolParameter(
                name="from_timezone",
                type="string",
                description="The timezone of the input datetime (e.g. 'Asia/Jakarta').",
                required=True
            ),
            ToolParameter(
                name="to_timezone",
                type="string",
                description="The target timezone to convert to (e.g. 'America/New_York').",
                required=True
            )
        ]

    def execute(self, **kwargs) -> str:
        dt_str = kwargs.get("datetime")
        from_tz = kwargs.get("from_timezone")
        to_tz = kwargs.get("to_timezone")

        try:
            naive_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M")
            from_zone = pytz.timezone(from_tz)
            to_zone = pytz.timezone(to_tz)

            localized_dt = from_zone.localize(naive_dt)
            converted_dt = localized_dt.astimezone(to_zone)

            return f"{dt_str} in {from_tz} is {converted_dt.strftime('%Y-%m-%d %H:%M')} in {to_tz}"

        except Exception as e:
            return f"❌ Error converting timezone: {str(e)}"