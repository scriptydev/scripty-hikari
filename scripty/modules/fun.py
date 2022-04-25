import random
import typing

import hikari
import miru
import tanchi
import tanjun

import scripty


component = tanjun.Component()


@component.with_command
@tanchi.as_slash_command()
async def coin(ctx: tanjun.abc.SlashContext) -> None:
    """Flip a coin"""
    coin = ["Heads", "Tails"]
    embed = hikari.Embed(
        title="Coin",
        description=random.choice(coin),
        color=scripty.Color.dark_embed(),
    )
    await ctx.respond(embed)


@component.with_command
@tanchi.as_slash_command()
async def dice(
    ctx: tanjun.abc.SlashContext, sides: tanchi.Range[2, ...] = 6
) -> None:
    """Roll a die

    Parameters
    ----------
    sides : int
        Number of sides on the die
    """
    embed = hikari.Embed(
        title="Dice",
        description=random.randint(1, sides),
        color=scripty.Color.dark_embed(),
    )

    await ctx.respond(embed)


class MemeView(miru.View):
    def __init__(self, submissions: typing.Any, index: int) -> None:
        super().__init__(timeout=30.0)
        self.submissions = submissions
        self.index = index

    @miru.button(label="Previous", style=hikari.ButtonStyle.PRIMARY)
    async def previous(self, button: miru.Button, ctx: miru.Context) -> None:  # type: ignore
        self.index -= 1
        if self.index == len(self.submissions):
            self.index = 0

        embed = hikari.Embed(
            title=self.submissions[self.index]["title"],
            url=f"https://reddit.com{self.submissions[self.index]['permalink']}",
            color=scripty.Color.dark_embed(),
        )
        embed.set_image(self.submissions[self.index]["url"])
        await ctx.edit_response(embed)

    @miru.button(label="Stop", style=hikari.ButtonStyle.DANGER)
    async def stop_(self, button: miru.Button, ctx: miru.Context) -> None:  # type: ignore
        await ctx.edit_response(components=[])
        self.stop()

    @miru.button(label="Next", style=hikari.ButtonStyle.PRIMARY)
    async def next(self, button: miru.Button, ctx: miru.Context) -> None:  # type: ignore
        self.index += 1
        if self.index == len(self.submissions):
            self.index = 0

        embed = hikari.Embed(
            title=self.submissions[self.index]["title"],
            url=f"https://reddit.com{self.submissions[self.index]['permalink']}",
            color=scripty.Color.dark_embed(),
        )
        embed.set_image(self.submissions[self.index]["url"])
        await ctx.edit_response(embed)

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True

        self.add_item(
            miru.Button(
                style=hikari.ButtonStyle.SECONDARY,
                label="Timed out",
                disabled=True,
            )
        )

        assert self.message is not None, "Message is None"
        await self.message.edit(components=self.build())


@component.with_command
@tanchi.as_slash_command()
async def meme(
    ctx: tanjun.abc.SlashContext,
    bot: scripty.AppBot = tanjun.inject(type=scripty.AppBot),
) -> None:
    """The hottest Reddit r/memes"""
    reddit_url = "https://reddit.com/r/memes/hot.json"
    async with bot.aiohttp_session.get(
        reddit_url, headers={"User-Agent": "Scripty"}
    ) as response:
        reddit = await response.json()

    submissions: typing.Any = []
    for submission in range(len(reddit["data"]["children"])):
        if not reddit["data"]["children"][submission]["data"]["over_18"]:
            if not reddit["data"]["children"][submission]["data"]["is_video"]:
                submissions.append(
                    reddit["data"]["children"][submission]["data"]
                )

    random.shuffle(submissions)

    index = 0

    view = MemeView(submissions, index)

    embed = hikari.Embed(
        title=submissions[index]["title"],
        url=f"https://reddit.com{submissions[index]['permalink']}",
        color=scripty.Color.dark_embed(),
    )
    embed.set_image(submissions[index]["url"])

    await ctx.respond(embed, components=view.build())

    message = await ctx.interaction.fetch_initial_response()
    view.start(message)
    await view.wait()


