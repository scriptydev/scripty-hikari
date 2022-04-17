import hikari
import lightbulb

import scripty


error = lightbulb.Plugin("Error")


@error.listener(lightbulb.CommandErrorEvent)
async def on_error(event: lightbulb.CommandErrorEvent) -> None:
    exception = event.exception.__cause__ or event.exception

    if isinstance(exception, lightbulb.BotMissingRequiredPermission):
        embed = hikari.Embed(
            title="Error",
            description=f"Bot missing required `{exception.missing_perms}` permission!",
            color=scripty.functions.Color.background_secondary(),
        )
        await event.context.respond(embed)

    elif isinstance(exception, lightbulb.MissingRequiredPermission):
        embed = hikari.Embed(
            title="Error",
            description=f"User missing required `{exception.missing_perms}` permission!",
            color=scripty.functions.Color.background_secondary(),
        )
        await event.context.respond(embed)

    else:
        embed = hikari.Embed(
            title="Error",
            description=f"This interaction failed! \n ```{exception}```",
            color=scripty.functions.Color.background_secondary(),
        )
        await event.context.respond(embed)
        raise event.exception


def load(bot: scripty.core.BotApp):
    bot.add_plugin(error)


def unload(bot: scripty.core.BotApp):
    bot.remove_plugin(error)
