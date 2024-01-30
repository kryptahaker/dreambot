import nextcord
from nextcord.ext import commands
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests
import asyncio
import psutil
import datetime
import time

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='superperfix', intents=intents)

właściciele = [835959167540789279, 776494298450755594, 1024755404904874054, 1199613034868514846]
plus_minus_allowed = [1176973813003595837, 1173962190995324999, 1194337016914116699, 1142059932011741284, 1173965066891178014, 1142059921580507157, 1173965067780378634]
plus_roles_order = [1171906897964703845, 1171906931431051368, 1171906928889311232]
plus_roles_remove = [1171906928889311232, 1171906931431051368, 1171906897964703845]
minus_roles_order = [1171907227330822177, 1171907230157774909, 1171907232347193435]
minus_roles_remove = [1171907232347193435, 1171907230157774909, 1171907227330822177]
Token = "MTE0MjE4MzgyODMxNjc2MjE4Mg.GIDJie.KcuOn5e4aDhdHZ9CIpjS8KSFL2OSfrHgSRGEDs"

#Baza danych
DBAccount = "MainAccount"
DBPassword = "1EfzIeQYvsBvTir3"
uri = f"mongodb+srv://{DBAccount}:{DBPassword}@dreambot.utpybla.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Main']
dbInfo = client['Info']
settings_collection = db['settings']
currency_collection = db['currency']
cooldowns_collection = db['cooldowns']
notes_collection = db['notes']
users_collection = dbInfo['Users']
backup_collection = dbInfo['Backup']
fish_collection = dbInfo['Fish']
guilds_collection = dbInfo['Guilds']
website_collection = dbInfo['Website']



class AddPremium(nextcord.ui.View):
    def __init__(self, id):
        super().__init__(timeout=None)
        self.value = None
        self.id = id

    @nextcord.ui.button(label="Dodaj premium ⭐", style=nextcord.ButtonStyle.green)
    async def button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        if any(interaction.user.id == owner_id for owner_id in właściciele):
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            server_id = str(self.id)
            server_data = settings_collection.find_one({"_id": server_id})
            if server_data:
                new_premium_status = not server_data.get("premium", False)
                settings_collection.update_one({"_id": server_id}, {"$set": {"premium": new_premium_status}})
            else:
                settings_collection.insert_one({"_id": server_id, "premium": True})

            await interaction.send(f"`[✅]:` Pomyslnie dodano premium na serwer o ID: *{self.id}*", ephemeral=True)

            channel = bot.get_channel(1142449182855147660)
            
            server_info = settings_collection.find_one({"_id": str(id)})
            if server_info and "owner" in server_info:
                wlasciciel = server_info["owner"]
            else:
                wlasciciel = "Brak"

            embed = nextcord.Embed(title=f"**Premium zostalo nadane ⭐**", description=f"**🎈 ID: {server_id}**\n**👨‍💼 Wlasciciel: {wlasciciel}**\n**👤 Administrator: {interaction.user.mention}**", color=0xffe600)
            thumbnail_url = bot.user.avatar.url
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_footer(text=current_time)
            await channel.send(embed=embed)
        else:
            await interaction.send("`[❌]:` Tej komendy moga jedynie uzywac wlasciciele bota!", ephemeral=True)

