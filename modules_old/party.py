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
    await msg.edit(content = "This group has been marked formed. GLHF bois!")
    await ctx.message.delete()
    return

def generate_embed_message(message, content_reason, image = None):
    embedVar = discord.Embed(title= strings.PARTY_TITLE, description="", color=0x0000ff)
    embedVar.add_field(name=strings.PARTY_LEADER, value=message.author.display_name, inline=False)
    embedVar.add_field(name=strings.PARTY_CONTENT, value=content_reason, inline=False)
    embedVar.add_field(name="Needed Roles:", value="** **", inline=False)
    embedVar.add_field(name="{0} MDPS".format(commands.REACT_ROLE_MDPS), value="--", inline=False)
    embedVar.add_field(name="{0} RDPS".format(commands.REACT_ROLE_RDPS), value="--", inline=False)
    embedVar.add_field(name="{0} SUPP".format(commands.REACT_ROLE_SUPP), value="--", inline=False)
    embedVar.add_field(name="{0} TANK".format(commands.REACT_ROLE_TANK), value="--", inline=False)
    embedVar.add_field(name="{0} HEAL".format(commands.REACT_ROLE_HEAL), value="--", inline=False)
    embedVar.add_field(name=strings.DATETIME, value=message.created_at, inline=False)
    embedVar.set_footer(text = "To define needed roles, reply `!<role> <required_member_count>` on this message.\nIf done using this, reply with `!ptfound`.\n\nSelect only your *MAIN* role.")
    if not image == None:
        embedVar.set_thumbnail(url=image)
    return embedVar


async def set_role(ctx, role_name, count):
    msg = await ctx.message.channel.fetch_message(ctx.message.reference.message_id)
    embed_dict =  msg.embeds[0].to_dict()
    for field in embed_dict["fields"]:
        if field["name"] == "{0} MDPS".format(commands.REACT_ROLE_MDPS) and role_name.upper() == "MDPS":
            field["value"] = count
        if field["name"] == "{0} RDPS".format(commands.REACT_ROLE_RDPS) and role_name.upper() == "RDPS":
            field["value"] = count
        if field["name"] == "{0} SUPP".format(commands.REACT_ROLE_SUPP) and role_name.upper() == "SUPP":
            field["value"] = count
        if field["name"] == "{0} TANK".format(commands.REACT_ROLE_TANK) and role_name.upper() == "TANK":
            field["value"] = count
        if field["name"] == "{0} HEAL".format(commands.REACT_ROLE_HEAL) and role_name.upper() == "HEAL":
            field["value"] = count
    
    embed = discord.Embed.from_dict(embed_dict)
    await msg.edit(embed = embed)
    await ctx.message.delete()
    return

async def fulfill_role(reaction):
    msg = reaction.message
    roles = {
        "mdps" : 0,
        "rdps" : 0,
        "supp" : 0,
        "tank" : 0,
        "heal" : 0
    }
    embed_dict =  msg.embeds[0].to_dict()
    for field in embed_dict["fields"]:
        if field["name"] == "{0} MDPS".format(commands.REACT_ROLE_MDPS):
            roles["mdps"] = int(field["value"]) if field["value"].isdigit() else 0
        if field["name"] == "{0} RDPS".format(commands.REACT_ROLE_RDPS):
            roles["rdps"] = int(field["value"]) if field["value"].isdigit() else 0
        if field["name"] == "{0} SUPP".format(commands.REACT_ROLE_SUPP):
            roles["supp"] = int(field["value"]) if field["value"].isdigit() else 0
        if field["name"] == "{0} TANK".format(commands.REACT_ROLE_TANK):
            roles["tank"] = int(field["value"]) if field["value"].isdigit() else 0
        if field["name"] == "{0} HEAL".format(commands.REACT_ROLE_HEAL):
            roles["heal"] = int(field["value"]) if field["value"].isdigit() else 0
    users = []
    print(roles)
    embed_dict = await process_comp(reaction, embed_dict, roles["mdps"], "{0} MDPS".format(commands.REACT_ROLE_MDPS), commands.REACT_ROLE_MDPS)
    embed_dict = await process_comp(reaction, embed_dict, roles["rdps"], "{0} RDPS".format(commands.REACT_ROLE_RDPS), commands.REACT_ROLE_RDPS)
    embed_dict = await process_comp(reaction, embed_dict, roles["tank"], "{0} TANK".format(commands.REACT_ROLE_TANK), commands.REACT_ROLE_TANK)
    embed_dict = await process_comp(reaction, embed_dict, roles["heal"], "{0} HEAL".format(commands.REACT_ROLE_HEAL), commands.REACT_ROLE_HEAL)
    embed_dict = await process_comp(reaction, embed_dict, roles["supp"], "{0} SUPP".format(commands.REACT_ROLE_SUPP), commands.REACT_ROLE_SUPP)
    
    embed = discord.Embed.from_dict(embed_dict)
    await msg.edit(embed = embed)
    return

async def process_comp(reaction, embed_dict, role_value, field_name, emoji):
    print("checking if emoji matches: " + str(reaction.emoji) + " = " + str(emoji) + str(reaction.emoji == emoji))
    if reaction.emoji == emoji:
        print("checkng if role is not zero: " + str(role_value == 0))
        if not role_value == 0:
            users = await get_users_by_emoji(reaction, emoji)
            print("checkng if users are valid: " + str(len(users) - 1 == role_value))
            if len(users) - 1 == role_value:
                print(emoji)
                embed_dict = update_role_embed(reaction.message.author, embed_dict, field_name, users)
                await reaction.message.clear_reaction(emoji)
                return embed_dict
    return embed_dict

async def get_users_by_emoji(reaction, emoji):
    users = []
    async for user in reaction.users():
        if reaction.emoji == emoji:
            users.append(user.mention)
    return users

def update_role_embed(bot, embed_dict, field_name, users):
    users.remove(bot.mention)
    for field in embed_dict["fields"]:
        if field["name"] == field_name:
            field["value"] = ", ".join(users)
    return embed_dict
        
def get_roles():
    return [
        commands.REACT_ROLE_MDPS,
        commands.REACT_ROLE_RDPS,
        commands.REACT_ROLE_SUPP,
        commands.REACT_ROLE_TANK,
        commands.REACT_ROLE_HEAL
    ]