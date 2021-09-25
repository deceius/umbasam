
import discord
import constants.strings as strings

async def set_description(ctx, arg):
    message = ctx.message
    if message.reference is not None:
        msg = await message.channel.fetch_message(message.reference.message_id)
        embed_dict = msg.embeds[0].to_dict()    
        if embed_dict["color"] == strings.COLOR_SUCCESS:
            return False
        embed_dict["description"] = arg
        embed = discord.Embed.from_dict(embed_dict)
        await msg.edit(embed = embed)
        await ctx.message.delete()
        return True

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def has_role(user, role_id):
    for role in user.roles:
        if role.id == role_id:
            return True
    return False        