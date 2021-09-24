
import discord

async def set_description(ctx, arg):
    message = ctx.message
    if message.reference is not None:
        msg = await message.channel.fetch_message(message.reference.message_id)
        embed_dict = msg.embeds[0].to_dict()
        embed_dict["description"] = arg
        embed = discord.Embed.from_dict(embed_dict)
        await msg.edit(embed = embed)
        await ctx.message.delete()

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()