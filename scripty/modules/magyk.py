__all__: tuple[str, ...] = ("loader_magyk",)

import alluka

# import hikari
import plane
import tanchi
import tanjun

import scripty

magykmod = tanjun.slash_command_group("magykmod", "Scripty MagykMod moderation")

analyze = magykmod.with_command(
    tanjun.slash_command_group("analyze", "Analysis subcomponents for MagykMod")
)

wizard = magykmod.with_command(
    tanjun.slash_command_group("wizard", "Automation of MagykMod moderation")
)


# @wizard.with_command
# @tanchi.as_slash_command("activate")
# async def shield_activate(ctx: tanjun.abc.SlashContext) -> None:
#     """Activate MagykMod Wizard"""
#     # TODO: Some database system here probably to store the activation status along
#     # with the guild ID. Then a on_message event listener somewhere to listen for
#     # messages, check the content for links, and run them through Aero.
#     await ctx.respond("Not implemented error")


# @wizard.with_command
# @tanchi.as_slash_command("deactivate")
# async def shield_deactivate(ctx: tanjun.abc.SlashContext) -> None:
#     """Deactivate MagykMod Wizard"""
#     # TODO: Let's see how lazy I am and wait until Johan actually decides to implement
#     # audit logging and then add automod.
#     await ctx.respond("Not implemented error")


@analyze.with_command
@tanchi.as_slash_command("url")
async def analyze_url(
    ctx: tanjun.abc.SlashContext,
    plane_client: alluka.Injected[plane.Client],
    url: str,
) -> None:
    """
    Analyze URL input for scams

    Parameters
    ----------
    url : str
        URL to analyze
    """
    url_parsed = scripty.validate_and_encode_url(url)

    if url_parsed is None:
        await ctx.respond(
            scripty.Embed(
                title="Analyze Error",
                description=(
                    "Provided URL is malformed!\nPlease check if complies with [DNS]"
                    "(https://en.wikipedia.org/wiki/Domain_Name_System) structure"
                ),
            )
        )
        return

    try:
        data = await plane_client.urls.get_url(url_parsed["encoded"])

    except plane.HTTPException as e:
        await ctx.respond(
            scripty.Embed(
                title="Analyze Error",
                description="An error occurred while analyzing the URL",
            )
        )

        raise Exception from e

    else:
        embed = (
            scripty.Embed(
                title="Analyze",
                description=url_parsed["input"],
            )
            .add_field("Fraudulent", data["isFraudulent"], inline=True)
            .add_field("Information", data["message"], inline=True)
        )

        await ctx.respond(embed)


# @analyze.with_command
# @tanchi.as_slash_command("user")
# async def analyze_user(
#     ctx: tanjun.abc.SlashContext,
#     session: alluka.Injected[aiohttp.ClientSession],
#     user: hikari.User,
# ) -> None:
#     """
#     Analyze a user for fraudulency

#     Parameters
#     ----------
#     user : hikari.User
#         User to analyze
#     """
#     async with session.get(
#         f"{scripty.AERO_API}/users/{user.id}/bans", headers=scripty.AERO_HEADERS
#     ) as response:
#         data = await response.json()

#         if not response.ok:
#             await ctx.respond(
#                 scripty.Embed(
#                     title="Analyze Error",
#                     description="An error occurred while analyzing the user",
#                 )
#             )

#             raise scripty.HTTPError(
#                 f"The Aero Ravy API returned a mentally unok {response.status} status"
#                 f" with the following data: {data}"
#             )

#         # TODO: The rest of this:
#         embed = scripty.Embed(description=f"```json\n{data}\n```")

#         await ctx.respond(embed)


loader_magyk = tanjun.Component(name="magyk").load_from_scope().make_loader()