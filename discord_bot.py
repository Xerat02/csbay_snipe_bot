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
        latest_message = None
        async for message in channel.history(limit=100):
            for embed in message.embeds:
                if embed.title == target_title:
                    latest_message = message
                    break
        return latest_message
    except Exception as e:
        print(e)



#function that will create embed message for statistic data
async def send_statistics_embed():
    while not bot.is_closed():
        try:
            now = datetime.now()
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
                await asyncio.sleep(5)
                stats_message2 = await find_existing_message(stats_channel, "Best Snipes")
                await asyncio.sleep(5)
                stats_message3 = await find_existing_message(stats_channel, "Hourly Activity Levels")
                await asyncio.sleep(5)
                stats_message4 = await find_existing_message(stats_channel, "Most Common Snipes")

                await asyncio.sleep(5)

                data = db["snipe_statistic_market_data"].find().sort("count", -1)
                time_frame_data = db["snipe_statistic_time_frame"].find()
                hour_data = db["snipe_statistic_hour_data"].find()
                common_snipes_data = db["snipe_statistic_item_snipes"].find().sort("count", -1).limit(7)
                all_markets_stats = db["snipe_statistic"].find_one({"_id": "All markets"})

                if data and time_frame_data and hour_data and common_snipes_data and all_markets_stats:
                    # Embed 1: Market Statistics
                    embed1 = discord.Embed(title="Market Statistics", color=discord.Color.blue())

                    embed1.add_field(name=f"{all_markets_stats.get('_id')}", value=f"📚 Recorded snipes: {all_markets_stats.get('count')} (*+{all_markets_stats.get('count') - all_markets_stats.get('last_hour_count')} last hour*)\n🔖 Average Discount: {all_markets_stats.get('average')}%\n💵 Max recorded profit: ${all_markets_stats.get('max_profit')} ([Jump]({all_markets_stats.get('message_url')}))", inline=False)
                    for row in data:
                        embed1.add_field(name=f"{row.get('_id')}", value=f"📚 Recorded snipes: {row.get('count')} (*+{row.get('count') - row.get('last_hour_count')} last hour*)\n🔖 Average Discount: {row.get('average')}%\n💵 Max recorded profit: ${row.get('max_profit')} ([Jump]({row.get('message_url')}))", inline=False)

                    embed1.add_field(name="", value=f"Last updated: <t:{int(now.timestamp())}:R>")

                    # Embed 2: Best Snipes
                    def remove_trailing_zeros(x):
                        if "." in x:
                            if x.endswith("0") or x.endswith("."):
                                return(remove_trailing_zeros(x[:-1]))
                        else:
                            return(x)

                    embed2 = discord.Embed(title="Best Snipes", color=discord.Color.pink())   

                    for row in time_frame_data:
                        time_frame = int(row.get("_id")) 
                        x = 0   
                        if time_frame < 60:
                            x = time_frame
                            time_frame = remove_trailing_zeros(str(x)) + " min"
                        elif time_frame / 60 < 24:
                            x = time_frame / 60
                            time_frame = remove_trailing_zeros(str(x)) + " h" 
                        elif time_frame / 1440 < 7:
                            x = time_frame / 1440
                            time_frame = remove_trailing_zeros(str(x)) + " d"
                        elif time_frame / 10080 < 5:
                            x = time_frame / 10080
                            time_frame = remove_trailing_zeros(str(x)) + " w"     

                        embed2.add_field(name=f"The best snipe in {time_frame}:", value=f"Market: {row.get('market')}\nPotencial profit: ${row.get('potencial_profit')} ([Jump]({row.get('message_url')}))\nDiscount: {row.get('discount')}%", inline=False)

                    embed2.add_field(name="", value=f"Last updated: <t:{int(now.timestamp())}:R>")


                    # Embed 3: Hourly Activity Levels
                    embed3 = discord.Embed(title="Hourly Activity Levels", description="Activity level = ⭐\n Profitability Level = 💰", color=discord.Color.red())
                    for row in hour_data:
                        activity_indicator = "⭐" * int(round(row.get("busyness_percentage", 0)))
                        profit_indicator = "💰" * int(round(row.get("profit_percentage", 0)))
                        hour = f"{row.get('_id'):02d}:00"
                        value = f"{activity_indicator}\n{profit_indicator}"

                        if now.hour == row.get("_id"):
                            embed3.add_field(name=f"> __<t:{int(now.timestamp())}:t>__", value=value, inline=False)
                        else:
                            embed3.add_field(name=f"> <t:{((int(now.timestamp()) - (now.hour * 3600) - (now.minute*60))) + (int(row.get('_id')) * 3600)}:t>", value=value, inline=False)
                    embed3.add_field(name="", value=f"Last updated: <t:{int(now.timestamp())}:R>")

                    # Embed 4: Most Common Snipes
                    embed4 = discord.Embed(title="Most Common Snipes", description="", color=discord.Color.green())
                    for row in common_snipes_data:
                        embed4.add_field(name=f"{row.get('_id')}", value=f"📚 Recorded snipes: {row.get('count')}\n🔖 Average Discount: {round(row.get('average_discount'), 2)}%", inline=False)
                    embed4.add_field(name="", value=f"Last updated: <t:{int(now.timestamp())}:R>")

                    if stats_message1:
                        await stats_message1.edit(embed=embed1)
                    else:
                        await stats_channel.send(embed=embed1)

                    await asyncio.sleep(2)

                    if stats_message2:
                        await stats_message2.edit(embed=embed2)
                    else:
                        await stats_channel.send(embed=embed2)

                    await asyncio.sleep(2)

                    if stats_message3:
                        await stats_message3.edit(embed=embed3)
                    else:
                        await stats_channel.send(embed=embed3)

                    await asyncio.sleep(2)

                    if stats_message4:
                        await stats_message4.edit(embed=embed4)
                    else:
                        await stats_channel.send(embed=embed4)
        except Exception as e:
            print(e)
        finally:
            await asyncio.sleep(cfg["main"]["statistic_message_update_delay"])



