import constants.strings as strings 
import modules.lfg as lfg


async def start(ctx, bot, arg):
    user = ctx.message.author
    embedVar = lfg.generate_embed("Avalonian Raid T{0}".format(str(arg)), thumbnail="https://render.albiononline.com/v1/item/T8_HEAD_PLATE_AVALON.png?quality=5")

    await ctx.send( 
        content = strings.AVA_RAID_START.format(user),
        embed = embedVar, 
        components =  lfg.generate_buttons(bot))
    await ctx.message.delete()

 
    