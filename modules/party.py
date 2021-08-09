import discord
import constants.strings as strings
import constants.commands as commands
from discord.utils import get

async def start(ctx, content_reason):
    message = ctx.message
    msg = await message.channel.send(embed = generate_embed_message(message, content_reason), content = strings.PARTY_REPORT.format("@here", message.author, content_reason))
    await msg.add_reaction(commands.REACT_ROLE_MDPS)
    await msg.add_reaction(commands.REACT_ROLE_RDPS)
    await msg.add_reaction(commands.REACT_ROLE_SUPP)
    await msg.add_reaction(commands.REACT_ROLE_TANK)
    await msg.add_reaction(commands.REACT_ROLE_HEAL)
    await message.delete()
    return

async def found(ctx):
    msg = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)

    mdps_count = get(msg.reactions, emoji=commands.REACT_ROLE_MDPS).count - 1 
    rdps_count = get(msg.reactions, emoji=commands.REACT_ROLE_RDPS).count - 1 
    supp_count = get(msg.reactions, emoji=commands.REACT_ROLE_SUPP).count - 1 
    tank_count = get(msg.reactions, emoji=commands.REACT_ROLE_TANK).count - 1 
    heal_count = get(msg.reactions, emoji=commands.REACT_ROLE_HEAL).count - 1 
    roles = "{0} MDPS - {5}\n{1} RDPS - {6}\n{2} SUPP - {7}\n{3} TANK - {8}\n{4} HEAL - {9}".format(
            commands.REACT_ROLE_MDPS,
            commands.REACT_ROLE_RDPS,
            commands.REACT_ROLE_SUPP,
            commands.REACT_ROLE_TANK,
            commands.REACT_ROLE_HEAL,
            mdps_count,
            rdps_count,
            supp_count,
            tank_count,
            heal_count
            )
    embed_dict =  msg.embeds[0].to_dict()
    embed_dict["color"] = strings.COLOR_SUCCESS
    for field in embed_dict["fields"]:
        if field["name"] == "React your Role:":
            field["value"] = roles
    embed = discord.Embed.from_dict(embed_dict)

    await msg.clear_reaction(commands.REACT_ROLE_MDPS)
    await msg.clear_reaction(commands.REACT_ROLE_RDPS)
    await msg.clear_reaction(commands.REACT_ROLE_HEAL)
    await msg.clear_reaction(commands.REACT_ROLE_TANK)
    await msg.clear_reaction(commands.REACT_ROLE_SUPP)
    await msg.edit(embed = embed, content = "This group has been formed. GLHF bois!")
    await ctx.message.delete()
    return

def generate_embed_message(message, content_reason, image = None):
    roles = "{0} MDPS\n{1} RDPS\n{2} SUPP\n{3} TANK\n{4} HEAL".format(
        commands.REACT_ROLE_MDPS,
        commands.REACT_ROLE_RDPS,
        commands.REACT_ROLE_SUPP,
        commands.REACT_ROLE_TANK,
        commands.REACT_ROLE_HEAL,
        )
    embedVar = discord.Embed(title= strings.PARTY_TITLE, description="", color=0x0000ff)
    embedVar.add_field(name=strings.PARTY_LEADER, value=message.author.display_name, inline=False)
    embedVar.add_field(name=strings.PARTY_CONTENT, value=content_reason, inline=False)
    embedVar.add_field(name="React your Role:", value=roles, inline=False)
    embedVar.add_field(name=strings.DATETIME, value=message.created_at, inline=False)
    if not image == None:
        embedVar.set_thumbnail(url=image)
    return embedVar