#function that will embed message for the snipe feed 
async def create_embed(data):
    try:
        header = data.get("item_name", "Unknown Item")
        risk_factor = data.get("market_risk_factor", 3)
        buff_sell_num = data.get("buff_item_sell_num", "N/A")

        risk_levels = ["Low", "Medium", "High", "Very High"]
        risk = f"{risk_levels[min(risk_factor, 3)]} ({buff_sell_num} on sale)"

        buff_discount = data.get("buff_discount", 0)
        steam_discount = data.get("steam_discount", 0)
        market_price = data.get("market_price", 0.0)
        buff_price = data.get("buff_price", 0.0)
        potential_profit = data.get("profit", [0, 0])[0]

        if buff_discount >= 15:
            buff_color = "🟩"  
        elif buff_discount >= 10:
            buff_color = "🟨"  
        elif buff_discount >= 6.5:
            buff_color = "🟧"  
        else:
            buff_color = "🟥"  


        desc = (
            f"**Risk:** `{risk}`\n"
            f"**Market price:** ${market_price}\n"
            f"**Buff price:** ${buff_price}\n"
            f"**Potential profit:** ${potential_profit}\n"
            f"**Buff discount:** {buff_color} **{buff_discount}%** ({round(100 - buff_discount, 2)}% Buff)"
        )
        
        if steam_discount > buff_discount:
            desc += f"\n**Steam discount:** {steam_discount}% ({round(100 - steam_discount, 2)}% Steam)"
        
        buff_update_time = int(data.get("buff_data_update_time", datetime.now()).timestamp())
        desc += f"\n\nBuff data was last updated <t:{buff_update_time}:R>"

        embed = discord.Embed(title=header, description=desc, url=data.get("market_link", ""))
        embed.set_thumbnail(url=data.get("buff_item_image", ""))
        
        footer_text = data.get("market_name", "Unknown Market")
        embed.set_footer(text=footer_text, icon_url=cfg["main"]["icons_urls"].get(data.get("market_name", ""), ""))

        return embed
    except Exception as e:
        tl.exceptions(e)




