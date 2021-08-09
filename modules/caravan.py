
import discord
import constants.strings as strings
import constants.commands as commands

MIN_CARAVAN_REACTIONS = 15

async def start(ctx, message, route):
    msg = await message.channel.send(embed = generate_embed_message(message, route), content = strings.CARAVAN_REPORT.format(message.author))
    await msg.add_reaction(commands.REACT_CARAVAN)
    return

def notify_caravan(ctx):
    return

def approve_caravan(ctx):
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