class RemovePremium(nextcord.ui.View):
    def __init__(self, id):
        super().__init__(timeout=None)
        self.value = None
        self.id = id

    @nextcord.ui.button(label="Zabierz premium ⭐", style=nextcord.ButtonStyle.red)
    async def button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        if any(interaction.user.id == owner_id for owner_id in właściciele):
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            server_id = str(self.id)
            server_data = settings_collection.find_one({"_id": server_id})
            if server_data:
                settings_collection.update_one({"_id": server_id}, {"$unset": {"premium": ""}})
                await interaction.send(f"`[✅]:` Pomyślnie zabrano premium z serwera o ID: *{self.id}*", ephemeral=True)

                channel = bot.get_channel(1142449182855147660)
                server_info = settings_collection.find_one({"_id": str(id)})
                if server_info and "owner" in server_info:
                    wlasciciel = server_info["owner"]
                else:
                    wlasciciel = "Brak"

                embed = nextcord.Embed(title=f"**Premium zostało odebrane ⭐**", description=f"**🎈 ID: {server_id}**\n**👨‍💼 Właściciel: {wlasciciel}**\n**👤 Administrator: {interaction.user.mention}**", color=0xe40c0c)
                thumbnail_url = bot.user.avatar.url
                embed.set_thumbnail(url=thumbnail_url)
                embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                embed.set_footer(text=current_time)
                await channel.send(embed=embed)
        else:
            await interaction.send("`[❌]:` Tej komendy mogą jedynie używać właściciele bota!", ephemeral=True)

global turned_on
turned_on = True

async def CheckStatus():
    global turned_on
    try:
        response = requests.get("http://localhost:5000/status")
        if turned_on == False:
            turned_on = True
            channel = bot.get_channel(1142449182855147660)
            previous_messages = await channel.history(limit=5).flatten()
            for message in previous_messages:
                if message.author == bot.user:
                    await message.delete()

            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=f"*Bot jest online*", color=0x008000)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_footer(text=current_time)
            await channel.send(embed=embed)
    except Exception:
        if turned_on == True:
            turned_on = False
            channel = bot.get_channel(1142449182855147660)
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=f"*Bot jest offline*", color=0xd7231a)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_footer(text=current_time)
            await channel.send(embed=embed)
            
async def CheckStatusLoop():
    while True:
        await CheckStatus()
        await asyncio.sleep(5)

#On_ready
@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"DreamBot support"))
    await CheckStatusLoop()

#Info
@bot.slash_command(description="Wyświetla statystyki bota (Tylko właściciele bota)")
async def info(ctx):
    if any(ctx.user.id == owner_id for owner_id in właściciele):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        target_date = datetime.datetime(2023, 8, 17, 22, 19)
        author = ctx.user
        ping = round(bot.latency * 1000)

        statistics_document = website_collection.find_one({'_id': 'statistics'})
        if statistics_document:
            total_users = statistics_document.get('users', 0)
            serwery = statistics_document.get('servers', 0)
            kanaly = statistics_document.get('channels', 0)

        current_time2 = datetime.datetime.now()
        uptime = current_time2 - target_date
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        uptime_str = f"{days} dni, {hours} godzin, {minutes} minut"
        ram = psutil.virtual_memory()
        used_mb = ram.used / (1024 ** 3)
        usage = f"{used_mb:.2f}"  
        whole_part, decimal_part = usage.split('.')
        usage = f"{whole_part}.{decimal_part[:2]}"

        available_databases = client.list_database_names()
        database_info = []
        for database_name in available_databases:
            if database_name not in ["admin", "local"]:
                db = client[database_name]
                collections = db.list_collection_names()
                collections = [collection for collection in collections if collection != "oplog.rs"]
                if collections:
                    collections_str = ", ".join(collections)
                    database_info.append(f"{database_name} ({collections_str})")

        database_info_str = "\n".join(database_info)

        embed = nextcord.Embed(title="DreamBot", description="*Oto statystyki bota!*", color=0x00ff00)
        embed.add_field(name="**Serwery:**", value=f"```{serwery}```", inline=True)
        embed.add_field(name="**Osoby:**", value=f"```{total_users}```", inline=True)
        embed.add_field(name="**Kanały:**", value=f"```{kanaly}```", inline=True)
        embed.add_field(name="**Bot online:**", value=f"```{uptime_str}```", inline=True)
        embed.add_field(name="**Ping:**", value=f"```{ping}```", inline=True)
        embed.add_field(name="**RAM:**", value=f"```{usage}MB```", inline=True)

        latest_backup = backup_collection.find_one(sort=["_id"])
        if latest_backup:
            backup_date = latest_backup.get("_id")
            embed.add_field(name="**Data najnowszego backupu:**", value=f"```{backup_date}```", inline=False)
        else:
            embed.add_field(name="**Data najnowszego backupu:**", value="```Brak dostępnych backupów! (Stwórz takowy jak najszybciej!)```", inline=False)

        embed.add_field(name="**Node'y:**", value=f"```{database_info_str}```", inline=False)
        embed.add_field(name="**Właściciele:**", value=f"```xdokinelek#0 / dokinelek#0\nhhakerr#0```", inline=False)
        embed.add_field(name="**Współwłaściciel:**", value=f"```1kvs.#0```", inline=False)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        thumbnail_url = ctx.guild.icon.url if ctx.guild.icon else bot.user.avatar.url
        embed.set_thumbnail(url=thumbnail_url)
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        await ctx.send(embed=embed)
    else:
        await ctx.send("`[❌]:` Tej komendy mogą jedynie używać właściciele bota!", ephemeral=True)