#function that will send newest offer
async def send_message(data):
    if not data:
        return
    
    guilds = bot.guilds
    for guild in guilds:
        try:
            print(f"Processing guild: {guild.name}")
            collection = db["snipe_discord_channels"]
            channels_data = collection.find_one({"_id": guild.id})
            if not channels_data:
                continue

            low_channel_id = channels_data.get("low_channel")
            mid_channel_id = channels_data.get("mid_channel")
            high_channel_id = channels_data.get("high_channel")
            best_snipes_channel_id = channels_data.get("best_snipes_channel")

            low_channel = bot.get_channel(low_channel_id) if low_channel_id else None
            mid_channel = bot.get_channel(mid_channel_id) if mid_channel_id else None
            high_channel = bot.get_channel(high_channel_id) if high_channel_id else None
            best_snipes_channel = bot.get_channel(best_snipes_channel_id) if best_snipes_channel_id else None

            for item in data:
                embed = await create_embed(item)
                market_button = discord.ui.Button(label="Check it", style=discord.ButtonStyle.url, url=item["market_link"])
                buff_button = discord.ui.Button(label="Buff price", style=discord.ButtonStyle.url, url=item["buff_item_link"])
                view = discord.ui.View()
                view.add_item(market_button)
                view.add_item(buff_button)
                
                price = item["market_price"]

                if price <= cfg["main"]["price_ranges"][0] and low_channel:
                    embed.colour = discord.Colour(cfg["main"]["message_colors"][0])
                    message = await low_channel.send(embed=embed, view=view)
                elif price < cfg["main"]["price_ranges"][1] and mid_channel:
                    embed.colour = discord.Colour(cfg["main"]["message_colors"][1])
                    message = await mid_channel.send(embed=embed, view=view)
                elif high_channel:     
                    embed.colour = discord.Colour(cfg["main"]["message_colors"][2])
                    message = await high_channel.send(embed=embed, view=view)

                if (item["buff_discount"] >= 10 or item["profit"][1] >= 70) and item["market_risk_factor"] < 2 and item["market_price"] >= 10 and best_snipes_channel:
                    embed.colour = discord.Colour(cfg["main"]["message_colors"][3])
                    message = await best_snipes_channel.send(embed=embed, view=view)

        except Exception as e:
            tl.exceptions(e)
            continue


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
                
        await asyncio.sleep(0.1)



#main discord run function
@bot.event
async def on_ready():
    await bot.tree.sync()
    activity = discord.Activity(type=discord.ActivityType.watching, name="csbay.net/sniper")
    await bot.change_presence(activity=activity)
    await asyncio.gather(message_worker(), send_statistics_embed())

    print(f"Logged on as {bot.user}!")
    


#check if user is admin
def is_admin():
    async def predicate(interaction: discord.Interaction):
        return interaction.user.guild_permissions.administrator
    return app_commands.check(predicate)



#slash command that will send info message
@bot.tree.command(name="send_info", description="Send information embed")
@is_admin()
async def send_info(interaction: discord.Interaction):
    embed = discord.Embed(
        title="CSBAY Skin Snipes",
        description=(
            "### How It Works:\n"
            "The Snipe Bot continuously monitors all well-known marketplaces in real-time. It compares the prices of skins across these platforms with the largest marketplace, Buff163. By doing this, it identifies the best deals and opportunities for you.\n\n"
            "### Benefits for Our Users:\n"
            "**Flip Skins for Profit:** Easily find underpriced skins on various marketplaces and flip them for a profit.\n"
            "**Smart Investments:** Invest in skins at the best market prices, ensuring you get the most value for your money.\n"
            "**Real-Time Alerts:** Receive instant notifications about price discrepancies and potential deals, so you never miss an opportunity.\n"
            "**Comprehensive Monitoring:** Our bot covers all major marketplaces, providing you with a complete overview of the market.\n\n"
            "**Market price** = price from the particular market\n"
            "**Buff price** = price from buff.163.com (biggest Asian marketplace)\n"
            "**Discount** = price difference between those two prices in %\n\n"
            "The CSBAY Team"
        ),
        color=discord.Colour(cfg["main"]["info_message_color"])
    )

    await interaction.response.send_message(embed=embed)



# Slash command to add a channel into the database
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
    
    # Check bot's permissions in the channel
    channel = bot.get_channel(channel_id)
    permissions = channel.permissions_for(channel.guild.me)
    
    required_permissions = [
        permissions.view_channel,
        permissions.send_messages,
        permissions.embed_links,
        permissions.attach_files
    ]
    
    if all(required_permissions):
        if field_name:
            collection.update_one(
                {"_id": guild_id},
                {"$set": {field_name: channel_id}},
                upsert=True
            )
            await interaction.response.send_message(
                f"Channel <#{channel_id}> has been successfully set up for this server! "
                f"Snipes will start rolling in soon, so stay tuned! Also make sure the bot has all the necessary **permissions** to keep things running smoothly."
            )
        else:
            await interaction.response.send_message("Invalid choice.")
    else:
        missing_perms = ", ".join([perm[0] for perm in zip(
            ["View Channel", "Send Messages", "Embed Links", "Attach Files"], required_permissions) if not perm[1]])
        await interaction.response.send_message(
            f"Bot is missing the following permissions in <#{channel_id}>: **{missing_perms}**! "
            f"Please ensure the bot has these permissions and try again. \n\nIf you still have a problem please join our [support server](https://discord.com/invite/csbay-cs2-trading-642813124629757953) and open a ticket."
        )



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
            await interaction.response.send_message(f"{channel_field} has been removed from this server.")
        else:
            await interaction.response.send_message(f"You can't remove this channel, because its not presented in our database!.")
    else:
        await interaction.response.send_message("Invalid choice.")



bot.run(cfg["main"]["discord_client_token"])