@component.with_command
@tanchi.as_slash_command()
async def rickroll(ctx: tanjun.abc.SlashContext) -> None:
    """;)"""
    await ctx.respond("https://youtu.be/dQw4w9WgXcQ")


class RPSView(miru.View):
    rps: dict[str, int] = {"Rock": 0, "Paper": 1, "Scissors": 2}

    def __init__(self):
        super().__init__(timeout=30.0)
        self._rps = random.choice((0, 1, 2))

    def get_value(self, key: str) -> int:
        return self.rps[key]

    def get_key(self, value: int) -> str:
        if not 0 <= value <= 2:
            raise ValueError("Invalid value")

        return tuple(k for k, v in self.rps.items() if v == value)[0]

    def generate_embed(self, message: str) -> hikari.Embed:
        return hikari.Embed(
            title="RPS",
            description=message,
            color=scripty.Color.dark_embed(),
        )

    def determine_outcome(self, player_choice: str) -> hikari.Embed:
        player_value = self.get_value(player_choice)
        computer_choice = self.get_key(self._rps)

        if (player_value + 1) % 3 == self._rps:
            return self.generate_embed(
                f"You lost! `{computer_choice}` beats `{player_choice}`"
            )

        elif player_value == self._rps:
            return self.generate_embed(
                f"You tied! Both chose `{player_choice}`"
            )

        else:
            return self.generate_embed(
                f"You won! `{player_choice}` beats `{computer_choice}`"
            )

    @miru.button(label="Rock", style=hikari.ButtonStyle.DANGER)
    async def rock(self, button: miru.Button, ctx: miru.Context) -> None:  # type: ignore
        await ctx.edit_response(self.determine_outcome("Rock"), components=[])
        self.stop()

    @miru.button(label="Paper", style=hikari.ButtonStyle.SUCCESS)
    async def paper(self, button: miru.Button, ctx: miru.Context) -> None:  # type: ignore
        await ctx.edit_response(self.determine_outcome("Paper"), components=[])
        self.stop()

    @miru.button(label="Scissors", style=hikari.ButtonStyle.PRIMARY)
    async def scissors(self, button: miru.Button, ctx: miru.Context) -> None:  # type: ignore
        await ctx.edit_response(
            self.determine_outcome("Scissors"), components=[]
        )
        self.stop()

    async def view_check(self, context: miru.Context) -> bool:
        assert self.message and self.message.interaction is not None

        if context.user != self.message.interaction.user:
            embed = hikari.Embed(
                title="Error",
                description="This command was not invoked by you!",
                color=scripty.Color.dark_embed(),
            )
            await context.respond(embed, flags=hikari.MessageFlag.EPHEMERAL)
            return False
        else:
            return True

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True

        self.add_item(
            miru.Button(
                style=hikari.ButtonStyle.SECONDARY,
                label="Timed out",
                disabled=True,
            )
        )

        assert self.message is not None, "Message is None"
        await self.message.edit(components=self.build())


@component.with_command
@tanchi.as_slash_command()
async def rps(ctx: tanjun.abc.SlashContext) -> None:
    """Play rock paper scissors"""
    view = RPSView()

    embed = hikari.Embed(
        title="RPS",
        description="Click on the button options to continue the game!",
        color=scripty.Color.dark_embed(),
    )

    await ctx.respond(embed, components=view.build())

    message = await ctx.interaction.fetch_initial_response()
    view.start(message)
    await view.wait()


@tanjun.as_loader
def load(client: tanjun.abc.Client) -> None:
    client.add_component(component.copy())


@tanjun.as_unloader
def unload_component(client: tanjun.Client) -> None:
    client.remove_component_by_name(component.name)