#Zakup
@bot.slash_command(description="Wysyła wiadomość po zakupie premium (Tylko właściciele bota)")
async def zakup(ctx, uzytkownik: nextcord.Member):
    if any(ctx.user.id == owner_id for owner_id in właściciele):
        await ctx.send(f"{uzytkownik.mention} dziękujemy za zakup!!\n\nCześć dziękujemy za zakup bota premium jesteśmy szczęśliwi że dzięki tobie możemy się rozwijać i tworzyć bota coraz lepszego.\n\nWrazie problemów z premium botem zgłoś się na ticketa.\n\nZwrot produktu:\n\nAby zwrócić produkt ( bot premium ) należy skontaktować się z <@1024755404904874054> zwrot kupionego produktu możliwy jest od momentu zakupu przez 4 dni ( jeśli zwrócisz produkt premium zostanie usunięte z twojego serwera )\n\nAdministracja DreamBot")

#Check
@bot.slash_command(description="XDX")
async def check(ctx):
    await ctx.send("XDX")

#Premium
@check.subcommand(description="Sprawdza czy podany serwer ma permium (Tylko właściciele bota)")
async def premium(ctx, id):
    if any(ctx.user.id == owner_id for owner_id in właściciele):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        author = ctx.user
        server_data = settings_collection.find_one({"_id": str(id)})
        server = bot.get_guild(int(id))

        if server_data and server_data.get("premium", False):
            color = 0xffe600
            embed = nextcord.Embed(title="Status premium ⭐ serwera", color=color)
            embed.description = f"Serwer o ID {id} ma premium!"
            view = RemovePremium(id)
        else:
            color = 0xe40c0c
            embed = nextcord.Embed(title="Status premium ⭐ serwera", color=color)
            embed.description = f"Serwer o ID {id} nie ma premium lub nie istnieje w bazie danych."
            view = AddPremium(id)

        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        if server and server.icon:
            embed.set_thumbnail(url=server.icon.url)

        await ctx.send(embed=embed, view=view)
    else:
        await ctx.send("`[❌]:` Tej komendy mogą jedynie używać właściciele bota!", ephemeral=True)

#Leave
@bot.slash_command(description="Opuszcza serwery z mniejszą ilością członków niż [minosob]")
async def leave(ctx, minosob: int):
    if any(ctx.user.id == owner_id for owner_id in właściciele):
        if ctx.user.id == 1024755404904874054:
            return
        servers_to_leave = [server for server in bot.guilds if len(server.members) < minosob]
        num = 0
        for server in servers_to_leave:
            num += 1
            await server.leave()
        await ctx.send(f'`[✅]:` Opuszczono serwery z mniej niż {minosob} członkami! ({num} serwerów)')
    else:
        await ctx.send("`[❌]:` Tej komendy mogą jedynie używać właściciele bota!", ephemeral=True)

#Akceptuj
@bot.slash_command(description="Akceptuje automatyczną reklamę!")
async def akceptuj(ctx):
    await ctx.send("XDX")

