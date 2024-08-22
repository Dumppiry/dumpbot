import discord
from dataclasses import dataclass
from datetime import datetime
from util import discord_utils


class Event:
    title: str
    url: str
    description: str
    price: int
    start_date: datetime
    image_url: str | None = None
    ticket_sale_start_date: datetime | None = None
    ticket_link: str | None = None
    footer: str | None = None

    def __init__(
        self,
        title: str,
        url: str,
        description: str,
        price: int,
        start_date: datetime,
        ticket_sale_start_date: datetime | None = None,
        ticket_link: str | None = None,
        footer: str | None = None,
        image_url: str | None = None,
    ):
        self.title = title
        self.url = url
        self.description = description
        self.price = price
        self.start_date = datetime.fromisoformat(start_date)
        self.ticket_sale_start_date = datetime.fromisoformat(
            ticket_sale_start_date
        )
        self.ticket_link = ticket_link
        self.footer = footer
        self.image_url = image_url

    def to_embed(self):
        embed = discord.Embed(
            title=self.title,
            url=self.url,
            description=self.description,
            color=0xAF271D,
        )
        print(self.image_url)
        embed.set_image(url=self.image_url)
        embed.set_footer(text=self.footer)
        embed.timestamp = datetime.now()
        embed.add_field(
            name="Tapahtuma alkaa",
            value=f"{discord_utils.get_discord_date(date=self.start_date)}\n{discord_utils.get_discord_time(date=self.start_date)}",
            inline=False,
        )
        if self.ticket_sale_start_date:
            embed.add_field(
                name="Lipunmyynti alkaa",
                value=f"{discord_utils.get_discord_date(date=self.ticket_sale_start_date)}\n{discord_utils.get_discord_time(date=self.ticket_sale_start_date)}",
                inline=False,
            )
        embed.add_field(
            name="Hinta",
            value=self.price if self.price != 0 else "Ilmainen!",
            inline=False,
        )
        if self.ticket_link:
            embed.add_field(
                name="Liput",
                value=f"[Liput täältä]({self.ticket_link})",
                inline=False,
            )
        return embed


@dataclass
class EventFeed:
    event: Event
    type: str
    post_to: int
    modified: str | None = None
