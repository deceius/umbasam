import constants.strings as strings 
import modules.lfg as lfg


async def start(ctx, bot):
    user = ctx.message.author
    embedVar = lfg.generate_embed(
        "Detailed Comp Preparation", 
        thumbnail="https://render.albiononline.com/v1/item/T8_2H_MACE_MORGANA@3.png?quality=3",
        is_zvz = True)

    await ctx.send( 
        content = strings.ZVZ_START.format(user),
        embed = embedVar, 
        components = lfg.generate_buttons(bot, is_zvz = True)
        )
    await ctx.message.delete()