#Odrzuć
@bot.slash_command(description="Odrzuca automatyczną reklamę!")
async def odrzuć(ctx):
    await ctx.send("XDX")

#Autoad
@akceptuj.subcommand(description="Akceptuje automatyczną reklamę!")
async def autoad(ctx, id: str, reklama):
    if ctx.channel.id == 1175540326845399049:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        settings_document = settings_collection.find_one({'_id': str(id)})
        if not settings_document:
            settings_document = {'_id': id}

        settings_document['autoReklamaStatus'] = "Zaakceptowana"
        settings_document['autoAdReklama'] = reklama

        await ctx.send(f"`[✅]:` Automatyczna reklama (*{id}*) została zaakceptowana!", ephemeral=True)
        settings_collection.update_one({'_id': id}, {'$set': settings_document})

        channel = bot.get_channel(1142449182855147660)
        logi = bot.get_channel(1148208855512264735)
        server_info = settings_collection.find_one({"_id": str(id)})
        if server_info and "owner" in server_info:
            wlasciciel = server_info["owner"]
            guild = ctx.guild
        else:
            wlasciciel = "Brak"

        embed = nextcord.Embed(title=f"**Reklama została zaakceptowana**", description=f"**🎈 ID: {id}**\n**👨‍💼 Właściciel: {wlasciciel}**\n**👤 Weryfikator: {ctx.user.mention}**", color=0x008000)
        thumbnail_url = bot.user.avatar.url
        embed.set_thumbnail(url=thumbnail_url)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_footer(text=current_time)
        wlasciciel = guild.get_member_named(wlasciciel)
        if wlasciciel:
            await channel.send(f"{wlasciciel.mention}", embed=embed)
        else:
            await channel.send(embed=embed)

        await logi.send(embed=embed)
        await logi.send(f"```{reklama}```")
    else:
        await ctx.send("`[❌]:` Tej komendy nie można używać na tym kanale!", ephemeral=True)

#Autoad
@odrzuć.subcommand(description="Odrzuca automatyczną reklamę!")
async def autoad(ctx, id: str, powód):
    if ctx.channel.id == 1175540326845399049:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        settings_document = settings_collection.find_one({'_id': str(id)})
        if not settings_document:
            settings_document = {'_id': id}

        if 'autoAdReklama' in settings_document:
            del settings_document['autoAdReklama']

        settings_document['autoReklamaStatus'] = f"Odrzucona - {powód}"
        settings_document['autoAdReklama'] = None

        await ctx.send(f"`[✅]:` Automatyczna reklama (*{id}*) została odrzucona z powodem {powód}!", ephemeral=True)
        settings_collection.update_one({'_id': id}, {'$set': settings_document})

        channel = bot.get_channel(1142449182855147660)
        server_info = settings_collection.find_one({"_id": str(id)})
        if server_info and "owner" in server_info:
            wlasciciel = server_info["owner"]
            guild = ctx.guild
        else:
            wlasciciel = "Brak"

        embed = nextcord.Embed(title=f"**Reklama została odrzucona**", description=f"**🎈 ID: {id}**\n**👨‍💼 Właściciel: {wlasciciel}**\n\n**🔨 Powód: {powód}**", color=0xe40c0c)
        thumbnail_url = bot.user.avatar.url
        embed.set_thumbnail(url=thumbnail_url)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_footer(text=current_time)
        wlasciciel = guild.get_member_named(wlasciciel)
        if wlasciciel:
            await channel.send(f"{wlasciciel.mention}", embed=embed)
        else:
            await channel.send(embed=embed)
    else:
        await ctx.send("`[❌]:` Tej komendy nie można używać na tym kanale!", ephemeral=True)

