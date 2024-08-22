from datetime import datetime


def get_discord_date(date: datetime):
    return f"<t:{int(date.timestamp())}:d>"


def get_discord_time(date: datetime):
    return f"<t:{int(date.timestamp())}:t>"
