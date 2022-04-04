import hikari
import lightbulb

from scripty import functions


misc = lightbulb.Plugin("Miscellaneous")


@misc.command()
@lightbulb.command("Avatar", "Retrieves user avatar", auto_defer=True)
@lightbulb.implements(lightbulb.UserCommand)
async def avatar(ctx: lightbulb.Context) -> None:
    user = ctx.options.target

    embed = hikari.Embed(
        title=f"Avatar",
        color=functions.Color.blurple(),
    )
    embed.set_author(name=str(user), icon=user.avatar_url)
    embed.set_image(user.avatar_url)

    await ctx.respond(embed)


@misc.command()
@lightbulb.option("text", "Text to repeat", str)
@lightbulb.command("echo", "Repeats user input", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def echo(ctx: lightbulb.Context) -> None:
    embed = hikari.Embed(
        title="Echo",
        description=f"{ctx.author.mention} said: ```{ctx.options.text}```",
        color=functions.Color.blurple(),
    )
    await ctx.respond(embed)


@misc.command()
@lightbulb.option("option_j", "Option J", str, required=False)
@lightbulb.option("option_i", "Option I", str, required=False)
@lightbulb.option("option_h", "Option H", str, required=False)
@lightbulb.option("option_g", "Option G", str, required=False)
@lightbulb.option("option_f", "Option F", str, required=False)
@lightbulb.option("option_e", "Option E", str, required=False)
@lightbulb.option("option_d", "Option D", str, required=False)
@lightbulb.option("option_c", "Option C", str, required=False)
@lightbulb.option("option_b", "Option B", str)
@lightbulb.option("option_a", "Option A", str)
@lightbulb.option("topic", "Topic of the poll", str)
@lightbulb.command("poll", "Creates a simple poll", auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def poll(ctx: lightbulb.Context) -> None:
    topic = ctx.options.topic
    options = {
        u"\U0001f1e6": ctx.options.option_a,
        u"\U0001f1e7": ctx.options.option_b,
        u"\U0001f1e8": ctx.options.option_c,
        u"\U0001f1e9": ctx.options.option_d,
        u"\U0001f1ea": ctx.options.option_e,
        u"\U0001f1eb": ctx.options.option_f,
        u"\U0001f1ec": ctx.options.option_g,
        u"\U0001f1ed": ctx.options.option_h,
        u"\U0001f1ee": ctx.options.option_i,
        u"\U0001f1ef": ctx.options.option_j,
    }

    embed = hikari.Embed(
        title=topic,
        description="\n\n".join(
            f"{key} {value}" for key, value in options.items() if value is not None
        ),
        color=functions.Color.blurple(),
    )
    embed.set_author(name=str(ctx.author), icon=ctx.author.avatar_url)

    await ctx.respond(embed)

    for key, value in options.items():
        if value is not None:
            response = await ctx.interaction.fetch_initial_response()
            await response.add_reaction(key)


def load(bot: lightbulb.BotApp):
    bot.add_plugin(misc)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(misc)
