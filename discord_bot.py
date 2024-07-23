import asyncio
import discord
import tools.module as tl
from pymongo import MongoClient, UpdateOne
from datetime import datetime, timedelta
from discord.ext import commands
from discord import app_commands



# discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=".",intents=intents)



#config
cfg = tl.cfg_load("config")



#mongoDB
mongo_client = MongoClient(cfg["mongoDB"]["uri"])
db = mongo_client["csbay"]



#function that will find message in channel accord passed data
async def find_existing_message(channel, target_title):
    try:
        async for message in channel.history(limit=100):
            for embed in message.embeds:
                if embed.title == target_title:
                    return message
        return None
    except Exception as e:
        print(e)



#function that will create embed message for statistic data
async def send_statistics_embed():
    while not bot.is_closed():
        try:
            all_guild_channels = db["snipe_discord_channels"].find()

            for guild_channels in all_guild_channels:
                guild_id = guild_channels["_id"]
                stats_channel_id = guild_channels.get("statistics_channel")

                if not stats_channel_id:
                    continue

                stats_channel = bot.get_channel(stats_channel_id)
                if not stats_channel:
                    continue

                stats_message1 = await find_existing_message(stats_channel, "Market Statistics")
                stats_message2 = await find_existing_message(stats_channel, "Hourly Activity Levels")
                stats_message3 = await find_existing_message(stats_channel, "Most Common Snipes")

                data = db["snipe_statistic_market_data"].find().sort("count", -1)
                time_frame_data = db["snipe_statistic_time_frame"].find()
                hour_data = db["snipe_statistic_hour_data"].find()
                common_snipes_data = db["snipe_statistic_item_snipes"].find().sort("count", -1).limit(7)

                if data and time_frame_data and hour_data and common_snipes_data:
                    # Embed 1: Market Statistics
                    embed1 = discord.Embed(title="Market Statistics", description="Here are the latest stats:", color=discord.Color.blue())
                    for row in data:
                        embed1.add_field(name=f"{row.get('_id')}", value=f"📚 Recorded snipes: {row.get('count')} (*+{row.get('count') - row.get('last_hour_count')} last hour*)\n🔖 Average Discount: {row.get('average')}%\n💵 Max recorded profit: ${row.get('max_profit')} ([Jump]({row.get('message_url')}))", inline=False)

                    # Embed 2: Hourly Activity Levels
                    embed2 = discord.Embed(title="Hourly Activity Levels", description="Bot timezone is GMT+2\n[Compare it with your time](https://time.is/compare/GMT+2)\nActivity level = ⭐\n Profitability Level = 💰", color=discord.Color.red())
                    for row in hour_data:
                        activity_indicator = "⭐" * int(round(row.get("busyness_percentage", 0) / 2))
                        profit_indicator = "💰" * int(round(row.get("profit_percentage", 0) / 2))
                        hour = f"{row.get('_id'):02d}:00"
                        value = f"{activity_indicator}\n{profit_indicator}"
                        if datetime.now().hour == row.get("_id"):
                            embed2.add_field(name=f"> __**{hour}**__", value=value, inline=False)
                        else:
                            embed2.add_field(name=f"> {hour}", value=value, inline=False)
                    embed2.set_footer(text=f"Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")

                    # Embed 3: Most Common Snipes
                    embed3 = discord.Embed(title="Most Common Snipes", description="", color=discord.Color.green())
                    for row in common_snipes_data:
                        embed3.add_field(name=f"{row.get('_id')}", value=f"📚 Recorded snipes: {row.get('count')}\n🔖 Average Discount: {round(row.get('average_discount'), 2)}%", inline=False)
                    embed3.set_footer(text=f"Last updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")

                    if stats_message1 and stats_message2 and stats_message3:
                        await stats_message1.edit(embed=embed1)
                        await stats_message2.edit(embed=embed2)
                        await stats_message3.edit(embed=embed3)
                    else:
                        await stats_channel.send(embed=embed1)
                        await stats_channel.send(embed=embed2)
                        await stats_channel.send(embed=embed3)
        except Exception as e:
            print(e)
        finally:
            await asyncio.sleep(cfg["main"]["statistic_message_update_delay"])



#function that will embed message for the snipe feed 
async def create_embed(data):
    header = data["item_name"]
    risk = data["market_risk_factor"]
    try:
        if risk < cfg["main"]["risk_ranges"][0]:
            risk = "Low"
        elif risk < cfg["main"]["risk_ranges"][0]:
            risk = "Medium"
        elif risk < cfg["main"]["risk_ranges"][0]:
            risk = "High"
        else:
            risk = "Very High"
        risk = risk + " (" + str(data["buff_item_sell_num"]) + " on sale)"

        desc = f"**Risk:** `{risk}`\n**Market price:** ${data['market_price']}\n**Buff price:** ${data['buff_price']}\n**Potencial profit:** ${data['profit'][0]} / ${data['profit'][1]} (With buff fees) \n**Discount:** {data['buff_discount']}% ({round(100-data['buff_discount'], 2)}% Buff) \n\nBuff data was last updated <t:{int(data['buff_data_update_time'].timestamp())}:R>"

        embed = discord.Embed(title=header, description=desc, url=data["_id"])
        embed.set_thumbnail(url=data["buff_item_image"])
        embed.timestamp = datetime.utcnow()
        footer_text = data["market_name"]
        embed.set_footer(text=footer_text, icon_url=cfg["main"]["icons_urls"].get(data["market_name"], ""))
        return embed
    except Exception as e:
        tl.exceptions(e)



