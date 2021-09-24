
import discord
import constants.strings as strings
import constants.commands as commands

MIN_CARAVAN_REACTIONS = 20

async def start(ctx, message, route):
    msg = await message.channel.send(embed = generate_embed_message(message, route), content = strings.CARAVAN_REPORT.format("@here", message.author))
    await msg.add_reaction(commands.REACT_CARAVAN)
    await msg.add_reaction(commands.REACT_DELETE)
    await message.delete()
    return

async def notify_caravan(ctx):
    msg = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
    embed_dict =  msg.embeds[0].to_dict()
    embed_dict["color"] = strings.COLOR_SUCCESS
    embed = discord.Embed.from_dict(embed_dict)
    await msg.clear_reaction(commands.REACT_CARAVAN)
    await msg.edit(embed = embed, content = "This caravan has been marked completed.")
    await ctx.message.delete()
    return

def approve_caravan(ctx):
    return

async def add_reaction(reaction):
    if reaction and reaction.count >= MIN_CARAVAN_REACTIONS - 1:
        embed_dict =  reaction.message.embeds[0].to_dict()
        embed_dict["color"] = strings.COLOR_SUCCESS
        embed = discord.Embed.from_dict(embed_dict)
        await reaction.message.edit(embed = embed)
        await reaction.message.reply(content = "<@&{0}>! This reached enough people to mass. Schedule this caravan and let's get going!".format(strings.CARAVAN_OFFICER_ID))
    return

def generate_embed_message(message, route, image = None):
    embedVar = discord.Embed(title= strings.CARAVAN_TITLE, description="", color=0x0000ff)
    embedVar.add_field(name=strings.PARTY_LEADER, value=message.author.display_name, inline=False)
    embedVar.add_field(name=strings.CARAVAN_ROUTE, value=route, inline=False)
    embedVar.add_field(name=strings.DATETIME, value=message.created_at, inline=False)
    embedVar.set_footer(text = strings.CARAVAN_PROMPT.format(MIN_CARAVAN_REACTIONS, commands.REACT_CARAVAN))
    if not image == None:
        embedVar.set_thumbnail(url=image)
    return embedVar



async def is_caravan_leader(message):
    msg = await message.channel.fetch_message(message.reference.message_id)
    # Check if the mentioned party lead is the one who reacted
    if msg.mentions[0].id == message.author.id:
        return True
    return False