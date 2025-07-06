from tools.available.timezoneconverter import TimezoneConverter

tool = TimezoneConverter()

result = tool.execute(
    datetime="2025-07-05 20:00",
    from_timezone = "Asia/Jakarta",
    to_timezone = "America/New_York"
)

print(result)