#function that will send newest offer
async def send_message(data):
    message = None
    message_url = None
    try:
        if not data:
            return
        
        guilds = bot.guilds
        for guild in guilds:
            collection = db["snipe_discord_channels"]
            channels_data = collection.find_one({"_id": guild.id})
            
            if not channels_data:
                continue

            channel_ids = [
                channels_data.get("low_channel"),
                channels_data.get("mid_channel"),
                channels_data.get("high_channel"),
                channels_data.get("best_snipes_channel"),
            ]

            channels = [bot.get_channel(ch_id) for ch_id in channel_ids if ch_id]
            
            if not channels:
                continue

            for item in data:
                embed = await create_embed(item)

                market_button = discord.ui.Button(label="Check it", style=discord.ButtonStyle.url, url=item["_id"])
                buff_button = discord.ui.Button(label="Buff price", style=discord.ButtonStyle.url, url=item["buff_item_link"])
                view = discord.ui.View()
                view.add_item(market_button)
                view.add_item(buff_button)

                price = item["market_price"]

                if price <= cfg["main"]["price_ranges"][0] and len(channels) > 0:
                    embed.colour = discord.Colour(cfg["main"]["message_colors"][0])
                    if channels[0]:
                        message = await channels[0].send(embed=embed, view=view)
                elif price < cfg["main"]["price_ranges"][1] and len(channels) > 1:
                    embed.colour = discord.Colour(cfg["main"]["message_colors"][1])
                    if channels[1]:
                        message = await channels[1].send(embed=embed, view=view)
                elif len(channels) > 2:     
                    embed.colour = discord.Colour(cfg["main"]["message_colors"][2])
                    if channels[2]:
                        message = await channels[2].send(embed=embed, view=view)

                if price > cfg["main"]["price_ranges"][2] and item["market_risk_factor"] < 7 and item["buff_discount"] >= 10 or item["profit"][1] > 5:
                    embed.colour = discord.Colour(cfg["main"]["message_colors"][3])
                    if len(channels) > 3 and channels[3]:
                        message = await channels[3].send(embed=embed, view=view)

    except Exception as e:
        tl.exceptions(e)
        return



#function that read data from database to get the newest snipe offers
async def message_worker():
    collection = db["snipe_processed_items"]
    
    while not bot.is_closed():
        # Fetch unprocessed items
        unprocessed_items = list(collection.find({"processed": {"$ne": True}}))
        if unprocessed_items:
            # Send message with unprocessed items
            await send_message(data=unprocessed_items)
            
            # Mark these items as processed
            for item in unprocessed_items:
                collection.update_one({"_id": item["_id"]}, {"$set": {"processed": True}})
                
        await asyncio.sleep(0.05)



#main discord run function
@bot.event
async def on_ready():
    print(f"Logged on as {bot.user}!")
    await asyncio.gather(message_worker(), send_statistics_embed())
    await bot.tree.sync()



#check if user is admin
def is_admin():
    async def predicate(interaction: discord.Interaction):
        return interaction.user.guild_permissions.administrator
    return app_commands.check(predicate)



#slash command to add channel into the database
@bot.tree.command(name="setup_channel", description="Setup snipe bot channels")
@app_commands.choices(choices=[
    app_commands.Choice(name="Channel for low value snipes", value="low"),
    app_commands.Choice(name="Channel for mid value snipes", value="mid"),
    app_commands.Choice(name="Channel for high value snipes", value="high"),
    app_commands.Choice(name="Channel for best snipes", value="best_snipes"),
    app_commands.Choice(name="Statistics channel", value="statistics"),
])
@is_admin()
async def setchannel(interaction: discord.Interaction, choices: app_commands.Choice[str]):
    channel_id = interaction.channel_id
    guild_id = interaction.guild_id
    collection = db["snipe_discord_channels"]
    field_map = {
        "low": "low_channel",
        "mid": "mid_channel",
        "high": "high_channel",
        "best_snipes": "best_snipes_channel",
        "statistics": "statistics_channel"
    }
    
    field_name = field_map.get(choices.value)
    if field_name:
        collection.update_one(
            {"_id": guild_id},
            {"$set": {field_name: channel_id}},
            upsert=True
        )
        await interaction.response.send_message(f"Channel <#{channel_id}> has been setup for this server.")
    else:
        await interaction.response.send_message("Invalid choice.")



#slash command that will remove snipe channel from the database
@bot.tree.command(name="remove_channel", description="Remove a snipe bot channel")
@app_commands.choices(choices=[
        app_commands.Choice(name="Remove low channel from database", value="low"),
        app_commands.Choice(name="Remove mid channel from database", value="mid"),
        app_commands.Choice(name="Remove high channel from database", value="high"),
        app_commands.Choice(name="Remove best snipes channel from database", value="best_snipes"),
        app_commands.Choice(name="Remove statistics channel from database", value="statistics"),
])
@is_admin()
async def removechannel(interaction: discord.Interaction, choices: app_commands.Choice[str]):
    guild_id = interaction.guild_id
    collection = db["snipe_discord_channels"]
    
    channel_field = ""
    
    if choices.value == "low":
        channel_field = "low_channel"
    elif choices.value == "mid":
        channel_field = "mid_channel"
    elif choices.value == "high":
        channel_field = "high_channel"
    elif choices.value == "best_snipes":
        channel_field = "best_snipes_channel"
    elif choices.value == "statistics":
        channel_field = "statistics_channel"

    if channel_field:
        existing_entry = collection.find_one({"_id": guild_id})
        if existing_entry and channel_field in existing_entry:
            collection.update_one(
                {"_id": guild_id},
                {"$unset": {channel_field: ""}},
                upsert=True
            )
            await interaction.response.send_message(f"Channel {channel_field} has been removed from this server.")
        else:
            await interaction.response.send_message(f"No existing channel found for {channel_field}.")
    else:
        await interaction.response.send_message("Invalid choice.")



bot.run(cfg["main"]["discord_client_token"])