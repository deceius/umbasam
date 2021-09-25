

import discord
from discord_components import ButtonStyle, Button, component

def generate_embed(title, thumbnail = None, color = 0xf0f0f0, is_zvz = False):
    embedVar = discord.Embed(title= title, description="Reply with `!desc <your_description_here>` to set a description.", color=color)
    embedVar.add_field(name="TANK", value="--", inline=True)
    embedVar.add_field(name="HEAL", value="--", inline=True)
    embedVar.add_field(name="SUPP", value="--", inline=True)
    if (is_zvz):        
        embedVar.add_field(name="RDPS", value="--", inline=True)
        embedVar.add_field(name="MDPS", value="--", inline=True)
        embedVar.add_field(name="** **", value="** **", inline=True)
    else:
        embedVar.add_field(name="DPS", value="--", inline=True)
    embedVar.set_footer(text = "Add required role numbers by replying:\n!<role> <number>\nShould you encounter any errors, report it to #umbasam-feedback channel.")
    if not thumbnail == None:
        embedVar.set_thumbnail(url= thumbnail)
    return embedVar

def generate_buttons(bot, is_zvz = False):
    if is_zvz:
        return [
            [
                    bot.components_manager.add_callback(
                        Button(label="TANK", emoji = "🛡️"),
                        btn_join_tank
                    ),
                    bot.components_manager.add_callback(
                        Button(label="HEAL", emoji = "💚"),
                        btn_join_heal
                    ),
                    bot.components_manager.add_callback(
                        Button(label="SUPP", emoji = "🔮"),
                        btn_join_supp
                    ),
                    bot.components_manager.add_callback(
                        Button(label="RDPS", emoji = "🏹"),
                        btn_join_rdps
                    ),
                    bot.components_manager.add_callback(
                        Button(label="MDPS", emoji = "⚔️"),
                        btn_join_mdps
                    )
                ],
                [
                 bot.components_manager.add_callback(
                    Button(style=ButtonStyle.red, label="Cancel Party Finder"),
                    btn_finish
                )]
        ]
                
    else:
        return [[
                bot.components_manager.add_callback(
                    Button(label="TANK", emoji = "🛡️"),
                    btn_join_tank
                ),
                bot.components_manager.add_callback(
                    Button(label="HEAL", emoji = "💚"),
                    btn_join_heal
                ),
                bot.components_manager.add_callback(
                    Button(label="SUPP", emoji = "🔮"),
                    btn_join_supp
                ),
                bot.components_manager.add_callback(
                    Button(label="DPS", emoji = "🏹"),
                    btn_join_dps
                ),
                 bot.components_manager.add_callback(
                    Button(style=ButtonStyle.red, label="Cancel Party Finder"),
                    btn_finish
                )
            ]]

async def btn_finish(interaction):
    msg = interaction.message
    if msg.mentions[0].id == interaction.user.id:
        await interaction.message.delete()
        await interaction.send(content = "You have deleted the party finder.")
    else:
        await interaction.send(content = "You are not the party leader of this party finder.")

async def btn_join_tank(interaction):
    await btn_join(interaction, interaction.user, "TANK")

async def btn_join_dps(interaction):
    await btn_join(interaction, interaction.user, "DPS")

    
async def btn_join_mdps(interaction):
    await btn_join(interaction, interaction.user, "MDPS")

async def btn_join_rdps(interaction):
    await btn_join(interaction, interaction.user, "RDPS")

async def btn_join_heal(interaction):
    await btn_join(interaction, interaction.user, "HEAL")

async def btn_join_supp(interaction):
    await btn_join(interaction, interaction.user, "SUPP")

async def btn_join(interaction, member, role):
    msg = interaction.message
    embed_dict = msg.embeds[0].to_dict()
    is_full = await process_join(member, role, embed_dict)
    
    if not is_full:
        embed = discord.Embed.from_dict(embed_dict)
        await msg.edit(embed = embed) 
        await interaction.respond(type = 6)
    else:
        await interaction.send(content = "The {0} is already full.".format(role))

async def btn_join(interaction, member, role):
    msg = interaction.message
    is_full = await process_join(member, role, msg)
    if not is_full: 
        await interaction.respond(type = 6)
    else:
        await interaction.send(content = "The {0} is already full.".format(role))

async def join_to_role(member, role, msg):
    await process_join(member, role, msg)

async def process_join(member, role, msg):
    result = False
    embed_dict = msg.embeds[0].to_dict()
    for field in embed_dict["fields"]:
        if " - " in field["name"]:
            role_header = field["name"].split(" - ")
        else: 
            role_header = [field["name"], 0]

        if role_header[0] == role:    
            if (int(role_header[1]) > 0):
                is_full = int(role_header[1]) == len(field["value"].replace("--", "").splitlines())
                print(is_full)
                if is_full and member.mention not in field["value"]:
                    result = True
                    break
            if (member.mention in field["value"]):
                field["value"] = field["value"].replace(member.mention + "\n", "")
                field["value"] = field["value"].replace(member.mention, "")
                if (len(field["value"]) == 0):
                    field["value"] = "--"
            else:
                if (field["value"] == "--"):
                    field["value"] = member.mention
                else:
                    field["value"] = field["value"] + "\n" + member.mention
        else:
            if (member.mention in field["value"]):
                field["value"] = field["value"].replace(member.mention + "\n", "")
                field["value"] = field["value"].replace(member.mention, "")
                if (len(field["value"]) == 0):
                    field["value"] = "--"

    embed = discord.Embed.from_dict(embed_dict)
    await msg.edit(embed = embed)
    return result

async def set_role_qty(ctx, role, arg):
    message = ctx.message
    if message.reference is not None:
        msg = await message.channel.fetch_message(message.reference.message_id)
        if ctx.message.mentions[0].id == msg.author.id:
            embed_dict = msg.embeds[0].to_dict()
            role_header = []
            for field in embed_dict["fields"]:
                if " - " in field["name"]:
                    role_header = field["name"].split(" - ")
                else: 
                    role_header = [field["name"], 0]
                    
                if role_header[0] == role:
                    field["name"] = role + " - " + str(arg)
                    
            embed = discord.Embed.from_dict(embed_dict)
            await msg.edit(embed = embed)
        await message.delete()