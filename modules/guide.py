import constants.strings as strings

async def cdg(ctx):
    await ctx.message.send(content = "The Oathbreaker's [Corrupted Dungeon Guide]({0})".format(strings.URL_CORRUPTED))
async def pvp(ctx):
    await ctx.message.send(content = "The Oathbreaker's [MoreThin's PvP Guide]({0})".format(strings.URL_PVP))

