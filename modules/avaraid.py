from modules.mageraid import btn_join
from discord_components import ButtonStyle, Button, component
import discord
import constants.strings as strings 
import modules.util as util


async def start(ctx, bot, arg):
    user = ctx.message.author
    embedVar = discord.Embed(title= "Avalonian Raid T" + str(arg), description="Reply with `!desc <your_description_here>` to set a description.", color=0xf0f0f0)
    embedVar.add_field(name="TANK", value="--", inline=True)
    embedVar.add_field(name="DPS", value="--", inline=True)
    embedVar.add_field(name="HEAL", value="--", inline=True)
    embedVar.add_field(name="SUPP", value="--", inline=True)
    embedVar.set_footer(text = "Add required role numbers by replying:\n!<role> <number>")
    embedVar.set_thumbnail(url="https://render.albiononline.com/v1/item/T8_HEAD_PLATE_AVALON.png?quality=5")

    await ctx.send( 
        content = strings.AVA_RAID_START.format(user),
        embed = embedVar, 
        components = [
            [
                bot.components_manager.add_callback(
                    Button(label="TANK", emoji = "🛡️"),
                    btn_join_tank
                ),
                bot.components_manager.add_callback(
                    Button(label="DPS", emoji = "🏹"),
                    btn_join_dps
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
                    Button(style=ButtonStyle.red, label="Delete Raid"),
                    btn_finish
                )
            ]
               
        ])
    await ctx.message.delete()

async def btn_join_tank(interaction):
    await btn_join(interaction, interaction.user, "TANK")

async def btn_join_dps(interaction):
    await btn_join(interaction, interaction.user, "DPS")

async def btn_join_heal(interaction):
    await btn_join(interaction, interaction.user, "HEAL")

async def btn_join_supp(interaction):
    await btn_join(interaction, interaction.user, "SUPP")

async def btn_join(interaction, member, role):
    print("----btn-join")
    msg = interaction.message
    embed_dict = msg.embeds[0].to_dict()
    is_full = False
    for field in embed_dict["fields"]:
        if " - " in field["name"]:
            role_header = field["name"].split(" - ")
        else: 
            role_header = [field["name"], 0]

        if role_header[0] == role:    
            if (int(role_header[1]) > 0):
                is_full = int(role_header[1]) == len(field["value"].replace("--", "").splitlines())
                print(is_full)
                if is_full and member.display_name not in field["value"]:
                    await interaction.send(content = "The {0} is already full.".format(role))
                    break
            if (member.display_name in field["value"]):
                field["value"] = field["value"].replace(member.display_name, "")
                if (len(field["value"]) == 0):
                    field["value"] = "--"
            else:
                if (field["value"] == "--"):
                    field["value"] = member.display_name
                else:
                    field["value"] = field["value"] + "\n" + member.display_name
        else:
            if (member.display_name in field["value"]):
                field["value"] = field["value"].replace(member.display_name, "")
                if (len(field["value"]) == 0):
                    field["value"] = "--"

            
           
  
    embed = discord.Embed.from_dict(embed_dict)
    

    await msg.edit(embed = embed) 
    await interaction.respond(type = 6)

async def disable_button(button, is_disable):
    btn_dict = button.to_dict()
    btn_dict["disabled"] = is_disable
    return button.from_json(btn_dict)

async def btn_finish(interaction):
    msg = interaction.message
    if msg.mentions[0].id == interaction.user.id:
        await interaction.message.delete()
        await interaction.send(content = "You have deleted the raid.")
    else:
        await interaction.send(content = "You are not the party leader of this avalonian raid.")

async def set_role_qty(ctx, role, arg):
    message = ctx.message
    if message.reference is not None:
        msg = await message.channel.fetch_message(message.reference.message_id)
        embed_dict = msg.embeds[0].to_dict()
        for field in embed_dict["fields"]:
            if field["name"] == role:
                field["name"] = role + " - " + str(arg)
                
        embed = discord.Embed.from_dict(embed_dict)
        await msg.edit(embed = embed)
        await ctx.message.delete()
    
    