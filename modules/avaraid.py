from modules.mageraid import btn_join
from discord_components import ButtonStyle, Button
import discord
import constants.strings as strings 


async def start(ctx, bot, arg):
    user = ctx.message.author
    embedVar = discord.Embed(title= "Avalonian Raid T" + str(arg), description="Reply with `!desc <your_description_here>` to set a description.", color=0xf0f0f0)
    embedVar.add_field(name="🛡️ TANK", value="--", inline=True)
    embedVar.add_field(name="🏹 DPS", value="--", inline=True)
    embedVar.add_field(name="💚 HEAL", value="--", inline=True)
    embedVar.add_field(name="🔮 SUPP", value="--", inline=True)
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

async def btn_join_tank(interaction):
    btn_join(interaction, "🛡️ TANK")
async def btn_join_dps(interaction):
    btn_join(interaction, "🏹 DPS")
async def btn_join_heal(interaction):
    btn_join(interaction, "💚 HEAL")
async def btn_join_supp(interaction):
    btn_join(interaction, "🔮 SUPP")

async def btn_join(interaction, role):
    return

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