#plus
@bot.slash_command(description='Nadaje rolę plusa')
async def plus(ctx, uzytkownik: nextcord.Member):
    author_roles = [role.id for role in ctx.user.roles]
    if any(role_id in plus_minus_allowed for role_id in author_roles):
        try:
            for role_id_to_remove in minus_roles_remove:
                role_to_remove = ctx.guild.get_role(role_id_to_remove)
                if role_to_remove and role_to_remove in uzytkownik.roles:
                    await uzytkownik.remove_roles(role_to_remove)
                    await ctx.send(f'`[✅]:` Dodano użytkownikowi {uzytkownik.mention} plusa!', ephemeral=True)
                    return

            for role_id_to_add in plus_roles_order:
                role_to_add = ctx.guild.get_role(role_id_to_add)
                if role_to_add and role_to_add not in uzytkownik.roles:
                    await uzytkownik.add_roles(role_to_add)
                    await ctx.send(f'`[✅]:` Dodano użytkownikowi {uzytkownik.mention} plusa!', ephemeral=True)
                    break

        except Exception:
            await ctx.send('`[❌]:` Ten użytkownik ma maksymalną ilość plusów', ephemeral=True)

#minus
@bot.slash_command(description='Nadaje rolę minusa')
async def minus(ctx, uzytkownik: nextcord.Member):
    author_roles = [role.id for role in ctx.user.roles]
    if any(role_id in plus_minus_allowed for role_id in author_roles):
        try:
            for role_id_to_remove in plus_roles_remove:
                role_to_remove = ctx.guild.get_role(role_id_to_remove)
                if role_to_remove and role_to_remove in uzytkownik.roles:
                    await uzytkownik.remove_roles(role_to_remove)
                    await ctx.send(f'`[✅]:` Dodano użytkownikowi {uzytkownik.mention} minusa!', ephemeral=True)
                    return

            for role_id_to_add in minus_roles_order:
                role_to_add = ctx.guild.get_role(role_id_to_add)
                if role_to_add and role_to_add not in uzytkownik.roles:
                    await uzytkownik.add_roles(role_to_add)
                    await ctx.send(f'`[✅]:` Dodano użytkownikowi {uzytkownik.mention} minusa!', ephemeral=True)
                    break

        except Exception:
            await ctx.send('`[❌]:` Ten użytkownik ma maksymalną ilość minusów', ephemeral=True)

#admininfo
@bot.slash_command(description='Wyświetla ilość plusów i minusów')
async def admininfo(ctx, uzytkownik: nextcord.Member):
    author = ctx.user
    server_id = str(ctx.guild.id)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    user_document = users_collection.find_one({'_id': str(uzytkownik.id)})
    if user_document:
        tickets_taken_data = user_document.get('Guilds', {}).get(server_id, {})
        tickets_taken = tickets_taken_data.get('TicketsTaken', 0)

    main_role = uzytkownik.top_role.name
    if main_role == "@everyone" or main_role == "all" or main_role == "𝗔𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗰𝗷𝗮 | 𝗗𝗿𝗲𝗮𝗺𝗕𝗼𝘁":
        roles = [role.name for role in uzytkownik.roles if role.name != "@everyone" and role.name != "𝗔𝗱𝗺𝗶𝗻𝗶𝘀𝘁𝗿𝗮𝗰𝗷𝗮 | 𝗗𝗿𝗲𝗮𝗺𝗕𝗼𝘁"]
        if roles:
            main_role = roles[-1]

    plus_count = sum(1 for role_id in plus_roles_order if ctx.guild.get_role(role_id) in uzytkownik.roles)
    minus_count = sum(1 for role_id in minus_roles_order if ctx.guild.get_role(role_id) in uzytkownik.roles)

    embed = nextcord.Embed(description=f"> 👤 Ranga: {main_role}\n> ➕ Plus: {plus_count}\n> ➖ Minus: {minus_count}\n> ✋ Przejęte tickety: {tickets_taken}", color=0xffe600)
    thumbnail_url = uzytkownik.avatar.url if uzytkownik.avatar else bot.user.avatar.url
    embed.set_thumbnail(url=thumbnail_url)
    embed.set_author(name=uzytkownik.display_name, icon_url=thumbnail_url)
    embed.set_footer(text=f"Invoked by {author} | {current_time}")
    await ctx.send(embed=embed)



bot.run(Token)