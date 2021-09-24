import constants.strings as strings 
import modules.lfg as lfg


async def start(ctx, bot):
    user = ctx.message.author
    embedVar = lfg.generate_embed(
        "Fighting Party", 
        thumbnail="https://render.albiononline.com/v1/item/T7_2H_DUALSWORD@1.png?quality=2")

    await ctx.send( 
        content = strings.GANK_START.format(user),
        embed = embedVar, 
        components =  lfg.generate_buttons(bot))
    await ctx.message.delete()



    