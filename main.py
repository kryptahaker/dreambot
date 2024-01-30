import nextcord
from nextcord import utils
from nextcord.ext import commands
from nextcord import FFmpegPCMAudio, File
from flask import Flask, jsonify
import threading
import os
import re
import io
import time
import json
import pytz
import emoji
import random
import string
import aiohttp
import asyncio
import requests
import datetime
from datetime import timedelta
from translate import Translator
from collections import defaultdict
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import urlparse
from nextcord import TextInputStyle



intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='superperfix', intents=intents)
słowa_zgadywanka1 = ["sztuka", "muzyka", "literatura", "teatr", "film", "malarstwo", "rzeźba", "fotografia", "architektura", "design", "moda", "kultura", "historia", "nauka", "matematyka", "fizyka", "chemia", "biologia", "geografia", "astronomia", "psychologia", "socjologia", "filozofia", "ekonomia", "polityka", "religia", "technologia", "informatyka", "programowanie", "internet", "komunikacja", "komputery", "smartfony", "aplikacje", "serwisy społecznościowe", "gry", "sport", "fitness", "zdrowie", "medycyna", "dieta", "psychoterapia", "yoga", "medytacja", "podróże", "turystyka", "wycieczki", "zwiedzanie", "przyroda", "krajobrazy", "wakacje", "kultura", "historia", "muzea", "zabytki", "relaks", "odpoczynek", "rozrywka", "film", "książki", "muzyka", "koncerty", "festiwale", "sztuka", "teatr", "komedia", "dramat", "romans", "akcja", "thriller", "science fiction", "fantasy", "detektywistyczny", "kryminał", "horror", "komiksy", "pozycja", "przeżycie", "emocje", "kreatywność", "twórczość", "wyobraźnia", "inspiracja", "pasja", "zainteresowania", "hobby", "rękodzieło", "handmade", "projektowanie", "szydełkowanie", "hakowanie", "malowanie", "rzeźbienie", "krawiectwo", "kulinaria", "gotowanie", "pieczenie", "desery", "kuchnia światowa", "wegańskie", "wegetariańskie", "diety specjalne", "kuchnia fusion", "smaki", "aromat", "przyprawy"]
słowa_zgadywanka2 = ["żółty", "niebieski", "czerwony", "zielony", "pomarańczowy", "fioletowy", "różowy", "biały", "czarny", "szary", "brązowy", "złoty", "srebrny", "miedziany", "stalowy", "szafirowy", "rubinowy", "bursztynowy", "ametystowy", "perłowy", "diamentowy", "woda", "ogień", "ziemia", "powietrze", "energia", "światło", "cień", "dźwięk", "cisza", "radość", "smutek", "miłość", "nienawiść", "nadzieja", "strach", "marzenie", "rzeczywistość", "czas", "przestrzeń", "dźwięk", "muzyka", "melodia", "harmonia", "równowaga", "szaleństwo", "normalność", "tajemnica", "zagadka", "tęcza", "deszcz", "wiatr", "burza", "spokój", "haos", "natura", "wszechświat", "kosmos", "galaktyka", "planeta", "gwiazda", "księżyc", "słońce", "gwiazdozbiór", "zodiak", "horoskop", "zimno", "ciepło", "wiosna", "lato", "jesień", "zima", "pora roku", "święto", "uroczystość", "tradycja", "zwyczaj", "kultura", "religia", "wiara", "nauka", "wiedza", "mądrość", "pytanie", "odpowiedź", "sens", "cel", "zadanie", "praca", "wysiłek", "sukces", "porażka", "walka", "pokój", "wojna", "szansa", "ryzyko", "szczęście", "pech", "śmiech", "łzy", "uśmiech", "emocje"]
słowa_zgadywanka3 = ["ocean", "góra", "dolina", "las", "łąka", "rzeka", "jezioro", "morze", "pustynia", "savana", "dżungla", "polarna", "wydma", "wyżyna", "zatoka", "wyspa", "wysepka", "bajka", "mit", "legend", "księga", "dzieło", "epopeja", "opowieść", "fabuła", "tekst", "poezja", "proza", "komedia", "dramat", "tragedia", "romans", "thriller", "fantasy", "fikcja", "akcja", "przygoda", "detektywistyczny", "historyczny", "psychologiczny", "moralizatorski", "filozoficzny", "obyczajowy", "horror", "kryminał", "kryminalny", "horrory", "intryga", "katastrofa", "rozwój", "zakończenie", "postacie", "bohaterowie", "wątek", "fabularny", "narracja", "styl", "język", "słownictwo", "kompozycja", "konflikt", "punkty", "widok", "plan", "schemat", "przyjęcie", "zdarzenie", "scena", "obraz", "zaczepka", "pikietka", "pomoc", "wsparcie", "chwila", "moment", "minuta", "sekunda", "czasownik", "rzeczownik", "przymiotnik", "przysłówek", "zaimek", "spójnik", "przyimek", "końcówka", "forma", "strona", "człon", "tekst", "lektura", "wydanie", "podtytuł", "tytuł", "słowo", "zdanie", "akapit", "rozdział", "treść", "książka", "autor", "literatura", "pismo", "styl", "gatunek", "dramatyzm", "lyryka"]
słowa_zgadywanka4 = ["muzyka", "melodia", "rytm", "harmonia", "instrument", "gitara", "pianino", "skrzypce", "perkusja", "flet", "trąbka", "saksofon", "koncert", "utwór", "piosenka", "ballada", "opera", "sztuka", "malarstwo", "rzeźba", "rzeźbiarstwo", "rysunek", "obraz", "kolor", "paleta", "kamień", "drewno", "metal", "szkło", "plastyka", "rzeźbiarz", "malarz", "rzeźbiarka", "obraz", "przestrzeń", "forma", "abstrakcja", "realizm", "ekspresjonizm", "impresjonizm", "surrealizm", "modernizm", "klasycyzm", "romantyzm", "barok", "neoklasycyzm", "koloryzm", "kubizm", "futuryzm", "postimpresjonizm", "minimalizm", "konceptualizm", "nowoczesność", "awangarda", "eksperyment", "interpretacja", "ekspresja", "kreatywność", "artysta", "twórca", "mistrz", "kunszt", "talent", "inspiracja", "twórczość", "galeria", "muzeum", "wystawa", "artystyczny", "wyrazisty", "indywidualny", "twórczy", "oryginalny", "nowatorski", "emocje", "wyrażenie", "ekspresyjny", "dynamiczny", "statyczny", "kompozycja", "proporcje", "perspektywa", "ruch", "ładunek", "harmonia", "zgranie", "kontrapunkt", "kompozytor", "utwór", "partytura", "interludium", "przerwa", "akord", "dźwięk", "takt", "tempo", "melodia", "rytm", "tonacja", "fraza", "wariacja"]
słowa_zgadywanka5 = ["natura", "las", "góry", "morze", "jezioro", "rzeka", "pole", "łąka", "kwiaty", "drzewa", "ziemia", "krajobraz", "pejzaż", "kamienie", "skały", "piasek", "brzeg", "kra", "woda", "powietrze", "słońce", "księżyc", "gwiazdy", "chmury", "deszcz", "śnieg", "wiatr", "trawa", "liście", "gałęzie", "kora", "ptaki", "owady", "zwierzęta", "ssaki", "ryby", "plankton", "równina", "pagórki", "klify", "wodospad", "cascada", "wulkan", "gejzer", "pustynia", "oaza", "tundra", "tajga", "step", "puszcza", "bagna", "jaskinia", "ocean", "arktyka", "antarktyka", "ekosystem", "bioróżnorodność", "fauna", "flora", "ekologia", "ochrona", "zanieczyszczenie", "klimat", "globalne ocieplenie", "wymieranie gatunków", "zagrożone", "rezerwat", "park narodowy", "obszar chroniony", "ekologiczny", "odnawialne źródła energii", "sustainable", "eko", "ekologiczne produkty", "recykling", "naturalne środowisko", "ekosfera", "biosfera", "ekoaktywista", "ekoaktywizm", "zrównoważony rozwój", "regeneracja", "restauracja", "ekoturystyka", "zielony", "życie na wsi", "ekomoda", "ekożywność", "ekologiczna moda", "ekologiczny styl życia", "ekoetkieta", "ekoarchitektura", "ekoświadomość", "ekoedukacja", "ekoekonomia", "ekoprodukt", "ekologiczne opakowanie", "ekoinspiracja", "ekomeblarstwo", "ekoogrody", "ekoogrodnictwo", "ekoogrodnik", "ekospołeczność", "ekoaktywizacja"]
słowa_zgadywanka1ENG = ["art", "music", "literature", "theater", "film", "painting", "sculpture", "photography", "architecture", "design", "fashion", "culture", "history", "science", "mathematics", "physics", "chemistry", "biology", "geography", "astronomy", "psychology", "sociology", "philosophy", "economics", "politics", "religion", "technology", "computer science", "programming", "internet", "communication", "computers", "smartphones", "applications", "social media", "games", "sports", "fitness", "health", "medicine", "diet", "psychotherapy", "yoga", "meditation", "travel", "tourism", "excursions", "sightseeing", "nature", "landscapes", "vacations", "culture", "history", "museums", "monuments", "relaxation", "rest", "entertainment", "film", "books", "music", "concerts", "festivals", "art", "theater", "comedy", "drama", "romance", "action", "thriller", "science fiction", "fantasy", "detective", "crime", "horror", "comics", "position", "experience", "emotions", "creativity", "imagination", "inspiration", "passion", "interests", "hobbies", "handicraft", "handmade", "design", "crocheting", "hacking", "painting", "sculpting", "tailoring", "culinary arts", "cooking", "baking", "desserts", "world cuisine", "vegan", "vegetarian", "special diets", "fusion cuisine", "flavors", "aroma", "spices"]
słowa_zgadywanka2ENG = ["yellow", "blue", "red", "green", "orange", "purple", "pink", "white", "black", "gray", "brown", "gold", "silver", "copper", "steel", "sapphire", "ruby", "amber", "amethyst", "pearl", "diamond", "water", "fire", "earth", "air", "energy", "light", "shadow", "sound", "silence", "joy", "sadness", "love", "hatred", "hope", "fear", "dream", "reality", "time", "space", "sound", "music", "melody", "harmony", "balance", "madness", "normality", "mystery", "riddle", "rainbow", "rain", "wind", "storm", "peace", "chaos", "nature", "universe", "cosmos", "galaxy", "planet", "star", "moon", "sun", "constellation", "zodiac", "horoscope", "cold", "heat", "spring", "summer", "autumn", "winter", "season", "holiday", "celebration", "tradition", "custom", "culture", "religion", "faith", "science", "knowledge", "wisdom", "question", "answer", "meaning", "goal", "task", "work", "effort", "success", "failure", "struggle", "peace", "war", "chance", "risk", "luck", "misfortune", "laughter", "tears", "smile", "emotions"]
słowa_zgadywanka3ENG = ["ocean", "mountain", "valley", "forest", "meadow", "river", "lake", "sea", "desert", "savanna", "jungle", "polar", "dune", "plateau", "bay", "island", "islet", "fairy tale", "myth", "legend", "book", "work", "epic", "tale", "plot", "text", "poetry", "prose", "comedy", "drama", "tragedy", "romance", "thriller", "fantasy", "fiction", "action", "adventure", "detective", "historical", "psychological", "moralistic", "philosophical", "social", "horror", "crime", "criminal", "horrors", "intrigue", "catastrophe", "development", "ending", "characters", "heroes", "plot", "narration", "style", "language", "vocabulary", "composition", "conflict", "points", "view", "plan", "scheme", "reception", "event", "scene", "picture", "provocation", "picket", "help", "support", "moment", "instant", "minute", "second", "verb", "noun", "adjective", "adverb", "pronoun", "conjunction", "preposition", "suffix", "form", "page", "member", "text", "reading", "edition", "subtitle", "title", "word", "sentence", "paragraph", "chapter", "content", "book", "author", "literature", "writing", "style", "genre", "drama", "lyric"]
słowa_zgadywanka4ENG = ["music", "melody", "rhythm", "harmony", "instrument", "guitar", "piano", "violin", "percussion", "flute", "trumpet", "saxophone", "concert", "composition", "song", "ballad", "opera", "art", "painting", "sculpture", "sculpting", "drawing", "picture", "color", "palette", "stone", "wood", "metal", "glass", "plastic arts", "sculptor", "painter", "sculptress", "image", "space", "form", "abstraction", "realism", "expressionism", "impressionism", "surrealism", "modernism", "classicism", "romanticism", "baroque", "neoclassicism", "colorism", "cubism", "futurism", "post-impressionism", "minimalism", "conceptualism", "modernity", "avant-garde", "experiment", "interpretation", "expression", "creativity", "artist", "creator", "master", "skill", "talent", "inspiration", "creativity", "gallery", "museum", "exhibition", "artistic", "expressive", "individual", "creative", "original", "innovative", "emotions", "expression", "expressive", "dynamic", "static", "composition", "proportions", "perspective", "movement", "charge", "harmony", "concord", "counterpoint", "composer", "composition", "score", "interlude", "break", "chord", "sound", "beat", "tempo", "melody", "rhythm", "key", "phrase", "variation"]
słowa_zgadywanka5ENG = ["nature", "forest", "mountains", "sea", "lake", "river", "field", "meadow", "flowers", "trees", "earth", "landscape", "scenery", "stones", "rocks", "sand", "shore", "coast", "water", "air", "sun", "moon", "stars", "clouds", "rain", "snow", "wind", "grass", "leaves", "branches", "bark", "birds", "insects", "animals", "mammals", "fish", "plankton", "plain", "hills", "cliffs", "waterfall", "cascada", "volcano", "geyser", "desert", "oasis", "tundra", "taiga", "steppe", "forest", "swamps", "cave", "ocean", "arctic", "antarctic", "ecosystem", "biodiversity", "fauna", "flora", "ecology", "protection", "pollution", "climate", "global warming", "extinction of species", "endangered", "reserve", "national park", "protected area", "ecological", "renewable energy sources", "sustainable", "eco", "eco-friendly products", "recycling", "natural environment", "ecosphere", "biosphere", "eco-activist", "eco-activism", "sustainable development", "regeneration", "restoration", "ecotourism", "green", "rural life", "eco-fashion", "organic food", "eco-friendly fashion", "eco-friendly lifestyle", "eco-label", "eco-architecture", "eco-awareness", "eco-education", "eco-economy", "ecoproduct", "eco-friendly packaging", "eco-inspiration", "ecofurniture", "eco-gardens", "eco-gardening", "eco-gardener", "ecocommunity", "eco-activization"]
powiadomienia = 1142449182855147660
kanalTestowy = 1142059184037306408
kanalOcen = 1152335339537580182
ostatni_autor = None
lcd = 10
hcd = 30
earncd = 1800
fishcd = 1800
timezone = pytz.timezone('Europe/Warsaw')
last_message_times = defaultdict(lambda: 0)
last_message_content = defaultdict(lambda: '')
last_message_counts = defaultdict(lambda: 0)
data_wyswietlanie = time.strftime("%Y-%m-%d %H:%M:%S")
backup_folder = 'backup'
os.makedirs(backup_folder, exist_ok=True)
global verificationLang
verificationLang = "PL"
app = Flask(__name__)
właściciele = [835959167540789279, 776494298450755594, 1024755404904874054]
no_avatar = "https://dreambot.pl/DreamBotImages/NoLogoDC.png"
Token = "MTE0Njg4NTcyNDcyMTkwNTc0NA.GsZxpq.spermatoken"
DEVToken = "MTE2OTI0NjE2NjMwNzg0ODI1Mg.GISp6V.spermatoken"



#DEV
with open("settings.json", "r") as file:
    data = json.load(file)

if data.get("DEV") is True:
    DEV = True
else:
    DEV = False



#Baza danych
DBAccount = "MainAccount"
DBPassword = "1EfzIeQYvsBvTir3"
DBAccountDEV = "DEV"
DBPasswordDEV = "lFuHQ3NFmPdkyNUY"
if DEV == True:
    uri = f"mongodb+srv://{DBAccountDEV}:{DBPasswordDEV}@dreambot.utpybla.mongodb.net/?retryWrites=true&w=majority"
else:
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

#all_server_ids = [server['_id'] for server in settings_collection.find({}, {'_id': 1})]
#server_iterator = iter(all_server_ids)

all_servers_info = list(settings_collection.find({}, {'_id': 1}))
premium_servers_info = [server['_id'] for server in all_servers_info if server.get('premium', False)]

all_server_ids = [server['_id'] for server in all_servers_info]
all_server_ids_premium = premium_servers_info

merged_server_ids = all_server_ids + all_server_ids_premium
random.shuffle(merged_server_ids)

server_iterator = iter(merged_server_ids)



class Help(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="💻 Konfiguracja", style=nextcord.ButtonStyle.red, custom_id="konfiguracja")
    async def konfiguracja(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        author = interaction.user
        
        try:
            if interaction.channel.type == nextcord.ChannelType.private:
                thumbnail_url = bot.user.avatar.url
            else:
                thumbnail_url = interaction.guild.icon.url if interaction.guild.icon else bot.user.avatar.url

            embed = nextcord.Embed(title='Konfiguracja', description="`/statystyki` - pokazuje statystyki bota\n`/lang [PL/ENG/...]` - ustawia język\n`/settingsConfig ticket` - wyświetla konfigurację ticketów\n`/settingsConfig partnerstwa` - wyświetla konfigurację partnerstw\n`/settingsConfig weryfikacja` - wyświetla konfigurację weryfikacji\n`/settingsConfig globalchat` - wyświetla konfigurację globalchatu\n`/settingsconfig statystyki` - wyświetla konfigurację statystyk\n`/settingsconfig autoad` - wyświetla konfigurację autoAD\n`/settingsConfig kanal [komenda]` - ustawia kanał komendy\n`/settingsConfig kategoria [komenda]` - ustawia kategorię komendy\n`/settingsConfig partnerstwa stawka [np. 1zł]` - ustawia stawkę partnerstw\n`/settingsConfig whitelista [add/remove] [kanał]` - ustawia/usuwa kanał na którym anty nie działa\n`/settingsConfig whitelista kanaly`- lista kanałów na których anty nie działa\n`/settingsekonomia [komenda]` - ustawienia ekonomii\n`/settingsekonomia sklep remove [id]` - usuwa przedmiot z sklepu\n`/settingsekonomia sklep add [nazwa] [opis] [cena]` - dodaje przedmiot do sklepu\n`/settingsconfig selfrole add [rola] [wiadomosc]` - dodaje selfrolę\n`/settings4Fun [komenda]` - używane do włączania/wyłączania/konfigurowania komend 4Fun\n`/settingsAdm [komenda]` - używane do włączania/wyłączania/konfigurowania komend Administracyjnych\n`/settingsConfig [komenda]` - używane do konfiguracji komend\n`/settingsconfig whitelista ticketadd [rola]` - dodaje rolę do ticketów\n`/settingsconfig whitelista ticketremove [rola]` - usuwa rolę z ticketów\n`/settingsconfig blacklista ticketadd [rola]` - dodaje role która nie ma dostępu do ticketów\n`/settingsconfig blacklista ticketremove [rola]` - usuwa rolę która nie ma dostępu do ticketów\n`/radio [kanał]` - ustawia kanał radia\n`/unradia` - usuwa kanał radia\n`/settingsconfig dreamshield` - konfiguracja Anty-Raid", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await wiadomoscHelp.edit(embed=embed)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/help`!\n\n{e}", ephemeral=True)

    @nextcord.ui.button(label="❓ Ogólne", style=nextcord.ButtonStyle.red, custom_id="ogolne")
    async def ogolne(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        author = interaction.user

        try:
            if interaction.channel.type == nextcord.ChannelType.private:
                thumbnail_url = bot.user.avatar.url
            else:
                thumbnail_url = interaction.guild.icon.url if interaction.guild.icon else bot.user.avatar.url

            embed = nextcord.Embed(title='Ogólne', description="`/ankieta [treść]` - tworzy ankietę\n`/say [wiadomość]` - wysyła wiadomość jako bot\n`/partnerstwa [osoba]` - wyświetla liczbę partnerstw\n`/notes [sprawdz/napisz/usun]` - notes\n`/ocena [ocena] [opis]` - wysyła ocenę bota\n`/kalkulator [dzialanie]` - kalkulator\n`/sklep` - sklep serwerowy\n`/ekwipunek` - zakupione przez ciebie przedmioty\n`/buy [id]` - kupuje przedmiot z sklepu\n`/use [id]` - używa przedmiot z ekwipunku\n`/work` - praca praca\n`/crime` - praca (nielegalna)\n`/ruletka [kwota]` - postaw na czarne ⚫\n`/blackjack [kwota]` - umiesz w karty? 🃏\n`/deposit` - wpłaca pieniądze na konto\n`/withdraw` - wypłaca pieniądze z konta\n`/invites [osoba]` - sprawdza ilość zaproszeń\n`/selfchannel [kanal] [max]` - ustawia max użytkowników na własnym kanale\n`/rekrutacja` - pokazuje stan rekrutacji\n`/ranking partnerstwa` - pokazuje ranking partnerstw\n`/support` - wysyła link do serwera support", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await wiadomoscHelp.edit(embed=embed)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/help`!", ephemeral=True)

    @nextcord.ui.button(label="🔨 Administracyjne", style=nextcord.ButtonStyle.red, custom_id="adm")
    async def adm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        author = interaction.user

        try:
            if interaction.channel.type == nextcord.ChannelType.private:
                thumbnail_url = bot.user.avatar.url
            else:
                thumbnail_url = interaction.guild.icon.url if interaction.guild.icon else bot.user.avatar.url

            embed = nextcord.Embed(title='Administracyjne', description="`/ban [osoba] [powód]` - banuje osobę\n`/kick [osoba] [powód]` - kickuje osobę\n`/mute [osoba] [powód]` - wycisza osobę (perm.)\n`/unmute [osoba]` - odcisza osobę\n`/clear [ilość]` - usuwa wiadomości\n`/add role [rola] [uzytkownik]` - nadaje rolę\n`/remove role [rola] [uzytkownik]` - usuwa rolę\n`/giveaway [czas] [nagroda] [wygrani]` - giveaway\n`/reroll [id] [ilosc]` - ponownie losuje\n`/add partnerstwa [osoba] [ilość]` - dodaje partnerstwa *(a)*\n`/remove partnerstwa [osoba] [ilość]` - usuwa partnerstwa *(a)*\n`/add waluta [osoba]` - dodaje walutę *(a)*\n`/remove waluta [osoba]` - usuwa walutę *(a)*\n`/add invites [osoba]` - dodaje zaproszenia *(a)*\n`/remove invites [osoba]` - usuwa zaproszenia *(a)*\n\n*(a)* na końcu opisu oznacza, że jedynie administrator może użyć komendy", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await wiadomoscHelp.edit(embed=embed)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/help`!", ephemeral=True)

    @nextcord.ui.button(label="🤣 4Fun", style=nextcord.ButtonStyle.red, custom_id="fun")
    async def fun(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        author = interaction.user

        try:
            if interaction.channel.type == nextcord.ChannelType.private:
                thumbnail_url = bot.user.avatar.url
            else:
                thumbnail_url = interaction.guild.icon.url if interaction.guild.icon else bot.user.avatar.url

            embed = nextcord.Embed(title='4Fun', description="`/ship [osoba] [osoba]` - łączy 2 osoby\n`/iq` - sprawdza iq\n`/kostka` - losuje numer od 1 do 6\n`/chatbot [wiadomość]` - rozmowa z chatbotem\n`/info [osoba]` - wyświetla informacje\n`/mem [pl/eng]` - losowy mem (nsfw)\n`/zgaduj` - zgadywanka\n`/waluta` - wirtualna waluta\n`/translate [z] [na] [tekst]` - translator\n`/randomimg` - losowy obraz\n`/fish help` - komenda pomocy ryb\n\nJak zdobywać walutę? - walutę możesz zdobywać używając komend 4Fun (np. `/zgaduj`) lub pracując! (np. `/work`)\n\n(nsfw) na końcu opisu oznacza komendy może użyć jedynie na kanałach nswf", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await wiadomoscHelp.edit(embed=embed)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/help`!", ephemeral=True)

    @nextcord.ui.button(label="⭐ Premium", style=nextcord.ButtonStyle.blurple, custom_id="premium")
    async def fun(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        author = interaction.user

        try:
            if interaction.channel.type == nextcord.ChannelType.private:
                thumbnail_url = bot.user.avatar.url
            else:
                thumbnail_url = interaction.guild.icon.url if interaction.guild.icon else bot.user.avatar.url

            embed = nextcord.Embed(title='Premium', description="`/premium` - pokazuje korzyści i możliwość zakupu premium\n`/premiumconfig ticket addbutton [tekst]` - dodaje przycisk\n`/premiumconfig ticket removebutton [id]` - usuwa przycisk\n`/premiumconfig ticket showbuttons` - pokazuje wszystkie przyciski", color=0xffe600)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await wiadomoscHelp.edit(embed=embed)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/help`!", ephemeral=True)
        
class HelpENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="💻 Configuration", style=nextcord.ButtonStyle.red, custom_id="konfiguracjaENG")
    async def konfiguracja(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        author = interaction.user
        
        try:
            
            embed = nextcord.Embed(title='Configuration', description="`/statystyki` - show bot statistics\n`/lang [PL/ENG/...]` - set language\n`/settingsConfig ticket` - show ticket configuration\n`/settingsConfig partnerstwa` - displays configuration of partnerships\n`/settingsConfig weryfikacja` - displays configuration of verification\n`/settingsConfig globalchat` - display globalchat configuration\n\n`/settingsconfig statystyki` - display statistics configuration\n`/settingsconfig autoad` - displays the autoAD configuration\n`/settingsConfig kanal [command]` - set command channel\n`/settingsConfig kategoria [command]` - set command category\n``/settingsConfig partnerstwa stawka [e. c. 1$]`` - sets the partnership rate\n`/settingsConfig whitelista [add/remove] [channel]` - set/remove the channel on which anti doesn't work\n`/settingsConfig whitelista kanaly`- list of channels on which anti doesn't work\n\n`/settingsekonomia [command]` - economics settings\n`/settingsekonomia sklep remove [id]` - removes an item from the store\n`/settingsekonomia sklep add [name] [desc.] [price]` - adds an item to the store\n`/settingsconfig selfrole add [role] [message]` - adds selfrole\n`/settings4Fun [command]` - used to enable/disable/configure 4Fun commands\n`/settingsAdm [command]` - used to enable/disable/configure Admin commands\n`/settingsConfig [command]` - used to configure commands\n`/settingsconfig whitelista ticketadd [rola]` - adds a role to tickets\n`/settingsconfig whitelista ticketremove [rola]` - removes the role from tickets\n`/settingsconfig blacklista ticketadd [rola]` - adds a role that does not have access to tickets\n`/settingsconfig blacklista ticketremove [rola]` - removes a role that does not have access to tickets\n`/radio [kanał]` - sets the radio channel\n`/unradia` - deletes a radio channel\n`/settingsconfig dreamshield` - Anti-Raid configuration", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            thumbnail_url = interaction.guild.icon.url if interaction.guild.icon else bot.user.avatar.url
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await wiadomoscHelp.edit(embed=embed)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interaction timed out, try `/help` again!", ephemeral=True)

    @nextcord.ui.button(label="❓ General", style=nextcord.ButtonStyle.red, custom_id="ogolneENG")
    async def ogolne(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        author = interaction.user

        try:

            embed = nextcord.Embed(title='General', description="`/ankieta [content]` - creates a survey\n`/say [message]` - sends the message as a bot\n`/partnerstwa [member]` - displays the number of partnerships\n`/notes [sprawdz/napisz/usun]` - notebook\n`/ocena [rating] [desc.]` - wysyła ocenę bota\n`/calculator [action]` - calculator\n`/sklep` - server store\n`/ekwipunek` - items you purchased\n`/buy [id]` - buys an item from the store\n`/use [id]` - uses an item from your inventory\n`/work` - work work\n`/crime` - work (illegal)\n`/ruletka [kwota]` - go for black ⚫\n`/blackjack [kwota]` - do you know how to play? 🃏\n`/deposit` - deposits money into the account\n`/withdraw` - withdraws money from the account\n`/invites [osoba]` - checks the number of invites\n`/selfchannel [kanal] [max]` - sets the maximum number of users on your own channel\n`/rekrutacja` - shows the recruitment status\n`/ranking partnerstwa` - shows the partnership ranking\n`/support` - sends a link to the support server", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            thumbnail_url = interaction.guild.icon.url if interaction.guild.icon else bot.user.avatar.url
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await wiadomoscHelp.edit(embed=embed)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interaction timed out, try `/help` again!", ephemeral=True)

    @nextcord.ui.button(label="🔨 Administrative", style=nextcord.ButtonStyle.red, custom_id="admENG")
    async def adm(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        author = interaction.user

        try:

            embed = nextcord.Embed(title='Administrative', description="`/ban [member] [reason]` - bans a person\n`/kick [member] [reason]` - kicks a person\n`/mute [member] [reason]` - mute person (Perm.)\n`/unmute [member]` - unmutes person\n`/clear [amount]` - deletes messages\n`/add role [role] [member]` - gives role\n`/giveaway [czas] [nagroda] [winners]` - giveaway\n`/reroll [id] [number]` - drawing a giveaway again\n`/remove role [role] [member]` - removes role\n`/add partnerstwa [member] [amount]` - adds partnerships *(a)*\n`/remove partnerstwa [member] [amount]` - removes partnerships *(a)*\n`/add waluta [member]` - adds currency *(a)*\n`/remove waluta [member]` - removes the currency *(a)*\n`/add invites [osoba]` - adds invites *(a)*\n`/remove invites [osoba]` - remove invites *(a)*\n\n*(a)* at the end of the description means that only the administrator can use the command", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            thumbnail_url = interaction.guild.icon.url if interaction.guild.icon else bot.user.avatar.url
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await wiadomoscHelp.edit(embed=embed)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interaction timed out, try `/help` again!", ephemeral=True)

    @nextcord.ui.button(label="🤣 4Fun", style=nextcord.ButtonStyle.red, custom_id="funENG")
    async def fun(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        author = interaction.user

        try:

            embed = nextcord.Embed(title="4Fun", description="`/ship [member] [member]` - connects 2 people\n`/iq` - checks iq\n`/kostka` - draws a number from 1 to 6\n`/chatbot [message]` - talking to a chatbot\n`/info [member]` - displays information\n`/mem [pl/eng]` - random meme *(nsfw)*\n`/zgaduj` - guessing game\n`/waluta` - virtual currency\n`/translate [from] [to] [text]` - translator\n`/randomimg` - random image\n`/fish help` - fish help command\n\n*How to get currency?* - you can get currency using 4Fun commands! (e.g. `/zgaduj`)\n\n*(nsfw) at the end of the description means commands can only be used on nswf channels", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            thumbnail_url = interaction.guild.icon.url if interaction.guild.icon else bot.user.avatar.url
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await wiadomoscHelp.edit(embed=embed)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interaction timed out, try `/help` again!", ephemeral=True)

    @nextcord.ui.button(label="⭐ Premium", style=nextcord.ButtonStyle.blurple, custom_id="premium")
    async def fun(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        author = interaction.user

        try:

            embed = nextcord.Embed(title='Premium', description="`/premium` - shows the benefits and the possibility of purchasing premium\n`/premiumconfig ticket addbutton [tekst]` - adds a button\n`/premiumconfig ticket removebutton [id]` - removes the button\n`/premiumconfig ticket showbuttons` - shows all buttons", color=0xffe600)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            thumbnail_url = interaction.guild.icon.url if interaction.guild.icon else bot.user.avatar.url
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await wiadomoscHelp.edit(embed=embed)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/help`!", ephemeral=True)

class Otwieranie_ticketu(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="🎫 Otwórz ticket", style=nextcord.ButtonStyle.green, custom_id="openticket")
    async def openticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        try:
            server_id = str(interaction.guild.id)
            settings_document = settings_collection.find_one({'_id': server_id})
            user_document = users_collection.find_one({'_id': str(interaction.user.id)})

            if settings_document and settings_document.get("tickety", False):
                if user_document and 'mutes' in user_document:
                    current_time_mute = datetime.datetime.now()

                    for mute_info in user_document['mutes']:
                        sid = mute_info.get('server_id')
                        if sid == server_id:
                            end_time = mute_info.get('end_time')
                            if end_time and end_time > current_time_mute:
                                user = interaction.user
                                remaining_time = end_time - current_time_mute
                                remaining_time_str = str(remaining_time).split('.')[0]
                                remaining_time_str = remaining_time_str.replace(" days, ", "d ").replace(" day, ", "d ")
                                remaining_time_str = remaining_time_str.replace(":00:00", "h").replace(":00", "m")

                                await interaction.send(f"`[❌]:` {user.mention}, masz aktywne wyciszenie, poczekaj jeszcze `{remaining_time_str}`", ephemeral=True)
                                return

                guild = interaction.guild
                if settings_document.get("kategoriaOtwieraniaTicketow", False):
                    kategoriaID = settings_document.get("kategoriaOtwieraniaTicketow", False)
                    kategoria = guild.get_channel(kategoriaID)
                else:
                    kategoria = guild

                channel_name = f"ticket-{interaction.user.name}"
                ticket_channel = nextcord.utils.get(kategoria.channels, name=channel_name)
                
                if not ticket_channel:
                    user_id = interaction.user.id

                    guild = bot.get_guild(interaction.guild.id)
                    user = await guild.fetch_member(user_id)
                    overwrites = {}

                    if kategoria != guild:
                        for target, overwrite in kategoria.overwrites.items():
                            overwrites[target] = overwrite

                    if settings_document and settings_document.get("weryfikacja", False):
                        idroli = settings_document.get("rolaWeryfikacji", False)
                        rola = interaction.guild.get_role(idroli)
                    else:
                        rola = None

                    if 'ticketWLRoles' in settings_document:
                        for role_id in settings_document['ticketWLRoles']:
                            role = guild.get_role(int(role_id))
                            if role:
                                overwrites[role] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)

                    if 'ticketBLRoles' in settings_document:
                        for role_id in settings_document['ticketBLRoles']:
                            role = guild.get_role(int(role_id))
                            if role:
                                overwrites[role] = nextcord.PermissionOverwrite(read_messages=False)

                    if settings_document and settings_document.get("ticketyEveryone", False):
                        ping = True
                    else:
                        ping = False

                    overwrites[user] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
                    if rola != None:
                        overwrites[rola] = nextcord.PermissionOverwrite(read_messages=False)
                    overwrites[guild.default_role] = nextcord.PermissionOverwrite(read_messages=False)

                    ticket_channel = await kategoria.create_text_channel(f"Ticket-{interaction.user.name}", overwrites=overwrites)

                    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    stworzył = f"<t:{int(interaction.user.created_at.timestamp())}:R>"
                    dołączył = f"<t:{int(interaction.user.joined_at.timestamp())}:R>"

                    embed = nextcord.Embed(title=f'**Ticket**', description=f"**Aby zamknąć ticket kliknij przycisk `🔒 Zamknij`**\n\n**Autorem jest {interaction.user.mention} (*{interaction.user.id}*)**\n**Na serwer dołączył** {dołączył}\n**Na Discord dołączył** {stworzył}", color=0x00ff00)
                    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                    embed.set_thumbnail(url=bot.user.avatar.url)
                    embed.set_footer(text=f"{current_time}")
                    view = Zamykanie_ticketu(user=interaction.user)
                    if ping == True:
                        await ticket_channel.send("@everyone", embed=embed, view=view)
                    else:
                        await ticket_channel.send(embed=embed, view=view)

                    await interaction.send(f"`[✅]:` Ticket stworzony! {ticket_channel.mention}", ephemeral=True)

                    statistics = load_statistics()
                    if 'tickety' in statistics:
                        statistics['tickety'] += 1
                    else:
                        statistics['tickety'] = 1
                    save_statistics(statistics)
                else:
                    await interaction.send(f"`[✅]:` Masz już jeden ticket! {ticket_channel.mention}", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Tickety są wyłączone na tym serwerze", ephemeral=True)

        except nextcord.Forbidden as e:
            await interaction.send(f'`[❌]:` Bot nie posiada permisji! (Powiadom administrację serwera o tym błędzie, nie jest on spowodowany ze strony technicznej)\n\n`{e}`', ephemeral=True)
        #except Exception as e:
            #print(f"Wystąpił błąd na {server_id} (SERVER ID)\n{e}")

class Otwieranie_ticketuENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="🎫 Open ticket", style=nextcord.ButtonStyle.green, custom_id="openticketENG")
    async def openticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        try:
            server_id = str(interaction.guild.id)
            settings_document = settings_collection.find_one({'_id': server_id})
            user_document = users_collection.find_one({'_id': str(interaction.user.id)})

            if settings_document and settings_document.get("tickety", False):
                if user_document and 'mutes' in user_document:
                    current_time_mute = datetime.datetime.now()

                    for mute_info in user_document['mutes']:
                        sid = mute_info.get('server_id')
                        if sid == server_id:
                            end_time = mute_info.get('end_time')
                            if end_time and end_time > current_time_mute:
                                user = interaction.user
                                remaining_time = end_time - current_time_mute
                                remaining_time_str = str(remaining_time).split('.')[0]
                                remaining_time_str = remaining_time_str.replace(" days, ", "d ").replace(" day, ", "d ")
                                remaining_time_str = remaining_time_str.replace(":00:00", "h").replace(":00", "m")

                                await interaction.send(f"`[❌]:` {user.mention}, you have active mute, wait `{remaining_time_str}`", ephemeral=True)
                                return

                guild = interaction.guild
                if settings_document.get("kategoriaOtwieraniaTicketow", False):
                    kategoriaID = settings_document.get("kategoriaOtwieraniaTicketow", False)
                    kategoria = guild.get_channel(kategoriaID)
                else:
                    kategoria = guild

                channel_name = f"ticket-{interaction.user.name}"
                ticket_channel = nextcord.utils.get(kategoria.channels, name=channel_name)
                
                if not ticket_channel:
                    user_id = interaction.user.id

                    guild = bot.get_guild(interaction.guild.id)
                    user = await guild.fetch_member(user_id)
                    overwrites = {}

                    if kategoria != guild:
                        for target, overwrite in kategoria.overwrites.items():
                            overwrites[target] = overwrite

                    if settings_document and settings_document.get("weryfikacja", False):
                        idroli = settings_document.get("rolaWeryfikacji", False)
                        rola = interaction.guild.get_role(idroli)
                    else:
                        rola = None

                    if 'ticketWLRoles' in settings_document:
                        for role_id in settings_document['ticketWLRoles']:
                            role = guild.get_role(int(role_id))
                            if role:
                                overwrites[role] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)

                    if 'ticketBLRoles' in settings_document:
                        for role_id in settings_document['ticketBLRoles']:
                            role = guild.get_role(int(role_id))
                            if role:
                                overwrites[role] = nextcord.PermissionOverwrite(read_messages=False)

                    overwrites[user] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
                    if rola != None:
                        overwrites[rola] = nextcord.PermissionOverwrite(read_messages=False)
                    overwrites[guild.default_role] = nextcord.PermissionOverwrite(read_messages=False)

                    ticket_channel = await kategoria.create_text_channel(f"Ticket-{interaction.user.name}", overwrites=overwrites)

                    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    stworzył = f"<t:{int(interaction.user.created_at.timestamp())}:R>"
                    dołączył = f"<t:{int(interaction.user.joined_at.timestamp())}:R>"

                    embed = nextcord.Embed(title=f'**Ticket**', description=f"**To close the ticket, click the `🔒 Close` button**\n\n**Author {interaction.user.mention} (*{interaction.user.id}*)**\n**Joined the server** {dołączył}\n**Joined on Discord** {stworzył}", color=0x00ff00)
                    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                    embed.set_thumbnail(url=bot.user.avatar.url)
                    embed.set_footer(text=f"{current_time}")
                    view = Zamykanie_ticketuENG(user=interaction.user)
                    await ticket_channel.send(embed=embed, view=view)

                    await interaction.send(f"`[✅]:` Ticket created! {ticket_channel.mention}", ephemeral=True)

                    statistics = load_statistics()
                    if 'tickety' in statistics:
                        statistics['tickety'] += 1
                    else:
                        statistics['tickety'] = 1
                    save_statistics(statistics)
                else:
                    await interaction.send(f"`[✅]:` You already have one ticket! {ticket_channel.mention}", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Tickets are disabled on this server", ephemeral=True)
        except nextcord.Forbidden as e:
            await interaction.send(f'`[❌]:` The bot does not have permission! (Notify the server administration about this error, it is not technically caused)\n\n`{e}`', ephemeral=True)
        except Exception as e:
            print(f"Wystąpił błąd na {server_id} (SERVER ID)\n{e}")

class Zamykanie_ticketu(nextcord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=None)
        self.value = None
        self.user = user

    @nextcord.ui.button(label="☝ Przejmij ticket", style=nextcord.ButtonStyle.green, custom_id="claimticket")
    async def taketicket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        if self.user == interaction.user:
            await interaction.send("`[❌]:` Ten ticket należy do ciebie!", ephemeral=True)
            return

        if self.user == None:
            await interaction.send("`[❌]:` Ticket już został przejęty!", ephemeral=True)
            return
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        stworzył = f"<t:{int(self.user.created_at.timestamp())}:R>"
        dołączył = f"<t:{int(self.user.joined_at.timestamp())}:R>"

        embed = nextcord.Embed(title=interaction.message.embeds[0].title, description=f"**Aby zamknąć ticket kliknij przycisk `🔒 Zamknij`**\n\n**Autorem jest {self.user.mention} (*{self.user.id}*)**\n**Na serwer dołączył** {dołączył}\n**Na Discord dołączył** {stworzył}\n\n**Ticket przejęty przez {interaction.user.mention}**", color=0x00ff00)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(text=f"{current_time}")
        view = Zamykanie_ticketu(user=None)

        await interaction.message.edit(embed=embed, view=view)
        user_id = str(interaction.user.id)
        user_document = users_collection.find_one({'_id': user_id})
        if not user_document:
            user_document = {
                '_id': user_id,
                'Guilds': {
                    str(interaction.guild.id): {
                        'TicketsTaken': 1
                    }
                }
            }
            users_collection.insert_one(user_document)
        else:
            if 'Guilds' not in user_document:
                user_document['Guilds'] = {}

            server_id = str(interaction.guild.id)
            if server_id not in user_document['Guilds']:
                user_document['Guilds'][server_id] = {
                    'TicketsTaken': 1
                }
            else:
                if 'TicketsTaken' not in user_document['Guilds'][server_id]:
                    user_document['Guilds'][server_id]['TicketsTaken'] = 1
                else:
                    user_document['Guilds'][server_id]['TicketsTaken'] += 1

            users_collection.update_one({'_id': user_id}, {'$set': {'Guilds': user_document['Guilds']}})

    @nextcord.ui.button(label="📝 Transkrypcja", style=nextcord.ButtonStyle.blurple, custom_id="showticket")
    async def showticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        channel = interaction.channel
        messages = await channel.history(limit=None, oldest_first=True).flatten()

        formatted_messages = ""
        for message in messages:
            if not message.author.bot:
                if message.content:
                    if len(formatted_messages) + len(message.author.name) + len(message.content) < 2000:
                        formatted_messages += f"{message.author.name}: {message.content}\n"
                    else:
                        await interaction.user.send(f"```{formatted_messages}```")
                        formatted_messages = f"{message.author.name}: {message.content}\n"
                for attachment in message.attachments:
                    if len(formatted_messages) + len(message.author.name) + len(attachment.url) < 2000:
                        formatted_messages += f"{message.author.name}: {attachment.url}\n"
                    else:
                        await interaction.user.send(f"```{formatted_messages}```")
                        formatted_messages = f"{message.author.name}: {attachment.url}\n"

        if formatted_messages:
            await interaction.user.send(f"```{formatted_messages}```")
        else:
            await interaction.send("`[❌]:` Brak wiadomości do wygenerowania transkrypcji!", ephemeral=True)

    @nextcord.ui.button(label="🔒 Zamknij", style=nextcord.ButtonStyle.red, custom_id="closeticket")
    async def openticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        server_id = str(interaction.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        premium = settings_document.get('premium')
        if premium == True and 'kategoriaZamykaniaTicketow' in settings_document:
            kategoria = settings_document.get('kategoriaZamykaniaTicketow')
            try:
                kategoria = bot.get_channel(kategoria)
                channel = interaction.channel
                permissions = kategoria.overwrites
                await channel.edit(category=kategoria, overwrites=permissions)
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                embed = nextcord.Embed(title=f"*Ticket został zamknięty przez {interaction.user}*", color=0xff0000)
                embed.set_thumbnail(url=bot.user.avatar.url)
                embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                embed.set_footer(text=current_time)
                view = Zamykanie_ticketu2(self.user)
                await channel.send(embed=embed, view=view)
            except Exception as e:
                await interaction.response.send_message(f"`[❌]:` Nie można odnaleść kategorii!\n\n{e}", ephemeral=True)
        else:
            channel = interaction.channel
            await channel.delete()

class Zamykanie_ticketuENG(nextcord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=None)
        self.value = None
        self.user = user

    @nextcord.ui.button(label="☝ Take the ticket", style=nextcord.ButtonStyle.green, custom_id="claimticketENG")
    async def taketicket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        if self.user == None:
            await interaction.send("`[❌]:` The ticket has already been taken!", ephemeral=True)
            return
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        stworzył = f"<t:{int(interaction.user.created_at.timestamp())}:R>"
        dołączył = f"<t:{int(interaction.user.joined_at.timestamp())}:R>"
        
        embed = nextcord.Embed(title=f'**Ticket**', description=f"**To close the ticket, click the `🔒 Close` button**\n\n**Author {self.user.mention} (*{self.user.id}*)**\n**Joined the server** {dołączył}\n**Joined on Discord** {stworzył}\n\n**Ticket taken by {interaction.user.mention}**", color=0x00ff00)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(text=f"{current_time}")
        view = Zamykanie_ticketuENG(user=None)

        await interaction.message.edit(embed=embed, view=view)

    @nextcord.ui.button(label="📝 Transcript", style=nextcord.ButtonStyle.blurple, custom_id="showticketENG")
    async def showticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        channel = interaction.channel
        messages = await channel.history(limit=None, oldest_first=True).flatten()

        formatted_messages = ""
        for message in messages:
            if not message.author.bot:
                if message.content:
                    formatted_messages += f"{message.author}: {message.content}\n"
                for attachment in message.attachments:
                    formatted_messages += f"{message.author}: {attachment.url}\n"

        await interaction.user.send(f"```{formatted_messages}```")

    @nextcord.ui.button(label="🔒 Close", style=nextcord.ButtonStyle.red, custom_id="closeticketENG")
    async def openticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        server_id = str(interaction.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        premium = settings_document.get('premium')
        if premium == True and 'kategoriaZamykaniaTicketow' in settings_document:
            kategoria = settings_document.get('kategoriaZamykaniaTicketow')
            try:
                kategoria = bot.get_channel(kategoria)
                channel = interaction.channel
                permissions = kategoria.overwrites
                await channel.edit(category=kategoria, overwrites=permissions)
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                embed = nextcord.Embed(title=f"*Ticket has been closed by {interaction.user}*", color=0xff0000)
                embed.set_thumbnail(url=bot.user.avatar.url)
                embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                embed.set_footer(text=current_time)
                view = Zamykanie_ticketu2ENG(self.user)
                await channel.send(embed=embed, view=view)
            except Exception as e:
                await interaction.response.send_message("`[❌]:` Category not found!", ephemeral=True)
        else:
            channel = interaction.channel
            await channel.delete()

class Zamykanie_ticketu2(nextcord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=None)
        self.value = None
        self.user = user

    @nextcord.ui.button(label="📝 Transkrypcja", style=nextcord.ButtonStyle.blurple, custom_id="showticket2")
    async def showticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        channel = interaction.channel
        messages = await channel.history(limit=None, oldest_first=True).flatten()

        formatted_messages = ""
        for message in messages:
            if not message.author.bot:
                if message.content:
                    if len(formatted_messages) + len(message.author.name) + len(message.content) < 2000:
                        formatted_messages += f"{message.author.name}: {message.content}\n"
                    else:
                        await interaction.user.send(f"```{formatted_messages}```")
                        formatted_messages = f"{message.author.name}: {message.content}\n"
                for attachment in message.attachments:
                    if len(formatted_messages) + len(message.author.name) + len(attachment.url) < 2000:
                        formatted_messages += f"{message.author.name}: {attachment.url}\n"
                    else:
                        await interaction.user.send(f"```{formatted_messages}```")
                        formatted_messages = f"{message.author.name}: {attachment.url}\n"

        if formatted_messages:
            await interaction.user.send(f"```{formatted_messages}```")
        else:
            await interaction.send("`[❌]:` Brak wiadomości do wygenerowania transkrypcji!", ephemeral=True)

    @nextcord.ui.button(label="🔁 Przywróć", style=nextcord.ButtonStyle.green, custom_id="uncloseticket")
    async def openticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        server_id = str(interaction.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        premium = settings_document.get('premium')
        if premium == True and 'kategoriaOtwieraniaTicketow' in settings_document:
            kategoria = settings_document.get('kategoriaOtwieraniaTicketow')
            try:
                kategoria = bot.get_channel(kategoria)
                channel = interaction.channel
                overwrites = kategoria.overwrites
                if settings_document and settings_document.get("weryfikacja", False):
                    idroli = settings_document.get("rolaWeryfikacji", False)
                    rola = interaction.guild.get_role(idroli)
                else:
                    rola = None

                if 'ticketWLRoles' in settings_document:
                    for role_id in settings_document['ticketWLRoles']:
                        role = interaction.guild.get_role(int(role_id))
                        if role:
                            overwrites[role] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)

                if 'ticketBLRoles' in settings_document:
                    for role_id in settings_document['ticketBLRoles']:
                        role = interaction.guild.get_role(int(role_id))
                        if role:
                            overwrites[role] = nextcord.PermissionOverwrite(read_messages=False)

                overwrites[self.user] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
                if rola != None:
                    overwrites[rola] = nextcord.PermissionOverwrite(read_messages=False)
                overwrites[interaction.guild.default_role] = nextcord.PermissionOverwrite(read_messages=False)

                await channel.edit(category=kategoria, overwrites=overwrites)
            except Exception as e:
                await interaction.response.send_message(f"`[❌]:` Nie można odnaleść kategorii!\n\n{e}", ephemeral=True)

    @nextcord.ui.button(label="❌ Usuń", style=nextcord.ButtonStyle.red, custom_id="deleteticket")
    async def deleteticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        channel = interaction.channel
        await channel.delete()

class Zamykanie_ticketu2ENG(nextcord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=None)
        self.value = None
        self.user = user

    @nextcord.ui.button(label="📝 Transcript", style=nextcord.ButtonStyle.blurple, custom_id="showticket2ENG")
    async def showticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        channel = interaction.channel
        messages = await channel.history(limit=None, oldest_first=True).flatten()

        formatted_messages = ""
        for message in messages:
            if not message.author.bot:
                if message.content:
                    formatted_messages += f"{message.author}: {message.content}\n"
                for attachment in message.attachments:
                    formatted_messages += f"{message.author}: {attachment.url}\n"

        await interaction.user.send(f"```{formatted_messages}```")

    @nextcord.ui.button(label="🔁 Restore", style=nextcord.ButtonStyle.red, custom_id="uncloseticketENG")
    async def openticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        server_id = str(interaction.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        premium = settings_document.get('premium')
        if premium == True and 'kategoriaOtwieraniaTicketow' in settings_document:
            kategoria = settings_document.get('kategoriaOtwieraniaTicketow')
            try:
                kategoria = bot.get_channel(kategoria)
                channel = interaction.channel
                overwrites = kategoria.overwrites
                if settings_document and settings_document.get("weryfikacja", False):
                    idroli = settings_document.get("rolaWeryfikacji", False)
                    rola = interaction.guild.get_role(idroli)
                else:
                    rola = None

                if 'ticketWLRoles' in settings_document:
                    for role_id in settings_document['ticketWLRoles']:
                        role = interaction.guild.get_role(int(role_id))
                        if role:
                            overwrites[role] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)

                if 'ticketBLRoles' in settings_document:
                    for role_id in settings_document['ticketBLRoles']:
                        role = interaction.guild.get_role(int(role_id))
                        if role:
                            overwrites[role] = nextcord.PermissionOverwrite(read_messages=False)

                overwrites[self.user] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
                if rola != None:
                    overwrites[rola] = nextcord.PermissionOverwrite(read_messages=False)
                overwrites[interaction.guild.default_role] = nextcord.PermissionOverwrite(read_messages=False)

                await channel.edit(category=kategoria, overwrites=overwrites)
            except Exception as e:
                await interaction.response.send_message("`[❌]:` Category cannot be found!", ephemeral=True)

    @nextcord.ui.button(label="❌ Delete", style=nextcord.ButtonStyle.red, custom_id="deleteticket")
    async def deleteticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        channel = interaction.channel
        await channel.delete()

class Wylaczanie_Wlaczanie_ankiet(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz ankiety", style=nextcord.ButtonStyle.blurple, custom_id="offankiety")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("ankiety", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'ankiety': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'ankiety': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "turned on" if new_status else "turned off"
                await interaction.send(f"`[✅]:` Komenda `ankieta` została {status_text} dla tego serwera.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `ankieta`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/settingsConfig ankiety`!", ephemeral=True)

class Wylaczanie_Wlaczanie_ankietENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Turn off / ✅ Turn on surveys", style=nextcord.ButtonStyle.blurple, custom_id="offankiety")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("ankiety", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'ankiety': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'ankiety': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "turned on" if new_status else "turned off"
                await interaction.send(f"`[✅]:` The `ankieta` command has been {status_text} for this server.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `ankieta`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interaction timed out, try the command again `/settingsConfig ankiety`!", ephemeral=True)

class Wylaczanie_Wlaczanie_ticketow(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz tickety", style=nextcord.ButtonStyle.blurple, custom_id="offticket")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("tickety", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'tickety': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'tickety': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączone" if new_status else "wyłączone"
                await interaction.send(f"`[✅]:` `tickety` zostały {status_text} dla tego serwera.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `tickety`!", ephemeral=True)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/settingsConfig tickety`!", ephemeral=True)

class Wylaczanie_Wlaczanie_ticketowENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Turn off / ✅ Turn on tickets", style=nextcord.ButtonStyle.blurple, custom_id="offticketENG")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("tickety", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'tickety': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'tickety': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "turned on" if new_status else "turned off"
                await interaction.send(f"`[✅]:` `tickets` have been {status_text} for this server.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `tickets`!", ephemeral=True)

        except Exception as e:
            await interaction.send(f"`[❌]:` The interaction has expired, please try the `/settingsConfig tickety` command again!", ephemeral=True)

class Wylaczanie_Wlaczanie_partnerstw(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz partnerstwa", style=nextcord.ButtonStyle.blurple, custom_id="offpartnerstwa")
    async def offpartnerstwa(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("partnerstwa", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'partnerstwa': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'partnerstwa': new_status}
                    settings_collection.insert_one(settings_document)

                status_text = "włączone" if new_status else "wyłączone"
                await interaction.send(f"`[✅]:` `partnerstwa` zostały {status_text} dla tego serwera.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `partnerstwa`!", ephemeral=True)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/settingsConfig partnerstwa`!", ephemeral=True)

class Wylaczanie_Wlaczanie_partnerstwENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Turn off / ✅ Turn on partnerships", style=nextcord.ButtonStyle.blurple, custom_id="offpartnerstwaENG")
    async def offpartnerstwa(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("partnerstwa", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'partnerstwa': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'partnerstwa': new_status}
                    settings_collection.insert_one(settings_document)

                status_text = "turned on" if new_status else "turned off"
                await interaction.send(f"`[✅]:` `partnerships` have been {status_text} for this server.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `partnerships`!", ephemeral=True)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interaction timed out, try `/settingsConfig partnerstwa` again!", ephemeral=True)

class Wylaczanie_Wlaczanie_globalchatu(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz globalchat", style=nextcord.ButtonStyle.blurple, custom_id="offankiety")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("globalchat", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'globalchat': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'globalchat': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` Funkcja `globalchat` została {status_text} dla tego serwera.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `globalchat`!", ephemeral=True)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/settingsConfig globalchat`!", ephemeral=True)

class Wylaczanie_Wlaczanie_globalchatuENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Turn off / ✅ Turn on globalchat", style=nextcord.ButtonStyle.blurple, custom_id="offankietyENG")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("globalchat", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'globalchat': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'globalchat': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "turned on" if new_status else "turned off"
                await interaction.send(f"`[✅]:` The `globalchat` function has been {status_text} for this server.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `globalchat`!", ephemeral=True)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interaction timed out, try `/settingsConfig globalchat` again!", ephemeral=True)

class Wylaczanie_Wlaczanie_weryfikacji(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz weryfikację", style=nextcord.ButtonStyle.blurple, custom_id="offweryfikacja")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("weryfikacja", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'weryfikacja': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'weryfikacja': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączone" if new_status else "wyłączone"
                await interaction.send(f"`[✅]:` Funkcja `weryfikacja` została {status_text} dla tego serwera.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `weryfikacja`!", ephemeral=True)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/settingsConfig weryfikacja`!", ephemeral=True)

class Wylaczanie_Wlaczanie_weryfikacjiENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Turn off / ✅ Turn on verification", style=nextcord.ButtonStyle.blurple, custom_id="offweryfikacjaENG")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("weryfikacja", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'weryfikacja': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'weryfikacja': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "turned on" if new_status else "turned off"
                await interaction.send(f"`[✅]:` The function `verification` has been {status_text} for this server.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `verification`!", ephemeral=True)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interaction timed out, try `/settingsConfig verify` again!", ephemeral=True)

class WeryfikacjaModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title="Weryfikacja", timeout=None)
        self.first = random.randint(1, 35)
        self.second = random.randint(1, 35)
        self.emTitle = nextcord.ui.TextInput(label=f"Ile to {self.first} + {self.second}?", required=True, placeholder="Wykonaj działanie aby przejść na serwer")
        self.add_item(self.emTitle)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        try:
            if int(self.emTitle.value) == self.first + self.second:
                server_id = str(interaction.guild.id)
                settings_document = settings_collection.find_one({'_id': server_id})
                if settings_document and settings_document.get("weryfikacja", False):
                    member = interaction.guild.get_member(interaction.user.id)
                    idroli = settings_document.get("rolaWeryfikacji", False)
                    rola = interaction.guild.get_role(idroli)
                    if rola not in member.roles:
                        await interaction.user.add_roles(nextcord.utils.get(interaction.guild.roles, name=rola.name))
                        await interaction.send("`[✅]:` Zostałeś zweryfikowany!", ephemeral=True)

                        statistics = load_statistics()
                        if 'weryfikacja' in statistics:
                            statistics['weryfikacja'] += 1
                        else:
                            statistics['weryfikacja'] = 1
                        save_statistics(statistics)
                    else:
                        await interaction.send("`[❌]:` Jesteś już zweryfikowany!", ephemeral=True)
                else:
                    await interaction.send("`[❌]:` Weryfiacja jest wyłączona na tym serwerze!", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Podałeś zły wynik!", ephemeral=True)

        except nextcord.errors.Forbidden as e:
            await interaction.send(f'`[❌]:` Bot nie posiada permisji! (Powiadom administrację serwera o tym błędzie, nie jest on spowowodowany ze strony technicznej)\nWiadomość dla administratora: Sprawdź czy rola weryfikacyjna jest pod rolą bota\n\n`{e}`')
        except nextcord.NotFound as e:
            await interaction.send(f'`[❌]:` Nie odnaleziono roli! (Powiadom administrację serwera o tym błędzie, nie jest on spowowodowany ze strony technicznej)\n\n`{e}`')
        except ValueError:
            await interaction.send("`[❌]:` Podałeś zły wynik!", ephemeral=True)

class WeryfikacjaModalENG(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title="Weryfikacja", timeout=None)
        self.first = random.randint(1, 35)
        self.second = random.randint(1, 35)
        self.emTitle = nextcord.ui.TextInput(label=f"what is {self.first} + {self.second}?", required=True, placeholder="Perform the action to go to the server")
        self.add_item(self.emTitle)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        try:
            if int(self.emTitle.value) == self.first + self.second:
                server_id = str(interaction.guild.id)
                settings_document = settings_collection.find_one({'_id': server_id})
                if settings_document and settings_document.get("weryfikacja", False):
                    member = interaction.guild.get_member(interaction.user.id)
                    idroli = settings_document.get("rolaWeryfikacji", False)
                    rola = interaction.guild.get_role(idroli)
                    if rola not in member.roles:
                        await interaction.user.add_roles(nextcord.utils.get(interaction.guild.roles, name=rola.name))
                        await interaction.send("`[✅]:` You have been verified!", ephemeral=True)

                        statistics = load_statistics()
                        if 'weryfikacja' in statistics:
                            statistics['weryfikacja'] += 1
                        else:
                            statistics['weryfikacja'] = 1
                        save_statistics(statistics)
                    else:
                        await interaction.send("`[❌]:` You are already verified!", ephemeral=True)
                else:
                    await interaction.send("`[❌]:` Verification is disabled on this server!", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You entered the wrong result!", ephemeral=True)

        except nextcord.errors.Forbidden as e:
            await interaction.send(f'`[❌]:` The bot does not have permission! (Notify the server administration about this error, it is not technically caused)\n\n`{e}`')
        except nextcord.NotFound:
            await interaction.send(f'`[❌]:` Role not found! (Notify the server administration about this error, it is not technically caused)\n\n`{e}`')
        except ValueError:
            await interaction.send("`[❌]:` You entered the wrong result!", ephemeral=True)

class Weryfikacja(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="✅ Zweryfikuj", style=nextcord.ButtonStyle.green, custom_id="weryfikacja")
    async def openticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        user = interaction.user

        try:
            server_id = str(interaction.guild.id)
            settings_document = settings_collection.find_one({'_id': server_id})
            if settings_document and settings_document.get("weryfikacja", False):
                await interaction.response.send_modal(WeryfikacjaModal())
            else:
                await interaction.send("`[❌]:` Weryfikacja jest wyłączona na tym serwerze", ephemeral=True)

        except nextcord.errors.Forbidden as e:
            await user.send(f'`[❌]:` Bot nie posiada permisji! (Powiadom administrację serwera o tym błędzie, nie jest on spowowodowany ze strony technicznej)\n\n`{e}`')
        except nextcord.NotFound as e:
            await user.send(f'`[❌]:` Nie odnaleziono roli! (Powiadom administrację serwera o tym błędzie, nie jest on spowowodowany ze strony technicznej)\n\n`{e}`')

class WeryfikacjaENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="✅ Verify", style=nextcord.ButtonStyle.green, custom_id="weryfikacjaENG")
    async def openticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        user = interaction.user
        
        try:
            server_id = str(interaction.guild.id)
            settings_document = settings_collection.find_one({'_id': server_id})
            if settings_document and settings_document.get("weryfikacja", False):
                await interaction.response.send_modal(WeryfikacjaModalENG())
            else:
                await interaction.send("`[❌]:` Verification is disabled on this server", ephemeral=True)

        except nextcord.errors.Forbidden as e:
            await user.send(f'`[❌]:` The bot does not have permission! (Notify the server administration about this error, it is not technically caused)\n\n{e}')
        except nextcord.NotFound:
            await user.send(f'`[❌]:` Role not found! (Notify the server administration about this error, it is not technically caused)\n\n`{e}`')

class Wylaczanie_Wlaczanie_logow(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz logi", style=nextcord.ButtonStyle.blurple, custom_id="offlogi")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("logi", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'logi': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'logi': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` Funkcja `logi` została {status_text} dla tego serwera.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `logi`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/settingsConfig logi`!", ephemeral=True)

class Wylaczanie_Wlaczanie_logowENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Turn off / ✅ Turn on logi", style=nextcord.ButtonStyle.blurple, custom_id="offlogiENG")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("logi", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'logi': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'logi': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "turned on" if new_status else "turned off"
                await interaction.send(f"`[✅]:` The `log` function has been {status_text} for this server.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `logs`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interaction timed out, try `/settingsConfig log` again!", ephemeral=True)

class Wylaczanie_Wlaczanie_liczenia(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz liczenie", style=nextcord.ButtonStyle.blurple, custom_id="offliczenie")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("liczenie", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'liczenie': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'liczenie': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` Funkcja `liczenie` została {status_text} dla tego serwera.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `liczenie`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/settingsConfig liczenie`!", ephemeral=True)

class Wylaczanie_Wlaczanie_liczeniaENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Turn off / ✅ Turn on liczenie", style=nextcord.ButtonStyle.blurple, custom_id="offliczenieENG")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("liczenie", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'liczenie': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'liczenie': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "turned on" if new_status else "turned off"
                await interaction.send(f"`[✅]:` The `liczenie` function has been {status_text} for this server.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `liczenie`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interaction timed out, try the command `/settingsConfig liczenie` again!", ephemeral=True)

class Wylaczanie_Wlaczanie_litera(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz ostatnią literę", style=nextcord.ButtonStyle.blurple, custom_id="offlitera")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("litera", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'litera': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'litera': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` Funkcja `ostatnia litera` została {status_text} dla tego serwera.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `ostatnia litera`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/settings4Fun litera`!", ephemeral=True)

class Wylaczanie_Wlaczanie_literaENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Turn off / ✅ Turn on last letter", style=nextcord.ButtonStyle.blurple, custom_id="offliteraENG")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("litera", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'litera': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'litera': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` The function `ostatnia litera` has been {status_text} for this server.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `ostatnia litera`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interaction timed out, try the  `/settings4Fun litera` again!", ephemeral=True)

class Wylaczanie_Wlaczanie_powitan(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz powitania", style=nextcord.ButtonStyle.blurple, custom_id="offpowitania")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("powitania", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'powitania': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'powitania': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` Funkcja `powitania` została {status_text} dla tego serwera.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `powitania`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/settingsConfig powitania`!", ephemeral=True)

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz własne wiadomości", style=nextcord.ButtonStyle.blurple, custom_id="offpowitaniawiad")
    async def offticket2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("powitaniaWiadomoscON", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'powitaniaWiadomoscON': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'powitaniaWiadomoscON': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` Funkcja `wiadomość powitania` została {status_text} dla tego serwera.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `wiadomość powitania`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/settingsConfig powitania`!", ephemeral=True)

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz wiadomość PV", style=nextcord.ButtonStyle.blurple, custom_id="offpowitaniapv")
    async def offticket3(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("powitaniaPV", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'powitaniaPV': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'powitaniaPV': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` Funkcja `powitaniaPV` została {status_text} dla tego serwera.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `powitaniaPV`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/settingsConfig powitania`!", ephemeral=True)

class Wylaczanie_Wlaczanie_powitanENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Turn off / ✅ Turn on powitania", style=nextcord.ButtonStyle.blurple, custom_id="offpowitaniaENG")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("powitania", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'powitania': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'powitania': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "turned on" if new_status else "turned off"
                await interaction.send(f"`[✅]:` The `powitania` function has been {status_text} for this server.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You do not have `manage messages` permission to enable/disable `powitania`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` The interaction has expired, please try the `/settingsConfig powitania` command again!", ephemeral=True)

    @nextcord.ui.button(label="❌ Turn off / ✅ Turn on own content", style=nextcord.ButtonStyle.blurple, custom_id="offpowitaniawiadENG")
    async def offticket2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("powitaniaWiadomoscON", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'powitaniaWiadomoscON': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'powitaniaWiadomoscON': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "turned on" if new_status else "turned off"
                await interaction.send(f"`[✅]:` The `own content powitania` function has been {status_text} for this server.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You do not have `manage messages` permission to enable/disable `own content powitania`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` The interaction has expired, please try the `/settingsConfig powitania` command again!", ephemeral=True)

    @nextcord.ui.button(label="❌ Turn off / ✅ Turn on powitania PV", style=nextcord.ButtonStyle.blurple, custom_id="offpowitaniapvENG")
    async def offticket3(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("powitaniaPV", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'powitaniaPV': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'powitaniaPV': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` The `powitaniaPV` function has been {status_text} for this server.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You do not have `manage messages` permission to enable/disable `powitaniaPV`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` The interaction has expired, please try the `/settingsConfig powitania` command again!", ephemeral=True)

class Wylaczanie_Wlaczanie_pozegnan(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz pozegnania", style=nextcord.ButtonStyle.blurple, custom_id="offpozegnania")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("pozegnania", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'pozegnania': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'pozegnania': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` Funkcja `pozegnania` została {status_text} dla tego serwera.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `pozegnania`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/settingsConfig pozegnania`!", ephemeral=True)

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz własne wiadomości", style=nextcord.ButtonStyle.blurple, custom_id="offpozegnaniawiad")
    async def offticket2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("pozegnaniaWiadomoscON", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'pozegnaniaWiadomoscON': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'pozegnaniaWiadomoscON': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` Funkcja `wiadomość pożegnania` została {status_text} dla tego serwera.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `wiadomość pożegnania`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/settingsConfig pozegnania`!", ephemeral=True)

class Wylaczanie_Wlaczanie_pozegnanENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Turn off / ✅ Turn on z powitania", style=nextcord.ButtonStyle.blurple, custom_id="offpozegnaniaENG")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("pozegnania", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'pozegnania': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'pozegnania': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` The `pozegnania` function has been {status_text} for this server.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You do not have `manage messages` permission to enable/disable `pozegnania`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` The interaction has expired, please try the `/settingsConfig pozegnania` command again!", ephemeral=True)

    @nextcord.ui.button(label="❌ Turn off / ✅ Turn on own content", style=nextcord.ButtonStyle.blurple, custom_id="offpozegnaniawiadENG")
    async def offticket2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("pozegnaniaWiadomoscON", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'pozegnaniaWiadomoscON': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'pozegnaniaWiadomoscON': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "turned on" if new_status else "turned off"
                await interaction.send(f"`[✅]:` The `own content pożegnania` function has been {status_text} for this server.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You do not have `manage messages` permission to enable/disable `own content pożegnania`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` The interaction has expired, please try the `/settingsConfig pozegnania` command again!", ephemeral=True)

class Wylaczanie_Wlaczanie_ekonomii(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz ekonomie", style=nextcord.ButtonStyle.blurple, custom_id="offekonomia")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("ekonomia", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'ekonomia': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'ekonomia': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` Funkcja `ekonomia` została {status_text} dla tego serwera.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `ekonomia`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/settingsConfig ekonomia`!", ephemeral=True)

class Wylaczanie_Wlaczanie_ekonomiiENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Turn off / ✅ Turn on  ekonomie", style=nextcord.ButtonStyle.blurple, custom_id="offekonomiaENG")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("ekonomia", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'ekonomia': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'ekonomia': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "turned on" if new_status else "turned off"
                await interaction.send(f"`[✅]:` The `ekonomia` function has been {status_text} for this server.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You do not have `manage messages` permission to enable/disable `ekonomia`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` The interaction has expired, please try the `/settingsConfig ekonomia` command again!", ephemeral=True)

class Wylaczanie_Wlaczanie_selfchannel(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz własne kanały", style=nextcord.ButtonStyle.blurple, custom_id="offselfchannel")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("selfchannel", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'selfchannel': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'selfchannel': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` Funkcja `selfchannel` została {status_text} dla tego serwera.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `selfchannel`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/settingsConfig selfchannel`!", ephemeral=True)

class Wylaczanie_Wlaczanie_selfchannelENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Turn off / ✅ Turn on selfchannel", style=nextcord.ButtonStyle.blurple, custom_id="offselfchannelENG")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("selfchannel", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'selfchannel': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'selfchannel': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "turned on" if new_status else "turned off"
                await interaction.send(f"`[✅]:` The `selfchannel` function has been {status_text} for this server.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You do not have `manage messages` permission to enable/disable `selfchannel`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` The interaction has expired, please try the `/settingsConfig selfchannel` command again!", ephemeral=True)

class Wylaczanie_Wlaczanie_statystyk(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz statystyki", style=nextcord.ButtonStyle.blurple, custom_id="offstatystyki")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("statystyki", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'statystyki': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'statystyki': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` Funkcja `statystyki` została {status_text} dla tego serwera.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `statystyki`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/settingsConfig statystyki`!", ephemeral=True)

class Wylaczanie_Wlaczanie_statystykENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Turn off / ✅ Turn on statystyki", style=nextcord.ButtonStyle.blurple, custom_id="offstatystykiENG")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("statystyki", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'statystyki': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'statystyki': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` The `statystyki` function has been {status_text} for this server.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You do not have `manage messages` permission to enable/disable `statystyki`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` The interaction has expired, please try the `/settingsConfig statystyki` command again!", ephemeral=True)

class Wylaczanie_Wlaczanie_autoad(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz autoad", style=nextcord.ButtonStyle.blurple, custom_id="offautoad")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("autoad", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'autoad': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'autoad': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` Funkcja `autoad` została {status_text} dla tego serwera.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `autoad`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/settingsConfig autoad`!", ephemeral=True)

class Wylaczanie_Wlaczanie_autoadENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="❌ Turn off / ✅ Turn on autoad", style=nextcord.ButtonStyle.blurple, custom_id="offautoadENG")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:

            if interaction.user.guild_permissions.manage_messages:
                server_id = str(interaction.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if settings_document:
                    current_status = settings_document.get("autoad", False)
                    new_status = not current_status

                    settings_collection.update_one({'_id': server_id}, {'$set': {'autoad': new_status}})
                else:
                    new_status = True
                    settings_document = {'_id': server_id, 'autoad': new_status}
                    settings_collection.insert_one(settings_document)
                
                status_text = "włączona" if new_status else "wyłączona"
                await interaction.send(f"`[✅]:` The `autoad` function has been {status_text} for this server.", ephemeral=True)
            else:
                await interaction.send("`[❌]:` You do not have `manage messages` permission to enable/disable `autoad`!", ephemeral=True)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` The interaction has expired, please try the `/settingsConfig autoad` command again!", ephemeral=True)

class Zgadywanka_wybor(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label="🔢 Liczba", style=nextcord.ButtonStyle.green, custom_id="liczba")
    async def liczba(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg

            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=f'**Zgadywanka**', description=f"**Okej! poniżej wybierz liczbę!** 🧮", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/PytajnikiC.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            view = Zgadywanka_liczba(user_id=self.user_id)
            await msg.edit(embed=embed, view=view)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/zgaduj`!", ephemeral=True)

    @nextcord.ui.button(label="💬 Słowo", style=nextcord.ButtonStyle.green, custom_id="slowo")
    async def slowo(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg

            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=f'**Zgadywanka**', description=f"**Okej! poniżej wybierz słowo!** 🗣", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/PytajnikiC.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            view = Zgadywanka_slowo(user_id=self.user_id)
            await msg.edit(embed=embed, view=view)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/zgaduj`!", ephemeral=True)

class Zgadywanka_wyborENG(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label="🔢 Number", style=nextcord.ButtonStyle.green, custom_id="liczbaENG")
    async def liczba(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg

            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=f'**Zgadywanka**', description=f"**Okay! choose a number below!** 🧮", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/PytajnikiC.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            view = Zgadywanka_liczbaENG(user_id=self.user_id)
            await msg.edit(embed=embed, view=view)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interaction timed out, try the command `/zgaduj` again!", ephemeral=True)

    @nextcord.ui.button(label="💬 Word", style=nextcord.ButtonStyle.green, custom_id="slowoENG")
    async def slowo(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg

            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=f'**Zgadywanka**', description=f"**Okay! choose a word below!** 🗣", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/PytajnikiC.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            view = Zgadywanka_slowoENG(user_id=self.user_id)
            await msg.edit(embed=embed, view=view)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interaction timed out, try the command `/zgaduj` again!", ephemeral=True)


class Zgadywanka_liczba(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label=f"{random.randint(1, 100)}", style=nextcord.ButtonStyle.green, custom_id="liczba1")
    async def liczba1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Brawo! Zgadłeś! Przez cooldown twoja wygrana przepadła! Spróbuj ponownie za `{time_left.seconds} sekund`!**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                    tytul = "**ZGADŁEŚ**"
                    view = Zgadywanka_ponownie2(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Niestety! Nie zgadłeś**"
                tytul = "**NIESTETY**"
                view = Zgadywanka_ponownie(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/zgaduj`!", ephemeral=True)

    @nextcord.ui.button(label=f"{random.randint(1, 100)}", style=nextcord.ButtonStyle.green, custom_id="liczba2")
    async def liczba2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Brawo! Zgadłeś! Przez cooldown twoja wygrana przepadła! Spróbuj ponownie za `{time_left.seconds} sekund`!**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                    tytul = "**ZGADŁEŚ**"
                    view = Zgadywanka_ponownie2(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Niestety! Nie zgadłeś**"
                tytul = "**NIESTETY**"
                view = Zgadywanka_ponownie(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/zgaduj`!", ephemeral=True)

    @nextcord.ui.button(label=f"{random.randint(1, 100)}", style=nextcord.ButtonStyle.green, custom_id="liczba3")
    async def liczba3(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Brawo! Zgadłeś! Przez cooldown twoja wygrana przepadła! Spróbuj ponownie za `{time_left.seconds} sekund`!**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                    tytul = "**ZGADŁEŚ**"
                    view = Zgadywanka_ponownie2(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Niestety! Nie zgadłeś**"
                tytul = "**NIESTETY**"
                view = Zgadywanka_ponownie(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/zgaduj`!", ephemeral=True)
    
    @nextcord.ui.button(label=f"{random.randint(1, 100)}", style=nextcord.ButtonStyle.green, custom_id="liczba4")
    async def liczba4(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Brawo! Zgadłeś! Przez cooldown twoja wygrana przepadła! Spróbuj ponownie za `{time_left.seconds} sekund`!**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                    tytul = "**ZGADŁEŚ**"
                    view = Zgadywanka_ponownie2(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Niestety! Nie zgadłeś**"
                tytul = "**NIESTETY**"
                view = Zgadywanka_ponownie(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/zgaduj`!", ephemeral=True)

    @nextcord.ui.button(label=f"{random.randint(1, 100)}", style=nextcord.ButtonStyle.green, custom_id="liczba5")
    async def liczba5(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Brawo! Zgadłeś! Przez cooldown twoja wygrana przepadła! Spróbuj ponownie za `{time_left.seconds} sekund`!**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                    tytul = "**ZGADŁEŚ**"
                    view = Zgadywanka_ponownie2(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Niestety! Nie zgadłeś**"
                tytul = "**NIESTETY**"
                view = Zgadywanka_ponownie(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/zgaduj`!", ephemeral=True)

class Zgadywanka_liczbaENG(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label=f"{random.randint(1, 100)}", style=nextcord.ButtonStyle.green, custom_id="liczba1ENG")
    async def liczba1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Way to go! You guessed! Due to the cooldown, your winnings are gone! Please try again after `{time_left.seconds} seconds`!**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                    tytul = "**GUESSED**"
                    view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Unfortunately! You did not guess**"
                tytul = "**UNFORTUNATELY**"
                view = Zgadywanka_ponownieENG(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interaction timed out, please try `/zgaduj` again!", ephemeral=True)

    @nextcord.ui.button(label=f"{random.randint(1, 100)}", style=nextcord.ButtonStyle.green, custom_id="liczba2ENG")
    async def liczba2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Way to go! You guessed! Due to the cooldown, your winnings are gone! Please try again after `{time_left.seconds} seconds`!**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                    tytul = "**GUESSED**"
                    view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Unfortunately! You did not guess**"
                tytul = "**UNFORTUNATELY**"
                view = Zgadywanka_ponownieENG(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interaction timed out, please try `/zgaduj` again!", ephemeral=True)

    @nextcord.ui.button(label=f"{random.randint(1, 100)}", style=nextcord.ButtonStyle.green, custom_id="liczba3ENG")
    async def liczba3(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Way to go! You guessed! Due to the cooldown, your winnings are gone! Please try again after `{time_left.seconds} seconds`!**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                    tytul = "**GUESSED**"
                    view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Unfortunately! You did not guess**"
                tytul = "**UNFORTUNATELY**"
                view = Zgadywanka_ponownieENG(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interaction timed out, please try `/zgaduj` again!", ephemeral=True)
    
    @nextcord.ui.button(label=f"{random.randint(1, 100)}", style=nextcord.ButtonStyle.green, custom_id="liczba4ENG")
    async def liczba4(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Way to go! You guessed! Due to the cooldown, your winnings are gone! Please try again after `{time_left.seconds} seconds`!**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                    tytul = "**GUESSED**"
                    view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Unfortunately! You did not guess**"
                tytul = "**UNFORTUNATELY**"
                view = Zgadywanka_ponownieENG(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interaction timed out, please try `/zgaduj` again!", ephemeral=True)

    @nextcord.ui.button(label=f"{random.randint(1, 100)}", style=nextcord.ButtonStyle.green, custom_id="liczba5ENG")
    async def liczba5(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Way to go! You guessed! Due to the cooldown, your winnings are gone! Please try again after `{time_left.seconds} seconds`!**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                    tytul = "**GUESSED**"
                    view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Unfortunately! You did not guess**"
                tytul = "**UNFORTUNATELY**"
                view = Zgadywanka_ponownieENG(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interaction timed out, please try `/zgaduj` again!", ephemeral=True)

class Zgadywanka_slowo(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label=f"{random.choice(słowa_zgadywanka1)}", style=nextcord.ButtonStyle.green, custom_id="slowo1")
    async def slowo1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Brawo! Zgadłeś! Przez cooldown twoja wygrana przepadła! Spróbuj ponownie za `{time_left.seconds} sekund`!**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                    tytul = "**ZGADŁEŚ**"
                    view = Zgadywanka_ponownie2(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Niestety! Nie zgadłeś**"
                tytul = "**NIESTETY**"
                view = Zgadywanka_ponownie(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/zgaduj`!", ephemeral=True)

    @nextcord.ui.button(label=f"{random.choice(słowa_zgadywanka2)}", style=nextcord.ButtonStyle.green, custom_id="slowo2")
    async def slowo2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Brawo! Zgadłeś! Przez cooldown twoja wygrana przepadła! Spróbuj ponownie za `{time_left.seconds} sekund`!**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                    tytul = "**ZGADŁEŚ**"
                    view = Zgadywanka_ponownie2(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Niestety! Nie zgadłeś**"
                tytul = "**NIESTETY**"
                view = Zgadywanka_ponownie(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/zgaduj`!", ephemeral=True)

    @nextcord.ui.button(label=f"{random.choice(słowa_zgadywanka3)}", style=nextcord.ButtonStyle.green, custom_id="slowo3")
    async def slowo3(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Brawo! Zgadłeś! Przez cooldown twoja wygrana przepadła! Spróbuj ponownie za `{time_left.seconds} sekund`!**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                    tytul = "**ZGADŁEŚ**"
                    view = Zgadywanka_ponownie2(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Niestety! Nie zgadłeś**"
                tytul = "**NIESTETY**"
                view = Zgadywanka_ponownie(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/zgaduj`!", ephemeral=True)
    
    @nextcord.ui.button(label=f"{random.choice(słowa_zgadywanka4)}", style=nextcord.ButtonStyle.green, custom_id="slowo4")
    async def slowo4(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Brawo! Zgadłeś! Przez cooldown twoja wygrana przepadła! Spróbuj ponownie za `{time_left.seconds} sekund`!**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                    tytul = "**ZGADŁEŚ**"
                    view = Zgadywanka_ponownie2(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Niestety! Nie zgadłeś**"
                tytul = "**NIESTETY**"
                view = Zgadywanka_ponownie(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/zgaduj`!", ephemeral=True)

    @nextcord.ui.button(label=f"{random.choice(słowa_zgadywanka5)}", style=nextcord.ButtonStyle.green, custom_id="slowo5")
    async def slowo5(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Brawo! Zgadłeś! Przez cooldown twoja wygrana przepadła! Spróbuj ponownie za `{time_left.seconds} sekund`!**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                        tytul = "**ZGADŁEŚ**"
                        view = Zgadywanka_ponownie2(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Brawo! Zgadłeś! Wygrałeś `{wygrana}` waluty**"
                    tytul = "**ZGADŁEŚ**"
                    view = Zgadywanka_ponownie2(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Niestety! Nie zgadłeś**"
                tytul = "**NIESTETY**"
                view = Zgadywanka_ponownie(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/zgaduj`!", ephemeral=True)

class Zgadywanka_slowoENG(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label=f"{random.choice(słowa_zgadywanka1ENG)}", style=nextcord.ButtonStyle.green, custom_id="slowo1ENG")
    async def slowo1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Way to go! You guessed! Due to the cooldown, your winnings are gone! Please try again after `{time_left.seconds} seconds`!**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                    tytul = "**GUESSED**"
                    view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Unfortunately! You did not guess**"
                tytul = "**UNFORTUNATELY**"
                view = Zgadywanka_ponownieENG(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interaction timed out, try `/zgaduj` again!", ephemeral=True)

    @nextcord.ui.button(label=f"{random.choice(słowa_zgadywanka2ENG)}", style=nextcord.ButtonStyle.green, custom_id="slowo2ENG")
    async def slowo2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Way to go! You guessed! Due to the cooldown, your winnings are gone! Please try again after `{time_left.seconds} seconds`!**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                    tytul = "**GUESSED**"
                    view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Unfortunately! You did not guess**"
                tytul = "**UNFORTUNATELY**"
                view = Zgadywanka_ponownieENG(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interaction timed out, try `/zgaduj` again!", ephemeral=True)

    @nextcord.ui.button(label=f"{random.choice(słowa_zgadywanka3ENG)}", style=nextcord.ButtonStyle.green, custom_id="slowo3ENG")
    async def slowo3(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Way to go! You guessed! Due to the cooldown, your winnings are gone! Please try again after `{time_left.seconds} seconds`!**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                    tytul = "**GUESSED**"
                    view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Unfortunately! You did not guess**"
                tytul = "**UNFORTUNATELY**"
                view = Zgadywanka_ponownieENG(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interaction timed out, try `/zgaduj` again!", ephemeral=True)
    
    @nextcord.ui.button(label=f"{random.choice(słowa_zgadywanka4ENG)}", style=nextcord.ButtonStyle.green, custom_id="slowo4ENG")
    async def slowo4(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Way to go! You guessed! Due to the cooldown, your winnings are gone! Please try again after `{time_left.seconds} seconds`!**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                    tytul = "**GUESSED**"
                    view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Unfortunately! You did not guess**"
                tytul = "**UNFORTUNATELY**"
                view = Zgadywanka_ponownieENG(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interaction timed out, try `/zgaduj` again!", ephemeral=True)

    @nextcord.ui.button(label=f"{random.choice(słowa_zgadywanka5ENG)}", style=nextcord.ButtonStyle.green, custom_id="slowo5ENG")
    async def slowo5(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            server_id = str(interaction.guild.id)

            num = random.randint(1, 4)
            if num == 1:
                user_id = str(interaction.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "zgadujCD" in cooldown_data:
                    last_usage = cooldown_data["zgadujCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        wynik = f"**Way to go! You guessed! Due to the cooldown, your winnings are gone! Please try again after `{time_left.seconds} seconds`!**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"

                    else:
                        wygrana = round(random.uniform(0.1, 2), 2)
                        wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                        tytul = "**GUESSED**"
                        view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                        obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                        user_id = str(interaction.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(interaction.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"zgadujCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "zgadujCD": current_time})

                    wygrana = round(random.uniform(0.1, 2), 2)
                    wynik = f"**Way to go! You guessed! You won `{wygrana}` currency**"
                    tytul = "**GUESSED**"
                    view = Zgadywanka_ponownie2ENG(user_id=self.user_id)
                    obr = "https://dreambot.pl/DreamBotImages/PytajnikiD.png"
                        
                    user_id = str(interaction.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(interaction.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                wynik = "**Unfortunately! You did not guess**"
                tytul = "**UNFORTUNATELY**"
                view = Zgadywanka_ponownieENG(user_id=self.user_id)
                obr = "https://dreambot.pl/DreamBotImages/PytajnikiC.png"
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=tytul, description=wynik, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=obr)
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await msg.edit(embed=embed, view=view)

        except Exception as e:
                await interaction.send(f"`[❌]:` Interaction timed out, try `/zgaduj` again!", ephemeral=True)

class Zgadywanka_ponownie(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label=f"🔁 Spróbuj ponownie", style=nextcord.ButtonStyle.green, custom_id="ponownie")
    async def liczba1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=f'**Zgadywanka**', description=f"**Aby rozpocząć zgadywankę wybierz czy chcesz zgadywać liczbę czy słowo!** 🤔", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/PytajnikiC.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            view = Zgadywanka_wybor(user_id=self.user_id)
            await msg.edit(embed=embed, view=view)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/zgaduj`!", ephemeral=True)

class Zgadywanka_ponownieENG(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label=f"🔁 Retry", style=nextcord.ButtonStyle.green, custom_id="ponownieENG")
    async def liczba1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=f'**Guessing game**', description=f"**To start the guessing game choose whether you want to guess a number or a word!** 🤔", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/PytajnikiC.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            view = Zgadywanka_wyborENG(user_id=self.user_id)
            await msg.edit(embed=embed, view=view)
        
        except Exception as e:
            await interaction.send(f"`[❌]:` Interaction timed out, try `/guessing` again!", ephemeral=True)

class Zgadywanka_ponownie2(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label=f"🧅 Ja chcę jeszcze raz!", style=nextcord.ButtonStyle.green, custom_id="ponownie2")
    async def liczba1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=f'**Zgadywanka**', description=f"**Aby rozpocząć zgadywankę wybierz czy chcesz zgadywać liczbę czy słowo!** 🤔", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/PytajnikiC.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            view = Zgadywanka_wybor(user_id=self.user_id)
            await msg.edit(embed=embed, view=view)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interakcja wygasła, spróbuj znowu użyć komendy `/zgaduj`!", ephemeral=True)

class Zgadywanka_ponownie2ENG(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label=f"🧅 I want again!", style=nextcord.ButtonStyle.green, custom_id="ponownie2ENG")
    async def liczba1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False

        try:
            if not self.user_id == interaction.user.id:
                await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/zgaduj`!", ephemeral=True)
                return

            msg = zgadywanka_msg
            
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed = nextcord.Embed(title=f'**Guessing game**', description=f"**To start guessing choose whether you want to guess a number or a word!** 🤔", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/PytajnikiC.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            view = Zgadywanka_wyborENG(user_id=self.user_id)
            await msg.edit(embed=embed, view=view)

        except Exception as e:
            await interaction.send(f"`[❌]:` Interaction timed out, try `/guessing` again!", ephemeral=True)

class SelfRole(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="✋ Odbierz rolę", style=nextcord.ButtonStyle.blurple, custom_id="selfrole")
    async def role(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        try:
            guild_id = str(interaction.guild.id)
            message_id = str(interaction.message.id)
            server = interaction.guild
            settings_document = settings_collection.find_one({'_id': guild_id})

            if settings_document:
                selfrole_entry = None
                if 'selfrole' in settings_document:
                    for entry in settings_document['selfrole']:
                        if entry['msg_id'] == message_id:
                            selfrole_entry = entry
                            break

                if selfrole_entry:
                    rola_id = selfrole_entry['rola_id']
                    rola = server.get_role(int(rola_id))

                    if rola in interaction.user.roles:
                        await interaction.user.remove_roles(rola)
                        await interaction.send(f"`[✅]:` Pomyślnie zabrano rolę {rola.mention}!", ephemeral=True)
                        return

                    await interaction.user.add_roles(rola)
                    await interaction.send(f"`[✅]:` Pomyślnie otrzymano rolę {rola.mention}!", ephemeral=True)
                else:
                    await interaction.response.send_message("`[❌]:` Brak konfiguracji roli i kanału.", ephemeral=True)
            else:
                await interaction.response.send_message("`[❌]:` Brak konfiguracji serwera!", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"`[❌]:` Wystąpił błąd (Powiadom o nim administratora serwera, nie jest on spowodowany z strony technicznej)\n\n{e}", ephemeral=True)

class SelfRoleENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="✋ Take role", style=nextcord.ButtonStyle.blurple, custom_id="selfroleENG")
    async def role(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        try:
            guild_id = str(interaction.guild.id)
            message_id = str(interaction.message.id)
            server = interaction.guild
            settings_document = settings_collection.find_one({'_id': guild_id})

            if settings_document:
                selfrole_entry = None
                if 'selfrole' in settings_document:
                    for entry in settings_document['selfrole']:
                        if entry['msg_id'] == message_id:
                            selfrole_entry = entry
                            break

                if selfrole_entry:
                    rola_id = selfrole_entry['rola_id']
                    rola = server.get_role(int(rola_id))

                    if rola in interaction.user.roles:
                        await interaction.user.remove_roles(rola)
                        await interaction.send(f"`[✅]:` Successfully taken role {rola.mention}!", ephemeral=True)
                        return

                    await interaction.user.add_roles(rola)
                    await interaction.send(f"`[✅]:` Successfully received role {rola.mention}!", ephemeral=True)
                    
                else:
                    await interaction.response.send_message("`[❌]:` No role and channel configuration.", ephemeral=True)
            else:
                await interaction.response.send_message("`[❌]:` No server configuration!", ephemeral=True)
        
        except Exception as e:
            await interaction.response.send_message(f"`[❌]:` An error has occurred (Notify the server administrator about this, it is not technical)\n\n{e}", ephemeral=True)

class SayModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title="/Say", timeout=None)
        self.emTitle = nextcord.ui.TextInput(label=f"Tytuł", required=True, placeholder="Wpisz tutaj tytuł embeda")
        self.emDesc = nextcord.ui.TextInput(label=f"Opis", required=True, placeholder="Wpisz tutaj opis embeda")
        self.emThumbnail = nextcord.ui.TextInput(label=f"Obraz", required=False, placeholder="Link do obrazu (np. https://dreambot.pl/obraz.png)")
        self.emColor = nextcord.ui.TextInput(label=f"Kolor", required=False, placeholder="Kolor embeda (np. ffe600)")
        self.emFooter = nextcord.ui.TextInput(label=f"Stopka", required=False, placeholder="Dół embeda")
        self.add_item(self.emTitle)
        self.add_item(self.emDesc)
        self.add_item(self.emThumbnail)
        self.add_item(self.emColor)
        self.add_item(self.emFooter)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        try:
            link = False
            if contains_link(self.emTitle.value):
                link = True
            elif contains_link(self.emDesc.value):
                link = True
            elif contains_link(self.emThumbnail.value):
                link = True
            elif contains_link(self.emColor.value):
                link = True
            elif contains_link(self.emFooter.value):
                link = True

            if link == True:
                await interaction.send("`[❌]:` Wiadomość zwiera link!", ephemeral=True)
                return

            current_time = time.strftime("%H:%M:%S")
            try:
                color = int(self.emColor.value, 16)
            except Exception:
                color = 0xffe600

            embed = nextcord.Embed(title=self.emTitle.value, description=self.emDesc.value, color=color)
            embed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)

            if self.emThumbnail.value:
                embed.set_thumbnail(url=self.emThumbnail.value)

            if self.emFooter.value:
                embed.set_footer(text=f"{self.emFooter.value} | {current_time}")
            else:
                embed.set_footer(text=f"{current_time}")

            await interaction.send(embed=embed)
        except Exception as e:
            await interaction.send(f"`[❌]:` Wystąpił błąd:\n\n{e}", ephemeral=True)

class SayModalENG(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title="/Say", timeout=None)
        self.emTitle = nextcord.ui.TextInput(label=f"Title", required=True, placeholder="Enter your embed title here")
        self.emDesc = nextcord.ui.TextInput(label=f"Description", required=True, placeholder="Enter a description of the embed here")
        self.emThumbnail = nextcord.ui.TextInput(label=f"Image", required=False, placeholder="Link to image (e.g. https://dreambot.pl/obraz.png)")
        self.emColor = nextcord.ui.TextInput(label=f"Color", required=False, placeholder="Embed color (e.g. ffe600)")
        self.emFooter = nextcord.ui.TextInput(label=f"Footer", required=False, placeholder="Embed bottom")
        self.add_item(self.emTitle)
        self.add_item(self.emDesc)
        self.add_item(self.emThumbnail)
        self.add_item(self.emColor)
        self.add_item(self.emFooter)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        try:
            current_time = time.strftime("%H:%M:%S")
            try:
                color = int(self.emColor.value, 16)
            except Exception:
                color = 0xffe600

            embed = nextcord.Embed(title=self.emTitle.value, description=self.emDesc.value, color=color)
            embed.set_author(name=interaction.user, icon_url=interaction.user.avatar.url)

            if self.emThumbnail.value:
                embed.set_thumbnail(url=self.emThumbnail.value)

            if self.emFooter.value:
                embed.set_footer(text=f"{self.emFooter.value} | {current_time}")
            else:
                embed.set_footer(text=f"{current_time}")

            await interaction.send(embed=embed)
        except Exception as e:
            await interaction.send(f"`[❌]:` An error occured:\n\n{e}", ephemeral=True)

class AutoAdReklamaModal(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title="AutoAD Reklama", timeout=None)
        self.emTitle = nextcord.ui.TextInput(label="Reklama", required=True, placeholder="Jaki super serwerek!", style=TextInputStyle.paragraph, max_length=1200)
        self.add_item(self.emTitle)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel = await bot.fetch_channel(1175540326845399049)
        reklama_text = self.emTitle.value.replace('\n', '\\n')
        reklama_message = f"{self.emTitle.value}"

        file_content = File(io.StringIO(reklama_text), filename='reklama.txt')
        await channel.send(f"Informacje:\n\nUżytkownik - {interaction.user} (*{interaction.user.id}*)\nSerwer - {interaction.guild.name} (*{interaction.guild.id}*)\n\n\n{reklama_message}", file=file_content)
        await interaction.send("`[✅]:` Reklama została wysłana do weryfikacji! Dołącz na *[nasz serwer](https://discord.gg/wwtXdvtyKG)* aby wiedzieć kiedy ją zweryfikujemy!", ephemeral=True)
        
        settings_document = settings_collection.find_one({'_id': str(interaction.guild.id)})
        settings_document['autoReklamaStatus'] = "W trakcie weryfikacji"
        settings_collection.update_one({'_id': id}, {'$set': settings_document})
        os.remove('reklama.txt')

class AutoAdReklamaModalENG(nextcord.ui.Modal):
    def __init__(self):
        super().__init__(title="AutoAD Advertisiment", timeout=None)
        self.emTitle = nextcord.ui.TextInput(label="Advert", required=True, placeholder="What a great server!", style=TextInputStyle.paragraph, max_length=1200)
        self.add_item(self.emTitle)

    async def callback(self, interaction: nextcord.Interaction) -> None:
        channel = await bot.fetch_channel(1175540919198556180)
        reklama_text = self.emTitle.value.replace('\n', '\\n')
        reklama_message = f"{self.emTitle.value}"
        
        file_content = File(io.StringIO(reklama_text), filename='reklama.txt')
        await channel.send(f"Informacje:\n\nUżytkownik - {interaction.user} (*{interaction.user.id}*)\nSerwer - {interaction.guild.name} (*{interaction.guild.id}*)\n\n\n{reklama_message}", file=file_content)
        await interaction.send("`[✅]:` The ad has been sent for verification! Join *[our server](https://discord.gg/wwtXdvtyKG)* to know when we will verify it!", ephemeral=True)
        
        settings_document = settings_collection.find_one({'_id': str(interaction.guild.id)})
        settings_document['autoReklamaStatus'] = "During the verification"
        settings_collection.update_one({'_id': id}, {'$set': settings_document})
        os.remove('reklama.txt')

class OwnerInfo(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="🧰 Backup", style=nextcord.ButtonStyle.red, custom_id="backup")
    async def offticket(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        try:
            backup_invites = {}
            today = datetime.datetime.today().strftime('%d-%m-%Y')
            backup_invites['_id'] = today

            num = 0
            for guild in bot.guilds:
                try:
                    invite = await guild.text_channels[0].create_invite(reason="Backup", temporary=False)
                    backup_invites[str(guild.id)] = invite.url
                    num += 1
                except Exception:
                    pass

            backup_collection.insert_one(backup_invites)
            await interaction.send(f"`[✅]:` Pomyślnie stworzono backup na datę `{today}`! Liczba serwerów: `{num}`", ephemeral=True)
        except Exception as e:
            if "E11000" in str(e):
                await interaction.send(f"`[❌]:` Backup z dzisiejszego dnia (`{today}`) jest już na serwerze!", ephemeral=True)

class FishShopWedki(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="🎣 Wędki", style=nextcord.ButtonStyle.blurple, custom_id="wedki", disabled=True)
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        await interaction.send("Nie działa :XDX:")

    @nextcord.ui.button(label="🔮 Ulepszenia", style=nextcord.ButtonStyle.blurple, custom_id="ulepszenia")
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        shop_data = fish_collection.find_one({'_id': 'Info'})
        if shop_data and 'Shop' in shop_data:
            shop_items = shop_data['ShopUpgrades']
            star = "<:Star:1166383827820748940>"
            embed = nextcord.Embed(title="Sklep z ulepszeniami", description="Oto dostępne przedmioty w sklepie:", color=0x3498db)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Fish.png")
            for item_name, item_data in shop_items.items():
                item_id = item_data.get('ID', 'Brak ID')
                item_price = item_data.get('Price', 'Nie podano ceny')
                item_description = item_data.get('Description', 'Brak opisu')
                embed.add_field(name=f"{item_name} (ID: {item_id})", value=f"Cena: {item_price} <:Moneta:1165730228652494968>\nOpis: {item_description}", inline=False)

            view = FishShopUlepszenia()
            await Fishmsg.edit(embed=embed, view=view)

class FishShopWedkiENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="🎣 Fishing rods", style=nextcord.ButtonStyle.blurple, custom_id="wedkiENG", disabled=True)
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        await interaction.send("Nie działa :XDX:")

    @nextcord.ui.button(label="🔮 Upgrades", style=nextcord.ButtonStyle.blurple, custom_id="ulepszeniaENG")
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        shop_data = fish_collection.find_one({'_id': 'Info'})
        if shop_data and 'Shop' in shop_data:
            shop_items = shop_data['ShopUpgrades']
            star = "<:Star:1166383827820748940>"
            embed = nextcord.Embed(title="Upgrade Shop", description="Here are the available items in the store:", color=0x3498db)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Fish.png")
            for item_name, item_data in shop_items.items():
                item_id = item_data.get('ID', 'None ID')
                item_price = item_data.get('Price', 'None')
                item_description = item_data.get('Description', 'None')
                embed.add_field(name=f"{item_name} (ID: {item_id})", value=f"Price: {item_price} <:Moneta:1165730228652494968>\Description: {item_description}", inline=False)

            view = FishShopUlepszeniaENG()
            await Fishmsg.edit(embed=embed, view=view)

class FishShopUlepszenia(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="🎣 Wędki", style=nextcord.ButtonStyle.blurple, custom_id="wedki2")
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        shop_data = fish_collection.find_one({'_id': 'Info'})
        if shop_data and 'Shop' in shop_data:
            shop_items = shop_data['Shop']
            star = "<:Star:1166383827820748940>"
            embed = nextcord.Embed(title="Sklep z wędkami", description="Oto dostępne przedmioty w sklepie:", color=0x3498db)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Fish.png")
            embed.add_field(name=f"Drewniana wędka (ID: 0) {1 * star}", value=f"Cena: 0 <:Moneta:1165730228652494968>\nOpis: Podstawowa wędka", inline=False)
            for item_name, item_data in shop_items.items():
                item_id = item_data.get('ID', 'Brak ID')
                item_price = item_data.get('Price', 'Nie podano ceny')
                item_prestige = item_data.get('Prestige', '1')
                item_description = item_data.get('Description', 'Brak opisu')
                embed.add_field(name=f"{item_name} (ID: {item_id}) {item_prestige * star}", value=f"Cena: {item_price} <:Moneta:1165730228652494968>\nOpis: {item_description}", inline=False)
           
            view = FishShopWedki()
            await Fishmsg.edit(embed=embed, view=view)

    @nextcord.ui.button(label="🔮 Ulepszenia", style=nextcord.ButtonStyle.blurple, custom_id="ulepszenia2", disabled=True)
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        await interaction.send("Nie działa :XDX:")

class FishShopUlepszeniaENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="🎣 Fishing rods", style=nextcord.ButtonStyle.blurple, custom_id="wedki2ENG")
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        shop_data = fish_collection.find_one({'_id': 'Info'})
        if shop_data and 'Shop' in shop_data:
            shop_items = shop_data['Shop']
            star = "<:Star:1166383827820748940>"
            embed = nextcord.Embed(title="Fishing shop", description="Oto dostępne przedmioty w sklepie:", color=0x3498db)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Fish.png")
            embed.add_field(name=f"Wooden fishing rod (ID: 0) {1 * star}", value=f"Price: 0 <:Moneta:1165730228652494968>\nOpis: Basic fishing rod", inline=False)
            for item_name, item_data in shop_items.items():
                item_id = item_data.get('ID', 'None ID')
                item_price = item_data.get('Price', 'None')
                item_prestige = item_data.get('Prestige', '1')
                item_description = item_data.get('Description', 'None')
                embed.add_field(name=f"{item_name} (ID: {item_id}) {item_prestige * star}", value=f"Price: {item_price} <:Moneta:1165730228652494968>\Description: {item_description}", inline=False)
            view = FishShopWedkiENG()
            await Fishmsg.edit(embed=embed, view=view)

    @nextcord.ui.button(label="🔮 Upgrades", style=nextcord.ButtonStyle.blurple, custom_id="ulepszenia2ENG", disabled=True)
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        await interaction.send("Nie działa :XDX:")

class Premium(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="Zakup premium ⭐", style=nextcord.ButtonStyle.blurple, custom_id="premium")
    async def konfiguracja(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        await interaction.send("Aby zakupić premium należy:\n\n1. Wejdź na [naszego discorda](https://discord.gg/wwtXdvtyKG)\n2. Otwórz ticket\n3. napisz formę płatności i ID serwera", ephemeral=True)

class PremiumENG(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

    @nextcord.ui.button(label="Buy premium ⭐", style=nextcord.ButtonStyle.blurple, custom_id="premium")
    async def konfiguracja(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        await interaction.send("To purchase premium:\n\n1. Go to [our discord](https://discord.gg/wwtXdvtyKG)\n2. Open a ticket\n3. write the form of payment and server ID", ephemeral=True)

class AutoADJoin(nextcord.ui.View):
    def __init__(self, id):
        super().__init__(timeout=None)
        self.value = None
        self.id = id

    @nextcord.ui.button(label="✋ Dołącz", style=nextcord.ButtonStyle.green, custom_id="autoadjoin")
    async def button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        if self.id == None:
            await interaction.send("`[❌]:` Interakcja wygasła!", ephemeral=True)
            return
        
        target_guild = bot.get_guild(self.id)
        if target_guild:
            invite = await target_guild.text_channels[0].create_invite(max_age=10800, max_uses=1, unique=True, temporary=True, reason="AutoAD")
            if invite:
                await interaction.send(f"Aby dołączyć do tego serwera użyj poniższego linku!\n\n{invite}", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Wystąpił błąd!", ephemeral=True)
        else:
            await interaction.send("`[❌]:` Wystąpił błąd!", ephemeral=True)

class AutoADJoinENG(nextcord.ui.View):
    def __init__(self, id):
        super().__init__(timeout=None)
        self.value = None
        self.id = id

    @nextcord.ui.button(label="✋ Join", style=nextcord.ButtonStyle.green, custom_id="autoadjoinENG")
    async def button(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        self.value = False
        self.value = False
        if self.id == None:
            await interaction.send("`[❌]:` The interaction has expired!", ephemeral=True)
            return
        
        target_guild = bot.get_guild(self.id)
        if target_guild:
            invite = await target_guild.text_channels[0].create_invite(max_age=10800, max_uses=1, unique=True, temporary=True, reason="AutoAD")
            if invite:
                await interaction.send(f"To join this server use the link below!\n\n{invite}", ephemeral=True)
            else:
                await interaction.send("`[❌]:` An error occured!", ephemeral=True)
        else:
            await interaction.send("`[❌]:` An error occured!", ephemeral=True)

class Ruletka(nextcord.ui.View):
    def __init__(self, kwota, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.kwota = kwota
        self.user_id = user_id
        self.czerwone = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        self.czarne = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        self.zielone = 0

    @nextcord.ui.button(label="🔴 Czerwone", style=nextcord.ButtonStyle.red, custom_id="czerwone")
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/ruletka`!", ephemeral=True)
            return
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        server_id = str(interaction.guild.id)
        user_id = str(interaction.user.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        user_currency = currency_collection.find_one({"_id": server_id})
        win = False
        num = random.randint(0, 37) #+1 zielone 00
        if num in self.czerwone:
            kolor = "czerwone"
            win = True
        elif num in self.czarne:
            kolor = "czarne"
        elif num == 0 or num == 37:
            if num == 37:
                num = 00
            kolor = "zielone"

        if settings_document:
            if 'ruletkaCzerwone' in settings_document:
                ruletkaMnoznik = settings_document['ruletkaCzerwone']
            else:
                ruletkaMnoznik = 2
        else:
            ruletkaMnoznik = 2

        ruletkaMnoznik = ruletkaMnoznik - 1
        if win == True:
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] + self.kwota*ruletkaMnoznik
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota*ruletkaMnoznik}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota*ruletkaMnoznik})

            embed = nextcord.Embed(title="Ruletka 🎲", description=f"Wylosowałeś...", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
            time.sleep(2)

            embed = nextcord.Embed(title="Ruletka 🎲", description=f"Wylosowałeś **{kolor} {num}** i wygrałeś `{self.kwota*ruletkaMnoznik}`!", color=0x009000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
        else:
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] - self.kwota
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota})

            embed = nextcord.Embed(title="Ruletka 🎲", description=f"Wylosowałeś...", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
            time.sleep(2)

            embed = nextcord.Embed(title="Ruletka 🎲", description=f"Wylosowałeś **{kolor} {num}** i przegrałeś `{self.kwota}`!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)

    @nextcord.ui.button(label="⚫ Czarne", style=nextcord.ButtonStyle.grey, custom_id="szare")
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/ruletka`!", ephemeral=True)
            return
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        server_id = str(interaction.guild.id)
        user_id = str(interaction.user.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        user_currency = currency_collection.find_one({"_id": server_id})
        win = False
        num = random.randint(0, 37) #+1 zielone 00
        if num in self.czerwone:
            kolor = "czerwone"
        elif num in self.czarne:
            kolor = "czarne"
            win = True
        elif num == 0 or num == 37:
            if num == 37:
                num = 00
            kolor = "zielone"

        if settings_document:
            if 'ruletkaCzarne' in settings_document:
                ruletkaMnoznik = settings_document['ruletkaCzarne']
            else:
                ruletkaMnoznik = 2
        else:
            ruletkaMnoznik = 2

        ruletkaMnoznik = ruletkaMnoznik - 1
        if win == True:
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] + self.kwota*ruletkaMnoznik
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota*ruletkaMnoznik}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota*ruletkaMnoznik})

            embed = nextcord.Embed(title="Ruletka 🎲", description=f"Wylosowałeś...", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
            time.sleep(2)

            embed = nextcord.Embed(title="Ruletka 🎲", description=f"Wylosowałeś **{kolor} {num}** i wygrałeś `{self.kwota*ruletkaMnoznik}`!", color=0x009000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
        else:
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] - self.kwota
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota})
            
            embed = nextcord.Embed(title="Ruletka 🎲", description=f"Wylosowałeś...", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
            time.sleep(2)

            embed = nextcord.Embed(title="Ruletka 🎲", description=f"Wylosowałeś **{kolor} {num}** i przegrałeś `{self.kwota}`!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)

    @nextcord.ui.button(label="🟢 Zielone", style=nextcord.ButtonStyle.green, custom_id="zielone")
    async def button3(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/ruletka`!", ephemeral=True)
            return
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        server_id = str(interaction.guild.id)
        user_id = str(interaction.user.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        user_currency = currency_collection.find_one({"_id": server_id})
        win = False
        num = random.randint(0, 37) #+1 zielone 00
        if num in self.czerwone:
            kolor = "czerwone"
        elif num in self.czarne:
            kolor = "czarne"
        elif num == 0 or num == 37:
            if num == 37:
                num = 00
            kolor = "zielone"
            win = True

        if settings_document:
            if 'ruletkaZielone' in settings_document:
                ruletkaMnoznik = settings_document['ruletkaZielone']
            else:
                ruletkaMnoznik = 2
        else:
            ruletkaMnoznik = 2

        ruletkaMnoznik = ruletkaMnoznik - 1
        if win == True:
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] + self.kwota*ruletkaMnoznik
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota*ruletkaMnoznik}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota*ruletkaMnoznik})

            embed = nextcord.Embed(title="Ruletka 🎲", description=f"Wylosowałeś...", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
            time.sleep(2)

            embed = nextcord.Embed(title="Ruletka 🎲", description=f"Wylosowałeś **{kolor} {num}** i wygrałeś `{self.kwota*ruletkaMnoznik}`!", color=0x009000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
        else:
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] - self.kwota
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota})

            embed = nextcord.Embed(title="Ruletka 🎲", description=f"Wylosowałeś...", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
            time.sleep(2)

            embed = nextcord.Embed(title="Ruletka 🎲", description=f"Wylosowałeś **{kolor} {num}** i przegrałeś `{self.kwota}`!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)

class RuletkaENG(nextcord.ui.View):
    def __init__(self, kwota, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.kwota = kwota
        self.user_id = user_id
        self.czerwone = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
        self.czarne = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
        self.zielone = 0

    @nextcord.ui.button(label="🔴 Red", style=nextcord.ButtonStyle.red, custom_id="czerwoneENG")
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/ruletka`!", ephemeral=True)
            return
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        server_id = str(interaction.guild.id)
        user_id = str(interaction.user.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        user_currency = currency_collection.find_one({"_id": server_id})
        win = False
        num = random.randint(0, 37) #+1 zielone 00
        if num in self.czerwone:
            kolor = "czerwone"
            win = True
        elif num in self.czarne:
            kolor = "czarne"
        elif num == 0 or num == 37:
            if num == 37:
                num = 00
            kolor = "zielone"

        if settings_document:
            if 'ruletkaCzerwone' in settings_document:
                ruletkaMnoznik = settings_document['ruletkaCzerwone']
            else:
                ruletkaMnoznik = 2
        else:
            ruletkaMnoznik = 2

        ruletkaMnoznik = ruletkaMnoznik - 1
        if win == True:
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] + self.kwota*ruletkaMnoznik
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota*ruletkaMnoznik}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota*ruletkaMnoznik})

            embed = nextcord.Embed(title="Roulette 🎲", description=f"You drew...", color=0x009000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
            time.sleep(2)

            embed = nextcord.Embed(title="Roulette 🎲", description=f"You drew **{kolor} {num}** and won `{self.kwota*ruletkaMnoznik}`!", color=0x009000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
        else:
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] - self.kwota
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota})

            embed = nextcord.Embed(title="Roulette 🎲", description=f"You drew...", color=0x009000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
            time.sleep(2)

            embed = nextcord.Embed(title="Roulette 🎲", description=f"You drew **{kolor} {num}** and lost `{self.kwota}`!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)

    @nextcord.ui.button(label="⚫ Black", style=nextcord.ButtonStyle.grey, custom_id="szareENG")
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/ruletka`!", ephemeral=True)
            return
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        server_id = str(interaction.guild.id)
        user_id = str(interaction.user.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        user_currency = currency_collection.find_one({"_id": server_id})
        win = False
        num = random.randint(0, 37) #+1 zielone 00
        if num in self.czerwone:
            kolor = "czerwone"
        elif num in self.czarne:
            kolor = "czarne"
            win = True
        elif num == 0 or num == 37:
            if num == 37:
                num = 00
            kolor = "zielone"

        if settings_document:
            if 'ruletkaCzerwone' in settings_document:
                ruletkaMnoznik = settings_document['ruletkaCzerwone']
            else:
                ruletkaMnoznik = 2
        else:
            ruletkaMnoznik = 2

        ruletkaMnoznik = ruletkaMnoznik - 1
        if win == True:
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] + self.kwota*ruletkaMnoznik
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota*ruletkaMnoznik}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota*ruletkaMnoznik})

            embed = nextcord.Embed(title="Roulette 🎲", description=f"You drew...", color=0x009000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
            time.sleep(2)

            embed = nextcord.Embed(title="Roulette 🎲", description=f"You drew **{kolor} {num}** and won `{self.kwota*ruletkaMnoznik}`!", color=0x009000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
        else:
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] - self.kwota
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota})

            embed = nextcord.Embed(title="Roulette 🎲", description=f"You drew...", color=0x009000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
            time.sleep(2)

            embed = nextcord.Embed(title="Roulette 🎲", description=f"You drew **{kolor} {num}** and lost `{self.kwota}`!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)

    @nextcord.ui.button(label="🟢 Green", style=nextcord.ButtonStyle.green, custom_id="zieloneENG")
    async def button3(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/ruletka`!", ephemeral=True)
            return
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        server_id = str(interaction.guild.id)
        user_id = str(interaction.user.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        user_currency = currency_collection.find_one({"_id": server_id})
        win = False
        num = random.randint(0, 37) #+1 zielone 00
        if num in self.czerwone:
            kolor = "czerwone"
        elif num in self.czarne:
            kolor = "czarne"
        elif num == 0 or num == 37:
            if num == 37:
                num = 00
            kolor = "zielone"
            win = True

        if settings_document:
            if 'ruletkaCzerwone' in settings_document:
                ruletkaMnoznik = settings_document['ruletkaCzerwone']
            else:
                ruletkaMnoznik = 2
        else:
            ruletkaMnoznik = 2

        ruletkaMnoznik = ruletkaMnoznik - 1
        if win == True:
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] + self.kwota*ruletkaMnoznik
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota*ruletkaMnoznik}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota*ruletkaMnoznik})

            embed = nextcord.Embed(title="Roulette 🎲", description=f"You drew...", color=0x009000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
            time.sleep(2)

            embed = nextcord.Embed(title="Roulette 🎲", description=f"You drew **{kolor} {num}** and won `{self.kwota*ruletkaMnoznik}`!", color=0x009000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
        else:
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] - self.kwota
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota})

            embed = nextcord.Embed(title="Roulette 🎲", description=f"You drew...", color=0x009000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)
            time.sleep(2)

            embed = nextcord.Embed(title="Roulette 🎲", description=f"You drew **{kolor} {num}** and lost `{self.kwota}`!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            await ruletkamsg.edit(embed=embed, view=None)

class Blackjack(nextcord.ui.View):
    def __init__(self, karty, kwota, kartaG, kartaK, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.kwota = kwota
        self.karty = karty
        self.kartaG = kartaG
        self.kartaK = kartaK
        self.user_id = user_id

    @nextcord.ui.button(label="🃏 Hit", style=nextcord.ButtonStyle.green, custom_id="hit")
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/ruletka`!", ephemeral=True)
            return
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        server_id = str(interaction.guild.id)
        user_id = str(interaction.user.id)
        user_currency = currency_collection.find_one({"_id": server_id})

        if len(self.karty) < 2:
            embed = nextcord.Embed(title="Blackjack 🃏", description=f"Zabrakło kart w talii! Musisz przestać grać!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            view = Blackjack(self.karty, self.kwota, self.kartaG, self.kartaK, self.user_id)
            await blackjackmsg.edit(embed=embed, view=view)
            return

        kartaGN = random.choice(self.karty)
        self.karty.remove(kartaGN)
        kartaKN = random.choice(self.karty)
        self.karty.remove(kartaKN)

        razemG = self.kartaG + kartaGN
        razemK = self.kartaK + kartaKN

        if razemG > 21:
            embed = nextcord.Embed(title="Blackjack 🃏", description=f"Posiadasz więcej niż 21, przegrywasz!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            view = None
            await blackjackmsg.edit(embed=embed, view=view)
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] - self.kwota
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota})
            return

        embed = nextcord.Embed(title="Blackjack 🃏", description=f"Wylosowałeś kartę z wartością {kartaGN} (razem {razemG}), grasz dalej?", color=0xe40c0c)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
        embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
        view = Blackjack(self.karty, self.kwota, razemG, razemK, self.user_id)

        await blackjackmsg.edit(embed=embed, view=view)

    @nextcord.ui.button(label="🔴 Pass", style=nextcord.ButtonStyle.red, custom_id="pass")
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/ruletka`!", ephemeral=True)
            return
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        server_id = str(interaction.guild.id)
        user_id = str(interaction.user.id)
        user_currency = currency_collection.find_one({"_id": server_id})
        if self.kartaG > 21:
            embed = nextcord.Embed(title="Blackjack 🃏", description=f"Posiadasz więcej niż 21, przegrywasz!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] - self.kwota
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota})

        elif self.kartaK > 21:
            embed = nextcord.Embed(title="Blackjack 🃏", description=f"Krupier posiada więcej niż 21, wygrywasz!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] + self.kwota
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota})
            
        elif self.kartaG > self.kartaK:
            embed = nextcord.Embed(title="Blackjack 🃏", description=f"Posiadasz {self.kartaG}, a krupier {self.kartaK}, wygrywasz!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] + self.kwota
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota})

        elif self.kartaG < self.kartaK:
            embed = nextcord.Embed(title="Blackjack 🃏", description=f"Posiadasz {self.kartaG}, a krupier {self.kartaK}, przegrywasz!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] - self.kwota
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota})

        else:
            embed = nextcord.Embed(title="Blackjack 🃏", description=f"Posiadasz {self.kartaG}, a krupier {self.kartaK}, remis!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
        
        view = None
        await blackjackmsg.edit(embed=embed, view=view)

class BlackjackENG(nextcord.ui.View):
    def __init__(self, karty, kwota, kartaG, kartaK, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.kwota = kwota
        self.karty = karty
        self.kartaG = kartaG
        self.kartaK = kartaK
        self.user_id = user_id

    @nextcord.ui.button(label="🃏 Hit", style=nextcord.ButtonStyle.green, custom_id="hit")
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/roulette`!", ephemeral=True)
            return
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        server_id = str(interaction.guild.id)
        user_id = str(interaction.user.id)
        user_currency = currency_collection.find_one({"_id": server_id})

        if len(self.karty) < 2:
            embed = nextcord.Embed(title="Blackjack 🃏", description=f"There are no cards left in the deck! You have to stop playing!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            view = Blackjack(self.karty, self.kwota, self.kartaG, self.kartaK, self.user_id)
            await blackjackmsg.edit(embed=embed, view=view)
            return

        kartaGN = random.choice(self.karty)
        self.karty.remove(kartaGN)
        kartaKN = random.choice(self.karty)
        self.karty.remove(kartaKN)

        razemG = self.kartaG + kartaGN
        razemK = self.kartaK + kartaKN

        if razemG > 21:
            embed = nextcord.Embed(title="Blackjack 🃏", description=f"You have more than 21, you lose!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            view = None
            await blackjackmsg.edit(embed=embed, view=view)
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] - self.kwota
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota})
            return

        embed = nextcord.Embed(title="Blackjack 🃏", description=f"You have drawn a card with the value {kartaGN} (together {razemG}), do you continue playing?", color=0xe40c0c)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
        embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
        view = Blackjack(self.karty, self.kwota, razemG, razemK, self.user_id)

        await blackjackmsg.edit(embed=embed, view=view)

    @nextcord.ui.button(label="🔴 Pass", style=nextcord.ButtonStyle.red, custom_id="pass")
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/roulette`!", ephemeral=True)
            return
        
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        server_id = str(interaction.guild.id)
        user_id = str(interaction.user.id)
        user_currency = currency_collection.find_one({"_id": server_id})
        if self.kartaG > 21:
            embed = nextcord.Embed(title="Blackjack 🃏", description=f"You have more than 21, you lose!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] - self.kwota
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota})

        elif self.kartaK > 21:
            embed = nextcord.Embed(title="Blackjack 🃏", description=f"The dealer has more than 21, you win!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] + self.kwota
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota})
            
        elif self.kartaG > self.kartaK:
            embed = nextcord.Embed(title="Blackjack 🃏", description=f"You have {self.kartaG} and the dealer has {self.kartaK}, you win!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] + self.kwota
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota})

        elif self.kartaG < self.kartaK:
            embed = nextcord.Embed(title="Blackjack 🃏", description=f"You have {self.kartaG} and the dealer has {self.kartaK}, you lose!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
            if user_currency:
                if user_id in user_currency:
                    new_currency = user_currency[str(interaction.user.id)] - self.kwota
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                else:
                    currency_collection.update_one({"_id": server_id}, {"$set": {user_id: self.kwota}})
            else:
                currency_collection.insert_one({"_id": server_id, user_id: self.kwota})

        else:
            embed = nextcord.Embed(title="Blackjack 🃏", description=f"You have {self.kartaG} and the dealer has {self.kartaK}, tie!", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
            embed.set_footer(text=f"Invoked by {interaction.user} | {current_time}")
        
        view = None
        await blackjackmsg.edit(embed=embed, view=view)

class DreamShield(nextcord.ui.Select):
    def __init__(self, user_id):
        self.user_id = user_id
        options=[
            nextcord.SelectOption(label="AntyLink", description="Wyświetla konfigurację blokowania linków", emoji="🔗"),
            nextcord.SelectOption(label="AntyMention", description="Wyświetla konfigurację blokowania @oznaczeń", emoji="👤"),
            nextcord.SelectOption(label="AntyCaps", description="Wyświetla konfigurację blokowania nadmiernego capsa", emoji="🔠"),
            nextcord.SelectOption(label="AntyFlood", description="Wyświetla konfigurację blokowania zaśmiecania czatu", emoji="🔥")
        ]
        super().__init__(placeholder="Wybierz funkcję!", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        if self.values[0] == "AntyLink":
            author = interaction.user
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed=nextcord.Embed(title="🔗 AntyLink", description="Blokuje wszystkie linki wysyłane przez użytkowników!", color=0x008000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            view = AntyLink(self.user_id)
            await antyshieldmsg.edit(embed=embed, view=view)

        elif self.values[0] == "AntyMention":
            author = interaction.user
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed=nextcord.Embed(title="👤 AntyMention", description="Blokuje oznaczanie użytkowników przez innych!", color=0x008000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            view = AntyMention(self.user_id)
            await antyshieldmsg.edit(embed=embed, view=view)

        elif self.values[0] == "AntyCaps":
            author = interaction.user
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed=nextcord.Embed(title="🔠 AntyCaps", description="Blokuje nadmierne używanie dużych liter!", color=0x008000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            view = AntyCaps(self.user_id)
            await antyshieldmsg.edit(embed=embed, view=view)

        elif self.values[0] == "AntyFlood":
            author = interaction.user
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed=nextcord.Embed(title="🔠 AntyFlood", description="Wyświetla konfigurację blokowania zaśmiecania czatu!", color=0x008000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            view = AntyFlood(self.user_id)
            await antyshieldmsg.edit(embed=embed, view=view)

class DreamShieldView(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.add_item(DreamShield(user_id))

class AntyLink(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label="<- Wróć", style=nextcord.ButtonStyle.red, custom_id="backantylinki")
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        author = interaction.user
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        embed=nextcord.Embed(title="🛡 DreamShield", description="DreamShield jest systemem Anty-Raid", color=0x008000)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        view = DreamShieldView(author.id)
        global antyshieldmsg
        await antyshieldmsg.edit(embed=embed, view=view)

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz antylink", style=nextcord.ButtonStyle.green, custom_id="offantylink")
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        server_id = str(interaction.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        if interaction.user.guild_permissions.manage_messages:
            server_id = str(interaction.guild.id)

            settings_document = settings_collection.find_one({'_id': server_id})

            if settings_document:
                current_status = settings_document.get("antyLink", False)
                new_status = not current_status

                settings_collection.update_one({'_id': server_id}, {'$set': {'antyLink': new_status}})
            else:
                new_status = True
                settings_document = {'_id': server_id, 'antyLink': new_status}
                settings_collection.insert_one(settings_document)

            status_text = "włączona" if new_status else "wyłączona"
            await interaction.send(f"`[✅]:` Funkcja `antyLink` została {status_text} dla tego serwera.", ephemeral=True)
        else:
            await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `antyLink`!", ephemeral=True)

class AntyMention(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label="<- Wróć", style=nextcord.ButtonStyle.red, custom_id="backantymention")
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        author = interaction.user
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        embed=nextcord.Embed(title="🛡 DreamShield", description="DreamShield jest systemem Anty-Raid", color=0x008000)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        view = DreamShieldView(author.id)
        await antyshieldmsg.edit(embed=embed, view=view)

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz antymention", style=nextcord.ButtonStyle.green, custom_id="offantymention")
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        server_id = str(interaction.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        if interaction.user.guild_permissions.manage_messages:
            server_id = str(interaction.guild.id)

            settings_document = settings_collection.find_one({'_id': server_id})

            if settings_document:
                current_status = settings_document.get("antyMention", False)
                new_status = not current_status

                settings_collection.update_one({'_id': server_id}, {'$set': {'antyMention': new_status}})
            else:
                new_status = True
                settings_document = {'_id': server_id, 'antyMention': new_status}
                settings_collection.insert_one(settings_document)

            status_text = "włączona" if new_status else "wyłączona"
            await interaction.send(f"`[✅]:` Funkcja `antyMention` została {status_text} dla tego serwera.", ephemeral=True)
        else:
            await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `antyMention`!", ephemeral=True)

class AntyCaps(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label="<- Wróć", style=nextcord.ButtonStyle.red, custom_id="backantycaps")
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        author = interaction.user
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        embed=nextcord.Embed(title="🛡 DreamShield", description="DreamShield jest systemem Anty-Raid", color=0x008000)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        view = DreamShieldView(author.id)
        global antyshieldmsg
        await antyshieldmsg.edit(embed=embed, view=view)

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz antycaps", style=nextcord.ButtonStyle.green, custom_id="offantycaps")
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        server_id = str(interaction.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        if interaction.user.guild_permissions.manage_messages:
            server_id = str(interaction.guild.id)

            settings_document = settings_collection.find_one({'_id': server_id})

            if settings_document:
                current_status = settings_document.get("antyCaps", False)
                new_status = not current_status

                settings_collection.update_one({'_id': server_id}, {'$set': {'antyCaps': new_status}})
            else:
                new_status = True
                settings_document = {'_id': server_id, 'antyCaps': new_status}
                settings_collection.insert_one(settings_document)

            status_text = "włączona" if new_status else "wyłączona"
            await interaction.send(f"`[✅]:` Funkcja `antyCaps` została {status_text} dla tego serwera.", ephemeral=True)
        else:
            await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `antyCaps`!", ephemeral=True)

class AntyFlood(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label="<- Wróć", style=nextcord.ButtonStyle.red, custom_id="backantyflood")
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        author = interaction.user
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        embed=nextcord.Embed(title="🛡 DreamShield", description="DreamShield jest systemem Anty-Raid", color=0x008000)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        view = DreamShieldView(author.id)
        global antyshieldmsg
        await antyshieldmsg.edit(embed=embed, view=view)

    @nextcord.ui.button(label="❌ Wyłącz / ✅ Włącz antyflood", style=nextcord.ButtonStyle.green, custom_id="offantyflood")
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` Ta interakcja należy do kogoś innego! Użyj `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        server_id = str(interaction.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        if interaction.user.guild_permissions.manage_messages:
            server_id = str(interaction.guild.id)

            settings_document = settings_collection.find_one({'_id': server_id})

            if settings_document:
                current_status = settings_document.get("antyFlood", False)
                new_status = not current_status

                settings_collection.update_one({'_id': server_id}, {'$set': {'antyFlood': new_status}})
            else:
                new_status = True
                settings_document = {'_id': server_id, 'antyFlood': new_status}
                settings_collection.insert_one(settings_document)

            status_text = "włączona" if new_status else "wyłączona"
            await interaction.send(f"`[✅]:` Funkcja `antyFlood` została {status_text} dla tego serwera.", ephemeral=True)
        else:
            await interaction.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `antyFlood`!", ephemeral=True)

class DreamShieldENG(nextcord.ui.Select):
    def __init__(self, user_id):
        self.user_id = user_id
        options=[
            nextcord.SelectOption(label="AntyLink", description="Displays the link blocking configuration", emoji="🔗"),
            nextcord.SelectOption(label="AntyMention", description="Displays the @tag blocking configuration", emoji="👤"),
            nextcord.SelectOption(label="AntyCaps", description="Displays the configuration for blocking excessive use of caps", emoji="🔠"),
            nextcord.SelectOption(label="AntyFlood", description="Displays the chat clutter blocking configuration", emoji="🔥")
        ]
        super().__init__(placeholder="Wybierz funkcję!", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        if self.values[0] == "AntyLink":
            author = interaction.user
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed=nextcord.Embed(title="🔗 AntyLink", description="Blocks all links sent by users!", color=0x008000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            view = AntyLinkENG(self.user_id)
            await antyshieldmsg.edit(embed=embed, view=view)

        elif self.values[0] == "AntyMention":
            author = interaction.user
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed=nextcord.Embed(title="👤 AntyMention", description="Blocks users from being tagged by others!", color=0x008000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            view = AntyMentionENG(self.user_id)
            await antyshieldmsg.edit(embed=embed, view=view)

        elif self.values[0] == "AntyCaps":
            author = interaction.user
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed=nextcord.Embed(title="🔠 AntyCaps", description="Blocks excessive use of capital letters!", color=0x008000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            view = AntyCapsENG(self.user_id)
            await antyshieldmsg.edit(embed=embed, view=view)

        elif self.values[0] == "AntyFlood":
            author = interaction.user
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            embed=nextcord.Embed(title="🔠 AntyFlood", description="Displays chat clutter blocking configuration!", color=0x008000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            view = AntyFloodENG(self.user_id)
            await antyshieldmsg.edit(embed=embed, view=view)

class DreamShieldViewENG(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.add_item(DreamShieldENG(user_id))

class AntyLinkENG(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label="<- Wróć", style=nextcord.ButtonStyle.red, custom_id="backantylinkiENG")
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        author = interaction.user
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        embed=nextcord.Embed(title="🛡 DreamShield", description="DreamShield is an Anti-Raid system", color=0x008000)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        view = DreamShieldViewENG(author.id)
        global antyshieldmsg
        await antyshieldmsg.edit(embed=embed, view=view)

    @nextcord.ui.button(label="❌ Turn on / ✅ Turn off antylink", style=nextcord.ButtonStyle.green, custom_id="offantylinkENG")
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        server_id = str(interaction.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        if interaction.user.guild_permissions.manage_messages:
            server_id = str(interaction.guild.id)

            settings_document = settings_collection.find_one({'_id': server_id})

            if settings_document:
                current_status = settings_document.get("antyLink", False)
                new_status = not current_status

                settings_collection.update_one({'_id': server_id}, {'$set': {'antyLink': new_status}})
            else:
                new_status = True
                settings_document = {'_id': server_id, 'antyLink': new_status}
                settings_collection.insert_one(settings_document)

            status_text = "turned on" if new_status else "turned off"
            await interaction.send(f"`[✅]:` The `antiLink` function has been {status_text} for this server.", ephemeral=True)
        else:
            await interaction.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `antiLink`!", ephemeral=True)

class AntyMentionENG(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label="<- Wróć", style=nextcord.ButtonStyle.red, custom_id="backantymentionENG")
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        author = interaction.user
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        embed=nextcord.Embed(title="🛡 DreamShield", description="DreamShield is an Anti-Raid system", color=0x008000)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        view = DreamShieldViewENG(author.id)
        await antyshieldmsg.edit(embed=embed, view=view)

    @nextcord.ui.button(label="❌ Turn on / ✅ Turn off antymention", style=nextcord.ButtonStyle.green, custom_id="offantymentionENG")
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        server_id = str(interaction.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        if interaction.user.guild_permissions.manage_messages:
            server_id = str(interaction.guild.id)

            settings_document = settings_collection.find_one({'_id': server_id})

            if settings_document:
                current_status = settings_document.get("antyMention", False)
                new_status = not current_status

                settings_collection.update_one({'_id': server_id}, {'$set': {'antyMention': new_status}})
            else:
                new_status = True
                settings_document = {'_id': server_id, 'antyMention': new_status}
                settings_collection.insert_one(settings_document)

            status_text = "turned on" if new_status else "turned off"
            await interaction.send(f"`[✅]:` The `antiMention` function has been {status_text} for this server.", ephemeral=True)
        else:
            await interaction.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `antiMention`!", ephemeral=True)

class AntyCapsENG(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label="<- Wróć", style=nextcord.ButtonStyle.red, custom_id="backantycapsENG")
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        author = interaction.user
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        embed=nextcord.Embed(title="🛡 DreamShield", description="DreamShield is an Anti-Raid system", color=0x008000)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        view = DreamShieldViewENG(author.id)
        await antyshieldmsg.edit(embed=embed, view=view)

    @nextcord.ui.button(label="❌ Turn on / ✅ Turn off antycaps", style=nextcord.ButtonStyle.green, custom_id="offantycapsENG")
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        server_id = str(interaction.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        if interaction.user.guild_permissions.manage_messages:
            server_id = str(interaction.guild.id)

            settings_document = settings_collection.find_one({'_id': server_id})

            if settings_document:
                current_status = settings_document.get("antyCaps", False)
                new_status = not current_status

                settings_collection.update_one({'_id': server_id}, {'$set': {'antyCaps': new_status}})
            else:
                new_status = True
                settings_document = {'_id': server_id, 'antyCaps': new_status}
                settings_collection.insert_one(settings_document)

            status_text = "turned on" if new_status else "turned off"
            await interaction.send(f"`[✅]:` The `antyCaps` function has been {status_text} for this server.", ephemeral=True)
        else:
            await interaction.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `antyCaps`!", ephemeral=True)

class AntyFloodENG(nextcord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.value = None
        self.user_id = user_id

    @nextcord.ui.button(label="<- Wróć", style=nextcord.ButtonStyle.red, custom_id="backantyfloodENG")
    async def button2(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        author = interaction.user
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        embed=nextcord.Embed(title="🛡 DreamShield", description="DreamShield is an Anti-Raid system", color=0x008000)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        view = DreamShieldViewENG(author.id)
        await antyshieldmsg.edit(embed=embed, view=view)

    @nextcord.ui.button(label="❌ Turn on / ✅ Turn off antycaps", style=nextcord.ButtonStyle.green, custom_id="offantyfloodENG")
    async def button1(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not self.user_id == interaction.user.id:
            await interaction.send(f"`[❌]:` This interaction belongs to someone else! Use `/settingsconfig dreamshield`!", ephemeral=True)
            return
        
        server_id = str(interaction.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        if interaction.user.guild_permissions.manage_messages:
            server_id = str(interaction.guild.id)

            settings_document = settings_collection.find_one({'_id': server_id})

            if settings_document:
                current_status = settings_document.get("antyFlood", False)
                new_status = not current_status

                settings_collection.update_one({'_id': server_id}, {'$set': {'antyFlood': new_status}})
            else:
                new_status = True
                settings_document = {'_id': server_id, 'antyFlood': new_status}
                settings_collection.insert_one(settings_document)

            status_text = "turned on" if new_status else "turned off"
            await interaction.send(f"`[✅]:` The `antyFlood` function has been {status_text} for this server.", ephemeral=True)
        else:
            await interaction.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `antyFlood`!", ephemeral=True)

async def log_role_event(description, kanalLogi, current_time, color, after2, link):
    embed = nextcord.Embed(description=description, color=color)
    
    user = after2
    if user.avatar:
        avatar_url = user.avatar.url
    else:
        avatar_url = no_avatar

    if link == None:
        link = "https://dreambot.pl/DreamBotImages/NoLogoDC.png"
    
    embed.set_author(name=user.display_name, icon_url=avatar_url)
    embed.set_thumbnail(url=link)
    embed.set_footer(text=f"{current_time}")
    
    channel = await bot.fetch_channel(kanalLogi)
    await channel.send(embed=embed)

def parse_duration(duration_str):
    duration_pattern = re.compile(r'(\d+)([mshd])')

    unit_map = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'y': 31536000}

    total_seconds = 0
    matches = duration_pattern.findall(duration_str)
    for match in matches:
        amount, unit = match
        if unit == 'd':
            total_seconds += int(amount) * 86400
        else:
            total_seconds += int(amount) * unit_map[unit]
    
    return total_seconds

def get_available_fonts():
    font_dir = "Fonts/"
    available_fonts = [os.path.join(font_dir, file) for file in os.listdir(font_dir) if file.endswith(".ttf")]
    return available_fonts

def generate_random_text(length):
    characters = string.ascii_letters.replace('g', 'N').replace('o', 'X').replace('c', 'H').replace('s', 'N').replace('z', 'X').replace('a', 'H').replace('w', 'H').replace('u', 'H').replace('G', 'N').replace('O', 'X').replace('C', 'H').replace('S', 'N').replace('Z', 'X').replace('W', 'H').replace('U', 'H').replace('0', 'E').replace('e', 'K').replace('q', 'N').replace('Q', 'N') + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

async def get_random_memePL():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.reddit.com/r/PolandMemes/random.json") as response:
            data = await response.json()
            meme_url = data[0]["data"]["children"][0]["data"]["url"]
            meme_title = data[0]["data"]["children"][0]["data"]["title"]
            return meme_url, meme_title
        
async def get_random_memeENG():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.reddit.com/r/memes/random.json") as response:
            data = await response.json()
            meme_url = data[0]["data"]["children"][0]["data"]["url"]
            meme_title = data[0]["data"]["children"][0]["data"]["title"]
            return meme_url, meme_title

def check_settings(guild_id):
    with open('settings.json', 'r') as file:
        settings_data = json.load(file)
    if str(guild_id) in settings_data:
        return settings_data[str(guild_id)]
    else:
        return None

def load_ai_data():
    try:
        with open('ai_data.json', 'r') as file:
            ai_data = json.load(file)
        return ai_data
    except FileNotFoundError:
        return {}
    
def save_statistics(statistics):
    with open('statystyki.json', 'w') as file:
        json.dump(statistics, file, indent=4)

def load_statistics():
    try:
        with open('statystyki.json', 'r') as file:
            statistics = json.load(file)
    except FileNotFoundError:
        statistics = {}
    return statistics

def get_status_text(status):
        return "on" if status else "off"

def contains_link(content):
    parsed = urlparse(content)
    return bool(parsed.scheme) and bool(parsed.netloc)

@app.route('/status')
def get_status():
    status_data = {
    'status': 'online',
    }

    return jsonify(status_data)

def run_flask():
    app.run(port=5000)

async def check_and_draw_winners():
    current_time = datetime.datetime.now()
    for giveaway_data in guilds_collection.find({'giveaways': {'$exists': True, '$ne': []}}):
        server_id = giveaway_data["_id"]
        settings_document = settings_collection.find_one({'_id': server_id})
        if settings_document:
            if 'language' in settings_document:
                lang = settings_document['language']
            else:
                lang = "PL"
        else:
            lang = "PL"

        for giveaway in giveaway_data.get('giveaways', []):
            channel_id = giveaway.get("channel_id")
            message_id = giveaway.get("message_id")
            giveaway_id = giveaway.get("id")
            prize = giveaway.get("prize")
            end_time = giveaway.get("end_time")
            ended = giveaway.get("ended")
            winners_count = giveaway.get("winners", 1)

            if current_time >= end_time and not ended:
                try:
                    channel = bot.get_channel(int(channel_id))
                    message = await channel.fetch_message(int(message_id))
                    reactions = message.reactions
                except Exception:
                    continue

                if reactions:
                    users = []
                    while len(users) < winners_count:
                        winning_reaction = random.choice(reactions)
                        users.extend(await winning_reaction.users().flatten())

                    non_bot_users = [user for user in set(users) if not user.bot]

                    if non_bot_users:
                        winners = random.sample(non_bot_users, min(winners_count, len(non_bot_users)))
                    else:
                        winners = []
                else:
                    winners = []

                if lang == "PL":
                    if winners:
                        winners_mentions = ', '.join(winner.mention for winner in winners)
                        embed = nextcord.Embed(
                            title="🎉 Giveaway się zakończył!",
                            description=f"Nagroda: **{prize}**\nWygrani: **{winners_mentions}**\n\nSkończył się **<t:{int(end_time.timestamp())}:R>**",
                            color=0x00ff00
                        )
                        embed.set_footer(text=f"ID: {giveaway_id}")
                        await message.reply(f"🎉 Giveaway na **{prize}** się zakończył! Gratulacje dla {winners_mentions}!")
                    else:
                        await message.reply(f"🎉 Giveaway na **{prize}** się zakończył! Niestety nikt nie dołączył. 😢")

                elif lang == "ENG":
                    if winners:
                        winners_mentions = ', '.join(winner.mention for winner in winners)
                        embed = nextcord.Embed(
                            title="🎉 Giveaway has ended!",
                            description=f"Prize: **{prize}**\nWinners: **{winners_mentions}**\n\nIt ended **<t:{int(end_time.timestamp())}:R>**",
                            color=0x00ff00
                        )
                        embed.set_footer(text=f"ID: {giveaway_id}")
                        await message.reply(f"🎉 Giveaway for **{prize}** has ended! Congratulations to {winners_mentions}!")
                    else:
                        await message.reply(f"🎉 Giveaway for **{prize}** has ended! No one entered the giveaway. 😢")

                embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Konfetti.png")
                msg = await channel.fetch_message(int(message_id))
                await msg.edit(embed=embed)

                guilds_collection.update_one(
                    {"_id": server_id, "giveaways.message_id": message_id},
                    {"$set": {"giveaways.$.ended": True}}
                )

async def check_and_draw_winners_loop():
    while True:
        await check_and_draw_winners()
        await asyncio.sleep(60)

async def send_autoad_to_random_server():
    try:
        global server_iterator
        random_server_id = str(next(server_iterator))
        server = settings_collection.find_one({'_id': random_server_id})

        if server:
            server_id = server['_id']
            turned_on = server.get('autoad')
            advert = server.get('autoAdReklama')
            premium = server.get('premium')
            embedDB = server.get('autoAdEmbed')

            if advert and turned_on:
                all_servers = settings_collection.find()
                for server in all_servers:
                    auto_ad_channel_id = server.get('kanalAutoReklam')
                    turned_on2 = server.get('autoad')
                    if auto_ad_channel_id and turned_on2:
                        channel = bot.get_channel(auto_ad_channel_id)
                        if channel:
                            reklama_text = advert.replace(r'\n', '\n')
                            typ = "Normal Server (NS)"
                            if server_id == "1141830471903359047":
                                typ = "Bot Support Server (BSS)"
                            elif premium == True:
                                typ = "Premium Server (PS)"
                                
                            lang = server.get('language')
                            if lang == None:
                                lang = "PL"

                            guild = bot.get_guild(int(server_id))
                            if lang == "PL":
                                text = f"*ID:* `{server_id}`\n*Typ:* `{typ}`\n\n{reklama_text}"
                                if premium == True and embedDB == True:
                                    embed = nextcord.Embed(description=text, color=0xffe600)
                                    if guild:
                                        thumbnail_url = guild.icon.url if guild.icon else bot.user.avatar.url
                                        embed.set_thumbnail(url=thumbnail_url)
                                    
                                    view = AutoADJoin(id=int(server_id))
                                    await channel.send(embed=embed, view=view)
                                else:
                                    await channel.send(text)

                            elif lang == "ENG":
                                text = f"*ID:* `{server_id}`\n*Type:* `{typ}`\n\n{reklama_text}"
                                if premium == True:
                                    embed = nextcord.Embed(description=text, color=0xffe600)
                                    if guild:
                                        thumbnail_url = guild.icon.url if guild.icon else bot.user.avatar.url
                                        embed.set_thumbnail(url=thumbnail_url)
                                    
                                    view = AutoADJoinENG(id=int(server_id))
                                    await channel.send(embed=embed)
                                else:
                                    await channel.send(text)

                            turned_on2 = None
            else:
                await send_autoad_to_random_server()
                
    except StopIteration:
        server_iterator = iter(all_server_ids)

async def AutomatyczneReklamy():
    while True:
        await send_autoad_to_random_server()
        await asyncio.sleep(150)

async def Desc():
    statistics_document = website_collection.find_one({'_id': 'statistics'})
    if statistics_document:
        total_users = statistics_document.get('users', 0)

    total_users = total_users // 1000
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"{len(bot.guilds)} serwerów!"))
    await asyncio.sleep(8)
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"{total_users}k użytkowników!"))

async def DescLoop():
    while True:
        await Desc()
        await asyncio.sleep(8)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.datetime, )):
            return o.isoformat()
        return super().default(o)

#On_ready
@bot.event
async def on_ready():
    print(" ")
    time.sleep(0.4)
    if DEV == True:
        print(f">>> Pomyślnie zalogowano na konto DEV DreamBot'a!")
    else:
        print(f">>> Pomyślnie zalogowano na konto DreamBot'a!")
        
    bot.add_view(Otwieranie_ticketu())
    bot.add_view(Otwieranie_ticketuENG())
    bot.add_view(Zamykanie_ticketu(user=None))
    bot.add_view(Zamykanie_ticketuENG(user=None))
    bot.add_view(Wylaczanie_Wlaczanie_ankiet())
    bot.add_view(Wylaczanie_Wlaczanie_ankietENG())
    bot.add_view(Wylaczanie_Wlaczanie_ticketow())
    bot.add_view(Wylaczanie_Wlaczanie_ticketowENG())
    bot.add_view(Wylaczanie_Wlaczanie_partnerstw())
    bot.add_view(Wylaczanie_Wlaczanie_partnerstwENG())
    bot.add_view(Wylaczanie_Wlaczanie_globalchatu())
    bot.add_view(Wylaczanie_Wlaczanie_globalchatuENG())
    bot.add_view(Wylaczanie_Wlaczanie_weryfikacji())
    bot.add_view(Wylaczanie_Wlaczanie_weryfikacjiENG())
    bot.add_view(Weryfikacja())
    bot.add_view(WeryfikacjaENG())
    bot.add_view(Zgadywanka_wybor(user_id=None))
    bot.add_view(Zgadywanka_wyborENG(user_id=None))
    bot.add_view(Zgadywanka_liczba(user_id=None))
    bot.add_view(Zgadywanka_liczbaENG(user_id=None))
    bot.add_view(Zgadywanka_ponownie(user_id=None))
    bot.add_view(Zgadywanka_ponownieENG(user_id=None))
    bot.add_view(Zgadywanka_ponownie2(user_id=None))
    bot.add_view(Zgadywanka_ponownie2ENG(user_id=None))
    bot.add_view(Help())
    bot.add_view(HelpENG())
    bot.add_view(Wylaczanie_Wlaczanie_liczenia())
    bot.add_view(Wylaczanie_Wlaczanie_liczeniaENG())
    bot.add_view(Wylaczanie_Wlaczanie_litera())
    bot.add_view(Wylaczanie_Wlaczanie_literaENG())
    bot.add_view(Wylaczanie_Wlaczanie_powitan())
    bot.add_view(Wylaczanie_Wlaczanie_powitanENG())
    bot.add_view(Wylaczanie_Wlaczanie_pozegnan())
    bot.add_view(Wylaczanie_Wlaczanie_pozegnanENG())
    bot.add_view(Wylaczanie_Wlaczanie_ekonomii())
    bot.add_view(Wylaczanie_Wlaczanie_ekonomiiENG())
    bot.add_view(SelfRole())
    bot.add_view(SelfRoleENG())
    bot.add_view(OwnerInfo())
    bot.add_view(FishShopWedki())
    bot.add_view(FishShopUlepszenia())
    bot.add_view(Wylaczanie_Wlaczanie_selfchannel())
    bot.add_view(Wylaczanie_Wlaczanie_selfchannelENG())
    bot.add_view(Premium())
    bot.add_view(AutoADJoin(id=None))
    bot.add_view(AutoADJoinENG(id=None))
    bot.add_view(Zamykanie_ticketu2(user=None))
    bot.add_view(Zamykanie_ticketu2ENG(user=None))
    for guild in bot.guilds:
        guild_id = guild.id
        bot.add_view(YourCustomTicketView(guild_id))
    time.sleep(0.4)
    print(f">>> Pomyślnie załdowano przyciski!")
    time.sleep(0.4)
    if DEV == False:
        bot.loop.create_task(AutomatyczneReklamy())
        print(f">>> Pomyślnie włączono automatyczne reklamy!")
        time.sleep(0.4)
        bot.loop.create_task(check_and_draw_winners_loop())
        print(f">>> Pomyślnie załdowano giveaway'e!")
        time.sleep(0.4)
        threading.Thread(target=run_flask).start()

        #Kopia zapasowa bazy danych
        main_collections = db.list_collection_names()
        info_collections = dbInfo.list_collection_names()
        for collection_name in main_collections:
            main_collection = db[collection_name]
            documents = list(main_collection.find())
            backup_path = os.path.join(backup_folder, f'{collection_name}_Main.json')
            with open(backup_path, 'w', encoding='utf-8') as file:
                json.dump(documents, file, ensure_ascii=False, indent=2, cls=CustomJSONEncoder)

        for collection_name in info_collections:
            info_collection = dbInfo[collection_name]
            documents = list(info_collection.find())
            backup_path = os.path.join(backup_folder, f'{collection_name}_Info.json')
            with open(backup_path, 'w', encoding='utf-8') as file:
                json.dump(documents, file, ensure_ascii=False, indent=2, cls=CustomJSONEncoder)

    for guild in bot.guilds:
        settings_document = settings_collection.find_one({'_id': str(guild.id)})
        if settings_document and 'kanalRadia' in settings_document and settings_document.get('premium', False):
            kanal_id = settings_document['kanalRadia']
            kanal = guild.get_channel(kanal_id)
            
            if kanal and isinstance(kanal, nextcord.VoiceChannel):
                try:
                    voice_channel = await kanal.connect()
                    await voice_channel.guild.change_voice_state(channel=kanal, self_deaf=True)
                    voice_channel.play(nextcord.FFmpegPCMAudio(settings_document['stacjaRadia']))
                except Exception:
                    continue

    print(f">>> Bot jest na {len(bot.guilds)} serwerach!")
    time.sleep(0.4)
    print(" ")
    bot.loop.create_task(DescLoop())

#Powiadomienie - dodanie
@bot.event
async def on_guild_join(guild):
    server_id = str(guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document and settings_document.get("globalBan", False):
        server = bot.get_guild(guild.id)
        await server.leave()
        return
    
    #Statystyki
    statistics_document = website_collection.find_one({'_id': 'statistics'})
    users_count = sum(guild.member_count for guild in bot.guilds)
    servers_count = len(bot.guilds)
    channels_count = sum(len(guild.channels) for guild in bot.guilds)
    statistics_document['users'] = users_count
    statistics_document['servers'] = servers_count
    statistics_document['channels'] = channels_count

    website_collection.update_one({'_id': 'statistics'}, {'$set': statistics_document}, upsert=True)

    if guild.owner:
        owner_id = str(guild.owner)
        guild_id = str(guild.id)
        settings_document = settings_collection.find_one({'_id': guild_id})
        if not settings_document:
            settings_document = {'_id': guild_id}
            settings_document['owner'] = owner_id
            settings_collection.update_one({'_id': guild_id}, {'$set': settings_document}, upsert=True)

        elif 'owner' not in settings_document:
            settings_document['owner'] = owner_id
            settings_collection.update_one({'_id': guild_id}, {'$set': settings_document}, upsert=True)
    
    if len(bot.guilds) == 100:
        channel = bot.get_channel(powiadomienia)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        server_name = guild.name
        server_owner = guild.owner
        if guild.member_count != None:
            member_count = guild.member_count - 1

            embed = nextcord.Embed(title=f"**⭐ 100 serwer ⭐**", description=f"**🧨 Nazwa: `{server_name}`**\n**👥 Użytkownicy: `{member_count}`**\n**👨‍💼 Właściciel: `{server_owner}`**\n**🎈 ID: `{guild.id}`**\n**🌐 Liczba serwerów: `{len(bot.guilds)}`**", color=0x008000)
            thumbnail_url = guild.icon.url if guild.icon else bot.user.avatar.url
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_footer(text=current_time)
            await channel.send(embed=embed)

    elif len(bot.guilds) == 500:
        channel = bot.get_channel(powiadomienia)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        server_name = guild.name
        server_owner = guild.owner
        if guild.member_count != None:
            member_count = guild.member_count - 1

            embed = nextcord.Embed(title=f"**⭐⭐ 500 serwer ⭐⭐**", description=f"**🧨 Nazwa: `{server_name}`**\n**👥 Użytkownicy: `{member_count}`**\n**👨‍💼 Właściciel: `{server_owner}`**\n**🎈 ID: `{guild.id}`**\n**🌐 Liczba serwerów: `{len(bot.guilds)}`**", color=0x008000)
            thumbnail_url = guild.icon.url if guild.icon else bot.user.avatar.url
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_footer(text=current_time)
            await channel.send(embed=embed)

    elif len(bot.guilds) == 1000:
        channel = bot.get_channel(powiadomienia)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        server_name = guild.name
        server_owner = guild.owner
        if guild.member_count != None:
            member_count = guild.member_count - 1

            embed = nextcord.Embed(title=f"**⭐⭐⭐ 1000 serwer ⭐⭐⭐**", description=f"**🧨 Nazwa: `{server_name}`**\n**👥 Użytkownicy: `{member_count}`**\n**👨‍💼 Właściciel: `{server_owner}`**\n**🎈 ID: `{guild.id}`**\n**🌐 Liczba serwerów: `{len(bot.guilds)}`**", color=0x008000)
            thumbnail_url = guild.icon.url if guild.icon else bot.user.avatar.url
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_footer(text=current_time)
            await channel.send(embed=embed)

    else:
        channel = bot.get_channel(powiadomienia)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        server_name = guild.name
        server_owner = guild.owner
        if guild.member_count != None:
            member_count = guild.member_count - 1

            embed = nextcord.Embed(title=f"**Nowy serwer**", description=f"**🧨 Nazwa: `{server_name}`**\n**👥 Użytkownicy: `{member_count}`**\n**👨‍💼 Właściciel: `{server_owner}`**\n**🎈 ID: `{guild.id}`**\n**🌐 Liczba serwerów: `{len(bot.guilds)}`**", color=0x008000)
            thumbnail_url = guild.icon.url if guild.icon else bot.user.avatar.url
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_footer(text=current_time)
            await channel.send(embed=embed)

    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"{len(bot.guilds)} serwerów!"))

#Powiadomienie - usunięcie
@bot.event
async def on_guild_remove(guild):
    server_id = str(guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document and settings_document.get("globalBan", False):
        return
    
    channel = bot.get_channel(powiadomienia)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    server_name = guild.name
    if guild.member_count != None:
        member_count = guild.member_count - 1

        embed = nextcord.Embed(title=f"**Wyrzucono**", description=f"**🧨 Nazwa: `{server_name}`**\n**👥 Użytkownicy: `{member_count}`**\n**🌐 Liczba serwerów: `{len(bot.guilds)}`**", color=0xd7231a)
        thumbnail_url = guild.icon.url if guild.icon else bot.user.avatar.url
        embed.set_thumbnail(url=thumbnail_url)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_footer(text=current_time)
        await channel.send(embed=embed)

    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=f"{len(bot.guilds)} serwerów!"))

    if settings_document:
        if not settings_document.get("globalBan", False):
            settings_collection.delete_one({'_id': server_id})

    if guilds_collection.find_one({'_id': server_id}):
        guilds_collection.delete_one({'_id': server_id})

    if currency_collection.find_one({'_id': server_id}):
        currency_collection.delete_one({'_id': server_id})

#Powitania #InviteLogger
@bot.event
async def on_member_join(member):
    try:
        server_id = str(member.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        if settings_document:
            if 'language' in settings_document:
                lang = settings_document['language']
            else:
                lang = "PL"
        else:
            lang = "PL"

        if settings_document and settings_document.get('inviteLogger', False):
            invites = await member.guild.invites()
            if not hasattr(bot, 'invites'):
                bot.invites = {}

            for invite in invites:
                if invite.uses > bot.invites.get(invite.id, 0):
                    inviter = invite.inviter
                    inviter_id = str(inviter.id)
                    user_document = users_collection.find_one({'_id': inviter_id})

                    if not user_document:
                        user_document = {
                            '_id': inviter_id,
                            'invites': {
                                str(member.guild.id): {
                                    'Invites': 1
                                }
                            }
                        }
                        users_collection.insert_one(user_document)
                    else:
                        if 'invites' not in user_document:
                            user_document['invites'] = {}

                        server_id = str(member.guild.id)
                        if server_id not in user_document['invites']:
                            user_document['invites'][server_id] = {
                                'Invites': 1
                            }
                        else:
                            if 'Invites' not in user_document['invites'][server_id]:
                                user_document['invites'][server_id]['Invites'] = 1
                            else:
                                user_document['invites'][server_id]['Invites'] += 1

                        users_collection.update_one({'_id': inviter_id}, {'$set': {'invites': user_document['invites']}})

                    continue

        if settings_document and settings_document.get('powitania', False):
            idkanalu = settings_document.get('kanalPowitan')

            if member.avatar:
                avatar_url = member.avatar.url
            else:
                avatar_url = no_avatar

            premium_status = get_status_text(settings_document.get("premium", False))
            wiadomoscON = settings_document.get('powitaniaWiadomoscON')
            if premium_status and wiadomoscON:
                wiadomosc = settings_document.get('powitaniaWiadomosc')
                wiadomosc = wiadomosc.replace("[user]", member.mention).replace("[guild]", member.guild.name).replace("/n", "\n").replace("\\n", "\n")
                if lang == "PL":
                    embed = nextcord.Embed(
                        description=f"{wiadomosc}",
                        color=0x00ff00
                    )
                    embed.set_footer(text=f"Jesteś {member.guild.member_count} użytkownikiem • {current_time}", icon_url=avatar_url)
                elif lang == "ENG":
                    embed = nextcord.Embed(
                        description=f"{wiadomosc}",
                        color=0x00ff00
                    )
                    embed.set_footer(text=f"You are a {member.guild.member_count} user • {current_time}", icon_url=avatar_url)

            else:
                if lang == "PL":
                    embed = nextcord.Embed(
                        description=f"` 👋 ` Witaj *{member.mention}* na {member.guild.name}\nMamy nadzieję, że zostaniesz z nami na długo!",
                        color=0x00ff00
                    )
                    embed.set_footer(text=f"Jesteś {member.guild.member_count} użytkownikiem • {current_time}", icon_url=avatar_url)
                elif lang == "ENG":
                    embed = nextcord.Embed(
                        description=f"` 👋 ` Welcome *{member.mention}* to {member.guild.name}\nWe hope you will stay with us for a long time!",
                        color=0x00ff00
                    )
                    embed.set_footer(text=f"You are a {member.guild.member_count} user • {current_time}", icon_url=avatar_url)

            if idkanalu:
                channel = bot.get_channel(idkanalu)
                await channel.send(embed=embed)

        if settings_document and settings_document.get('powitaniaPV', False):
            wiadomosc = settings_document.get('powitaniaWiadomoscPV')
            if lang == "PL":
                await member.send(f"{wiadomosc}  |  *`Jesteś {member.guild.member_count} użytkownikiem na {member.guild.name}`*")
            elif lang == "ENG":
                await member.send(f"{wiadomosc}  |  *`You are a {member.guild.member_count} user on {member.guild.name}`*")

        if settings_document and settings_document.get('statystyki', False):
            liczba_uzytkownikow = len([m for m in member.guild.members if not m.bot])
            liczba_botow = len([m for m in member.guild.members if m.bot])

            if settings_document.get('kanalStatystykiOsoby'):
                kanalstatyOsoby = settings_document.get('kanalStatystykiOsoby')
                kanalstatyOsoby = bot.get_channel(kanalstatyOsoby)
            else:
                kanalstatyOsoby = None

            if settings_document.get('kanalStatystykiBoty'):
                kanalstatyBoty = settings_document.get('kanalStatystykiBoty')
                kanalstatyBoty = bot.get_channel(kanalstatyBoty)
            else:
                kanalstatyBoty = None
            
            if kanalstatyOsoby != None:
                if lang == "PL":
                    await kanalstatyOsoby.edit(name=f"Użytkownicy: {liczba_uzytkownikow}")
                elif lang == "ENG":
                    await kanalstatyOsoby.edit(name=f"Members: {liczba_uzytkownikow}")

            if kanalstatyBoty != None:
                if lang == "PL":
                    await kanalstatyBoty.edit(name=f"Boty: {liczba_botow}")
                elif lang == "ENG":
                    await kanalstatyBoty.edit(name=f"Bots: {liczba_botow}")

    except Exception:
        pass

#Pozegnania #InviteLogger
@bot.event
async def on_member_remove(member):
    try:
        server_id = str(member.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        if settings_document:
            if 'language' in settings_document:
                lang = settings_document['language']
            else:
                lang = "PL"
        else:
            lang = "PL"

        if settings_document:
            kanalPartnerstw = settings_document.get('kanalPartnerstw', 0)
            rolaPartnerstw = settings_document.get('rolaPartnerstw', 0)
            if kanalPartnerstw != 0 and rolaPartnerstw != 0:
                role = member.guild.get_role(rolaPartnerstw)
                if role in member.roles:
                    embed = nextcord.Embed(title=f'💼 Aktywne partnerstwo', description=f"Na serwerze {member.guild.name} posiadałeś aktywne partnerstwo! Zostało ono usunięte!", color=0xe40c0c)
                    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                    embed.set_thumbnail(url=bot.user.avatar.url)
                    embed.set_footer(text=f"{current_time}")
                    await member.send(embed=embed)

                    kanal_partnerstw = member.guild.get_channel(kanalPartnerstw)
                    if kanal_partnerstw:
                        async for message in kanal_partnerstw.history():
                            if member.mention in message.content:
                                await message.delete()
                                logi_enabled = settings_document.get("logi", False)
                                kanalLogi = settings_document.get("kanalLogi", None)
                                if not kanalLogi:
                                    kanalLogi = 0

                                if logi_enabled and kanalLogi:
                                    if message.author.avatar:
                                        avatar_url = message.author.avatar.url
                                    else:
                                        avatar_url = no_avatar

                                    if lang == "PL":
                                        embed = nextcord.Embed(description=f"**💼 Usunięto wiadomość partnerstwa**\n\n**Realizator:** *{message.author.mention}*\n**Partner:** *{member.mention}*\n\n*Uwaga:*\n*Nie usunięto tego partnerstwa realizatorowi, jest to po to aby realizator specjalnie nie usuwał wiadomości!*", color=0xe40c0c)
                                        embed.set_author(name=message.author, icon_url=avatar_url)
                                        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/gumka.png")
                                        embed.set_footer(text=f"{current_time}")
                                    elif lang == "ENG":
                                        embed = nextcord.Embed(description=f"**💼 Partnership message removed**\n\n**Executor:** *{message.author.mention}*\n**Partner:** *{member.mention}*\n\n*Note:*\n*This partnership was not deleted from the producer, this is so that the producer does not delete the message on purpose!*", color=0xe40c0c)
                                        embed.set_author(name=message.author, icon_url=avatar_url)
                                        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/gumka.png")
                                        embed.set_footer(text=f"{current_time}")
                                    
                                    channel = await bot.fetch_channel(kanalLogi)
                                    await channel.send(embed=embed)
                    
        if settings_document and settings_document.get('inviteLogger', False):
            invites = await member.guild.invites()
            if not hasattr(bot, 'invites'):
                bot.invites = {}

            for invite in invites:
                if invite.uses > bot.invites.get(invite.id, 0):
                    inviter = invite.inviter
                    inviter_id = str(inviter.id)
                    user_document = users_collection.find_one({'_id': inviter_id})

                    if not user_document:
                        user_document = {
                            '_id': inviter_id,
                            'invites': {
                                str(member.guild.id): {
                                    'Left': 1
                                }
                            }
                        }
                        users_collection.insert_one(user_document)
                    else:
                        if 'invites' not in user_document:
                            user_document['invites'] = {}

                        server_id = str(member.guild.id)
                        if server_id not in user_document['invites']:
                            user_document['invites'][server_id] = {
                                'Left': 1
                            }
                        else:
                            if 'Left' not in user_document['invites'][server_id]:
                                user_document['invites'][server_id]['Left'] = 1
                            else:
                                user_document['invites'][server_id]['Left'] += 1

                        users_collection.update_one({'_id': inviter_id}, {'$set': {'invites': user_document['invites']}})

                    continue

        if settings_document and settings_document.get('pozegnania', False):
            idkanalu = settings_document.get('kanalPozegnan')
            if member.avatar:
                avatar_url = member.avatar.url
            else:
                avatar_url = no_avatar

            premium_status = get_status_text(settings_document.get("premium", False))
            wiadomoscON = settings_document.get('pozegnaniaWiadomoscON')
            if premium_status and wiadomoscON:
                wiadomosc = settings_document.get('pozegnaniaWiadomosc')
                wiadomosc = wiadomosc.replace("[user]", member.mention).replace("[guild]", member.guild.name).replace("/n", "\n").replace("\\n", "\n")
                if lang == "PL":
                    embed = nextcord.Embed(
                        description=f"{wiadomosc}",
                        color=0xff0000
                    )
                    embed.set_footer(text=f"Byłeś {member.guild.member_count + 1} użytkownikiem • {current_time}", icon_url=avatar_url)

                elif lang == "ENG":
                    embed = nextcord.Embed(
                        description=f"{wiadomosc}",
                        color=0xff0000
                    )
                    embed.set_footer(text=f"You were {member.guild.member_count + 1} user • {current_time}", icon_url=avatar_url)

            else:
                if lang == "PL":
                    embed = nextcord.Embed(
                        description=f"` 👋 ` Żegnaj *{member.mention}*\nMamy nadzieję, że wrócisz do nas!",
                        color=0xff0000
                    )
                    embed.set_footer(text=f"Byłeś {member.guild.member_count + 1} użytkownikiem • {current_time}", icon_url=avatar_url)

                elif lang == "ENG":
                    embed = nextcord.Embed(
                        description=f"` 👋 ` Goodbye *{member.mention}*\nWe hope you'll come back to us!",
                        color=0xff0000
                    )
                    embed.set_footer(text=f"You were {member.guild.member_count + 1} user • {current_time}", icon_url=avatar_url)

            if idkanalu:
                channel = bot.get_channel(idkanalu)
                await channel.send(embed=embed)

        if settings_document and settings_document.get('statystyki', False):
            liczba_uzytkownikow = len([m for m in member.guild.members if not m.bot])
            liczba_botow = len([m for m in member.guild.members if m.bot])

            if settings_document.get('kanalStatystykiOsoby'):
                kanalstatyOsoby = settings_document.get('kanalStatystykiOsoby')
                kanalstatyOsoby = bot.get_channel(kanalstatyOsoby)
            else:
                kanalstatyOsoby = None

            if settings_document.get('kanalStatystykiBoty'):
                kanalstatyBoty = settings_document.get('kanalStatystykiBoty')
                kanalstatyBoty = bot.get_channel(kanalstatyBoty)
            else:
                kanalstatyBoty = None
            
            if kanalstatyOsoby != None:
                if lang == "PL":
                    await kanalstatyOsoby.edit(name=f"Użytkownicy: {liczba_uzytkownikow}")
                elif lang == "ENG":
                    await kanalstatyOsoby.edit(name=f"Members: {liczba_uzytkownikow}")

            if kanalstatyBoty != None:
                if lang == "PL":
                    await kanalstatyBoty.edit(name=f"Boty: {liczba_botow}")
                elif lang == "ENG":
                    await kanalstatyBoty.edit(name=f"Bots: {liczba_botow}")
                    
    except Exception:
        pass

#Partnerstwa #Anty #GlobalChat #Liczenie #Litera #Mute
@bot.event
async def on_message(message):
    try:
        if message.channel.type == nextcord.ChannelType.private:
            return
        
        global ostatni_autor
        server_id = str(message.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        user_id = str(message.author.id)
        cooldown_data = cooldowns_collection.find_one({"_id": user_id})
        user_document = users_collection.find_one({'_id': str(message.author.id)})
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        author = message.author


        if settings_document:
            kanalPartnerstw = settings_document.get("kanalPartnerstw", None)
            rolaPartnerstw = settings_document.get("rolaPartnerstw", None)
            kanalLiczenia = settings_document.get("kanalLiczenia", None)
            kanalLitery = settings_document.get("kanalLitery", None)

            if not kanalPartnerstw:
                kanalPartnerstw = 0
            if not rolaPartnerstw:
                rolaPartnerstw = 0
            if not kanalLiczenia:
                kanalLiczenia = 0
            if not kanalLitery:
                kanalLitery = 0
        else:
            kanalPartnerstw = 0
            kanalLiczenia = 0

        if settings_document:
            if 'language' in settings_document:
                lang = settings_document['language']
            else:
                lang = "PL"
        else:
            lang = "PL"

        if user_document and 'mutes' in user_document:
            current_time_mute = datetime.datetime.now()

            for mute_info in user_document['mutes']:
                sid = mute_info.get('server_id')
                if sid == server_id:
                    end_time = mute_info.get('end_time')
                    if end_time and end_time > current_time_mute:
                        await message.delete()
                        user = message.author
                        remaining_time = end_time - current_time_mute
                        remaining_time_str = str(remaining_time).split('.')[0]
                        remaining_time_str = remaining_time_str.replace(" days, ", "d ").replace(" day, ", "d ")
                        remaining_time_str = remaining_time_str.replace(":00:00", "h").replace(":00", "m")

                        if lang == "PL":
                            await message.channel.send(f"`[❌]:` {user.mention}, masz aktywne wyciszenie, poczekaj jeszcze `{remaining_time_str}`", delete_after=3)
                        elif lang == "ENG":
                            await message.channel.send(f"`[❌]:` {user.mention}, you have active mute, wait `{remaining_time_str}`", delete_after=3)
                        return
                
        if settings_document:
            antyMention_enabled = settings_document.get("antyMention", False)
            antyLink_enabled = settings_document.get("antyLink", False)
            antyCaps_enabled = settings_document.get("antyCaps", False)
            antyFlood_enabled = settings_document.get("antyFlood", False)
            partnerstwa_enabled = settings_document.get("partnerstwa", False)
            globalchat_enabled = settings_document.get("globalchat", False)
            liczenie_enabled = settings_document.get("liczenie", False)
            litera_enabled = settings_document.get("litera", False)

            if message.channel.id == kanalOcen and not message.author.bot and not "@everyone" in message.content and not "@here" in message.content:
                channel = bot.get_channel(kanalOcen)
                await channel.send("`[❌]:` Aby dodać opinię użyj `/ocena`!", delete_after=5)
                await message.delete()

            if bot.user.mentioned_in(message) and not "@everyone" in message.content and not "@here" in message.content and not message.author.bot:
                if cooldown_data and "helpCD" in cooldown_data:
                    last_usage = cooldown_data["helpCD"]
                    current_time = datetime.datetime.now()
                    time_difference = current_time - last_usage
                    cooldown_duration = datetime.timedelta(seconds=hcd)
                    
                    if time_difference >= cooldown_duration:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"helpCD": current_time}})

                        if lang == "PL":
                            embed = nextcord.Embed(title=f'**Help**', description=f"**Wybierz poniżej kategorię komend!**", color=0xe40c0c)
                            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                            thumbnail_url = message.guild.icon.url if message.guild.icon else bot.user.avatar.url
                            embed.set_thumbnail(url=thumbnail_url)
                            embed.set_footer(text=f"Invoked by {author} | {current_time}")
                            view = Help()
                        elif lang == "ENG":
                            embed = nextcord.Embed(title=f'**Help**', description=f"**Choose a command category below!**", color=0xe40c0c)
                            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                            thumbnail_url = message.guild.icon.url if message.guild.icon else bot.user.avatar.url
                            embed.set_thumbnail(url=thumbnail_url)
                            embed.set_footer(text=f"Invoked by {author} | {current_time}")
                            view = HelpENG()
                        
                        global wiadomoscHelp
                        wiadomoscHelp = await message.channel.send(embed=embed, view=view)
                        
                        statistics = load_statistics()
                        if 'help' in statistics:
                            statistics['help'] += 1
                        if 'allCommands' in statistics:
                            statistics['allCommands'] += 1
                        else:
                            statistics['help'] = 1
                            statistics['allCommands'] = 1
                        save_statistics(statistics)
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"helpCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": str(message.author.id), "helpCD": current_time})

                    if lang == "PL":
                        embed = nextcord.Embed(title=f'**Help**', description=f"**Wybierz poniżej kategorię komend!**", color=0xe40c0c)
                        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                        thumbnail_url = message.guild.icon.url if message.guild.icon else bot.user.avatar.url
                        embed.set_thumbnail(url=thumbnail_url)
                        embed.set_footer(text=f"Invoked by {author} | {current_time}")
                        view = Help()
                    elif lang == "ENG":
                        embed = nextcord.Embed(title=f'**Help**', description=f"**Choose a command category below!**", color=0xe40c0c)
                        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                        thumbnail_url = message.guild.icon.url if message.guild.icon else bot.user.avatar.url
                        embed.set_thumbnail(url=thumbnail_url)
                        embed.set_footer(text=f"Invoked by {author} | {current_time}")
                        view = HelpENG()
                    
                    statistics = load_statistics()
                    if 'help' in statistics:
                        statistics['help'] += 1
                    if 'allCommands' in statistics:
                        statistics['allCommands'] += 1
                    else:
                        statistics['help'] = 1
                        statistics['allCommands'] = 1
                    save_statistics(statistics)

            if kanalPartnerstw:
                idkanalu = kanalPartnerstw
            else:
                idkanalu = 0

            if message.channel.id == kanalLiczenia and liczenie_enabled and not message.author.bot:

                if ostatni_autor == message.author:
                    await message.reply("`[❌]`", delete_after=3)
                    await message.delete()
                else:
                    messages = await message.channel.history(limit=None).flatten()
                    numer_wiadomosci = len(messages)

                    if not message.content == str(numer_wiadomosci):
                        await message.delete()

                ostatni_autor = message.author

            elif message.channel.id == kanalLitery and litera_enabled and not message.author.bot:
                async for prev_message in message.channel.history(limit=2):
                    if prev_message != message:
                        break
                else:
                    prev_message = None

                if prev_message:
                    last_char_prev_message = prev_message.content[-1].lower() if prev_message.content else None
                    first_char_current_message = message.content[0].lower() if message.content else None

                    if not last_char_prev_message == first_char_current_message:
                        await message.delete()

            elif partnerstwa_enabled and message.channel.id == idkanalu:
                if "discord.gg" in message.content or "discord.com" in message.content or "dsc.gg" in message.content:
                    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    user_id = str(message.author.id)

                    partnerstwa_stats = guilds_collection.find_one({"_id": server_id})

                    if not partnerstwa_stats:
                        partnerstwa_stats = {"_id": server_id, "partnerships": {user_id: 1}}
                    else:
                        partnerships = partnerstwa_stats.get("partnerships", {})
                        partnerships[user_id] = partnerships.get(user_id, 0) + 1
                        partnerstwa_stats["partnerships"] = partnerships

                    guilds_collection.replace_one({"_id": server_id}, partnerstwa_stats, upsert=True)

                    partnerstwa = partnerstwa_stats.get("partnerships", {}).get(user_id, 1)

                    sorted_partnerships = sorted(partnerstwa_stats.get("partnerships", {}).items(), key=lambda x: x[1], reverse=True)
                    user_rank = sorted_partnerships.index((user_id, partnerstwa)) + 1

                    mentions = message.role_mentions + message.mentions
                    non_everyone_mentions = [mention for mention in mentions if mention.name not in ['everyone', 'here']]

                    if non_everyone_mentions:
                        if lang == "PL":
                            embed = nextcord.Embed(title=f"Dziękujemy za partnerstwo!", description=f"**To już `{partnerstwa}`**\n**Jesteś na `{user_rank}` miejscu w rankingu!**\n\nRealizator: {message.author.mention}\n\nPartner: {', '.join(mention.mention for mention in non_everyone_mentions)}\n\n**Miłego dnia!**", color=0xffe600)
                        elif lang == "ENG":
                            embed = nextcord.Embed(title=f"Thank you for your partnership!", description=f"**That's `{partnerstwa}`**\n**You are ranked `{user_rank}` in the leaderboard!**\n\nProducer: {message.author.mention}\n\nPartner: {', '.join(mention.mention for mention in non_everyone_mentions)}\n\n**Have a nice day!**", color=0xffe600)
                    else:
                        if lang == "PL":
                            embed = nextcord.Embed(title=f"Dziękujemy za partnerstwo!", description=f"**To już `{partnerstwa}`**\n**Jesteś na `{user_rank}` miejscu w rankingu!**\n\n**Miłego dnia!**", color=0xffe600)
                        elif lang == "ENG":
                            embed = nextcord.Embed(title=f"Thank you for your partnership!", description=f"**That's `{partnerstwa}`**\n**You are ranked `{user_rank}` in the leaderboard!**\n\n**Thank you for your partnership!**", color=0xffe600)

                    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                    embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Partnerstwo.png")
                    embed.set_footer(text=f"{current_time}")
                    await message.reply(embed=embed)

                    if non_everyone_mentions and rolaPartnerstw != 0:
                        role = message.guild.get_role(rolaPartnerstw)
                        for member in non_everyone_mentions:
                            await member.add_roles(role)

                    statistics = load_statistics()
                    if 'partnerstwa' in statistics:
                        statistics['partnerstwa'] += 1
                    else:
                        statistics['partnerstwa'] = 1

            elif globalchat_enabled and "kanalGlobalChatu" in settings_document and settings_document["kanalGlobalChatu"] == message.channel.id and not message.author.bot:
                mentions = ["@everyone", "@here"]
                if message.mentions or any(phrase in message.content for phrase in mentions):
                    await message.channel.send(f"`[❌]:` {message.author.mention} na globalchacie nie wolno używać `@mention`!", delete_after=10)
                    await message.delete()
                    return
                
                antyLinki = ["https://", "http://"]
                gifs = ["https://media.discordapp.net", "https://tenor.com"]
                if any(phrase in message.content for phrase in antyLinki) and not any(phrase in message.content for phrase in gifs):
                    await message.channel.send(f"`[❌]:` {message.author.mention} na globalchacie nie wolno wysyłać `linków`!", delete_after=10)
                    await message.delete()
                    return
                
                all_servers = settings_collection.find({})
                server_name = message.guild.name
                        
                await message.delete()

                for server_data in all_servers:
                    server_id = server_data["_id"]
                    gc = server_data.get("globalchat", False)
                    if "kanalGlobalChatu" in server_data and gc == True:
                        channel_id = server_data["kanalGlobalChatu"]
                                
                        try:
                            channel = await bot.fetch_channel(channel_id)
                            embed = nextcord.Embed(title=message.content, color=0xffd700)
                            if message.author.avatar:
                                avatar_url = message.author.avatar.url
                            else:
                                avatar_url = no_avatar

                            if message.attachments:
                                attachments = message.attachments
                                file_attachments = []
                                numOfAta = 0
                                for attachment in attachments:
                                    if attachment.url:
                                        if numOfAta == 0:
                                            numOfAta = 1
                                            embed.set_image(url=attachment.url)
                                        else:
                                            file_attachments.append(await attachment.to_file())

                            embed.set_author(name=message.author, icon_url=avatar_url)
                            embed.set_footer(text=f"{server_name} | {current_time}")

                            if message.attachments:
                                await channel.send(embed=embed, files=file_attachments)
                            else:
                                await channel.send(embed=embed)
                        except Exception:
                            pass

            elif antyMention_enabled and message.mentions and not message.author.bot:
                if not message.author.guild_permissions.manage_messages:
                    if idkanalu is None or message.channel.id != idkanalu:
                        server_id = str(message.guild.id)
                        settings_document = settings_collection.find_one({'_id': server_id})

                        if settings_document and 'whitelisted_anty' in settings_document:
                            whitelisted_anty = settings_document['whitelisted_anty']
                            if message.channel.id in whitelisted_anty:
                                return

                        await message.channel.send(f"`[❌]:` {message.author.mention} nie używaj `@mention`!", delete_after=6)
                        await message.delete()

            elif antyLink_enabled and not message.author.bot:
                antyLinki = ["https://", "http://"]
                gifs = ["https://media.discordapp.net", "https://tenor.com"]
                if not message.author.guild_permissions.manage_messages:
                    if any(phrase in message.content for phrase in antyLinki) and not any(phrase in message.content for phrase in gifs):
                        if idkanalu is None or message.channel.id != idkanalu:
                            server_id = str(message.guild.id)
                            settings_document = settings_collection.find_one({'_id': server_id})

                            if settings_document and 'whitelisted_anty' in settings_document:
                                whitelisted_anty = settings_document['whitelisted_anty']
                                if message.channel.id in whitelisted_anty:
                                    return
                                
                            await message.channel.send(f"`[❌]:` {message.author.mention} nie wysyłaj linków!", delete_after=6)
                            await message.delete()

            elif antyCaps_enabled and not message.author.bot and message.channel.id != idkanalu:
                if message.content.isupper() or sum(1 for char in message.content if char.isupper()) > 5:
                    await message.delete()
                    await message.channel.send(f"`[❌]:` {message.author.mention} nie nadużywaj dużych liter! 🔥🔥", delete_after=6)

            if antyFlood_enabled and not message.author.bot and message.channel.id != idkanalu:
                current_time = time.time()
                user_id = str(message.author.id)
                elapsed_time = current_time - last_message_times[user_id]
                if emoji.emoji_count(message.content) > 5:
                    await message.delete()
                    await message.channel.send(f"`[❌]:` {message.author.mention} nie spamuj! 🔥🔥", delete_after=6)
                elif elapsed_time < 60 and message.content == last_message_content.get(user_id, ''):
                    await message.delete()
                    await message.channel.send(f"`[❌]:` {message.author.mention} nie spamuj! 🔥🔥", delete_after=6)

    except nextcord.errors.NotFound:
        pass

    last_message_times[user_id] = current_time
    last_message_content[user_id] = message.content
    last_message_counts[user_id] += 1
    await bot.process_commands(message)

#Logi
@bot.event
async def on_message_delete(message):
    try:
        if message.channel.type == nextcord.ChannelType.private:
            return
        
        server_id = str(message.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        if settings_document and not message.author.bot and not message.channel.id == kanalOcen:
            logi_enabled = settings_document.get("logi", False)
            kanalLogi = settings_document.get("kanalLogi", None)
            kanalGlobal = settings_document.get("kanalGlobalChatu", None)
            kanalLiczenia = settings_document.get("kanalLiczenia", None)
            kanalLitery = settings_document.get("kanalLitery", None)

            if not kanalLogi:
                kanalLogi = 0
            if not kanalGlobal:
                kanalGlobal = 0
            if not kanalLiczenia:
                kanalLiczenia = 0
            if not kanalLitery:
                kanalLitery = 0

            if settings_document:
                if 'language' in settings_document:
                    lang = settings_document['language']
                else:
                    lang = "PL"
            else:
                lang = "PL"

            if logi_enabled and kanalLogi:
                if message.channel.id == kanalGlobal or message.channel.id == kanalLiczenia or message.channel.id == kanalLitery:
                    return
                channel = await bot.fetch_channel(kanalLogi)
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                max_length = 2000
                if len(message.content) > max_length:
                    message_content = message_content[:max_length - 3] + "..."

                if lang == "PL":
                    embed = nextcord.Embed(description=f"**Usunięta wiadomość**\n\n**Kanał:**\n{message.channel.mention}\n\n**Wiadomość:**\n`{message.content}`", color=0xe40c0c)
                elif lang == "ENG":
                    embed = nextcord.Embed(description=f"**Deleted message**\n\n**Channel:**\n{message.channel.mention}\n\n**Message:**\n`{message.content}`", color=0xe40c0c)

                if message.author.avatar:
                    avatar_url = message.author.avatar.url
                else:
                    avatar_url = no_avatar

                embed.set_author(name=message.author, icon_url=avatar_url)
                embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/gumka.png")
                embed.set_footer(text=f"{current_time}")
                await channel.send(embed=embed)

    except nextcord.errors.NotFound:
        return

#Logi
@bot.event
async def on_message_edit(before, after):
    try:
        if after.channel.type == nextcord.ChannelType.private:
            return
        
        server_id = str(after.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        if settings_document:
            antyMention_enabled = settings_document.get("antyMention", False)
            antyLink_enabled = settings_document.get("antyLink", False)
            antyCaps_enabled = settings_document.get("antyCaps", False)
            antyFlood_enabled = settings_document.get("antyFlood", False)

            if antyMention_enabled and after.mentions and not after.author.bot:
                if not after.author.guild_permissions.manage_messages:
                        server_id = str(after.guild.id)
                        settings_document = settings_collection.find_one({'_id': server_id})

                        if settings_document and 'whitelisted_anty' in settings_document:
                            whitelisted_anty = settings_document['whitelisted_anty']
                            if after.channel.id in whitelisted_anty:
                                return

                        await after.channel.send(f"`[❌]:` {after.author.mention} nie używaj `@mention`!", delete_after=6)
                        await after.delete()

            elif antyLink_enabled and not after.author.bot:
                antyLinki = ["https://", "http://"]
                gifs = ["https://media.discordapp.net", "https://tenor.com"]
                if not after.author.guild_permissions.manage_afters:
                    if any(phrase in after.content for phrase in antyLinki) and not any(phrase in after.content for phrase in gifs):
                            server_id = str(after.guild.id)
                            settings_document = settings_collection.find_one({'_id': server_id})

                            if settings_document and 'whitelisted_anty' in settings_document:
                                whitelisted_anty = settings_document['whitelisted_anty']
                                if after.channel.id in whitelisted_anty:
                                    return
                                
                            await after.channel.send(f"`[❌]:` {after.author.mention} nie wysyłaj linków!", delete_after=6)
                            await after.delete()

            elif antyCaps_enabled and not after.author.bot:
                if after.content.isupper() or sum(1 for char in after.content if char.isupper()) > 5:
                    await after.delete()
                    await after.channel.send(f"`[❌]:` {after.author.mention} nie nadużywaj dużych liter! 🔥🔥", delete_after=6)

        if settings_document and not after.author.bot and not after.channel.id == kanalOcen:
            logi_enabled = settings_document.get("logi", False)
            kanalLogi = settings_document.get("kanalLogi", None)
            kanalGlobal = settings_document.get("kanalGlobalChatu", None)
            kanalLiczenia = settings_document.get("kanalLiczenia", None)
            kanalLitery = settings_document.get("kanalLitery", None)

            if not kanalLogi:
                kanalLogi = 0
            if not kanalGlobal:
                kanalGlobal = 0
            if not kanalLiczenia:
                kanalLiczenia = 0
            if not kanalLitery:
                kanalLitery = 0

            if settings_document:
                if 'language' in settings_document:
                    lang = settings_document['language']
                else:
                    lang = "PL"
            else:
                lang = "PL"

            if logi_enabled and kanalLogi:
                if after.channel.id == kanalGlobal or after.channel.id == kanalLiczenia or after.channel.id == kanalLitery:
                    return
                channel = await bot.fetch_channel(kanalLogi)
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                max_length = 2000
                if len(after.content) > max_length:
                    message_content = message_content[:max_length - 3] + "..."
                    
                if lang == "PL":
                    embed = nextcord.Embed(description=f"**Zedytowano wiadomość**\n\n**Kanał:**\n{after.channel.mention}\n\n**Przed:**\n`{before.content}`\n\n**Po:**\n`{after.content}`", color=0xe40c0c)
                elif lang == "ENG":
                    embed = nextcord.Embed(description=f"**Message edited**\n\n**Channel:**\n{after.channel.mention}\n\n**Before:**\n`{before.content}`\n\n**After:**\n`{after.content}`", color=0xe40c0c)

                if after.author.avatar:
                    avatar_url = after.author.avatar.url
                else:
                    avatar_url = no_avatar

                embed.set_author(name=before.author, icon_url=avatar_url)
                embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/olowek.png")
                embed.set_footer(text=f"{current_time}")
                await channel.send(embed=embed)

    except nextcord.errors.NotFound:
        return

#Logi
@bot.event
async def on_guild_channel_create(channel):
    try:
        server_id = str(channel.guild.id)
        user = channel.guild.me
        settings_document = settings_collection.find_one({'_id': server_id})
        if settings_document:
            logi_enabled = settings_document.get("logi", False)
            kanalLogi = settings_document.get("kanalLogi", None)

            if settings_document:
                if 'language' in settings_document:
                    lang = settings_document['language']
                else:
                    lang = "PL"
            else:
                lang = "PL"

            if logi_enabled and kanalLogi:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")

                if lang == "PL":
                    embed = nextcord.Embed(description=f"**Nowy kanał**\n\n**Kanał:**\n{channel.mention}", color=0x008000)
                elif lang == "ENG":
                    embed = nextcord.Embed(description=f"**New channel**\n\n**Channel:**\n{channel.mention}", color=0x008000)

                if user.avatar:
                    avatar_url = user.avatar.url
                else:
                    avatar_url = no_avatar

                embed.set_author(name=user.name, icon_url=avatar_url)
                embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Plus.png")
                embed.set_footer(text=f"{current_time}")
                channel = await bot.fetch_channel(kanalLogi)
                await channel.send(embed=embed)

            if settings_document and settings_document.get('statystyki', False):
                liczba_kanalow_tekstowych = len([c for c in channel.guild.channels if isinstance(c, nextcord.TextChannel)])
                liczba_kanalow_glosowych = len([c for c in channel.guild.channels if isinstance(c, nextcord.VoiceChannel)])
                liczba_kanałow = liczba_kanalow_tekstowych + liczba_kanalow_glosowych

                if settings_document.get('kanalStatystykiKanaly'):
                    kanalStatystykiKanaly = settings_document.get('kanalStatystykiKanaly')
                    kanalStatystykiKanaly = bot.get_channel(kanalStatystykiKanaly)
                else:
                    kanalStatystykiKanaly = None
                
                if kanalStatystykiKanaly != None:
                    if lang == "PL":
                        await kanalStatystykiKanaly.edit(name=f"Kanały: {liczba_kanałow}")
                    elif lang == "ENG":
                        await kanalStatystykiKanaly.edit(name=f"Channels: {liczba_kanałow}")


    except nextcord.errors.NotFound:
        return

#Logi
@bot.event
async def on_guild_channel_delete(channel):
    try:
        server_id = str(channel.guild.id)
        user = channel.guild.me
        settings_document = settings_collection.find_one({'_id': server_id})
        if settings_document:
            logi_enabled = settings_document.get("logi", False)
            kanalLogi = settings_document.get("kanalLogi", None)

            if settings_document:
                if 'language' in settings_document:
                    lang = settings_document['language']
                else:
                    lang = "PL"
            else:
                lang = "PL"

            if logi_enabled and kanalLogi:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")

                if lang == "PL":
                    embed = nextcord.Embed(description=f"**Usunięto kanał**\n\n**Kanał:**\n{channel.mention}", color=0xe40c0c)
                elif lang == "ENG":
                    embed = nextcord.Embed(description=f"**Channel deleted**\n\n**Channel:**\n{channel.mention}", color=0xe40c0c)

                if user.avatar:
                    avatar_url = user.avatar.url
                else:
                    avatar_url = no_avatar

                embed.set_author(name=user.name, icon_url=avatar_url)
                embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/gumka.png")
                embed.set_footer(text=f"{current_time}")
                channel = await bot.fetch_channel(kanalLogi)
                await channel.send(embed=embed)

            if settings_document and settings_document.get('statystyki', False):
                liczba_kanalow_tekstowych = len([c for c in channel.guild.channels if isinstance(c, nextcord.TextChannel)])
                liczba_kanalow_glosowych = len([c for c in channel.guild.channels if isinstance(c, nextcord.VoiceChannel)])
                liczba_kanałow = liczba_kanalow_tekstowych + liczba_kanalow_glosowych

                if settings_document.get('kanalStatystykiKanaly'):
                    kanalStatystykiKanaly = settings_document.get('kanalStatystykiKanaly')
                    kanalStatystykiKanaly = bot.get_channel(kanalStatystykiKanaly)
                else:
                    kanalStatystykiKanaly = None
                
                if kanalStatystykiKanaly != None:
                    if lang == "PL":
                        await kanalStatystykiKanaly.edit(name=f"Kanały: {liczba_kanałow}")
                    elif lang == "ENG":
                        await kanalStatystykiKanaly.edit(name=f"Channels: {liczba_kanałow}")

    except nextcord.errors.NotFound:
        return

#Logi
@bot.event
async def on_member_update(before, after):
    try:
        server_id = str(after.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        if settings_document and not after.bot:
            logi_enabled = settings_document.get("logi", False)
            kanalLogi = settings_document.get("kanalLogi", None)

            if settings_document:
                if 'language' in settings_document:
                    lang = settings_document['language']
                else:
                    lang = "PL"
            else:
                lang = "PL"

            if logi_enabled and kanalLogi:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                added_roles = set(after.roles) - set(before.roles)
                removed_roles = set(before.roles) - set(after.roles)

                if added_roles:
                    for role in added_roles:
                        color = 0x008000
                        if lang == "PL":
                            description = f"**Użytkownik otrzymał rolę**\n\n**Użytkownik:**\n{after.mention}\n**Rola:**\n{role.mention}"
                        elif lang == "ENG":
                            description = f"**User received a role**\n\n**User:**\n{after.mention}\n**Role:**\n{role.mention}"
                        await log_role_event(description, kanalLogi, current_time, color, after, link=None)

                if removed_roles:
                    for role in removed_roles:
                        color = 0xe40c0c
                        if lang == "PL":
                            description = f"**Użytkownik stracił rolę**\n\n**Użytkownik:**\n{after.mention}\n**Rola:**\n{role.mention}"
                        elif lang == "ENG":
                            description = f"**User lost a role**\n\n**User:**\n{after.mention}\n**Role:**\n{role.mention}"
                        await log_role_event(description, kanalLogi, current_time, color, after, link=None)

    except nextcord.errors.NotFound:
        return

#Logi #Selfchannel
@bot.event
async def on_voice_state_update(member, before, after):
    try:
        join = False
        leave = False
        moved = False
        if before.channel is None and after.channel is not None:
            join = True
            server_id = str(after.channel.guild.id)

        elif before.channel is not None and after.channel is None:
            leave = True
            server_id = str(before.channel.guild.id)
        
        else:
            moved = True
            server_id = str(before.channel.guild.id)

        user = member
        settings_document = settings_collection.find_one({'_id': server_id})
        if settings_document:
            logi_enabled = settings_document.get("logi", False)
            selfchannel_enabled = settings_document.get("selfchannel", False)
            kanalLogi = settings_document.get("kanalLogi", None)
            kanalselfchannel = settings_document.get("KanalSelfchannel", None)
            if settings_document:
                if 'language' in settings_document:
                    lang = settings_document['language']
                else:
                    lang = "PL"
            else:
                lang = "PL"

            if selfchannel_enabled and kanalselfchannel:
                users_document = users_collection.find_one({'_id': "Info"})
                if join:
                    channel_id = str(after.channel.id)
                    if channel_id == str(kanalselfchannel):
                        previous_channel = member.voice.channel
                        if previous_channel:
                            category = previous_channel.category
                        else:
                            category = None

                        new_channel = await member.guild.create_voice_channel(name=f"🔈・{member.display_name}", category=category)
                        await member.move_to(new_channel)
                        await new_channel.set_permissions(member, manage_channels=True, manage_roles=True, mute_members=True, deafen_members=True)
                        new_channel_info = {"id": new_channel.id, "author": member.id}
                        if "selfchannels" not in users_document:
                            users_document["selfchannels"] = [new_channel_info]
                        else:
                            users_document["selfchannels"].append(new_channel_info)
                        users_collection.update_one({'_id': "Info"}, {'$set': {'selfchannels': users_document["selfchannels"]}}, upsert=True)

                elif leave or moved:
                    channel_id = before.channel.id
                    if "selfchannels" in users_document:
                        for channel_info in users_document["selfchannels"]:
                            if channel_info["id"] == channel_id:
                                channel = member.guild.get_channel(channel_id)
                                if not channel.members:
                                    await channel.delete()
                                    users_document["selfchannels"].remove(channel_info)
                                    users_collection.update_one({'_id': "Info"}, {'$set': {'selfchannels': users_document["selfchannels"]}})

            if logi_enabled and kanalLogi:
                current_time = time.strftime("%Y-%m-%d %H:%M:%S")

                if join == True:
                    if lang == "PL":
                        embed = nextcord.Embed(description=f"**Dołączono do kanału**\n\n**Użytkownik:**\n{member.mention}\n**Kanał:**\n{after.channel.mention}", color=0x008000)
                    elif lang == "ENG":
                        embed = nextcord.Embed(description=f"**Joined the channel**\n\n**Member:**\n{member.mention}\n**Channel:**\n{after.channel.mention}", color=0x008000)
                elif leave == True:
                    if lang == "PL":
                        embed = nextcord.Embed(description=f"**Opuszczono kanał**\n\n**Użytkownik:**\n{member.mention}\n**Kanał:**\n{before.channel.mention}", color=0xe40c0c)
                    elif lang == "ENG":
                        embed = nextcord.Embed(description=f"**Left channel**\n\n**Member:**\n{member.mention}\n**Channel:**\n{before.channel.mention}", color=0xe40c0c)
                elif moved == True:
                    if lang == "PL":
                        embed = nextcord.Embed(description=f"**Zmieniono kanał**\n\n**Użytkownik:**\n{member.mention}\n**Kanały:**\n{before.channel.mention} --> {after.channel.mention}", color=0xffef00)
                    elif lang == "ENG":
                        embed = nextcord.Embed(description=f"**Channel changed**\n\n**Member:**\n{member.mention}\n**Channels:**\n{before.channel.mention} --> {after.channel.mention}", color=0xffef00)

                if user.avatar:
                    avatar_url = user.avatar.url
                else:
                    avatar_url = no_avatar

                embed.set_author(name=user.name, icon_url=avatar_url)
                embed.set_thumbnail(url=no_avatar)
                embed.set_footer(text=f"{current_time}")
                channel = await bot.fetch_channel(kanalLogi)
                await channel.send(embed=embed)

    except Exception:
        pass

#Ping
@bot.slash_command(description= "Sprawdź ping bota!")
async def ping(ctx):
    await ctx.send(f"🏓 Aktualny ping bota wynosi `{round(bot.latency * 1000)}ms`", ephemeral=True)

    statistics = load_statistics()
    if 'ping' in statistics:
        statistics['ping'] += 1
    if 'allCommands' in statistics:
        statistics['allCommands'] += 1
    else:
        statistics['ping'] = 1
        statistics['allCommands'] = 1

#Statystyki
@bot.slash_command(description="Sprawdź statystyki bota i swojego serwera!")
async def statystyki(ctx):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    author = ctx.user
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    statistics = load_statistics()
    help_stats = statistics.get('help', 0)
    ankieta_stats = statistics.get('ankieta', 0)
    say_stats = statistics.get('say', 0)
    clear_stats = statistics.get('clear', 0)
    ship_stats = statistics.get('ship', 0)
    iq_stats = statistics.get('iq', 0)
    kostka_stats = statistics.get('kostka', 0)
    chatbot_stats = statistics.get('chatbot', 0)
    ban_stats = statistics.get('ban', 0)
    kick_stats = statistics.get('kick', 0)
    ticket_stats = statistics.get('tickety', 0)
    mute_stats = statistics.get('mute', 0)
    unmute_stats = statistics.get('unmute', 0)
    info_stats = statistics.get('info', 0)
    mem_stats = statistics.get('mem', 0)
    add_stats = statistics.get('add', 0)
    remove_stats = statistics.get('remove', 0)
    weryfikacja_stats = statistics.get('weryfikacja', 0)
    zgaduj_stats = statistics.get('zgaduj', 0)
    notes_stats = statistics.get('notes', 0)
    kalkulator_stats = statistics.get('kalkulator', 0)
    rob_stats = statistics.get('rob', 0)
    work_stats = statistics.get('work', 0)
    crime_stats = statistics.get('crime', 0)
    ruletka_stats = statistics.get('ruletka', 0)
    blackjack_stats = statistics.get('blackjack', 0)
    all_commands_stats = help_stats + ankieta_stats + say_stats + clear_stats + ship_stats + iq_stats + kostka_stats + chatbot_stats + ban_stats + kick_stats + mute_stats + unmute_stats + info_stats + mem_stats + add_stats + remove_stats + weryfikacja_stats + zgaduj_stats + notes_stats + kalkulator_stats + rob_stats + work_stats + crime_stats + ruletka_stats + blackjack_stats

    server = ctx.guild
    total_members = server.member_count
    total_text_channels = len(server.text_channels)
    total_voice_channels = len(server.voice_channels)
    
    if lang == "PL":
        embed = nextcord.Embed(title=f"Statystyki", description=f"**Statystyki bota:**\n\n🌐 Serwery: `{len(bot.guilds)}`\n🎫 Tickety: `{ticket_stats}`\n✅ Weryfikacje: `{weryfikacja_stats}`\n/help - `{help_stats}`\n/ankieta - `{ankieta_stats}`\n/say - `{say_stats}`\n/ban - `{ban_stats}`\n/kick - `{kick_stats}`\n/mute - `{mute_stats}`\n/unmute - `{unmute_stats}`\n/clear - `{clear_stats}`\n/ship - `{ship_stats}`\n/iq - `{iq_stats}`\n/kostka - `{kostka_stats}`\n/chatbot - `{chatbot_stats}`\n/info - `{info_stats}`\n/mem - `{mem_stats}`\n/add - `{add_stats}`\n/remove - `{remove_stats}`\n/zgaduj - `{zgaduj_stats}`\n/notes - `{notes_stats}`\n/kalkulator - `{kalkulator_stats}`\n/work - `{work_stats}`\n/rob - `{rob_stats}`\n/crime - `{crime_stats}`\n/ruletka - `{ruletka_stats}`\n/blackjack - `{blackjack_stats}`\n\nRazem - `{all_commands_stats}`\n\n\n**Statystyki serwerowe:**\n\nUżytkownicy - `{total_members}`\nKanały tekstowe - `{total_text_channels}`\nKanały głosowe - `{total_voice_channels}`\nWszystkie kanały - `{total_text_channels + total_voice_channels}`", color=0xe40c0c)
    elif lang == "ENG":
        embed = nextcord.Embed(title="Statistics", description=f"**Bot Statistics:**\n\n🌐 Servers: `{len(bot.guilds)}`\n🎫 Tickets: `{ticket_stats}`\n✅ Verifications: `{weryfikacja_stats}`\n/help - `{help_stats}`\n/poll - `{ankieta_stats}`\n/say - `{say_stats}`\n/ban - `{ban_stats}`\n/kick - `{kick_stats}`\n/mute - `{mute_stats}`\n/unmute - `{unmute_stats}`\n/clear - `{clear_stats}`\n/ship - `{ship_stats}`\n/iq - `{iq_stats}`\n/dice - `{kostka_stats}`\n/chatbot - `{chatbot_stats}`\n/info - `{info_stats}`\n/mem - `{mem_stats}`\n/add - `{add_stats}`\n/remove - `{remove_stats}`\n/guess - `{zgaduj_stats}`\n/notes - `{notes_stats}`\n/calculator - `{kalkulator_stats}`\n/work - `{work_stats}`\n/rob - `{rob_stats}`\n/crime - `{crime_stats}`\n/roulette - `{ruletka_stats}`\n/blackjack - `{blackjack_stats}`\n\nTotal - `{all_commands_stats}`\n\n\n**Server Statistics:**\n\nUsers - `{total_members}`\nText Channels - `{total_text_channels}`\nVoice Channels - `{total_voice_channels}`\nAll Channels - `{total_text_channels + total_voice_channels}`", color=0xe40c0c)

    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
    embed.set_footer(text=f"Invoked by {author} | {current_time}")
    await ctx.send(embed=embed)

#Help
@bot.slash_command(description="Wysyła listę komend bota")
async def help(ctx):
    global wiadomoscHelp
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    author = ctx.user
    if ctx.channel.type == nextcord.ChannelType.private:
        embed = nextcord.Embed(title=f'**Help**', description=f"**Wybierz poniżej kategorię komend!**", color=0xe40c0c)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        view = Help()
        wiadomoscHelp = await ctx.send(embed=embed, view=view)
        return
    
    user_id = str(ctx.user.id)
    cooldown_data = cooldowns_collection.find_one({"_id": user_id})
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"
    
    if cooldown_data and "helpCD" in cooldown_data:
        last_usage = cooldown_data["helpCD"]
        current_time = datetime.datetime.now()
        time_difference = current_time - last_usage
        cooldown_duration = datetime.timedelta(seconds=hcd)
        
        if time_difference >= cooldown_duration:
            cooldowns_collection.update_one({"_id": user_id}, {"$set": {"helpCD": current_time}})

            if lang == "PL":
                embed = nextcord.Embed(title=f'**Help**', description=f"**Wybierz poniżej kategorię komend!**", color=0xe40c0c)
                embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                thumbnail_url = ctx.guild.icon.url if ctx.guild.icon else bot.user.avatar.url
                embed.set_thumbnail(url=thumbnail_url)
                embed.set_footer(text=f"Invoked by {author} | {current_time}")
                view = Help()
            elif lang == "ENG":
                embed = nextcord.Embed(title=f'**Help**', description=f"**Choose a command category below!**", color=0xe40c0c)
                embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                thumbnail_url = ctx.guild.icon.url if ctx.guild.icon else bot.user.avatar.url
                embed.set_thumbnail(url=thumbnail_url)
                embed.set_footer(text=f"Invoked by {author} | {current_time}")
                view = HelpENG()
            
            wiadomoscHelp = await ctx.send(embed=embed, view=view)
            
            statistics = load_statistics()
            if 'help' in statistics:
                statistics['help'] += 1
            if 'allCommands' in statistics:
                statistics['allCommands'] += 1
            else:
                statistics['help'] = 1
                statistics['allCommands'] = 1
            save_statistics(statistics)
        else:
            time_left = cooldown_duration - time_difference
            await ctx.send(f"`[❌]:` Musisz poczekać jeszcze `{time_left.seconds} sekund` przed kolejnym użyciem komendy.", ephemeral=True)
    else:
        current_time = datetime.datetime.now()
        if cooldown_data:
            cooldowns_collection.update_one({"_id": user_id}, {"$set": {"helpCD": current_time}}, upsert=True)
        else:
            cooldowns_collection.insert_one({"_id": str(ctx.user.id), "helpCD": current_time})

        if lang == "PL":
            embed = nextcord.Embed(title=f'**Help**', description=f"**Wybierz poniżej kategorię komend!**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            thumbnail_url = ctx.guild.icon.url if ctx.guild.icon else bot.user.avatar.url
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            view = Help()
        elif lang == "ENG":
            embed = nextcord.Embed(title=f'**Help**', description=f"**Choose a command category below!**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            thumbnail_url = ctx.guild.icon.url if ctx.guild.icon else bot.user.avatar.url
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            view = HelpENG()
        
        statistics = load_statistics()
        if 'help' in statistics:
            statistics['help'] += 1
        if 'allCommands' in statistics:
            statistics['allCommands'] += 1
        else:
            statistics['help'] = 1
            statistics['allCommands'] = 1
        save_statistics(statistics)

#Settings
@bot.slash_command(description="Ustaw bota na twój serwer!")
async def settings(ctx):
    await ctx.send("Użyj 'help'")

#Settings
@bot.slash_command(description="Ustaw bota na twój serwer!")
async def settingsconfig(ctx):
    await ctx.send("Użyj 'help'")

#Settings
@bot.slash_command(description="Ustaw bota na twój serwer!")
async def settingsadm(ctx):
    await ctx.send("Użyj 'help'")

#Settings
@bot.slash_command(description="Ustaw bota na twój serwer!")
async def settings4fun(ctx):
    await ctx.send("Użyj 'help'")

#Help
@settings.subcommand(description="Komenda pomocy ustawień")
async def help(ctx):
    server_id = str(ctx.guild.id)
    server_name = ctx.guild.name

    #Tutaj gdy będzie wiele node'ów dodac wykrywanie na ktorym nodzie jest serwer
    node = "Main"

    author = ctx.user
    current_time2 = time.strftime("%Y-%m-%d %H:%M:%S")

    server_settings = settings_collection.find_one({'_id': server_id})
    if not server_settings:
        server_settings = {'_id': server_id}
    
    if 'language' in server_settings:
        lang = server_settings['language']
    else:
        lang = "PL"

    premium_status = get_status_text(server_settings.get("premium", False))
    poziom = "Normal Server (NS)"
    if server_id == "1141830471903359047":
        poziom = "Bot Support Server (BSS)"
    elif premium_status == "on":
        poziom = "Premium Server ⭐ (PS)"

    ankiety_status = get_status_text(server_settings.get("ankiety", False))
    say_status = get_status_text(server_settings.get("say", False))
    ship_status = get_status_text(server_settings.get("ship", False))
    clear_status = get_status_text(server_settings.get("clear", False))
    iq_status = get_status_text(server_settings.get("iq", False))
    kostka_status = get_status_text(server_settings.get("kostka", False))
    chatbot_status = get_status_text(server_settings.get("chatbot", False))
    ban_status = get_status_text(server_settings.get("ban", False))
    kick_status = get_status_text(server_settings.get("kick", False))
    mute_status = get_status_text(server_settings.get("mute", False))
    unmute_status = get_status_text(server_settings.get("unmute", False))
    ticket_status = get_status_text(server_settings.get("tickety", False))
    info_status = get_status_text(server_settings.get("info", False))
    partnerstwa_status = get_status_text(server_settings.get("partnerstwa", False))
    antyMention_status = get_status_text(server_settings.get("antyMention", False))
    antyLink_status = get_status_text(server_settings.get("antyLink", False))
    mem_status = get_status_text(server_settings.get("mem", False))
    weryfikacja_status = get_status_text(server_settings.get("weryfikacja", False))
    zgaduj_status = get_status_text(server_settings.get("zgaduj", False))
    globalchat_status = get_status_text(server_settings.get("globalchat", False))
    logi_status = get_status_text(server_settings.get("logi", False))
    liczenie_status = get_status_text(server_settings.get("liczenie", False))
    litera_status = get_status_text(server_settings.get("litera", False))
    powitania_status = get_status_text(server_settings.get("powitania", False))
    pozegnania_status = get_status_text(server_settings.get("pozegnania", False))
    kalkulator_status = get_status_text(server_settings.get("kalkulator", False))
    ekonomia_status = get_status_text(server_settings.get("ekonomia", False))
    invitelogger_status = get_status_text(server_settings.get("inviteLogger", False))
    selfchannel_status = get_status_text(server_settings.get("selfchannel", False))
    statystyki_status = get_status_text(server_settings.get("statystyki", False))
    giveaway_status = get_status_text(server_settings.get("giveaway", False))
    autoad_status = get_status_text(server_settings.get("autoad", False))
    
    user_id = str(ctx.user.id)
    cooldown_data = cooldowns_collection.find_one({"_id": user_id})
    
    current_time = datetime.datetime.now()
    if cooldown_data and "settingsHelpCD" in cooldown_data:
        last_usage = cooldown_data["settingsHelpCD"]
        time_difference = current_time - last_usage
        cooldown_duration = datetime.timedelta(seconds=hcd)
        
        if time_difference >= cooldown_duration:
            cooldowns_collection.update_one({"_id": user_id}, {"$set": {"settingsHelpCD": current_time}})
            if lang == "PL":
                embed = nextcord.Embed(title=f"{server_name} SETTINGS", description=f"Informacje:\n\nID Serwera - *{server_id}*\nPoziom - *{poziom}*\nNode - *{node}*\n\nFunkcje:\n\nTickety - `{ticket_status}` /settingsConfig ticket\nPartnerstwa - `{partnerstwa_status}` /settingsConfig partnerstwa\nAnty @mention - `{antyMention_status}` /settingsConfig anty mention\nAnty link - `{antyLink_status}` /settingsConfig anty link\nWeryfikacja - `{weryfikacja_status}` /settingsConfig weryfikacja\nPowitania - `{powitania_status}` /settingsConfig powitania\nPozegnania - `{pozegnania_status}` /settingsConfig pozegnania\nSelfchannel - `{selfchannel_status}` /settingsConfig selfchannel\nStatystyki - `{statystyki_status}` /settingsConfig statystyki\nAutoAD - `{autoad_status}` /settingsConfig autoad\nEkonomia - `{ekonomia_status}` /settingsekonomia config\n\nOgólne:\n\nAnkiety - `{ankiety_status}` /settingsConfig ankiety\nSay - `{say_status}` /settings4fun say\n\nAdministracyjne:\n\nBan - `{ban_status}` /settingsAdm ban\nKick - `{kick_status}` /settingsAdm kick\nMute - `{mute_status}` /settingsAdm mute\nUnMute - `{unmute_status}` /settingsAdm unmute\nClear - `{clear_status}` /settingsAdm clear\nLogi - `{logi_status}` /settingsadm logi\nInviteLogger - `{invitelogger_status}` /settingsadm invitelogger\nGiveaway - `{giveaway_status}` /settingsadm giveaway\n\n4Fun:\n\nShip - `{ship_status}` /settings4Fun ship\nIQ - `{iq_status}` /settings4Fun iq\nKostka - `{kostka_status}` /settings4Fun kostka\nChatbot - `{chatbot_status}` /settings4Fun chatbot\nInfo - `{info_status}` /settings4Fun info\nMem - `{mem_status}` /settings4Fun mem\nZgaduj - `{zgaduj_status}` /settings4Fun zgaduj\nGlobalchat - `{globalchat_status}` /settings4Fun globalchat\nLiczenie - `{liczenie_status}` /settings4Fun liczenie\nOstatnia litera - `{litera_status}` /settings4Fun litera\nKalkulator - `{kalkulator_status}` /settings4Fun kalkulator", color=0xe40c0c)
            
                thumbnail_url = ctx.guild.icon.url if ctx.guild.icon else bot.user.avatar.url
                embed.set_thumbnail(url=thumbnail_url)
                    
                embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                embed.set_footer(text=f"Invoked by {author} | {current_time2}")
                await ctx.send(embed=embed)
            elif lang == "ENG":
                embed = nextcord.Embed(title=f"{server_name} SETTINGS", description=f"Informacje:\n\nServer ID - *{server_id}*\nLevel - *{poziom}*\nNode - *{node}*\n\nFunctions:\n\nTickets - `{ticket_status}` /settingsConfig ticket\nPartnerships - `{partnerstwa_status}` /settingsConfig partnerstwa\nAnty @mention - `{antyMention_status}` /settingsConfig anty mention\nAnty link - `{antyLink_status}` /settingsConfig anty link\nVerification - `{weryfikacja_status}` /settingsConfig weryfikacja\nGreetings - `{powitania_status}` /settingsConfig powitania\nGoodbyes - `{pozegnania_status}` /settingsConfig pozegnania\nSelfchannel - `{selfchannel_status}` /settingsConfig selfchannel\nStatystics - `{statystyki_status}` /settingsConfig statystyki\nAutoAD - `{autoad_status}` /settingsConfig autoad\nEconomy - `{ekonomia_status}` /settingsekonomia config\n\nOgólne:\n\nPolls - `{ankiety_status}` /settingsConfig ankiety\nSay - `{say_status}` /settings4fun say\n\nAdministracyjne:\n\nBan - `{ban_status}` /settingsAdm ban\nKick - `{kick_status}` /settingsAdm kick\nMute - `{mute_status}` /settingsAdm mute\nUnMute - `{unmute_status}` /settingsAdm unmute\nClear - `{clear_status}` /settingsAdm clear\nLogi - `{logi_status}` /settingsadm logi\nInviteLogger - `{invitelogger_status}` /settingsadm invitelogger\nGiveaway - `{giveaway_status}` /settingsadm giveaway\n\n4Fun:\n\nShip - `{ship_status}` /settings4Fun ship\nIQ - `{iq_status}` /settings4Fun iq\nKostka - `{kostka_status}` /settings4Fun kostka\nChatbot - `{chatbot_status}` /settings4Fun chatbot\nInfo - `{info_status}` /settings4Fun info\nMem - `{mem_status}` /settings4Fun mem\nGuess - `{zgaduj_status}` /settings4Fun zgaduj\nGlobalchat - `{globalchat_status}` /settings4Fun globalchat\nCounting - `{liczenie_status}` /settings4Fun liczenie\nLast letter - `{litera_status}` /settings4Fun litera\nCalculator - `{kalkulator_status}` /settings4Fun kalkulator", color=0xe40c0c)
            
                thumbnail_url = ctx.guild.icon.url if ctx.guild.icon else bot.user.avatar.url
                embed.set_thumbnail(url=thumbnail_url)
                    
                embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                embed.set_footer(text=f"Invoked by {author} | {current_time2}")
                await ctx.send(embed=embed)

            statistics = load_statistics()
            if 'settingsHelp' in statistics:
                statistics['settingsHelp'] += 1
            if 'all' in statistics:
                statistics['all'] += 1
            else:
                statistics['settingsHelp'] = 1
                statistics['all'] = 1
            save_statistics(statistics)
        else:
            time_left = cooldown_duration - time_difference
            await ctx.send(f"`[❌]:` Musisz poczekać jeszcze `{time_left.seconds} sekund` przed kolejnym użyciem komendy.", ephemeral=True)
    else:
        current_time = datetime.datetime.now()
        if cooldown_data:
            cooldowns_collection.update_one({"_id": user_id}, {"$set": {"settingsHelpCD": current_time}}, upsert=True)
        else:
            cooldowns_collection.insert_one({"_id": str(ctx.user.id), "settingsHelpCD": current_time})

        if lang == "PL":
            embed = nextcord.Embed(title=f"**Ustawienia {server_name}**", description=f"**Informacje:**\n\n**ID Serwera - *{server_id}***\n**Poziom - *{poziom}***\n**Node - *{node}***\n\n**Funkcje:**\n\n**Tickety - `{ticket_status}` /settingsConfig ticket**\n**Partnerstwa - `{partnerstwa_status}` /settingsConfig partnerstwa**\n**Anty @mention - `{antyMention_status}` /settingsConfig anty mention**\n**Anty link - `{antyLink_status}` /settingsConfig anty link**\n**Weryfikacja - `{weryfikacja_status}` /settingsConfig weryfikacja**\n\n**Ogólne:**\n\n**Ankiety - `{ankiety_status}` /settingsConfig ankiety**\n**Say - `{say_status}` /settingsConfig say**\n\n**Administracyjne:**\n\n**Ban - `{ban_status}` /settingsConfig ban**\n**Kick - `{kick_status}` /settingsConfig kick**\n**Mute - `{mute_status}` /settingsConfig mute**\n**UnMute - `{unmute_status}` /settingsConfig unmute**\n**Clear - `{clear_status}` /settingsConfig clear**\n\n**4Fun:**\n\n**Ship - `{ship_status}` /settingsConfig ship**\n**IQ - `{iq_status}` /settingsConfig iq**\n**Kostka - `{kostka_status}` /settingsConfig kostka**\n**Chatbot - `{chatbot_status}` /settingsConfig chatbot**\n**Info - `{info_status}` /settingsConfig info**\n**Mem - `{mem_status}` /settingsConfig mem**\n**zgaduj - `{zgaduj_status}` /settingsConfig zgaduj**", color=0xe40c0c)
        
            thumbnail_url = ctx.guild.icon.url if ctx.guild.icon else bot.user.avatar.url
            embed.set_thumbnail(url=thumbnail_url)
                
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time2}")
            await ctx.send(embed=embed)
        elif lang == "ENG":
            embed = nextcord.Embed(title=f"**{server_name} settings**", description=f"**Informacje:**\n\n**Server ID - *{server_id}***\n**Level - *{poziom}***\n**Node - *{node}***\n\n**Functions:**\n\n**Tickets - `{ticket_status}` /settingsConfig ticket**\n**Partnerships - `{partnerstwa_status}` /settingsConfig partnerstwa**\n**Anty @mention - `{antyMention_status}` /settingsConfig anty mention**\n**Anty link - `{antyLink_status}` /settingsConfig anty link**\n**Verification - `{weryfikacja_status}` /settingsConfig weryfikacja**\n\n**Ogólne:**\n\n**Polls - `{ankiety_status}` /settingsConfig ankiety**\n**Say - `{say_status}` /settingsConfig say**\n\n**Administracyjne:**\n\n**Ban - `{ban_status}` /settingsConfig ban**\n**Kick - `{kick_status}` /settingsConfig kick**\n**Mute - `{mute_status}` /settingsConfig mute**\n**UnMute - `{unmute_status}` /settingsConfig unmute**\n**Clear - `{clear_status}` /settingsConfig clear**\n\n**4Fun:**\n\n**Ship - `{ship_status}` /settingsConfig ship**\n**IQ - `{iq_status}` /settingsConfig iq**\n**Kostka - `{kostka_status}` /settingsConfig kostka**\n**Chatbot - `{chatbot_status}` /settingsConfig chatbot**\n**Info - `{info_status}` /settingsConfig info**\n**Mem - `{mem_status}` /settingsConfig mem**\n**zgaduj - `{zgaduj_status}` /settingsConfig zgaduj**", color=0xe40c0c)
        
            thumbnail_url = ctx.guild.icon.url if ctx.guild.icon else bot.user.avatar.url
            embed.set_thumbnail(url=thumbnail_url)
                
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time2}")
            await ctx.send(embed=embed)

        statistics = load_statistics()
        if 'settingsHelp' in statistics:
            statistics['settingsHelp'] += 1
        if 'all' in statistics:
            statistics['all'] += 1
        else:
            statistics['settingsHelp'] = 1
            statistics['all'] = 1
        save_statistics(statistics)

#Clear
@settingsadm.subcommand(description="Włącza/Wyłącza clear")
async def clear(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        server_id = str(ctx.guild.id)

        if settings_document:
            current_status = settings_document.get("clear", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'clear': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'clear': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Komenda `clear` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "turned on" if new_status else "turned off"
            await ctx.send(f"`[✅]:` The `clear` command has been {status_text} for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `clear`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `clear`!", ephemeral=True)

#Say
@settings4fun.subcommand(description="Włącza/Wyłącza say")
async def say(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        server_id = str(ctx.guild.id)

        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            current_status = settings_document.get("say", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'say': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'say': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Komenda `say` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "turned on" if new_status else "turned off"
            await ctx.send(f"`[✅]:` The `say` command has been {status_text} for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `say`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `say`!", ephemeral=True)

#Ship
@settings4fun.subcommand(description="Włącza/Wyłącza ship")
async def ship(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        server_id = str(ctx.guild.id)

        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            current_status = settings_document.get("ship", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'ship': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'ship': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Komenda `ship` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "turned on" if new_status else "turned off"
            await ctx.send(f"`[✅]:` The `ship` command has been {status_text} for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `ship`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `ship`!", ephemeral=True)

#Iq
@settings4fun.subcommand(description="Włącza/Wyłącza iq")
async def iq(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:

        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            current_status = settings_document.get("iq", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'iq': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'iq': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Komenda `iq` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "turned on" if new_status else "turned off"
            await ctx.send(f"`[✅]:` The `iq` command has been {status_text} for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `iq`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `iq`!", ephemeral=True)

#Kostka
@settings4fun.subcommand(description="Włącza/Wyłącza kostka")
async def kostka(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:

        if settings_document:
            current_status = settings_document.get("kostka", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'kostka': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'kostka': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Komenda `kostka` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "turn on" if new_status else "turn off"
            await ctx.send(f"`[✅]:` The `kostka` command has been {status_text} for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `kostka`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `kostka`!", ephemeral=True)

#Ankiety
@settingsconfig.subcommand(description="Wyświetla konfigurację ankiet")
async def ankiety(ctx):
    author = ctx.user
    server_id = str(ctx.guild.id)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    settings_document = settings_collection.find_one({'_id': server_id})

    if not settings_document:
        settings_document = {'_id': server_id}

    if settings_document.get('ankiety', False):
        ticket_status = "on"
    else:
        ticket_status = "off"

    idkanalu_lista = settings_document.get('kanalyAnkiet', [])

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if lang == "PL":
        view = Wylaczanie_Wlaczanie_ankiet()
        if idkanalu_lista and isinstance(idkanalu_lista, list):  # Sprawdza, czy idkanalu_lista istnieje i czy to lista
            channels = [f"<#{channel}>" for channel in idkanalu_lista]
            channels_text = "\n".join(channels)
            embed = nextcord.Embed(title=f'**/ankieta settings**', description=f"\n**Status `{ticket_status}`**\n**Kanały: {channels_text}**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**/ankieta settings**', description=f"**Status `{ticket_status}`**\n**Kanał: `None`**\n\n**Command `/settingsConfig kanal ankietyadd`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
    elif lang == "ENG":
        view = Wylaczanie_Wlaczanie_ankietENG()
        if idkanalu_lista and isinstance(idkanalu_lista, list):  # Sprawdza, czy idkanalu_lista istnieje i czy to lista
            channels = [f"<#{channel}>" for channel in idkanalu_lista]
            channels_text = "\n".join(channels)
            embed = nextcord.Embed(title=f'**/ankieta settings**', description=f"\n**Status `{ticket_status}`**\n**Channels: {channels_text}**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**/ankieta settings**', description=f"**Status `{ticket_status}`**\n**Channel: `None`**\n\n**Command `/settingsConfig kanal ankietyadd`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)

#Kanal
@settingsconfig.subcommand(description="Ustawia kanał")
async def kanal(ctx):
    await ctx.send("XDX")

#Rola_
@settingsconfig.subcommand(description="Ustawia rolę")
async def rola_(ctx):
    await ctx.send("XDX")

#Wiadomosc
@settingsconfig.subcommand(description="Ustawia wiadomość")
async def wiadomosc(ctx):
    await ctx.send("XDX")

#Ankiety
@kanal.subcommand(description="Dodaje kanał ankiet")
async def ankietyadd(ctx, kanał: nextcord.TextChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    
    if not settings_document:
        settings_document = {'_id': server_id}

    if 'language' in settings_document:
        lang = settings_document['language']
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:
        if kanał.permissions_for(ctx.guild.me).send_messages:
            if 'kanalyAnkiet' not in settings_document:
                settings_document['kanalyAnkiet'] = []

            settings_document['kanalyAnkiet'].append(kanał.id)

            settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

            if lang == "PL":
                await ctx.send(f"`[✅]:` Kanał komendy `ankieta` dodany: <#{kanał.id}>", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Channel for the `ankieta` command added: <#{kanał.id}>", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Bot nie posiada uprawnień do wysyłania wiadomości!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` The bot does not have permission to send messages!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić kanał dla `ankieta`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set up a channel for `ankieta`!", ephemeral=True)

#Ankiety
@kanal.subcommand(description="Usuwa kanał ankiet")
async def ankietyremove(ctx, kanał: nextcord.TextChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if not settings_document or 'kanalyAnkiet' not in settings_document or not settings_document['kanalyAnkiet']:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"

        if lang == "PL":
            await ctx.send("`[❌]:` Brak kanałów do usunięcia dla komendy `ankieta`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` No channels to remove for the `ankieta` command!", ephemeral=True)
        return

    if ctx.user.guild_permissions.manage_channels:
        if kanał.id in settings_document['kanalyAnkiet']:
            settings_document['kanalyAnkiet'].remove(kanał.id)
            settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

            if lang == "PL":
                await ctx.send(f"`[✅]:` Kanał komendy `ankieta` usunięty: <#{kanał.id}>", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Channel for the `ankieta` command removed: <#{kanał.id}>", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Podany kanał nie jest ustawiony dla komendy `ankieta`!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` The provided channel is not set for the `ankieta` command!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby usunąć kanał dla `ankieta`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to remove a channel for `ankieta`!", ephemeral=True)

#Chatbot
@settings4fun.subcommand(description="Włącza/Wyłącza chatbota")
async def chatbot(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        server_id = str(ctx.guild.id)

        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            current_status = settings_document.get("chatbot", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'chatbot': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'chatbot': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Komenda `chatbot` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "turned on" if new_status else "turned off"
            await ctx.send(f"`[✅]:` The `chatbot` command has been {status_text} for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `chatbot`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set up `chatbot` command!", ephemeral=True)

#Ban
@settingsadm.subcommand(description="Włącza/Wyłącza bany")
async def ban(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.ban_members:
        server_id = str(ctx.guild.id)

        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            current_status = settings_document.get("ban", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'ban': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'ban': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Komenda `ban` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "turned on" if new_status else "turned off"
            await ctx.send(f"`[✅]:` The `ban` command has been {status_text} for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `ban members` aby włączyć/wyłączyć `ban`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `ban members` permission to set `ban` command!", ephemeral=True)

#Kick
@settingsadm.subcommand(description="Włącza/Wyłącza kick")
async def kick(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.kick_members:
        server_id = str(ctx.guild.id)

        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            current_status = settings_document.get("kick", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'kick': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'kick': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Komenda `kick` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "turned on" if new_status else "turned off"
            await ctx.send(f"`[✅]:` The `kick` command has been {status_text} for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `kick members` aby włączyć/wyłączyć `kick`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `kick members` permission to set `kick` command!", ephemeral=True)

#Tickety
@settingsconfig.subcommand(description="Wyświetla konfigurację ticketów")
async def ticket(ctx):
    server_id = str(ctx.guild.id)
    author = ctx.user
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document:
        settings_document = {'_id': server_id}

    if settings_document.get('tickety', False):
        ticket_status = "on"
    else:
        ticket_status = "off"

    if settings_document.get('kategoriaOtwieraniaTicketow'):
        idkategoriiDB = settings_document.get('kategoriaOtwieraniaTicketow')
        kategoria = bot.get_channel(idkategoriiDB)
        idkategorii = f"{kategoria.mention}"
    else:
        idkategorii = "`Brak - /settingsconfig kategoria tickety`"

    if settings_document.get('ticketyEveryone', False):
        everyone_status = "on"
    else:
        everyone_status = "off - /settingsconfig ping tickety"

    idkanalu = settings_document.get('kanalOtwieraniaTicketow')

    if lang == "PL":
        view = Wylaczanie_Wlaczanie_ticketow()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Ustawienia ticketów**', description=f"\n**Status `{ticket_status}`**\n**Kanał otwierania: <#{idkanalu}>**\n**Kategoria - {idkategorii}**\n**Ping everyone - `{everyone_status}`**\n\n**WAŻNE:**\n**Jeżeli nie używasz naszego systemu weryfikacji, bot nie może zabrać dostępu do ticketów zweryfikowanym (Wyłącz całą weryfikację, użyj naszej lub zblackklistuj rolę)**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Ustawienia ticketów**', description=f"**Status `{ticket_status}`**\n**Kanał otwierania: <#{idkanalu}>**\n**Kategoria - {idkategorii}**\n**Ping everyone - `{everyone_status}`**\n\n**WAŻNE:**\n**Jeżeli nie używasz naszego systemu weryfikacji, bot nie może zabrać dostępu do ticketów zweryfikowanym (Wyłącz całą weryfikację, użyj naszej lub zblackklistuj rolę)**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Ustawienia ticketów**', description=f"**Status `{ticket_status}`**\n**Kanał otwierania: `Brak`**\n**Kategoria - {idkategorii}**\n**Ping everyone - `{everyone_status}`**\n\n**Komenda `/settingsConfig kanal tickety`**\n\n**WAŻNE:**\n**Jeżeli nie używasz naszego systemu weryfikacji, bot nie może zabrać dostępu do ticketów zweryfikowanym (Wyłącz całą weryfikację, użyj naszej lub zblackklistuj rolę)**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
    elif lang == "ENG":
        view = Wylaczanie_Wlaczanie_ticketowENG()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Ticket settings**', description=f"\n**Status `{ticket_status}`**\n**Opening channel: <#{idkanalu}>**\n**Category - {idkategorii}**\n**Ping everyone - `{everyone_status}`**\n\n**IMPORTANT:**\n**If you do not use our verification system, the bot cannot take away access to verified users (Disable all verification, use our or blacklist role)**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Ticket settings**', description=f"**Status `{ticket_status}`**\n**Opening channel: <#{idkanalu}>**\n**Category - {idkategorii}**\n**Ping everyone - `{everyone_status}`**\n\n**IMPORTANT:**\n**If you do not use our verification system, the bot cannot take away access to verified users (Disable all verification, use our or blacklist role)**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Ticket settings**', description=f"**Status `{ticket_status}`**\n**Opening channel: `Brak`**\n**Category - {idkategorii}**\n**Ping everyone - `{everyone_status}`**\n\n**Command `/settingsConfig kanal tickety`**\n\n**IMPORTANT:**\n**If you do not use our verification system, the bot cannot take away access to verified users (Disable all verification, use our or blacklist role)**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)

class YourCustomTicketView(nextcord.ui.View):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, guild_id, timeout=None):
        super().__init__(timeout=timeout)
        self.guild_id = guild_id
        self.setup_buttons()

    def setup_buttons(self):
        server_id = str(self.guild_id)
        settings_document = settings_collection.find_one({'_id': server_id})

        if not settings_document:
            settings_document = {'_id': server_id}

        button_list = settings_document.get('ticketButtons', [])
        for button_data in button_list:
            button_text = button_data.get('tekst', 'Default Text')
            button_ping = button_data.get('ping', 'Brak')
            button_color = button_data.get('kolor', 'niebieski')
            button_premission = button_data.get('uprawnienia', 'Brak')
            custom_id = f"Button-{button_text.replace(' ', '-')}"

            if button_color == "czerwony" or button_color == "red":
                style = nextcord.ButtonStyle.red
            elif button_color == "zielony" or button_color == "green":
                style = nextcord.ButtonStyle.green
            elif button_color == "niebieski" or button_color == "blue":
                style = nextcord.ButtonStyle.blurple
            elif button_color == "szary" or button_color == "gray":
                style = nextcord.ButtonStyle.gray

            async def button_callback(interaction, button_label=button_text):
                await self.handle_button(interaction, button_label, button_ping, button_premission)

            button_callback.__name__ = f"button_callback_{custom_id}"
            
            button = nextcord.ui.Button(label=button_text, custom_id=custom_id, style=style)
            button.callback = button_callback
            self.add_item(button)

    async def handle_button(self, interaction, button_text, button_ping, button_premission):
        server_id = str(interaction.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        if settings_document:
            if 'language' in settings_document:
                lang = settings_document['language']
            else:
                lang = "PL"
        else:
            lang = "PL"

        if lang == "PL":
            if settings_document and not settings_document.get("premium", False):
                await interaction.send(f"`[❌]:` Ten serwer nie posiada premium, które jest wymagane do działania `custom buttons`! Jeżeli to pomyłka, dołącz na nasz serwer support i otwórz ticket!", ephemeral=True)
                return
            
            if settings_document and settings_document.get("tickety", False):
                user_document = users_collection.find_one({'_id': str(interaction.user.id)})
                if user_document and 'mutes' in user_document:
                    current_time_mute = datetime.datetime.now()

                    for mute_info in user_document['mutes']:
                        sid = mute_info.get('server_id')
                        if sid == server_id:
                            end_time = mute_info.get('end_time')
                            if end_time and end_time > current_time_mute:
                                user = interaction.user
                                remaining_time = end_time - current_time_mute
                                remaining_time_str = str(remaining_time).split('.')[0]
                                remaining_time_str = remaining_time_str.replace(" days, ", "d ").replace(" day, ", "d ")
                                remaining_time_str = remaining_time_str.replace(":00:00", "h").replace(":00", "m")

                                await interaction.send(f"`[❌]:` {user.mention}, masz aktywne wyciszenie, poczekaj jeszcze `{remaining_time_str}`", ephemeral=True)
                                return

                guild = interaction.guild                    
                if settings_document.get("kategoriaOtwieraniaTicketow", False):
                    kategoriaID = settings_document.get("kategoriaOtwieraniaTicketow", False)
                    kategoria = guild.get_channel(kategoriaID)
                else:
                    kategoria = guild

                channel_name = f"ticket-{interaction.user.name}"
                ticket_channel = nextcord.utils.get(kategoria.channels, name=channel_name)
                        
                if not ticket_channel:
                    user_id = interaction.user.id

                    guild = bot.get_guild(interaction.guild.id)
                    user = await guild.fetch_member(user_id)
                    overwrites = {}

                    if kategoria != guild:
                        for target, overwrite in kategoria.overwrites.items():
                            overwrites[target] = overwrite

                    if settings_document and settings_document.get("weryfikacja", False):
                        idroli = settings_document.get("rolaWeryfikacji", False)
                        rola = interaction.guild.get_role(idroli)
                    else:
                        rola = None

                    if 'ticketWLRoles' in settings_document:
                        for role_id in settings_document['ticketWLRoles']:
                            role = guild.get_role(int(role_id))
                            if role:
                                overwrites[role] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)

                    if 'ticketBLRoles' in settings_document:
                        for role_id in settings_document['ticketBLRoles']:
                            role = guild.get_role(int(role_id))
                            if role:
                                overwrites[role] = nextcord.PermissionOverwrite(read_messages=False)

                    if settings_document and settings_document.get("ticketyEveryone", False):
                        ping = True
                    else:
                        ping = False

                    button_role = None
                    button_ping = None
                    if settings_document and settings_document.get("tickety", False):
                        for button_data in settings_document.get('ticketButtons', []):
                            if button_data.get('tekst') == button_text or button_data.get('tekst').replace(' ', '-') == button_text:
                                button_pingDB = str(button_data.get('ping', 'Brak'))
                                if button_pingDB != "Brak":
                                    button_ping = guild.get_role(int(button_pingDB))

                                button_roleDB = str(button_data.get('uprawnienia', 'Brak'))
                                if button_roleDB != "Brak":
                                    button_role = guild.get_role(int(button_roleDB))
                                break

                    overwrites[user] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
                    if rola != None:
                        overwrites[rola] = nextcord.PermissionOverwrite(read_messages=False)
                    overwrites[guild.default_role] = nextcord.PermissionOverwrite(read_messages=False)
                    if button_role != None:
                        overwrites[button_role] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
                    if button_ping != None:
                        overwrites[button_ping] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)

                    ticket_channel = await kategoria.create_text_channel(f"Ticket-{interaction.user.name}", overwrites=overwrites)

                    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    stworzył = f"<t:{int(interaction.user.created_at.timestamp())}:R>"
                    dołączył = f"<t:{int(interaction.user.joined_at.timestamp())}:R>"

                    button_text2 = button_text.replace('-', ' ')
                    embed = nextcord.Embed(title=f'**{button_text2}**', description=f"**Aby zamknąć ticket kliknij przycisk `🔒 Zamknij`**\n\n**Autorem jest {interaction.user.mention} (*{interaction.user.id}*)**\n**Na serwer dołączył** {dołączył}\n**Na Discord dołączył** {stworzył}", color=0x00ff00)
                    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                    embed.set_thumbnail(url=bot.user.avatar.url)
                    embed.set_footer(text=f"{current_time}")
                    view = Zamykanie_ticketu(user=interaction.user)
                    if button_ping != None:
                        await ticket_channel.send(f"{button_ping.mention}", embed=embed, view=view)
                    else:
                        if ping == True:
                            await ticket_channel.send("@everyone", embed=embed, view=view)
                        else:
                            await ticket_channel.send(embed=embed, view=view)

                    await interaction.send(f"`[✅]:` Ticket stworzony! {ticket_channel.mention}", ephemeral=True)

                    statistics = load_statistics()
                    if 'tickety' in statistics:
                        statistics['tickety'] += 1
                    else:
                        statistics['tickety'] = 1
                    save_statistics(statistics)
                else:
                    await interaction.send(f"`[✅]:` Masz już jeden ticket! {ticket_channel.mention}", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Tickety są wyłączone na tym serwerze", ephemeral=True)

        elif lang == "ENG":
            server_id = str(interaction.guild.id)
            settings_document = settings_collection.find_one({'_id': server_id})
            user_document = users_collection.find_one({'_id': str(interaction.user.id)})
            if settings_document and not settings_document.get("premium", False):
                await interaction.send(f"`[❌]:` Ten serwer nie posiada premium, które jest wymagane do działania `custom buttons`! Jeżeli to pomyłka, dołącz na nasz serwer support i otwórz ticket!", ephemeral=True)
                return

            if settings_document and settings_document.get("tickety", False):
                if user_document and 'mutes' in user_document:
                    current_time_mute = datetime.datetime.now()

                    for mute_info in user_document['mutes']:
                        sid = mute_info.get('server_id')
                        if sid == server_id:
                            end_time = mute_info.get('end_time')
                            if end_time and end_time > current_time_mute:
                                user = interaction.user
                                remaining_time = end_time - current_time_mute
                                remaining_time_str = str(remaining_time).split('.')[0]
                                remaining_time_str = remaining_time_str.replace(" days, ", "d ").replace(" day, ", "d ")
                                remaining_time_str = remaining_time_str.replace(":00:00", "h").replace(":00", "m")

                                await interaction.send(f"`[❌]:` {user.mention}, you have active mute, wait `{remaining_time_str}`", ephemeral=True)
                                return

                guild = interaction.guild
                if settings_document.get("kategoriaOtwieraniaTicketow", False):
                    kategoriaID = settings_document.get("kategoriaOtwieraniaTicketow", False)
                    kategoria = guild.get_channel(kategoriaID)
                else:
                        kategoria = guild

                channel_name = f"ticket-{interaction.user.name}"
                ticket_channel = nextcord.utils.get(kategoria.channels, name=channel_name)
                        
                if not ticket_channel:
                    user_id = interaction.user.id

                    guild = bot.get_guild(interaction.guild.id)
                    user = await guild.fetch_member(user_id)
                    overwrites = {}

                    if kategoria != guild:
                        for target, overwrite in kategoria.overwrites.items():
                            overwrites[target] = overwrite

                    if settings_document and settings_document.get("weryfikacja", False):
                        idroli = settings_document.get("rolaWeryfikacji", False)
                        rola = interaction.guild.get_role(idroli)
                    else:
                        rola = None

                    if 'ticketWLRoles' in settings_document:
                        for role_id in settings_document['ticketWLRoles']:
                            role = guild.get_role(int(role_id))
                            if role:
                                overwrites[role] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)

                    if 'ticketBLRoles' in settings_document:
                        for role_id in settings_document['ticketBLRoles']:
                            role = guild.get_role(int(role_id))
                            if role:
                                overwrites[role] = nextcord.PermissionOverwrite(read_messages=False)

                    if settings_document and settings_document.get("ticketyEveryone", False):
                        ping = True
                    else:
                        ping = False

                    button_role = None
                    button_ping = None
                    if settings_document and settings_document.get("tickety", False):
                        for button_data in settings_document.get('ticketButtons', []):
                            if button_data.get('tekst') == button_text or button_data.get('tekst').replace(' ', '-') == button_text:
                                button_pingDB = str(button_data.get('ping', 'Brak'))
                                if button_pingDB != "Brak":
                                    button_ping = guild.get_role(int(button_pingDB))

                                button_roleDB = str(button_data.get('uprawnienia', 'Brak'))
                                if button_roleDB != "Brak":
                                    button_role = guild.get_role(int(button_roleDB))
                                break

                    overwrites[user] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
                    if rola != None:
                        overwrites[rola] = nextcord.PermissionOverwrite(read_messages=False)
                    overwrites[guild.default_role] = nextcord.PermissionOverwrite(read_messages=False)
                    if button_role != None:
                        overwrites[button_role] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
                    if button_ping != None:
                        overwrites[button_ping] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)

                    ticket_channel = await kategoria.create_text_channel(f"Ticket-{interaction.user.name}", overwrites=overwrites)

                    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    stworzył = f"<t:{int(interaction.user.created_at.timestamp())}:R>"
                    dołączył = f"<t:{int(interaction.user.joined_at.timestamp())}:R>"

                    button_text2 = button_text.replace('-', ' ')
                    embed = nextcord.Embed(title=f'**{button_text2}**', description=f"**To close the ticket, click the `🔒 Close` button**\n\n**Author {interaction.user.mention} (*{interaction.user.id}*)**\n**Joined the server** {dołączył}\n**Joined on Discord** {stworzył}", color=0x00ff00)
                    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                    embed.set_thumbnail(url=bot.user.avatar.url)
                    embed.set_footer(text=f"{current_time}")
                    view = Zamykanie_ticketuENG()
                    if button_ping != "Brak":
                        await ticket_channel.send(f"{button_ping.mention}", embed=embed, view=view)
                    else:
                        if ping == True:
                            await ticket_channel.send("@everyone", embed=embed, view=view)
                        else:
                            await ticket_channel.send(embed=embed, view=view)

                    await interaction.send(f"`[✅]:` Ticket created! {ticket_channel.mention}", ephemeral=True)

                    statistics = load_statistics()
                    if 'tickety' in statistics:
                        statistics['tickety'] += 1
                    else:
                        statistics['tickety'] = 1
                    save_statistics(statistics)
                else:
                    await interaction.send(f"`[✅]:` You already have one ticket! {ticket_channel.mention}", ephemeral=True)
            else:
                await interaction.send("`[❌]:` Tickets are disabled on this server", ephemeral=True)

#Tickety
@kanal.subcommand(description="Ustawia kanał ticketów")
async def tickety(ctx, kanał: nextcord.TextChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    try:
        if ctx.user.guild_permissions.manage_channels:
            if kanał.permissions_for(ctx.guild.me).send_messages:
                server_id = str(ctx.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if not settings_document:
                    settings_document = {'_id': server_id}

                settings_document['kanalOtwieraniaTicketow'] = kanał.id

                settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

                if lang == "PL":
                    await ctx.send(f"`[✅]:` Kanał otwierania funkcji `tickety`: <#{kanał.id}>", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[✅]:` Opening channel of the `tickets` function: <#{kanał.id}>", ephemeral=True)

                button_list = settings_document.get('ticketButtons', [])
                if lang == "PL":
                    embed = nextcord.Embed(title=f'**TICKET**', description="**Aby otworzyć ticket kliknij przycisk `🎫 Otwórz ticket`**", color=0x00ff00)
                    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                    embed.set_image(url="https://dreambot.pl/DreamBotImages/ticket.gif")
                    if button_list:
                        view = YourCustomTicketView(guild_id=ctx.guild.id)
                        bot.add_view(view)
                    else:
                        view = Otwieranie_ticketu()

                    await kanał.send(embed=embed, view=view)
                elif lang == "ENG":
                    embed = nextcord.Embed(title=f'**TICKET**', description="**To open a ticket, click the `🎫 Open ticket` button**", color=0x00ff00)
                    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                    embed.set_image(url="https://dreambot.pl/DreamBotImages/ticket.gif")
                    if button_list:
                        view = YourCustomTicketView(guild_id=ctx.guild.id)
                        bot.add_view(view)
                    else:
                        view = Otwieranie_ticketuENG()

                    await kanał.send(embed=embed, view=view)
            else:
                if lang == "PL":
                    await ctx.send(f"`[❌]:` Bot nie posiada uprawnień do wysyłania wiadomości!", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[❌]:` The bot does not have permission to send messages!", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić kanał dla `tickety`!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` You do not have the `manage channels` permission to set the channel for `tickets`!", ephemeral=True)                
    except nextcord.errors.Forbidden:
        if lang == "PL":
            await ctx.send("`[❌]:` Bot nie ma wystarczających uprawnień do wysłania wiadomości na tym kanale.")
        elif lang == "ENG":
            await ctx.send("`[❌]:` The bot does not have sufficient permissions to send messages in this channel.")

#Kategoria
@settingsconfig.subcommand(description="Ustawia kanał ticketów")
async def kategoria(ctx):
    await ctx.send("Nima")

#Ping
@settingsconfig.subcommand(description="Ustawia ping ticketów")
async def ping(ctx):
    await ctx.send("Nima")

#Tickety
@ping.subcommand(description="Włącza/Wyłącza ping everyone na ticketach!")
async def tickety(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        server_id = str(ctx.guild.id)

        if settings_document:
            current_status = settings_document.get("ticketyEveryone", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'ticketyEveryone': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'ticketyEveryone': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Funkcja `ping everyone` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "turned on" if new_status else "turned off"
            await ctx.send(f"`[✅]:` The `ping everyone` function has been {status_text} for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `ping everyone`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `ping everyone`!", ephemeral=True)

#Tickety
@kategoria.subcommand(description="Ustawia kategorię ticketów")
async def tickety(ctx, kategoria: nextcord.CategoryChannel, kategoriazamkniecia: nextcord.CategoryChannel = nextcord.SlashOption(description="Ustawia kategorię do jakiej mają trafiać zamknięte tickety (Premium ⭐)")):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:
        server_id = str(ctx.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})
        if not settings_document:
            settings_document = {'_id': server_id}

        premium = settings_document.get('premium')
        if premium == True:
            settings_document['kategoriaZamykaniaTicketow'] = kategoriazamkniecia.id

        settings_document['kategoriaOtwieraniaTicketow'] = kategoria.id
        settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

        if premium == True:
            if lang == "PL":
                await ctx.send(f"`[✅]:` Kategoria otwierania funkcji `tickety`: <#{kategoria.id}>, zamykania: <#{kategoriazamkniecia.id}>", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` The category of opening the `tickets` function: <#{kategoria.id}>, closing <#{kategoriazamkniecia.id}>", ephemeral=True)
            return

        if lang == "PL":
            await ctx.send(f"`[✅]:` Kategoria otwierania funkcji `tickety`: <#{kategoria.id}>", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` The category of opening the `tickets` function: <#{kategoria.id}>", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić kategorię dla `tickety`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set the category for `tickets`!", ephemeral=True)

#Mute
@settingsadm.subcommand(description="Włącza/Wyłącza mute")
async def mute(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.mute_members:
        server_id = str(ctx.guild.id)

        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            current_status = settings_document.get("mute", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'mute': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'mute': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Komenda `mute` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "turned on" if new_status else "turned off"
            await ctx.send(f"`[✅]:` The `mute` command has been {status_text} for this server.", ephemeral=True)
    else:
        await ctx.send("`[❌]:` You do not have the `mute members` permission to enable/disable `mute`!", ephemeral=True)

#Unmute
@settingsadm.subcommand(description="Włącza/Wyłącza unmute")
async def unmute(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.mute_members:
        server_id = str(ctx.guild.id)

        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            current_status = settings_document.get("unmute", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'unmute': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'unmute': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Komenda `unmute` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "turned on" if new_status else "turned off"
            await ctx.send(f"`[✅]:` The `unmute` command has been {status_text} for this server.", ephemeral=True)
    else:
        await ctx.send("`[❌]:` You do not have the `mute members` permission to enable/disable `unmute`!", ephemeral=True)

#Info
@settings4fun.subcommand(description="Włącza/Wyłącza info")
async def info(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        server_id = str(ctx.guild.id)

        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            current_status = settings_document.get("info", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'info': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'info': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Komenda `info` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` The `info` command has been {status_text} for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `info`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `info`!", ephemeral=True)

#Partnerstwa
@settingsconfig.subcommand(description="Wyświetla konfigurację partnerstw")
async def partnerstwa(ctx):
    author = ctx.user
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if settings_document:
        partnerstwa_status = settings_document.get("partnerstwa", False)
        kanalPartnerstw = settings_document.get("kanalPartnerstw")
        rolaPartnerstw = settings_document.get("rolaPartnerstw")
    else:
        partnerstwa_status = False
        kanalPartnerstw = None
        rolaPartnerstw = None

    if partnerstwa_status == True:
        partnerstwa_status = "on"
    else:
        partnerstwa_status = "off"

    if kanalPartnerstw:
        idkanalu = kanalPartnerstw
        idkanalu_str_cleaned = str(idkanalu)
    else:
        idkanalu = None
        idkanalu_str_cleaned = None

    if rolaPartnerstw:
        idroli = rolaPartnerstw
        idroli_str_cleaned = str(idroli)
    else:
        idroli = None
        idroli_str_cleaned = None

    if lang == "PL":
        view = Wylaczanie_Wlaczanie_partnerstw()
        if idkanalu_str_cleaned and idroli_str_cleaned and partnerstwa_status == "on":
            embed = nextcord.Embed(title=f'**Ustawienia partnerstw**', description=f"\n**Status `{partnerstwa_status}`**\n**Kanał: <#{idkanalu}>**\n**Rola: <@&{idroli}>**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu_str_cleaned:
            embed = nextcord.Embed(title=f'**Ustawienia partnerstw**', description=f"**Status `{partnerstwa_status}`**\n**Kanał: <#{idkanalu}>**\n**Rola: `Brak`**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Ustawienia partnerstw**', description=f"**Status `{partnerstwa_status}`**\n**Kanał: `Brak`**\n**Rola: `Brak`**\n\n**Komendy:**\n`/settingsConfig kanal partnerstwa`\n`/settingsconfig rola partnerstwa`", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
    elif lang == "ENG":
        view = Wylaczanie_Wlaczanie_partnerstwENG()
        if idkanalu_str_cleaned and idroli_str_cleaned and partnerstwa_status == "on":
            embed = nextcord.Embed(title=f'**Partnership settings**', description=f"\n**Status `{partnerstwa_status}`**\n**Channel: <#{idkanalu}>**\n**Role: <@&{idroli}>**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu_str_cleaned:
            embed = nextcord.Embed(title=f'**Partnership settings**', description=f"**Status `{partnerstwa_status}`**\n**Channel: <#{idkanalu}>**\n**Role: `None`**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Partnership settings**', description=f"**Status `{partnerstwa_status}`**\n**Channel: `None`**\n**Role: `None`**\n\n**Commands:**\n`/settingsConfig kanal partnerstwa`\n`/settingsconfig rola partnerstwa`", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)

#Partnerstwa
@kanal.subcommand(description="Ustawia kanał partnerstw")
async def partnerstwa(ctx, kanał: nextcord.TextChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"
    
    if ctx.user.guild_permissions.manage_channels:
        if kanał.permissions_for(ctx.guild.me).send_messages:
            server_id = str(ctx.guild.id)

            settings_document = settings_collection.find_one({'_id': server_id})

            if settings_document:
                settings_collection.update_one({'_id': server_id}, {'$set': {'kanalPartnerstw': kanał.id}})

                if lang == "PL":
                    await ctx.send(f"`[✅]:` Kanał otwierania funkcji `partnerstwa`: <#{kanał}>", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[✅]:` Opening channel of the `partnership` feature: <#{kanał}>", ephemeral=True)
            else:
                new_settings_document = {'_id': server_id, 'kanalPartnerstw': kanał.id}
                settings_collection.insert_one(new_settings_document)

                if lang == "PL":
                    await ctx.send(f"`[✅]:` Kanał otwierania funkcji `partnerstwa`: <#{kanał}>", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[✅]:` Opening channel of the `partnership` feature: <#{kanał}>", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Bot nie posiada uprawnień do wysyłania wiadomości!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` The bot does not have permission to send messages!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić kanał dla `partnerstwa`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set up a channel for `partnership`!", ephemeral=True)

#Partnerstwa
@rola_.subcommand(description="Ustawia rolę partnerstw (Nadaje ją partnerowi z którym robisz partnerstwo)")
async def partnerstwa(ctx, partner: nextcord.Role):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"
    
    if ctx.user.guild_permissions.manage_channels:
        server_id = str(ctx.guild.id)

        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            settings_collection.update_one({'_id': server_id}, {'$set': {'rolaPartnerstw': partner.id}})

            if lang == "PL":
                await ctx.send(f"`[✅]:` Rola funkcji `partnerstwa`: <@&{partner.id}>", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Role of the `partnership` feature: <#&{partner.id}>", ephemeral=True)
        else:
            new_settings_document = {'_id': server_id, 'rolaPartnerstw': partner.id}
            settings_collection.insert_one(new_settings_document)

            if lang == "PL":
                await ctx.send(f"`[✅]:` Rola funkcji `partnerstwa`: <#&{partner.id}>", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Role of the `partnership` feature: <#&{partner.id}>", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić rolę dla `partnerstwa`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set up a role for `partnership`!", ephemeral=True)

#Parnterstwa
@settingsconfig.subcommand(description="Partnerstwa")
async def _partnerstwa(ctx):
    await ctx.send("XDX")

#Stawka
@_partnerstwa.subcommand(description="Ustawia stawkę za partnerstwa")
async def stawka(ctx, stawka):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if settings_document:
        partnerstwa_enabled = settings_document.get("partnerstwa", False)
        
        if partnerstwa_enabled:
            if ctx.user.guild_permissions.manage_messages:
                server_id = str(ctx.guild.id)
                db.settings.update_one({"_id": server_id}, {"$set": {"stawkaPartnerstwa": stawka}}, upsert=True)
                
                if lang == "PL":
                    await ctx.send(f'`[✅]:` Stawka `partnerstw` została ustawiona na `{stawka}`!', ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f'`[✅]:` The `partnerships` rate has been set to `{stawka}`!', ephemeral=True)
            else:
                if lang == "PL":
                    await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby ustawić stawkę `partnerstw`!", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send("`[❌]:` You do not have the `manage messages` permission to set the `partnership` rate!", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Funkcja `partnerstwa` nie jest włączona dla tego serwera.", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` The 'partnership' feature is not enabled for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Funkcja `partnerstwa` nie jest włączona dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` The 'partnership' feature is not enabled for this server.", ephemeral=True)
#Mem
@settings4fun.subcommand(description="Włącza/Wyłącza mem")
async def mem(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        server_id = str(ctx.guild.id)

        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            current_status = settings_document.get("mem", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'mem': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'mem': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Komenda `mem` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "turned on" if new_status else "turned off"
            await ctx.send(f"`[✅]:` The `mem` command has been {status_text} for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `mem`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `mem`!", ephemeral=True)

#Weryfikacja
@rola_.subcommand(description="Ustawia rolę weryfikacji")
async def weryfikacja(ctx, rola: nextcord.Role):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:
        if ctx.guild.me.guild_permissions.manage_roles:
            server_id = str(ctx.guild.id)

            settings_document = settings_collection.find_one({'_id': server_id})

            if settings_document:
                settings_collection.update_one({'_id': server_id}, {'$set': {'rolaWeryfikacji': rola.id}})

                if lang == "PL":
                    await ctx.send(f"`[✅]:` Rola `weryfikacji`: {rola}", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[✅]:` Role of `verification`: {rola}", ephemeral=True)
            else:
                new_settings_document = {'_id': server_id, 'rolaWeryfikacji': rola.id}
                settings_collection.insert_one(new_settings_document)
                if lang == "PL":
                    await ctx.send(f"`[✅]:` Rola `weryfikacji`: {rola}", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[✅]:` Role of `verification`: {rola}", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Bot nie posiada uprawnień do zarządzania rolami!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` The bot does not have permissions to manage roles!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić rolę dla `weryfikacja`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set the role for `verify`!", ephemeral=True)

#Weryfikacja
@kanal.subcommand(description="Ustawia kanał weryfikacji")
async def weryfikacja(ctx, kanał: nextcord.TextChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:
        if kanał.permissions_for(ctx.guild.me).send_messages:
            server_id = str(ctx.guild.id)

            settings_document = settings_collection.find_one({'_id': server_id})

            if not settings_document:
                settings_document = {'_id': server_id}

            settings_document['kanalWeryfikacji'] = kanał.id

            settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

            if lang == "PL":
                await ctx.send(f"`[✅]:` Kanał funkcji `weryfikacja`: <#{kanał.id}>", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Function channel `verification`: <#{kanał.id}>", ephemeral=True)

            if lang == "PL":
                embed = nextcord.Embed(title=f'**WERYFIKACJA**', description="**Aby się zweryfikować kliknij `✅ Zweryfikuj`**", color=0x00ff00)
                embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                embed.set_thumbnail(url=bot.user.avatar.url)
                embed.set_image(url="https://dreambot.pl/DreamBotImages/weryfikacja.gif")
                view = Weryfikacja()
                await kanał.send(embed=embed, view=view)
            elif lang == "ENG":
                embed = nextcord.Embed(title=f'**VERIFICATION**', description="**To verify yourself, click `✅ Verify`**", color=0x00ff00)
                embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                embed.set_thumbnail(url=bot.user.avatar.url)
                embed.set_image(url="https://dreambot.pl/DreamBotImages/weryfikacja.gif")
                view = WeryfikacjaENG()
                await kanał.send(embed=embed, view=view)
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Bot nie posiada uprawnień do wysyłania wiadomości!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` The bot does not have permission to send messages!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić kanał dla `weryfikacja`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set the channel for `verification`!", ephemeral=True)

#Weryfikacja
@settingsconfig.subcommand(description="Wyświetla konfigurację weryfikacji")
async def weryfikacja(ctx):
    author = ctx.user
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if settings_document:
        weryfikacja_status = settings_document.get("weryfikacja", False)
        kanal = settings_document.get("kanalWeryfikacji")
        rolaWeryfikacji = settings_document.get("rolaWeryfikacji")
    else:
        weryfikacja_status = False
        rolaWeryfikacji = None
        kanal = None

    if weryfikacja_status == True:
        weryfikacja_status = "on"
    else:
        weryfikacja_status = "off"

    if rolaWeryfikacji:
        idroli = rolaWeryfikacji
        role = ctx.guild.get_role(idroli)
        idroli_str_cleaned = str(idroli)
    else:
        idroli = None
        idroli_str_cleaned = None
        role = None
    rola = role.name if role != None else "Brak"

    if kanal:
        kanalstr = f"<#{kanal}>"
    else:
        kanalstr = "`Brak`"

    if lang == "PL":
        view = Wylaczanie_Wlaczanie_weryfikacji()
        if idroli_str_cleaned and weryfikacja_status == "on":
            embed = nextcord.Embed(title=f'**Ustawienia weryfikacji**', description=f"\n**Status `{weryfikacja_status}`**\n**Rola: {rola}**\n**Kanał: {kanalstr}**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idroli_str_cleaned:
            embed = nextcord.Embed(title=f'**Ustawienia weryfikacji**', description=f"**Status `{weryfikacja_status}`**\n**Rola: {rola}**\n**Kanał: {kanalstr}**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Ustawienia weryfikacji**', description=f"**Status `{weryfikacja_status}`**\n**Rola: `Brak`**\n**Kanał: `Brak`**\n\n**Rola: `/settingsConfig rola weryfikacja`**\n**Kanał: `/settingsConfig kanal weryfikacja`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
    elif lang == "ENG":
        view = Wylaczanie_Wlaczanie_weryfikacjiENG()
        if idroli_str_cleaned and weryfikacja_status == "on":
            embed = nextcord.Embed(title=f'**Verification settings**', description=f"\n**Status `{weryfikacja_status}`**\n**Role: {rola}**\n**Channel: {kanalstr}**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idroli_str_cleaned:
            embed = nextcord.Embed(title=f'**Verification settings**', description=f"**Status `{weryfikacja_status}`**\n**Role: {rola}**\n**Channel: {kanalstr}**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Verification settings**', description=f"**Status `{weryfikacja_status}`**\n**Role: `None`**\n**Channel: `None`**\n\n**Role: `/settingsConfig rola weryfikacja`**\n**Channel: `/settingsConfig kanal weryfikacja`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)

#Zgaduj
@settings4fun.subcommand(description="Włącza/Wyłącza zgaduj")
async def zgaduj(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        server_id = str(ctx.guild.id)

        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            current_status = settings_document.get("zgaduj", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'zgaduj': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'zgaduj': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Komenda `zgaduj` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "turned on" if new_status else "turned off"
            await ctx.send(f"`[✅]:` The `guess` command has been {status_text} for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `zgaduj`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `guess`!", ephemeral=True)

#Whitelista
@settingsconfig.subcommand(description="Whitelista")
async def whitelista(ctx):
    await ctx.send("XDX")

#Blacklista
@settingsconfig.subcommand(description="Blacklista")
async def blacklista(ctx):
    await ctx.send("XDX")

#Anty
@whitelista.subcommand(description="Ustawia kanały na które nie działają anty")
async def add(ctx, kanał: nextcord.TextChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:
        server_id = str(ctx.guild.id)

        settings_document = settings_collection.find_one({'_id': server_id})

        if not settings_document:
            settings_document = {'_id': server_id}

        if 'whitelisted_anty' not in settings_document:
            settings_document['whitelisted_anty'] = []

        whitelisted_anty = settings_document['whitelisted_anty']

        if kanał.id not in whitelisted_anty:
            whitelisted_anty.append(kanał.id)

        settings_collection.update_one({'_id': server_id}, {'$set': {'whitelisted_anty': whitelisted_anty}}, upsert=True)

        if lang == "PL":
            await ctx.send(f"`[✅]:` Dodano kanał {kanał.mention} do listy kanałów, na których nie działa anty.", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` Added channel {kanał.mention} to the list of channels on which anti doesn't work.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić whiteliste dla `anty`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to whitelist `anty`!", ephemeral=True)

#Anty
@whitelista.subcommand(description="Usuwa kanały na którym nie działają anty")
async def remove(ctx, kanał: nextcord.TextChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:
        server_id = str(ctx.guild.id)

        settings_document = settings_collection.find_one({'_id': server_id})

        if not settings_document or 'whitelisted_anty' not in settings_document:
            if lang == "PL":
                await ctx.send("`[❌]:` Nie ma żadnych kanałów na liście, na których nie działa anty.", ephemeral=True)
                return
            elif lang == "ENG":
                await ctx.send("`[❌]:` Nie ma żadnych kanałów na liście, na których nie działa anty.", ephemeral=True)
                return

        whitelisted_anty = settings_document['whitelisted_anty']

        if kanał.id in whitelisted_anty:
            whitelisted_anty.remove(kanał.id)

            settings_collection.update_one({'_id': server_id}, {'$set': {'whitelisted_anty': whitelisted_anty}}, upsert=True)

            if lang == "PL":
                await ctx.send(f"`[✅]:`Usunięto kanał {kanał.mention} z listy kanałów, na których nie działa anty.", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:`There are no channels in the list where anti is not working.", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Kanał {kanał.mention} nie znajduje się na liście kanałów, na których nie działa anty.", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` The channel {kanał.mention} is not in the list of channels where anti is not working.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby usuwać kanał z listy `anty`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to remove a channel from the `anti` list!", ephemeral=True)

#Kanały
@whitelista.subcommand(description="Lista kanałów na których nie działa anty")
async def kanaly(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    author = ctx.user

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if settings_document and 'whitelisted_anty' in settings_document:
        whitelisted_anty = settings_document['whitelisted_anty']

        if whitelisted_anty:
            kanaly_lista = "\n".join([ctx.guild.get_channel(channel_id).mention for channel_id in whitelisted_anty])
            embed = nextcord.Embed(title="Whitelista", description=kanaly_lista, color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            thumbnail_url = ctx.guild.icon.url if ctx.guild.icon else bot.user.avatar.url
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed)
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Nie ma żadnych kanałów na liście!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` There are no channels listed!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Brak ustawionych kanałów na liście!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` There are no channels listed!", ephemeral=True)

#GlobalChat
@kanal.subcommand(description="Ustawia kanał global chatu!")
async def globalchat(ctx, kanał: nextcord.TextChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:
        if kanał.permissions_for(ctx.guild.me).send_messages:
            server_id = str(ctx.guild.id)

            settings_document = settings_collection.find_one({'_id': server_id})

            if settings_document:
                settings_collection.update_one({'_id': server_id}, {'$set': {'kanalGlobalChatu': kanał.id}})
                if lang == "PL":
                    await ctx.send(f"`[✅]:` Kanał funkcji `global chat`: {kanał.mention}", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[✅]:` Global chat channel: {kanał.mention}", ephemeral=True)
            else:
                new_settings_document = {'_id': server_id, 'kanalGlobalChatu': kanał.id}
                settings_collection.insert_one(new_settings_document)
                if lang == "PL":
                    await ctx.send(f"`[✅]:` Kanał funkcji `global chat`: {kanał.mention}", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[✅]:` Global chat channel: {kanał.mention}", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Bot nie posiada uprawnień do wysyłania wiadomości!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` The bot does not have permission to send messages!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić kanał dla funkcji `global chat`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set the channel for the `global chat` feature!", ephemeral=True)

#Globalchat
@settings4fun.subcommand(description="Wyświetla konfiguracje globalchatu")
async def globalchat(ctx):
    server_id = str(ctx.guild.id)
    author = ctx.user
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document:
        settings_document = {'_id': server_id}

    if settings_document.get('globalchat', False):
        ticket_status = "on"
    else:
        ticket_status = "off"

    idkanalu = settings_document.get('kanalGlobalChatu')

    if lang == "PL":
        view = Wylaczanie_Wlaczanie_globalchatu()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Ustawienia global**', description=f"\n**Status `{ticket_status}`**\n**Kanał: <#{idkanalu}>**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Ustawienia global**', description=f"**Status `{ticket_status}`**\n**Kanał: <#{idkanalu}>**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Ustawienia global**', description=f"**Status `{ticket_status}`**\n**Kanał: `Brak`**\n\n**Komenda `/settingsConfig kanal globalchat`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
    elif lang == "ENG":
        view = Wylaczanie_Wlaczanie_globalchatuENG()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Global settings**', description=f"\n**Status `{ticket_status}`**\n**Channel: <#{idkanalu}>**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Global settings**', description=f"**Status `{ticket_status}`**\n**Channel: <#{idkanalu}>**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Global settings**', description=f"**Status `{ticket_status}`**\n**Channel: `None`**\n\n**Command `/settingsConfig kanal globalchat`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)

#Logi
@settingsadm.subcommand(description="Wyświetla konfiguracje logów")
async def logi(ctx):
    server_id = str(ctx.guild.id)
    author = ctx.user
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document:
        settings_document = {'_id': server_id}

    if settings_document.get('logi', False):
        ticket_status = "on"
    else:
        ticket_status = "off"

    idkanalu = settings_document.get('kanalLogi')

    if lang == "PL":
        view = Wylaczanie_Wlaczanie_logow()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Ustawienia logów**', description=f"\n**Status `{ticket_status}`**\n**Kanał: <#{idkanalu}>**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Ustawienia logów**', description=f"**Status `{ticket_status}`**\n**Kanał: <#{idkanalu}>**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Ustawienia logów**', description=f"**Status `{ticket_status}`**\n**Kanał: `Brak`**\n\n**Komenda `/settingsConfig kanal logi`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
    elif lang == "ENG":
        view = Wylaczanie_Wlaczanie_logowENG()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Log settings**', description=f"\n**Status `{ticket_status}`**\n**Channel: <#{idkanalu}>**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Log settings**', description=f"**Status `{ticket_status}`**\n**Channel: <#{idkanalu}>**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Log settings**', description=f"**Status `{ticket_status}`**\n**Channel: `None`**\n\n**Command `/settingsConfig kanal logi`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)

#Logi
@kanal.subcommand(description="Ustawia kanał logów")
async def logi(ctx, kanał: nextcord.TextChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:
        if kanał.permissions_for(ctx.guild.me).send_messages:

            if not settings_document:
                settings_document = {'_id': server_id}

            settings_document['kanalLogi'] = kanał.id

            settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

            if lang == "PL":
                await ctx.send(f"`[✅]:` Kanał funkcji `logi`: <#{kanał.id}>", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Channel of the `logs` function: <#{kanał.id}>", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Bot nie posiada uprawnień do wysyłania wiadomości!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` The bot does not have permission to send messages!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić kanał dla `logi`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set up a channel for `logs`!", ephemeral=True)

#Liczenie
@settings4fun.subcommand(description="Wyświetla konfiguracje liczenia")
async def liczenie(ctx):
    server_id = str(ctx.guild.id)
    author = ctx.user
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document:
        settings_document = {'_id': server_id}

    if settings_document.get('liczenie', False):
        ticket_status = "on"
    else:
        ticket_status = "off"

    idkanalu = settings_document.get('kanalLiczenia')

    if lang == "PL":
        view = Wylaczanie_Wlaczanie_liczenia()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Ustawienia liczenia**', description=f"\n**Status `{ticket_status}`**\n**Kanał: <#{idkanalu}>**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Ustawienia liczenia**', description=f"**Status `{ticket_status}`**\n**Kanał: <#{idkanalu}>**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Ustawienia liczenia**', description=f"**Status `{ticket_status}`**\n**Kanał: `Brak`**\n\n**Komenda `/settingsConfig kanal liczenie`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
    elif lang == "ENG":
        view = Wylaczanie_Wlaczanie_liczeniaENG()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Counting settings**', description=f"\n**Status `{ticket_status}`**\n**Channel: <#{idkanalu}>**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Counting settings**', description=f"**Status `{ticket_status}`**\n**Channel: <#{idkanalu}>**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Counting settings**', description=f"**Status `{ticket_status}`**\n**Channel: `None`**\n\n**Command `/settingsConfig kanal liczenie`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)

#Liczenie
@kanal.subcommand(description="Ustawia kanał liczenia!")
async def liczenie(ctx, kanał: nextcord.TextChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:
        if kanał.permissions_for(ctx.guild.me).send_messages:
            server_id = str(ctx.guild.id)

            settings_document = settings_collection.find_one({'_id': server_id})

            if settings_document:
                settings_collection.update_one({'_id': server_id}, {'$set': {'kanalLiczenia': kanał.id}})
                if lang == "PL":
                    await ctx.send(f"`[✅]:` Kanał funkcji `liczenie`: {kanał.mention}", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[✅]:` `liczenie` channel: {kanał.mention}", ephemeral=True)
                await kanał.send("1")
            else:
                new_settings_document = {'_id': server_id, 'kanalGlobalChatu': kanał.id}
                settings_collection.insert_one(new_settings_document)
                if lang == "PL":
                    await ctx.send(f"`[✅]:` Kanał funkcji `liczenie`: {kanał.mention}", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[✅]:` `liczenie`channel: {kanał.mention}", ephemeral=True)
                await kanał.send("1")
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Bot nie posiada uprawnień do wysyłania wiadomości!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` The bot does not have permission to send messages!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić kanał dla funkcji `liczenie`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set the channel for the `liczenie` feature!", ephemeral=True)

#Litera
@settings4fun.subcommand(description='Wyświetla konfiguracje "ostatnia litera"')
async def litera(ctx):
    server_id = str(ctx.guild.id)
    author = ctx.user
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document:
        settings_document = {'_id': server_id}

    if settings_document.get('litera', False):
        ticket_status = "on"
    else:
        ticket_status = "off"

    idkanalu = settings_document.get('kanalLitery')

    if lang == "PL":
        view = Wylaczanie_Wlaczanie_litera()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Ustawienia ostatniej litery**', description=f"\n**Status `{ticket_status}`**\n**Kanał: <#{idkanalu}>**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Ustawienia ostatniej litery**', description=f"**Status `{ticket_status}`**\n**Kanał: <#{idkanalu}>**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Ustawienia ostatniej litery**', description=f"**Status `{ticket_status}`**\n**Kanał: `Brak`**\n\n**Komenda `/settingsConfig kanal litera`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
    elif lang == "ENG":
        view = Wylaczanie_Wlaczanie_literaENG()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Counting last letter**', description=f"\n**Status `{ticket_status}`**\n**Channel: <#{idkanalu}>**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Counting last letter**', description=f"**Status `{ticket_status}`**\n**Channel: <#{idkanalu}>**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Counting last letter**', description=f"**Status `{ticket_status}`**\n**Channel: `None`**\n\n**Command `/settingsConfig kanal litera`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)

#Litera
@kanal.subcommand(description='Ustawia kanał "ostatniej litery"!')
async def litera(ctx, kanał: nextcord.TextChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:
        if kanał.permissions_for(ctx.guild.me).send_messages:
            server_id = str(ctx.guild.id)

            settings_document = settings_collection.find_one({'_id': server_id})

            if settings_document:
                settings_collection.update_one({'_id': server_id}, {'$set': {'kanalLitery': kanał.id}})
                if lang == "PL":
                    await ctx.send(f"`[✅]:` Kanał funkcji `ostatnia litera`: {kanał.mention}", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[✅]:` `ostatnia litera` channel: {kanał.mention}", ephemeral=True)
                await kanał.send("Dream")
            else:
                new_settings_document = {'_id': server_id, 'kanalGlobalChatu': kanał.id}
                settings_collection.insert_one(new_settings_document)
                if lang == "PL":
                    await ctx.send(f"`[✅]:` Kanał funkcji `ostatnia litera`: {kanał.mention}", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[✅]:` `ostatnia litera` channel: {kanał.mention}", ephemeral=True)
                await kanał.send("Dream")
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Bot nie posiada uprawnień do wysyłania wiadomości!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` The bot does not have permission to send messages!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić kanał dla funkcji `ostatnia litera`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set the channel for the `ostatnia litera` feature!", ephemeral=True)

#Kalkulator
@settings4fun.subcommand(description="Włącza/Wyłącza kalkulator")
async def kalkulator(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        server_id = str(ctx.guild.id)

        if settings_document:
            current_status = settings_document.get("kalkulator", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'kalkulator': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'kalkulator': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Komenda `kalkulator` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "turned on" if new_status else "turned off"
            await ctx.send(f"`[✅]:` The `kalkulator` command has been {status_text} for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `kalkulator`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `kalkulator`!", ephemeral=True)

#SettingsEkonomia
@bot.slash_command(description="Wyświetla konfigurację ekonomii")
async def settingsekonomia(ctx):
    await ctx.send("XDX")

#Ekonomia
@settingsekonomia.subcommand(description="Wyświetla konfigurację ekonomii")
async def config(ctx):
    server_id = str(ctx.guild.id)
    author = ctx.user
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document:
        settings_document = {'_id': server_id}

    if settings_document.get('ekonomia', False):
        ticket_status = "on"
    else:
        ticket_status = "off"

    if settings_document:
        if 'workMin' in settings_document:
            workMin = settings_document['workMin']
        else:
            workMin = "Brak"
        if 'workMax' in settings_document:
            workMax = settings_document['workMax']
        else:
            workMax = "Brak"
        if 'workTime' in settings_document:
            workTime = settings_document['workTime']
        else:
            workTime = "Brak"

        if 'crimeMin' in settings_document:
            crimeMin = settings_document['crimeMin']
        else:
            crimeMin = "Brak"
        if 'crimeMax' in settings_document:
            crimeMax = settings_document['crimeMax']
        else:
            crimeMax = "Brak"
        if 'crimeTime' in settings_document:
            crimeTime = settings_document['crimeTime']
        else:
            crimeTime = "Brak"

        if 'robMin' in settings_document:
            robMin = settings_document['robMin']
        else:
            robMin = "Brak"
        if 'robMax' in settings_document:
            robMax = settings_document['robMax']
        else:
            robMax = "Brak"
        if 'robTime' in settings_document:
            robTime = settings_document['robTime']
        else:
            robTime = "Brak"

        if 'ruletkaTime' in settings_document:
            ruletkaTime = settings_document['ruletkaTime']
        else:
            ruletkaTime = "Brak"
        if 'ruletkaMin' in settings_document:
            ruletkaMin = settings_document['ruletkaMin']
        else:
            ruletkaMin = "Brak"
        if 'ruletkaMax' in settings_document:
            ruletkaMax = settings_document['ruletkaMax']
        else:
            ruletkaMax = "Brak"
        if 'ruletkaCzerwone' in settings_document:
            ruletkaCzerwone = settings_document['ruletkaCzerwone']
        else:
            ruletkaCzerwone = 2
        if 'ruletkaCzarne' in settings_document:
            ruletkaCzarne = settings_document['ruletkaCzarne']
        else:
            ruletkaCzarne = 2
        if 'ruletkaZielone' in settings_document:
            ruletkaZielone = settings_document['ruletkaZielone']
        else:
            ruletkaZielone = 5

        if 'blackjackTime' in settings_document:
            blackjackTime = settings_document['blackjackTime']
        else:
            blackjackTime = "Brak"
        if 'blackjackMin' in settings_document:
            blackjackMin = settings_document['blackjackMin']
        else:
            blackjackMin = "Brak"
        if 'blackjackMax' in settings_document:
            blackjackMax = settings_document['blackjackMax']
        else:
            blackjackMax = "Brak"

    shop_list = settings_document.get('shop', [])
    if lang == "PL":
        view = Wylaczanie_Wlaczanie_ekonomii()
        if ticket_status == "on":
            embed = nextcord.Embed(title=f'**Ustawienia ekonomii**', description=f"**Work:**\nWypłata: `{workMin} - {workMax}`\nCooldown: `{workTime} sekund`\n\n**Crime:**\nWypłata: `{crimeMin} - {crimeMax}`\nCooldown: `{crimeTime} sekund`\n\n**Rob:**\nWypłata: `{robMin} - {robMax}`\nCooldown: `{robTime} sekund`\n\n**Blackjack:**\nZakład: `{blackjackMin} - {blackjackMax}`\nCooldown: `{blackjackTime} sekund`\n\n**Ruletka:**\nZakład: `{ruletkaMin} - {ruletkaMax}`\nCooldown: `{ruletkaTime} sekund`\nMnożniki: `czerwone - x{ruletkaCzerwone}, czarne - x{ruletkaCzarne}, zielone x{ruletkaZielone}`\n\n**Sklep:**", color=0x00ff00)
            
            for idx, item in enumerate(shop_list, start=1):
                nazwa = item['nazwa']
                cena = item['cena']
                opis = item['opis']

                embed.add_field(name=f"ID: *{idx}* - *{nazwa}*\nOpis: *{opis}*", value=f"Cena: {cena} 💵", inline=True)

            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Ustawienia ekonomii**', description=f"**Ekonomia jest wyłączona**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
    elif lang == "ENG":
        view = Wylaczanie_Wlaczanie_ekonomiiENG()
        if ticket_status == "on":
            embed = nextcord.Embed(title=f'**Economy settings**', description=f"**Work:**\nPayout: `{workMin} - {workMax}`\nCooldown: `{workTime} seconds`\n\n**Crime:**\n**Payout: `{crimeMin} - {crimeMax}`**\nCooldown: `{crimeTime} seconds`\n\n**Rob:**\nPayout: `{robMin} - {robMax}`\nCooldown: `{robTime} seconds`\n\n**Blackjack:**\nBet: `{blackjackMin} - {blackjackMax}`\nCooldown: `{blackjackTime} sekund`\n\n**Roulette:**\nBet: `{ruletkaMin} - {ruletkaMax}`\nCooldown: `{ruletkaTime} seconds`\nMultipliers: `red - x{ruletkaCzerwone}, black - x{ruletkaCzarne}, green x{ruletkaZielone}`\n\n**Shop:**", color=0x00ff00)
            
            for idx, item in enumerate(shop_list, start=1):
                nazwa = item['nazwa']
                cena = item['cena']
                opis = item['opis']

                embed.add_field(name=f"ID: *{idx}* - *{nazwa}*\nDescription: *{opis}*", value=f"Price: {cena} 💵", inline=True)

            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Economy settings**', description=f"**The economy is off**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)

#Work
@settingsekonomia.subcommand(description="Ustawia komendę work")
async def work(ctx, odstep: str, minwyplata: float, maxwyplata: float):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document or not settings_document.get("ekonomia", False):
        if lang == "PL":
            await ctx.send("`[❌]:` Aby użyć tej komendy, włącz `ekonomie` używając `/settingsekonomia config`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` To use that command, enable `ekonomia` using `/settingsekonomia config`", ephemeral=True)
        return

    if ctx.user.guild_permissions.manage_messages:
        max_float = maxwyplata
        min_float = minwyplata
        time = odstep
        work_time_seconds = parse_duration(time)
        if work_time_seconds is None:
            if lang == "PL":
                await ctx.send("`[❌]:` Niepoprawny format czasu, przykład poprawnych formatów: 10s, 20m, 10h!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` Incorrect time format, example of valid formats: 10s, 20m, 10h", ephemeral=True)
            return

        if settings_document:
            update_data = {
                "$set": {
                    "_id": server_id,
                    "workTime": work_time_seconds,
                    "workMin": min_float,
                    "workMax": max_float
                }
            }
            settings_collection.update_one({'_id': server_id}, update_data)

        else:
            data = {
                "_id": server_id,
                "workTime": work_time_seconds,
                "workMin": min_float,
                "workMax": max_float
            }
            settings_collection.insert_one({'_id': server_id}, data)

        if lang == "PL":
            await ctx.send(f"`[✅]:` Pomyślnie ustawiono komendę `work`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` `work` command successfully set!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby ustawić `work`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to set `work` command!", ephemeral=True)

#Sklep
@settingsekonomia.subcommand(description="Sklep")
async def sklep(ctx):
    await ctx.send("XDX")

#Sklep Add
@sklep.subcommand(description="Dodaje pozycję do sklepu")
async def add(ctx, nazwa: str, opis, cena: float):
    server_id = str(ctx.guild.id)

    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"
    
    if ctx.user.guild_permissions.manage_messages:
        if not settings_document:
            settings_document = {'_id': server_id, 'shop': []}

        shop_list = settings_document.get('shop', [])

        for item in shop_list:
            if item['nazwa'] == nazwa:
                if lang == "PL":
                    await ctx.send(f"`[❌]:` Taki przedmiot już istnieje!", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[❌]:` Such an item already exists!", ephemeral=True)
                return

        new_item = {'nazwa': nazwa, 'cena': cena, 'opis': opis}
        shop_list.append(new_item)

        settings_collection.update_one({'_id': server_id}, {'$set': {'shop': shop_list}}, upsert=True)

        if lang == "PL":
            await ctx.send(f"`[✅]:` Dodano przedmiot `{nazwa}` z ceną `{cena}` i opisem `{opis}`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` Added item `{nazwa}` with price `{cena}` and description `{opis}`", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby dodać przedmiot do sklepu!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to add an item to the store!", ephemeral=True)

#Sklep remove
@sklep.subcommand(description="Usuwa pozycję ze sklepu")
async def remove(ctx, id: int, nazwa: str = None):
    server_id = str(ctx.guild.id)

    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        if not settings_document:
            settings_document = {'_id': server_id, 'shop': []}

        shop_list = settings_document.get('shop', [])

        found_item = None
        if id <= len(shop_list):
            found_item = shop_list[id - 1]

        if not found_item and nazwa:
            for item in shop_list:
                if item['nazwa'] == nazwa:
                    found_item = item
                    break

        if found_item:
            nazwa = found_item['nazwa']
            shop_list.remove(found_item)

            settings_collection.update_one({'_id': server_id}, {'$set': {'shop': shop_list}}, upsert=True)

            if lang == "PL":
                await ctx.send(f"`[✅]:` Usunięto pozycję `{nazwa}` ze sklepu!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Removed item `{nazwa}` from the shop!", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Nie znaleziono pozycji o ID `{id}` lub nazwie `{nazwa}` do usunięcia!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` No item with ID `{id}` or name `{nazwa}` was found to remove!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby usunąć przedmiot z sklepu!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to remove an item from the store!", ephemeral=True)

#Powitania
@settingsconfig.subcommand(description="Wyświetla konfigurację powitań")
async def powitania(ctx):
    author = ctx.user
    server_id = str(ctx.guild.id)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    settings_document = settings_collection.find_one({'_id': server_id})

    if not settings_document:
        settings_document = {'_id': server_id}

    if settings_document.get('powitania', False):
        ticket_status = "on"
    else:
        ticket_status = "off"

    if settings_document.get('powitaniaPV', False):
        pv_status = "on"
    else:
        pv_status = "off"

    if settings_document.get('powitaniaWiadomoscON', False):
        wiad_status = "on"
    else:
        wiad_status = "off"

    idkanalu = settings_document.get('kanalPowitan')
    wiadomosc = settings_document.get('powitaniaWiadomosc')
    pvwiadomosc = settings_document.get('powitaniaWiadomoscPV')

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if lang == "PL":
        view = Wylaczanie_Wlaczanie_powitan()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Ustawienia powitan**', description=f"\n**Status `{ticket_status}`**\n**Kanał: <#{idkanalu}>**\n**Status własnej treści: `{wiad_status}`**\n**Własna treść: `{wiadomosc}`**\n**Wiadomość PV: `{pv_status}`**\n**Treść PV: `{pvwiadomosc}`**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Ustawienia powitan**', description=f"**Status `{ticket_status}`**\n**Kanał: <#{idkanalu}>**\n**Status własnej treści: `{wiad_status}`**\n**Własna treść: `{wiadomosc}`**\n**Wiadomość PV: `{pv_status}`**\n**Treść PV: `{pvwiadomosc}`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Ustawienia powitan**', description=f"**Status `{ticket_status}`**\n**Kanał: `None`**\n**Status własnej treści: `{wiad_status}`**\n**Własna treść: `{wiadomosc}`**\n**Wiadomość PV: `{pv_status}`**\n**Treść PV: `{pvwiadomosc}`**\n\n**Komenda `/settingsConfig kanal powitania`**\n**Komenda PV `/settingsConfig wiadomosc powitaniaPV`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
    elif lang == "ENG":
        view = Wylaczanie_Wlaczanie_powitanENG()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Greeting settings**', description=f"\n**Status `{ticket_status}`**\n**Channel: <#{idkanalu}>**\n**Status of own content: `{wiad_status}`**\n**Own content: `{wiadomosc}`**\n**PV message: `{pv_status}`**\n**pv content: `{pvwiadomosc}`**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Greeting settings**', description=f"**Status `{ticket_status}`**\n**Channel: <#{idkanalu}>**\n**Status of own content: `{wiad_status}`**\n**Own content: `{wiadomosc}`**\n**PV message: `{pv_status}`**\n**pv content: `{pvwiadomosc}`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Greeting settings**', description=f"**Status `{ticket_status}`**\n**Channel: `None`**\n**Status of own content: `{wiad_status}`**\n**Own content: `{wiadomosc}`**\n**PV message: `{pv_status}`**\n**pv content: `{pvwiadomosc}`**\n\n**Command `/settingsConfig kanal powitania`**\n**PV command `/settingsConfig wiadomosc powitaniaPV`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)

#Pozegnania
@settingsconfig.subcommand(description="Wyświetla konfigurację pożegnań")
async def pozegnania(ctx):
    author = ctx.user
    server_id = str(ctx.guild.id)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    settings_document = settings_collection.find_one({'_id': server_id})

    if not settings_document:
        settings_document = {'_id': server_id}

    if settings_document.get('pozegnania', False):
        ticket_status = "on"
    else:
        ticket_status = "off"

    if settings_document.get('pozegnaniaWiadomoscON', False):
        wiad_status = "on"
    else:
        wiad_status = "off"

    idkanalu = settings_document.get('kanalPozegnan')
    wiadomosc = settings_document.get('pozegnaniaWiadomosc')

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if lang == "PL":
        view = Wylaczanie_Wlaczanie_pozegnan()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Ustawienia pozegnan**', description=f"\n**Status `{ticket_status}`**\n**Kanał: <#{idkanalu}>**\n**Status własnej treści: `{wiad_status}`**\n**Własna treść: `{wiadomosc}`****", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Ustawienia pozegnan**', description=f"**Status `{ticket_status}`**\n**Channel: <#{idkanalu}>**\n**Status własnej treści: `{wiad_status}`**\n**Własna treść: `{wiadomosc}`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Ustawienia pozegnan**', description=f"**Status `{ticket_status}`**\n**Channel: `None`**\n**Status własnej treści: `{wiad_status}`**\n**Własna treść: `{wiadomosc}`**\n\n**Command `/settingsConfig kanal pozegnania`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
    elif lang == "ENG":
        view = Wylaczanie_Wlaczanie_pozegnanENG()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Goodbye Settings**', description=f"\n**Status `{ticket_status}`**\n**Channel: <#{idkanalu}>**\n**Status of own content: `{wiad_status}`**\n**Own content: `{wiadomosc}`**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Goodbye Settings**', description=f"**Status `{ticket_status}`**\n**Channel: <#{idkanalu}>**\n**Status of own content: `{wiad_status}`**\n**Own content: `{wiadomosc}`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Goodbye Settings**', description=f"**Status `{ticket_status}`**\n**Channel: `None`**\n**Status of own content: `{wiad_status}`**\n**Own content: `{wiadomosc}`**\n\n**Command `/settingsConfig kanal pozegnania`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)

#Powitania
@kanal.subcommand(description="Ustawia kanał powitań")
async def powitania(ctx, kanał: nextcord.TextChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:
        if kanał.permissions_for(ctx.guild.me).send_messages:

            if not settings_document:
                settings_document = {'_id': server_id}

            settings_document['kanalPowitan'] = kanał.id

            settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

            if lang == "PL":
                await ctx.send(f"`[✅]:` Kanał funkcji `powitania`: <#{kanał.id}>", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Channel of the `powitania` function: <#{kanał.id}>", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Bot nie posiada uprawnień do wysyłania wiadomości!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` The bot does not have permission to send messages!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić kanał dla `powitania`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set up a channel for `powitania`!", ephemeral=True)

#Powitania
@wiadomosc.subcommand(description="Ustawia wiadomość powitań na pv")
async def powitaniapv(ctx, wiadomosc):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:

        if not settings_document:
            settings_document = {'_id': server_id}

        settings_document['powitaniaWiadomoscPV'] = wiadomosc

        settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

        if lang == "PL":
            await ctx.send(f"`[✅]:` Wiadomość funkcji `powitaniaPV`: {wiadomosc}", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` Message of the `powitaniaPV` function: {wiadomosc}", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić wiadomość dla `powitaniaPV`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set up a message for `powitaniaPV`!", ephemeral=True)

#Powitania
@wiadomosc.subcommand(description="Ustawia wiadomość powitań (Premium ⭐)")
async def powitania(ctx, wiadomosc = nextcord.SlashOption(name="wiadomosc", description='[user] - ping, [guild] - nazwa serwera, \\n - nowa linia')):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document:
        settings_document = {'_id': server_id}

    premium_status = get_status_text(settings_document.get("premium", False))
    if premium_status == "on":
        if ctx.user.guild_permissions.manage_channels:
            settings_document['powitaniaWiadomosc'] = wiadomosc

            settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

            if lang == "PL":
                await ctx.send(f"`[✅]:` Wiadomość funkcji `powitania`: {wiadomosc}", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Message of the `powitania` function: {wiadomosc}", ephemeral=True)

        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić wiadomość dla `wiadomosc powitania`!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` You do not have the `manage channels` permission to set up a message for `wiadomosc powitania`!", ephemeral=True)
    
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz premium! Możesz je zakupić i sprawdzić co daje przy pomocy `/premium`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You don't have premium! You can purchase them and see what they offer using `/premium`", ephemeral=True)

#Pozegnania
@kanal.subcommand(description="Ustawia kanał pozegnan")
async def pozegnania(ctx, kanał: nextcord.TextChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:
        if kanał.permissions_for(ctx.guild.me).send_messages:

            if not settings_document:
                settings_document = {'_id': server_id}

            settings_document['kanalPozegnan'] = kanał.id

            settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

            if lang == "PL":
                await ctx.send(f"`[✅]:` Kanał funkcji `pozegnania`: <#{kanał.id}>", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Channel of the `pozegnania` function: <#{kanał.id}>", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Bot nie posiada uprawnień do wysyłania wiadomości!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` The bot does not have permission to send messages!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić kanał dla `pozegnania`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set up a channel for `pozegnania`!", ephemeral=True)

#Pozegnania
@wiadomosc.subcommand(description="Ustawia wiadomość pożegnań (Premium ⭐)")
async def pozegnania(ctx, wiadomosc = nextcord.SlashOption(name="wiadomosc", description='[user] - ping, [guild] - nazwa serwera, \\n - nowa linia')):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document:
        settings_document = {'_id': server_id}

    premium_status = get_status_text(settings_document.get("premium", False))
    if premium_status == "on":
        if ctx.user.guild_permissions.manage_channels:
            settings_document['pozegnaniaWiadomosc'] = wiadomosc

            settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

            if lang == "PL":
                await ctx.send(f"`[✅]:` Wiadomość funkcji `pożegnania`: {wiadomosc}", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Message of the `pożegnania` function: {wiadomosc}", ephemeral=True)

        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić wiadomość dla `wiadomość pożegnania`!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` You do not have the `manage channels` permission to set up a message for `wiadomość pożegnania`!", ephemeral=True)
    
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz premium! Możesz je zakupić i sprawdzić co daje przy pomocy `/premium`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You don't have premium! You can purchase them and see what they offer using `/premium`", ephemeral=True)

#Crime
@settingsekonomia.subcommand(description="Ustawia komendę crime")
async def crime(ctx, odstep: str, minwyplata: float, maxwyplata: float):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document or not settings_document.get("ekonomia", False):
        if lang == "PL":
            await ctx.send("`[❌]:` Aby użyć tej komendy, włącz `ekonomie` używając `/settingsekonomia config`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` To use that command, enable `ekonomia` using `/settingsekonomia config`", ephemeral=True)
        return

    if ctx.user.guild_permissions.manage_messages:
        max_float = maxwyplata
        min_float = minwyplata
        time = odstep
        crime_time_seconds = parse_duration(time)
        if crime_time_seconds is None:
            if lang == "PL":
                await ctx.send("`[❌]:` Niepoprawny format czasu, przykład poprawnych formatów: 10s, 20m, 10h!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` Incorrect time format, example of valid formats: 10s, 20m, 10h", ephemeral=True)
            return

        if settings_document:
            update_data = {
                "$set": {
                    "_id": server_id,
                    "crimeTime": crime_time_seconds,
                    "crimeMin": min_float,
                    "crimeMax": max_float
                }
            }
            settings_collection.update_one({'_id': server_id}, update_data)

        else:
            data = {
                "_id": server_id,
                "crimeTime": crime_time_seconds,
                "crimeMin": min_float,
                "crimeMax": max_float
            }
            settings_collection.insert_one({'_id': server_id}, data)

        if lang == "PL":
            await ctx.send(f"`[✅]:` Pomyślnie ustawiono komendę `crime`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` `crime` command successfully set!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby ustawić `crime`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to set `crime` command!", ephemeral=True)

#Rob
@settingsekonomia.subcommand(description="Ustawia komendę rob")
async def rob(ctx, odstep: str, minkwota: float, maxkwota: float):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document or not settings_document.get("ekonomia", False):
        if lang == "PL":
            await ctx.send("`[❌]:` Aby użyć tej komendy, włącz `ekonomie` używając `/settingsekonomia config`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` To use that command, enable `ekonomia` using `/settingsekonomia config`", ephemeral=True)
        return

    if ctx.user.guild_permissions.manage_messages:
        max_float = maxkwota
        min_float = minkwota
        time = odstep
        work_time_seconds = parse_duration(time)
        if work_time_seconds is None:
            if lang == "PL":
                await ctx.send("`[❌]:` Niepoprawny format czasu, przykład poprawnych formatów: 10s, 20m, 10h!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` Incorrect time format, example of valid formats: 10s, 20m, 10h", ephemeral=True)
            return

        if settings_document:
            update_data = {
                "$set": {
                    "_id": server_id,
                    "robTime": work_time_seconds,
                    "robMin": min_float,
                    "robMax": max_float
                }
            }
            settings_collection.update_one({'_id': server_id}, update_data)

        else:
            data = {
                "_id": server_id,
                "robTime": work_time_seconds,
                "robMin": min_float,
                "robMax": max_float
            }
            settings_collection.insert_one({'_id': server_id}, data)

        if lang == "PL":
            await ctx.send(f"`[✅]:` Pomyślnie ustawiono komendę `rob`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` `rob` command successfully set!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby ustawić `rob`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to set `rob` command!", ephemeral=True)

#Selfrole
@settingsconfig.subcommand(description="Ustawia rolę i kanał dla samoobsługowych ról")
async def selfrole(ctx, rola: nextcord.Role, kanal: nextcord.TextChannel):
    await ctx.send("XDX")

#Selfrole add
@selfrole.subcommand(description="Ustawia rolę i kanał dla samoobsługowych ról")
async def add(ctx, rola: nextcord.Role, wiadomosc, kanal: nextcord.TextChannel = None):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        try:
            if kanal == None:
                kanal = await bot.fetch_channel(int(ctx.channel.id))
            else:
                kanal = await bot.fetch_channel(int(kanal.id))

        except Exception as e:
            print(f"Błąd podczas wysyłania wiadomości na kanale: {e}")

        if lang == "PL":
            await ctx.send(f"`[✅]:` Pomyślnie dodano selfrolę na {kanal.mention}!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` Selfrola successfully added to {kanal.mention}!", ephemeral=True)
                
        if kanal:
            embed = nextcord.Embed(title=rola.name, description=wiadomosc, color=0x8DCD70)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)

            if lang == "PL":
                view = SelfRole()
            elif lang == "ENG":
                view = SelfRoleENG()

            msg = await kanal.send(embed=embed, view=view)

            if not settings_document:
                settings_document = {'_id': server_id, 'selfrole': []}

            if 'selfrole' not in settings_document:
                settings_document['selfrole'] = []

            autorole_entry = {'rola_id': str(rola.id), 'msg_id': str(msg.id)}
            settings_document['selfrole'].append(autorole_entry)

            settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby dodać `selfrole`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to add `selfrole`!", ephemeral=True)

#Random IMG
@settings4fun.subcommand(description="Włącza/Wyłącza random img")
async def randomimg(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        server_id = str(ctx.guild.id)

        if settings_document:
            current_status = settings_document.get("randomIMG", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'randomIMG': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'randomIMG': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Komenda `random img` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "turned on" if new_status else "turned off"
            await ctx.send(f"`[✅]:` The `random img` command has been {status_text} for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `random img`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `random img`!", ephemeral=True)

#InviteLogger
@settingsconfig.subcommand(description="Włącza/Wyłącza inviteloggera")
async def invitelogger(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        server_id = str(ctx.guild.id)

        if settings_document:
            current_status = settings_document.get("inviteLogger", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'inviteLogger': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'inviteLogger': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Funkcja `InviteLogger` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "turned on" if new_status else "turned off"
            await ctx.send(f"`[✅]:` The `InviteLogger` function has been {status_text} for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `InviteLogger`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `InviteLogger`!", ephemeral=True)

#Giveaway
@settingsadm.subcommand(description="Włącza/Wyłącza giveaway")
async def giveaway(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        server_id = str(ctx.guild.id)

        if settings_document:
            current_status = settings_document.get("giveaway", False)
            new_status = not current_status

            settings_collection.update_one({'_id': server_id}, {'$set': {'giveaway': new_status}})
        else:
            new_status = True
            settings_document = {'_id': server_id, 'giveaway': new_status}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            status_text = "włączona" if new_status else "wyłączona"
            await ctx.send(f"`[✅]:` Komenda `giveaway` została {status_text} dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            status_text = "turned on" if new_status else "turned off"
            await ctx.send(f"`[✅]:` The `giveaway` command has been {status_text} for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `giveaway`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `giveaway`!", ephemeral=True)

#Autoad
@settingsconfig.subcommand(description="Wyświetla konfigurację automatycznych reklam")
async def autoad(ctx):
    server_id = str(ctx.guild.id)
    author = ctx.user
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document:
        settings_document = {'_id': server_id}

    if settings_document.get('autoad', False):
        ticket_status = "on"
    else:
        ticket_status = "off"

    if settings_document.get('autoAdEmbed', False) and settings_document.get('premium', False):
        embed_status = "on"
    else:
        embed_status = "off"

    idkanalu = settings_document.get('kanalAutoReklam')
    status = settings_document.get('autoReklamaStatus')

    if lang == "PL":
        view = Wylaczanie_Wlaczanie_autoad()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Auto reklamy**', description=f"\n**Status `{ticket_status}`**\n**Reklama `{status}`**\n**Kanał: <#{idkanalu}>**\n**Embed: `{embed_status}`**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Auto reklamy**', description=f"**Status `{ticket_status}`**\n**Reklama `{status}`**\n**Kanał: <#{idkanalu}>**\n**Embed: `{embed_status}`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Auto reklamy**', description=f"**Status `{ticket_status}`**\n**Reklama `{status}`**\n**Kanał: `Brak`**\n**Embed: `{embed_status}`**\n\n**Komendy:\n`/settingsConfig kanal autoad`**\n`/settingsConfig autoad reklama`", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
    elif lang == "ENG":
        view = Wylaczanie_Wlaczanie_autoadENG()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Auto ad**', description=f"\n**Status `{ticket_status}`**\n**Ad `{status}`**\n**Channel: <#{idkanalu}>**\n**Embed: `{embed_status}`**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Auto ad**', description=f"**Status `{ticket_status}`**\n**Ad `{status}`**\n**Channel: <#{idkanalu}>**\n**Embed: `{embed_status}`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Auto ad**', description=f"**Status `{ticket_status}`**\n**Ad `{status}`**\n**Channel: `Brak`**\n**Embed: `{embed_status}`**\n\n**Commands:\n`/settingsConfig kanal autoad`**\n`/settingsConfig autoad reklama`", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)

#Autoad
@kanal.subcommand(description="Ustawia kanał automatycznych reklam")
async def autoad(ctx, kanał: nextcord.TextChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    try:
        if ctx.user.guild_permissions.manage_channels:
            if kanał.permissions_for(ctx.guild.me).send_messages:
                server_id = str(ctx.guild.id)

                settings_document = settings_collection.find_one({'_id': server_id})

                if not settings_document:
                    settings_document = {'_id': server_id}

                settings_document['kanalAutoReklam'] = kanał.id

                settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

                if lang == "PL":
                    await ctx.send(f"`[✅]:` Kanał funkcji `autoad`: <#{kanał.id}>", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[✅]:` Channel of the `autoad` function: <#{kanał.id}>", ephemeral=True)

                await kanał.edit(topic="Jest to kanał automatycznych reklam! 🤖")

                embed=nextcord.Embed(description=f">>> Ustawiono kanał automatycznych reklam! 🤖\nJeżeli też chcesz mieć takie reklamy dodaj naszego bota!", color=0x008000)
                embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                embed.set_thumbnail(url=bot.user.avatar.url)
                embed.set_footer(text=current_time)
                msg = await kanał.send(embed=embed)
                await msg.pin()
            else:
                if lang == "PL":
                    await ctx.send(f"`[❌]:` Bot nie posiada uprawnień do wysyłania wiadomości!", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[❌]:` The bot does not have permission to send messages!", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić kanał dla `autoad`!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` You do not have the `manage channels` permission to set the channel for `autoad`!", ephemeral=True)                
    except nextcord.errors.Forbidden:
        if lang == "PL":
            await ctx.send("`[❌]:` Bot nie ma wystarczających uprawnień do wysłania wiadomości na tym kanale.")
        elif lang == "ENG":
            await ctx.send("`[❌]:` The bot does not have sufficient permissions to send messages in this channel.")

#Reklama
@settingsconfig.subcommand(description="Reklama")
async def reklama(ctx):
    await ctx.send("XDX")

#Autoad
@reklama.subcommand(description="Ustawia reklamę automatycznych reklam!")
async def autoad(ctx, embed = nextcord.SlashOption(name="embed", description="Wybiera czy reklama ma być wysyłana w embedzie", choices={"Tak / Yes (Premium ⭐)", "Nie / No"})):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:
        if settings_document and settings_document.get("autoad", False):
            idkanalu = settings_document.get('kanalAutoReklam')
            premium = settings_document.get('premium')
            if idkanalu != None:
                if not settings_document:
                    settings_document = {'_id': server_id}

                if embed == "Tak / Yes" and premium == True:
                    embed = True
                else:
                    embed = False

                settings_document['autoAdEmbed'] = embed
                settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

                if lang == "PL":
                    await ctx.response.send_modal(AutoAdReklamaModal())
                elif lang == "ENG":
                    await ctx.response.send_modal(AutoAdReklamaModalENG())
            else:
                if lang == "PL":
                    await ctx.send("`[❌]:` Pierw ustaw kanał!", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send("`[❌]:` Set the channel first!", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Funkcja `autoad` nie jest włączona dla tego serwera.", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` The `autoad` function is not enabled for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić `reklamę`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set the `advert`!", ephemeral=True) 

#Clear
@bot.slash_command(description="Usuń kilka wiadomości!")
async def clear(ctx, ilosc: int):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        if settings_document and settings_document.get("clear", False):
            bot_permissions = ctx.channel.permissions_for(ctx.guild.me)
            if bot_permissions.manage_messages:
                if ilosc == 1:
                    if lang == "PL":
                        await ctx.send(f"`[✅]:` Usunięto `{ilosc}` wiadomość!", ephemeral=True)
                    elif lang == "PL":
                        await ctx.send(f"`[✅]:` Deleted `{ilosc}` message!", ephemeral=True)
                else:
                    if lang == "PL":
                        await ctx.send(f"`[✅]:` Usunięto `{ilosc}` wiadomości!", ephemeral=True)
                    elif lang == "PL":
                        await ctx.send(f"`[✅]:` Deleted `{ilosc}` messages!", ephemeral=True)
                await ctx.channel.purge(limit=ilosc)

                statistics = load_statistics()
                if statistics:
                    statistics['clear'] += 1
                    statistics['allCommands'] += 1
                else:
                    statistics = {'clear': 1, 'allCommands': 1}
                save_statistics(statistics)
            else:
                if lang == "PL":
                    await ctx.send("`[❌]:` Bot nie posiada uprawnienia `manage messages` aby użyć `clear`!", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send("`[❌]:` Bot do not have the `manage messages` permission to use `clear`!", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Komenda `clear` nie jest włączona dla tego serwera.", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` The `clear` command is not enabled for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby użyć `clear`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to use `clear`!", ephemeral=True)

#Say
@bot.slash_command(description="Powiedz coś botem!")
async def say(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if settings_document and settings_document.get("say", False):
        if lang == "PL":
            await ctx.response.send_modal(SayModal())
        elif lang == "ENG":
            await ctx.response.send_modal(SayModalENG())

        statistics = load_statistics()
        if 'say' in statistics:
            statistics['say'] += 1
        if 'allCommands' in statistics:
            statistics['allCommands'] += 1
        else:
            statistics['say'] = 1
            statistics['allCommands'] = 1
        save_statistics(statistics)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Komenda `say` nie jest włączona dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` The `say` command is not enabled for this server.", ephemeral=True)

#Ship
@bot.slash_command(description="Połącz 2 osoby!")
async def ship(ctx, osoba1: nextcord.Member, osoba2: nextcord.Member):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if settings_document and settings_document.get("ship", False):
        procent = random.randint(1,100)
        if procent == 69:
            znak = ":point_right: :ok_hand:"
        elif procent >= 65:
            znak = "❤️"
        elif procent <= 35:
            znak = "💔"
        else:
            znak = "❔"
        await ctx.send(f"{osoba1} + {osoba2} = {procent}% {znak}")

        statistics = load_statistics()
        if 'ship' in statistics:
            statistics['ship'] += 1
        if 'allCommands' in statistics:
            statistics['allCommands'] += 1
        else:
            statistics['ship'] = 1
            statistics['allCommands'] = 1
        save_statistics(statistics)
    else:
        if lang == "PL":
            await ctx.send("[❌]:` Komenda `ship` nie jest włączona dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("[❌]:` The `ship` command is not enabled for this server.", ephemeral=True)

#Iq
@bot.slash_command(description= "Sprawdź swoje IQ!")
async def iq(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if settings_document and settings_document.get("iq", False):
        if lang == "PL":
            iq = random.randrange(-200, 200)
            msg = await ctx.send(":thinking: Twoje IQ wynosi...")
            time.sleep(1.4)
            await msg.edit(f"Twoje IQ wynosi **{iq}**!")
        elif lang == "ENG":
            iq = random.randrange(-200, 200)
            msg = await ctx.send(":thinking: Your IQ is...")
            time.sleep(1.4)
            await msg.edit(f"Your IQ is **{iq}**!")

        statistics = load_statistics()
        if 'iq' in statistics:
            statistics['iq'] += 1
        if 'allCommands' in statistics:
            statistics['allCommands'] += 1
        else:
            statistics['iq'] = 1
            statistics['allCommands'] = 1
        save_statistics(statistics)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Komenda `iq` nie jest włączona dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` The `iq` command is not enabled for this server.", ephemeral=True)

#Kostka
@bot.slash_command(description= "Rzuć kostką!")
async def kostka(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if settings_document and settings_document.get("kostka", False):
        if lang == "PL":
            wyrz = "Wyrzucono"
        elif lang == "ENG":
            wyrz = "Rolled"

        numer = random.randrange(1, 6)
        msg = await ctx.send(f"{wyrz}.")
        time.sleep(0.25)
        await msg.edit(content=f"{wyrz}..")
        time.sleep(0.25)
        await msg.edit(content=f"{wyrz}...")
        time.sleep(0.25)
        await msg.edit(content=f"{wyrz} **{numer}**")

        statistics = load_statistics()
        if 'kostka' in statistics:
            statistics['kostka'] += 1
        if 'allCommands' in statistics:
            statistics['allCommands'] += 1
        else:
            statistics['kostka'] = 1
            statistics['allCommands'] = 1
        save_statistics(statistics)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Komenda `kostka` nie jest włączona dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` The `cube` command is not enabled for this server.", ephemeral=True)

#Ankieta
@bot.slash_command(description="Stwórz ankietę!")
async def ankieta(ctx, treść):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if settings_document and settings_document.get('ankiety', False):
        idkanalu_lista = settings_document.get('kanalyAnkiet', [])

        if idkanalu_lista is None:
            if lang == "PL":
                await ctx.send("`[❌]:` Nie skonfigurowano kanału dla ankiet w ustawieniach serwera. Użyj `/settingsConfig ankiety`!", ephemeral=True)
                return
            elif lang == "ENG":
                await ctx.send("`[❌]:` Channel for polls not configured in server settings. Use `/settingsConfig ankiety`!", ephemeral=True)
                return

        if idkanalu_lista and ctx.channel.id in idkanalu_lista:
            await send_poll(ctx, treść, ctx.channel.id, lang)
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Tej komendy nie można tutaj użyć!", ephemeral=True)
                return
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` This command cannot be used here!", ephemeral=True)
                return
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Komenda `ankieta` nie jest włączona dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` The `ankieta` command is not enabled for this server.", ephemeral=True)

async def send_poll(ctx, treść, channel_id, lang):
    await ctx.send("`[✅]:` Wiadomość ankiety została wysłana!", ephemeral=True)

    if ctx.user.avatar:
        avatar_url = ctx.user.avatar.url
    else:
        avatar_url = no_avatar

    embed = nextcord.Embed(description=f"```{treść}```", color=0x00ff00)
    if ctx.guild:
        if lang == "PL":
            embed.set_author(name=f"Ankieta od {ctx.user.display_name}", icon_url=avatar_url)
        elif lang == "ENG":
            embed.set_author(name=f"Poll from {ctx.user.display_name}", icon_url=avatar_url)

        channel = bot.get_channel(channel_id)
        message = await channel.send(embed=embed)

        reactions = ['✅', '❔', '❌']
        for reaction in reactions:
            await message.add_reaction(reaction)

        if len(treść) > 99:
            treść = treść[:99]

        await message.create_thread(name=treść)

        statistics = load_statistics()
        if 'ankieta' in statistics:
            statistics['ankieta'] += 1
        if 'allCommands' in statistics:
            statistics['allCommands'] += 1
        else:
            statistics['ankieta'] = 1
            statistics['allCommands'] = 1
        save_statistics(statistics)

#Chatbot
@bot.slash_command(description= "Porozmawiaj z AI!")
async def chatbot(ctx, wiadomość):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if settings_document and settings_document.get("chatbot", False):
        ai_data = load_ai_data()
        if wiadomość in ai_data:
            odpowiedzi = ai_data[wiadomość]
            wybrana_odpowiedz = random.choice(odpowiedzi)
            await ctx.send(f"{wybrana_odpowiedz}  `{wiadomość}`")
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Nie mam odpowiedzi na to pytanie.", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` I don't have an answer to that question.", ephemeral=True)

        statistics = load_statistics()
        if 'chatbot' in statistics:
            statistics['chatbot'] += 1
        if 'allCommands' in statistics:
            statistics['allCommands'] += 1
        else:
            statistics['chatbot'] = 1
            statistics['allCommands'] = 1
        save_statistics(statistics)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Komenda `chatbot` nie jest włączona dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` The `chatbot` command is not enabled for this server.", ephemeral=True)

#Ban
@bot.slash_command(description= "Zbanuj kogoś kto złamał regulamin!")
async def ban(ctx, osoba : nextcord.Member, *, powód="Brak"):
    try:
        server_id = str(ctx.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            if 'language' in settings_document:
                lang = settings_document['language']
            else:
                lang = "PL"
        else:
            lang = "PL"

        if settings_document and settings_document.get("ban", False):
            if ctx.user.guild_permissions.ban_members:
                server_name = ctx.guild.name
                await osoba.ban(reason=powód)

                if lang == "PL":
                    await ctx.send(f"Pomyślnie zbanowano {osoba.mention} za `{powód}`! :hammer:")
                    embed=nextcord.Embed(title="Zostałeś/aś zbanowany/a! :hammer:", description=f"Zostałeś/aś zbanowany/a na {server_name}!", color=0xe40c0c)
                    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                    embed.set_thumbnail(url=bot.user.avatar.url)
                    embed.add_field(name="**Powód:**", value=f"**{powód}**", inline=False)
                    embed.set_footer(text=server_name)
                    await osoba.send(embed=embed)

                    await osoba.ban(reason=powód)
                elif lang == "ENG":
                    await ctx.send(f"Successfully banned {osoba.mention} for `{powód}`! :hammer:")
                    embed=nextcord.Embed(title="Banned! :hammer:", description=f"You are banned at {server_name}!", color=0xe40c0c)
                    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                    embed.set_thumbnail(url=bot.user.avatar.url)
                    embed.add_field(name="**Reason:**", value=f"**{powód}**", inline=False)
                    embed.set_footer(text=server_name)
                    await osoba.send(embed=embed)

                statistics = load_statistics()
                if 'ban' in statistics:
                    statistics['ban'] += 1
                if 'allCommands' in statistics:
                    statistics['allCommands'] += 1
                else:
                    statistics['ban'] = 1
                    statistics['allCommands'] = 1
                save_statistics(statistics)
            else:
                if lang == "PL":
                    await ctx.send(f"`[❌]:` Nie posiadasz uprawnienia `ban members` aby użyć `ban`!", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[❌]:` You do not have the `ban members` permission to use `ban`!", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Komenda `ban` nie jest włączona dla tego serwera.", ephemeral=True)
            elif lang == "PL":
                await ctx.send("`[❌]:` The `ban` command is not enabled for this server.", ephemeral=True)

    except nextcord.Forbidden as e:
        if lang == "PL":
            await ctx.send(f'`[❌]:` Bot nie posiada permisji! (Powiadom administrację serwera o tym błędzie, nie jest on spowowodowany ze strony technicznej)\n\n`{e}`', ephemeral=True)
        elif lang == "PL":
            await ctx.send(f'`[❌]:` The bot does not have permission! (Notify the server administration about this error, it is not technically caused)\n\n`{e}`', ephemeral=True)

#Kick
@bot.slash_command(description= "Zkickuj kogoś kto złamał regulamin!")
async def kick(ctx, osoba : nextcord.Member, *, powód="Brak"):
    try:
        server_id = str(ctx.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            if 'language' in settings_document:
                lang = settings_document['language']
            else:
                lang = "PL"
        else:
            lang = "PL"

        if settings_document and settings_document.get("kick", False):
            if ctx.user.guild_permissions.kick_members:
                server_name = ctx.guild.name
                
                if lang == "PL":
                    await ctx.send(f"Pomyślnie zkickowano {osoba} za {powód}! :mans_shoe:")
                    embed=nextcord.Embed(title="Zostałeś/aś zkickowany/a! :mans_shoe:", description=f"Zostałeś/aś zkickowany/a na {server_name}!", color=0xe40c0c)
                    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                    embed.set_thumbnail(url=bot.user.avatar.url)
                    embed.add_field(name="**Powód:**", value=f"**{powód}**", inline=False)
                    embed.set_footer(text=server_name)
                    await osoba.send(embed=embed)

                    await osoba.kick(reason=powód)
                elif lang == "ENG":
                    await ctx.send(f"Successfully kicked {osoba} for {powód}! :mans_shoe:")
                    embed=nextcord.Embed(title="Kicked! :mans_shoe:", description=f"You are kicked on {server_name}!", color=0xe40c0c)
                    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                    embed.set_thumbnail(url=bot.user.avatar.url)
                    embed.add_field(name="**Reason:**", value=f"**{powód}**", inline=False)
                    embed.set_footer(text=server_name)
                    await osoba.send(embed=embed)

                    await osoba.kick(reason=powód)

                statistics = load_statistics()
                if 'kick' in statistics:
                    statistics['kick'] += 1
                if 'allCommands' in statistics:
                    statistics['allCommands'] += 1
                else:
                    statistics['kick'] = 1
                    statistics['allCommands'] = 1
                save_statistics(statistics)
            else:
                if lang == "PL":
                    await ctx.send(f"`[❌]:` Nie posiadasz uprawnienia `kick members` aby użyć `kick`!", ephemeral=True)
                if lang == "ENG":
                    await ctx.send(f"`[❌]:` You do not have the `kick members` permission to use `kick`!", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Komenda `kick` nie jest włączona dla tego serwera.", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` The `kick` command is not enabled for this server.", ephemeral=True)

    except nextcord.Forbidden as e:
        if lang == "PL":
            await ctx.send(f'`[❌]:` Bot nie posiada permisji! (Powiadom administrację serwera o tym błędzie, nie jest on spowowodowany ze strony technicznej)\n\n`{e}`', ephemeral=True)
        elif lang == "PL":
            await ctx.send(f'`[❌]:` The bot does not have permission! (Notify the server administration about this error, it is not technically caused)\n\n`{e}`', ephemeral=True)

#Zamknij
@bot.slash_command(description="Zamyka ticket")
async def zamknij(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    channel = ctx.channel
    if channel.name.startswith("ticket"):
        await channel.delete()
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Ta komenda działa tylko na kanałach ticketowych!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` This command only works on ticket channels!", ephemeral=True)

#Mute
@bot.slash_command(description= "Wycisz kogoś!")
async def mute(payload, osoba : nextcord.Member, czas, *, powód="Brak"):
    try:
        server_id = str(payload.guild.id)
        user_id = payload.user.id
        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            if 'language' in settings_document:
                lang = settings_document['language']
            else:
                lang = "PL"
        else:
            lang = "PL"

        if settings_document and settings_document.get("mute", False):
            if payload.user.guild_permissions.mute_members:
                server_name = payload.guild.name

                user_document = users_collection.find_one({'_id': str(osoba.id)})
                if user_document and 'mutes' in user_document:
                    for mute_info in user_document['mutes']:
                        if mute_info.get('server_id') == server_id:
                            unmute_time = mute_info.get('end_time')
                            unmute_time_str = unmute_time.strftime("%Y-%m-%d %H:%M:%S")
                            if lang == "PL":
                                await payload.send(f"`[❌]:` {osoba.mention} ma już aktywne wyciszenie na tym serwerze! Jest ono do `{unmute_time_str}`", ephemeral=True)
                            elif lang == "ENG":
                                await payload.send(f"`[❌]:` {osoba.mention} already has an active mute on this server until `{unmute_time_str}`!", ephemeral=True)
                            return

                if lang == "PL":
                    await payload.send(f"{osoba.mention} został/a zmutowany/a za {powód} na {czas}! 🔇")

                    embed=nextcord.Embed(title="Zostałeś/aś zmutowany/a! 🔇", description=f"**Zostałeś/aś zmutowany/a na {server_name} na {czas}!**", color=0xe40c0c)
                    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                    embed.set_thumbnail(url=bot.user.avatar.url)
                    embed.add_field(name="**Powód:**", value=f"**{powód}**", inline=False)
                    embed.set_footer(text=server_name)
                    await osoba.send(embed=embed)
                elif lang == "ENG":
                    await payload.send(f"{osoba.mention} muted for {powód}! 🔇")

                    embed=nextcord.Embed(title="Muted! 🔇", description=f"**You are muted on {server_name} for {czas}!**", color=0xe40c0c)
                    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                    embed.set_thumbnail(url=bot.user.avatar.url)
                    embed.add_field(name="**Reason:**", value=f"**{powód}**", inline=False)
                    embed.set_footer(text=server_name)
                    await osoba.send(embed=embed)
                        
                mute_duration_seconds = parse_duration(czas)

                unmute_time = datetime.datetime.now() + timedelta(seconds=mute_duration_seconds)

                user_document = users_collection.find_one({'_id': str(osoba.id)})
                if not user_document:
                    user_document = {'_id': str(osoba.id)}

                if 'mutes' not in user_document:
                    user_document['mutes'] = []

                mute_info = {'server_id': str(payload.guild.id), 'end_time': unmute_time}
                user_document['mutes'].append(mute_info)

                users_collection.update_one({'_id': str(osoba.id)}, {'$set': user_document}, upsert=True)

                statistics = load_statistics()
                if 'mute' in statistics:
                    statistics['mute'] += 1
                else:
                    statistics['mute'] = 1
                save_statistics(statistics)
            else:
                if lang == "PL":
                    await payload.send(f"`[❌]:` Nie posiadasz uprawnienia `mute members` aby użyć `mute`!", ephemeral=True)
                elif lang == "ENG":
                    await payload.send(f"`[❌]:` You do not have the `mute members` permission to use `mute`!", ephemeral=True)
        else:
            if lang == "PL":
                await payload.send("`[❌]:` Komenda `mute` nie jest włączona dla tego serwera.", ephemeral=True)
            elif lang == "ENG":
                await payload.send("`[❌]:` The `mute` command is not enabled for this server.", ephemeral=True)

    except nextcord.Forbidden as e:
        if lang == "PL":
            await payload.send(f'`[❌]:` Bot nie posiada permisji! (Powiadom administrację serwera o tym błędzie, nie jest on spowowodowany ze strony technicznej)\n\n`{e}`', ephemeral=True)
        elif lang == "ENG":
            await payload.send(f'`[❌]:` The bot does not have permission! (Notify the server administration about this error, it is not technically caused)\n\n`{e}`', ephemeral=True)

#Unmute
@bot.slash_command(description= "Odcisz kogoś!")
async def unmute(payload, osoba : nextcord.Member):
    try:
        server_id = str(payload.guild.id)
        user_id = payload.user.id
        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            if 'language' in settings_document:
                lang = settings_document['language']
            else:
                lang = "PL"
        else:
            lang = "PL"

        if settings_document and settings_document.get("unmute", False):
            if payload.user.guild_permissions.mute_members:
                server_name = payload.guild.name

                if lang == "PL":
                    await payload.send(f"{osoba.mention} został/a odmutowany/a! 🔈")

                    embed=nextcord.Embed(title="Zostałeś/aś odmutowany/a! 🔈", description=f"**Zostałeś/aś odmutowany/a na {server_name}!**", color=0xe40c0c)
                    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                    embed.set_thumbnail(url=bot.user.avatar.url)
                    embed.set_footer(text=server_name)
                    await osoba.send(embed=embed)
                elif lang == "ENG":
                    await payload.send(f"{osoba.mention} unmuted! 🔈")

                    embed=nextcord.Embed(title="Unmuted! 🔈", description=f"**You are unmuted on {server_name}!**", color=0xe40c0c)
                    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                    embed.set_thumbnail(url=bot.user.avatar.url)
                    embed.set_footer(text=server_name)
                    await osoba.send(embed=embed)

                user_document = users_collection.find_one({'_id': str(osoba.id)})
                if not user_document:
                    user_document = {'_id': str(osoba.id)}

                if 'mutes' in user_document:
                    for mute_info in user_document['mutes']:
                        if mute_info.get('server_id') == server_id:
                            user_document['mutes'].remove(mute_info)
                            break

                    users_collection.update_one({'_id': str(osoba.id)}, {'$set': user_document}, upsert=True)

                statistics = load_statistics()
                if 'unmute' in statistics:
                    statistics['unmute'] += 1
                else:
                    statistics['unmute'] = 1
                save_statistics(statistics)
            else:
                if lang == "PL":
                    await payload.send(f"`[❌]:` Nie posiadasz uprawnienia `mute members` aby użyć `unmute`!", ephemeral=True)
                elif lang == "ENG":
                    await payload.send(f"`[❌]:` You do not have `mute members` permission to use `unmute`!", ephemeral=True)
        else:
            if lang == "PL":
                await payload.send("`[❌]:` Komenda `unmute` nie jest włączona dla tego serwera.", ephemeral=True)
            elif lang == "ENG":
                await payload.send("`[❌]:` The `unmute` command is not enabled for this server.", ephemeral=True)

    except nextcord.Forbidden as e:
        if lang == "PL":
            await payload.send(f'`[❌]:` Bot nie posiada permisji! (Powiadom administrację serwera o tym błędzie, nie jest on spowowodowany ze strony technicznej)\n\n`{e}`', ephemeral=True)
        elif lang == "PL":
            await payload.send(f'`[❌]:` The bot does not have permission! (Notify the server administration about this error, it is not technically caused)\n\n`{e}`', ephemeral=True)

#Info
@bot.slash_command(description="Pokazuje informacje o użytkowniku.")
async def info(ctx, osoba: nextcord.Member):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    user_document = users_collection.find_one({'_id': str(osoba.id)})
    mute_list = None
    if user_document:
        mute_list = user_document.get('mutes', [])
        tickets_taken_data = user_document.get('Guilds', {}).get(server_id, {})
        tickets_taken = tickets_taken_data.get('TicketsTaken', 0)

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if settings_document and settings_document.get("info", False):
        author = ctx.user
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        
        if osoba.avatar:
            avatar_url = osoba.avatar.url
        else:
            avatar_url = no_avatar

        mute_fields = []
        mutes_num = 0
        if mute_list:
            for mute_info in mute_list:
                mute_server_id = mute_info.get('server_id')
                end_time = mute_info.get('end_time')
                mute_end_time = end_time.strftime('%Y-%m-%d %H:%M:%S')
                now_time = str(data)
                server_name = None

                if mutes_num == 3:
                    break

                if mute_server_id == server_id:
                    server = bot.get_guild(int(mute_server_id))
                    if server:
                        server_name = server.name

                    if mute_end_time > now_time:
                        if server_name and end_time:
                            if lang == "PL":
                                mute_fields.append(f"Serwer: *{server_name}*\nData zakończenia: *{mute_end_time}*")
                            elif lang == "ENG":
                                mute_fields.append(f"Server: *{server_name}*\nEnd date: *{mute_end_time}*")

                            mutes_num += 1

        if lang == "PL":
            if osoba.top_role.name == "@everyone":
                main_role = "Brak"
            else:
                main_role = osoba.top_role.name

            dołączył = f"<t:{int(osoba.joined_at.timestamp())}:R>"
            stworzył = f"<t:{int(osoba.created_at.timestamp())}:R>"

            embed = nextcord.Embed(title=f"Informacje o {osoba}", color=0x99FF05)
            embed.set_thumbnail(url=avatar_url)
            embed.add_field(name="Nazwa użytkownika", value=osoba.display_name, inline=False)
            embed.add_field(name="ID", value=osoba.id, inline=False)
            embed.add_field(name="Dołączył do serwera", value=dołączył, inline=False)
            embed.add_field(name="Dołączył na Discord", value=stworzył, inline=False)
            embed.add_field(name="Przejęte tickety", value=tickets_taken, inline=False)
            embed.add_field(name="Rola najwyższa", value=main_role, inline=False)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")

            if mute_fields:
                embed.add_field(name="Muty", value="\n\n".join(mute_fields), inline=False)

            await ctx.send(embed=embed)
        elif lang == "ENG":
            if osoba.top_role.name == "@everyone":
                main_role = "None"
            else:
                main_role = osoba.top_role.name

            dołączył = f"<t:{int(osoba.joined_at.timestamp())}:R>"
            stworzył = f"<t:{int(osoba.created_at.timestamp())}:R>"

            embed = nextcord.Embed(title=f"Info about {osoba}", color=0x99FF05)
            embed.set_thumbnail(url=avatar_url)
            embed.add_field(name="Name", value=osoba.display_name, inline=False)
            embed.add_field(name="ID", value=osoba.id, inline=False)
            embed.add_field(name="Joined to server", value=dołączył, inline=False)
            embed.add_field(name="Joined to discord", value=stworzył, inline=False)
            embed.add_field(name="Tickets taken", value=tickets_taken, inline=False)
            embed.add_field(name="Role", value=main_role, inline=False)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")

            if mute_fields:
                embed.add_field(name="Mutes", value="\n\n".join(mute_fields), inline=False)

            await ctx.send(embed=embed)

        statistics = load_statistics()
        if 'info' in statistics:
            statistics['info'] += 1
        else:
            statistics['info'] = 1
        save_statistics(statistics)
    else:
        await ctx.send("`[❌]:` Komenda `info` nie jest włączona dla tego serwera!", ephemeral=True)

#Partnerstwa
@bot.slash_command(description="Sprawdza liczbę partnerstw użytkownika!")
async def partnerstwa(ctx, uzytkownik: nextcord.User):
    try:
        author = ctx.user
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        serverID = str(ctx.guild.id)
        server_id = str(ctx.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            if 'language' in settings_document:
                lang = settings_document['language']
            else:
                lang = "PL"
        else:
            lang = "PL"

        server_data = guilds_collection.find_one({'_id': serverID})

        if server_data is None or 'partnerships' not in server_data:
            partnerstwa_stats = {}
        else:
            partnerstwa_stats = server_data.get('partnerships', {})

        user_id = str(uzytkownik.id)
        liczba_partnerstw = partnerstwa_stats.get(user_id, 0)

        sorted_partnerships = sorted(partnerstwa_stats.items(), key=lambda x: x[1], reverse=True)
        try:
            user_rank = sorted_partnerships.index((user_id, liczba_partnerstw)) + 1
        except ValueError:
            user_rank = 1

        stawka = None
        server_data = db.settings.find_one({"_id": serverID})
        if server_data and "stawkaPartnerstwa" in server_data:
            stawka = server_data["stawkaPartnerstwa"]

        if lang == "PL":
            if liczba_partnerstw == 1:
                koncowka = "partnerstwo"
            elif liczba_partnerstw <= 4:
                koncowka = "partnerstwa"
            else:
                koncowka = "partnerstw"
        elif lang == "ENG":
            if liczba_partnerstw == 1:
                koncowka = "partnership"
            else:
                koncowka = "partnerships"

        if uzytkownik.avatar:
            avatar_url = uzytkownik.avatar.url
        else:
            avatar_url = no_avatar

        if lang == "PL":
            if liczba_partnerstw == 0:
                embed=nextcord.Embed(title=f"Licznik partnerstw", description=f"**Ten użytkownik nie ma partnerstw!**", color=0xe40c0c)
                embed.set_author(name=f"{uzytkownik}", icon_url=avatar_url)
                embed.set_thumbnail(url=bot.user.avatar.url)
                embed.set_footer(text=f"Invoked by {author} | {current_time}")
                await ctx.send(embed=embed)
            else:
                if server_data and "stawkaPartnerstwa" in server_data:
                    stawka = server_data["stawkaPartnerstwa"]
                    zl = ["ZŁ", "zł", "Zł", "zl", "ZL"]
                    dol = ["$", "dol"]
                    eur = ["E", "€", "e"]

                    if stawka is not None:
                        if any(phrase in stawka for phrase in zl):
                            waluta = "zł"
                        elif any(phrase in stawka for phrase in dol):
                            waluta = "$"
                        elif any(phrase in stawka for phrase in eur):
                            waluta = "E"
                        else:
                            waluta = "zł"
                    else:
                        waluta = ""

                    stawka = stawka.replace("ZŁ", "").replace("zł", "").replace("Zł", "").replace("zl", "").replace("ZL", "").replace(",", ".").replace("$", "").replace("E", "").replace("e", "").replace("€", "")

                    stawka = float(stawka)

                if stawka is None:
                    stawka_check = None
                else:
                    stawka_check = "yes"
                    stawka_info = f"{stawka}{waluta}"
                    razem_info = f"{round(liczba_partnerstw * stawka, 2)}{waluta}"
                
                if stawka_check != None:
                    embed=nextcord.Embed(title=f"Licznik partnerstw", description=f"**Ten użytkownik ma `{liczba_partnerstw}` {koncowka}**\n**Zapłata - `{razem_info}` ({stawka_info})**\n\n**Jest na `{user_rank}` miejscu w rankingu!**", color=0xe40c0c)
                    embed.set_author(name=f"{uzytkownik}", icon_url=avatar_url)
                    embed.set_thumbnail(url=bot.user.avatar.url)
                    embed.set_footer(text=f"Invoked by {author} | {current_time}")
                    await ctx.send(embed=embed)
                else:
                    embed=nextcord.Embed(title=f"Licznik partnerstw", description=f"**Ten użytkownik ma `{liczba_partnerstw}` {koncowka}**\n\n**Jest na `{user_rank}` miejscu w rankingu!**", color=0xe40c0c)
                    embed.set_author(name=f"{uzytkownik}", icon_url=avatar_url)
                    embed.set_thumbnail(url=bot.user.avatar.url)
                    embed.set_footer(text=f"Invoked by {author} | {current_time}")
                    await ctx.send(embed=embed)
        elif lang == "ENG":
            if liczba_partnerstw == 0:
                embed=nextcord.Embed(title=f"Partnerships counter", description=f"**This user has no partnerships!**", color=0xe40c0c)
                embed.set_author(name=f"{uzytkownik}", icon_url=avatar_url)
                embed.set_thumbnail(url=bot.user.avatar.url)
                embed.set_footer(text=f"Invoked by {author} | {current_time}")
                await ctx.send(embed=embed)
            else:
                if server_data and "stawkaPartnerstwa" in server_data:
                    stawka = server_data["stawkaPartnerstwa"]
                    zl = ["ZŁ", "zł", "Zł", "zl", "ZL"]
                    dol = ["$", "dol"]
                    eur = ["E", "€", "e"]

                    if stawka is not None:
                        if any(phrase in stawka for phrase in zl):
                            waluta = "zł"
                        elif any(phrase in stawka for phrase in dol):
                            waluta = "$"
                        elif any(phrase in stawka for phrase in eur):
                            waluta = "E"
                        else:
                            waluta = "zł"
                    else:
                        waluta = ""

                    stawka = stawka.replace("ZŁ", "").replace("zł", "").replace("Zł", "").replace("zl", "").replace("ZL", "").replace(",", ".").replace("$", "").replace("E", "").replace("e", "").replace("€", "")

                    stawka = float(stawka)

                if stawka is None:
                    stawka_check = None
                else:
                    stawka_check = "yes"
                    stawka_info = f"{stawka}{waluta}"
                    razem_info = f"{liczba_partnerstw * stawka}{waluta}"
                
                if stawka_check != None:
                    embed=nextcord.Embed(title=f"Partnerships counter", description=f"**This user has `{liczba_partnerstw}` {koncowka}**\n**Payment - `{razem_info}` ({stawka_info})**\n\n**He is ranked `{user_rank}` in the leaderboard!**", color=0xe40c0c)
                    embed.set_author(name=f"{uzytkownik}", icon_url=avatar_url)
                    embed.set_thumbnail(url=bot.user.avatar.url)
                    embed.set_footer(text=f"Invoked by {author} | {current_time}")
                    await ctx.send(embed=embed)
                else:
                    embed=nextcord.Embed(title=f"Partnerships counter", description=f"**This user has `{liczba_partnerstw}` {koncowka}**\n\n**He is ranked `{user_rank}` in the leaderboard!**", color=0xe40c0c)
                    embed.set_author(name=f"{uzytkownik}", icon_url=avatar_url)
                    embed.set_thumbnail(url=bot.user.avatar.url)
                    embed.set_footer(text=f"Invoked by {author} | {current_time}")
                    await ctx.send(embed=embed)
    except ValueError:
        if lang == "PL":
            await ctx.send("`[❌]:` Stawka została źle ustawiona!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` The rate has been set incorrectly!", ephemeral=True)

#Mem
@bot.slash_command(description="Losuje mema")
async def mem(ctx):
    await ctx.send("Nima")

#Mem pl
@mem.subcommand(description="Losuje mema (Po polsku)" )
async def pl(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    
    if settings_document and settings_document.get("mem", False):
        if ctx.channel.is_nsfw():
            num = random.randint(1, 5)
            if num == 1:
                user_id = str(ctx.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "memCD" in cooldown_data:
                    last_usage = cooldown_data["memCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        desc = f"**Mogłeś wygrać ale trwa cooldown! `{time_left.seconds}` sekund**"

                    else:
                        server_id = str(ctx.guild.id)
                        wygrana = round(random.uniform(0.1, 2), 2)
                        desc = f"**Btw przy okazji wygrałeś `{wygrana}` waluty!**"

                        user_id = str(ctx.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"memCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(ctx.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"memCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "memCD": current_time})

                    server_id = str(ctx.guild.id)
                    wygrana = round(random.uniform(0.1, 1), 2)
                    desc = f"**Btw przy okazji wygrałeś `{wygrana}` waluty!**"
                        
                    user_id = str(ctx.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(ctx.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                desc = " "

            meme_url, meme_title = await get_random_memePL()
            author = ctx.user
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")

            embed = nextcord.Embed(title=f"*{meme_title}*", description=desc, url=meme_url, color=0x302c34)
            embed.set_image(url=meme_url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed)

            statistics = load_statistics()
            if 'mem' in statistics:
                statistics['mem'] += 1
            else:
                statistics['mem'] = 1
            save_statistics(statistics)
        else:
            await ctx.send("`[❌]:` Komendy `mem` można użyć jedynie na kanałach `🔞 nsfw`!", ephemeral=True)
    else:
        await ctx.send("`[❌]:` Komenda `mem` nie jest włączona dla tego serwera.", ephemeral=True)

#Mem eng
@mem.subcommand(description="Losuje mema (Po angielsku)")
async def eng(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    
    if settings_document and settings_document.get("mem", False):
        if ctx.channel.is_nsfw():
            num = random.randint(1, 5)
            if num == 1:
                user_id = str(ctx.user.id)
                cooldown_data = cooldowns_collection.find_one({"_id": user_id})

                if cooldown_data and "memCD" in cooldown_data:
                    last_usage = cooldown_data["memCD"]
                    current_time = datetime.datetime.now()
                    cooldown_duration = datetime.timedelta(seconds=earncd)
                    
                    time_difference = current_time - last_usage
                    
                    if time_difference < cooldown_duration:
                        time_left = cooldown_duration - time_difference
                        desc = f"**You could have won but it's cooldown! `{time_left.seconds}` seconds**"

                    else:
                        server_id = str(ctx.guild.id)
                        wygrana = round(random.uniform(0.1, 2), 2)
                        desc = f"**Btw you won `{wygrana}` currency!**"

                        user_id = str(ctx.user.id)
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"memCD": current_time}}, upsert=True)
                        user_currency = currency_collection.find_one({"_id": server_id})

                        if user_currency:
                            if user_id in user_currency:
                                new_currency = user_currency[str(ctx.user.id)] + wygrana
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                            else:
                                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                        else:
                            currency_collection.insert_one({"_id": server_id, user_id: wygrana})
                else:
                    current_time = datetime.datetime.now()
                    if cooldown_data:
                        cooldowns_collection.update_one({"_id": user_id}, {"$set": {"memCD": current_time}}, upsert=True)
                    else:
                        cooldowns_collection.insert_one({"_id": user_id, "memCD": current_time})

                    server_id = str(ctx.guild.id)
                    wygrana = round(random.uniform(0.1, 1), 2)
                    desc = f"**Btw you won `{wygrana}` currency!**"
                        
                    user_id = str(ctx.user.id)
                    user_currency = currency_collection.find_one({"_id": server_id})

                    if user_currency:
                        if user_id in user_currency:
                            new_currency = user_currency[str(ctx.user.id)] + wygrana
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
                        else:
                            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: wygrana}})
                    else:
                        currency_collection.insert_one({"_id": server_id, user_id: wygrana})
            else:
                desc = " "

            meme_url, meme_title = await get_random_memeENG()
            author = ctx.user
            current_time = time.strftime("%Y-%m-%d %H:%M:%S")

            embed = nextcord.Embed(title=f"*{meme_title}*", description=desc, url=meme_url, color=0x302c34)
            embed.set_image(url=meme_url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed)

            statistics = load_statistics()
            if 'mem' in statistics:
                statistics['mem'] += 1
            else:
                statistics['mem'] = 1
            save_statistics(statistics)
        else:
            await ctx.send("`[❌]:` The `mem` command can only be used on `🔞 nsfw` channels!", ephemeral=True)
    else:
        await ctx.send("`[❌]:` The `mem` command is not enabled for this server.", ephemeral=True)

#Add
@bot.slash_command(description="Używana do dodania (np. partnerstw)")
async def add(ctx):
    await ctx.send("XDX")

#Remove
@bot.slash_command(description="Używana do usunięcia (np. partnerstw)")
async def remove(ctx):
    await ctx.send("XDX")

#Add partnerstwa
@add.subcommand(description="Dodaje partnerstwa")
async def partnerstwa(ctx, uzytkownik: nextcord.Member, ilosc: int):
    user_id = str(uzytkownik.id)
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.administrator:
        if settings_document and settings_document.get("partnerstwa", False):
            server_data = guilds_collection.find_one({'_id': server_id})
            if server_data is None:
                server_data = {'_id': server_id, 'partnerships': {}}
                guilds_collection.insert_one(server_data)

            if 'partnerships' not in server_data:
                partnerstwa_stats = {}
            else:
                partnerstwa_stats = {str(user_id): int(liczba_partnerstw) for user_id, liczba_partnerstw in server_data['partnerships'].items()}

            if user_id in partnerstwa_stats:
                partnerstwa_stats[user_id] += ilosc
            else:
                partnerstwa_stats[user_id] = ilosc

            server_data['partnerships'] = partnerstwa_stats

            guilds_collection.replace_one({'_id': server_id}, server_data, upsert=True)

            if lang == "PL":
                if ilosc == 1:
                    koncowka = "partnerstwo"
                elif ilosc <= 4:
                    koncowka = "partnerstwa"
                else:
                    koncowka = "partnerstw"

                partnerstwa = partnerstwa_stats[user_id]

                await ctx.send(f"`[✅]:` Pomyślnie dodano użytkownikowi {uzytkownik.mention} `{ilosc}` {koncowka}! Ma ich teraz `{partnerstwa}`", ephemeral=True)            
            elif lang == "ENG":
                if ilosc == 1:
                    koncowka = "partnership"
                else:
                    koncowka = "partnerships"

                partnerstwa = partnerstwa_stats[user_id]

                await ctx.send(f"`[✅]:` Successfully added to {uzytkownik.mention} `{ilosc}` {koncowka}! He has them now `{partnerstwa}`", ephemeral=True)

            statistics = load_statistics()
            if 'add' in statistics:
                statistics['add'] += 1
            else:
                statistics['add'] = 1
                save_statistics(statistics)
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Funkcja `partnerstwa` nie jest włączona dla tego serwera.", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` The 'partnership' feature is not enabled for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `administrator` aby dodać partnerstwa!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `administr` permission to add partnerships!", ephemeral=True)    

#Remove partnerstwa
@remove.subcommand(description="Usuwa partnerstwa")
async def partnerstwa(ctx, uzytkownik: nextcord.Member, ilosc: int):
    server_id = str(ctx.guild.id)
    user_id = str(uzytkownik.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.administrator:
        if settings_document and settings_document.get("partnerstwa", False):
            server_data = guilds_collection.find_one({'_id': server_id})
            if server_data is None:
                server_data = {'_id': server_id, 'partnerships': {}}
                guilds_collection.insert_one(server_data)

            if 'partnerships' not in server_data:
                partnerstwa_stats = {}
            else:
                partnerstwa_stats = {str(user_id): int(liczba_partnerstw) for user_id, liczba_partnerstw in server_data['partnerships'].items()}

            if lang == "PL":
                if ilosc == 1:
                    koncowka = "partnerstwo"
                elif ilosc <= 4:
                    koncowka = "partnerstwa"
                else:
                    koncowka = "partnerstw"
            elif lang == "ENG":
                if ilosc == 1:
                    koncowka = "partnership"
                else:
                    koncowka = "partnerships"

            if user_id in partnerstwa_stats:
                partnerstwa_stats[user_id] -= ilosc
                if lang == "PL":
                    wiadomość = f"`[✅]:` Pomyślnie usunięto użytkownikowi {uzytkownik.mention} `{ilosc}` {koncowka}!"
                elif lang == "ENG":
                    wiadomość = f"`[✅]:` Successfully deleted user {uzytkownik.mention} `{ilosc}` {koncowka}!"
                stat = "yes"
            else:
                if lang == "PL":
                    wiadomość = f"`[❌]:` Użytkownik {uzytkownik.mention} nie ma partnerstw!"
                elif lang == "ENG":
                    wiadomość = f"`[❌]:` User {uzytkownik.mention} there are no partnerships!"
                stat = None

            server_data['partnerships'] = partnerstwa_stats

            guilds_collection.replace_one({'_id': server_id}, server_data, upsert=True)

            await ctx.send(f"{wiadomość}", ephemeral=True)

            if not stat == None:
                statistics = load_statistics()
                if 'remove' in statistics:
                    statistics['remove'] += 1
                else:
                    statistics['remove'] = 1
                    save_statistics(statistics)
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Funkcja `partnerstwa` nie jest włączona dla tego serwera.", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` The 'partnership' feature is not enabled for this server.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `administrator` aby dodać partnerstwa!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `administrator` permission to add partnerships!", ephemeral=True)

#Zgaduj
@bot.slash_command(description="Zagraj w zgadywankę!" )
async def zgaduj(ctx):
    server_id = str(ctx.guild.id)
    user_id = ctx.user.id
    settings_document = settings_collection.find_one({'_id': server_id})
    
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if settings_document and settings_document.get("zgaduj", False):
        author = ctx.user
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")

        if lang == "PL":
            embed = nextcord.Embed(title=f'**Zgadywanka**', description=f"**Aby rozpocząć zgadywankę wybierz czy chcesz zgadywać liczbę czy słowo!** 🤔", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/PytajnikiC.png")
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            view = Zgadywanka_wybor(user_id)
        if lang == "ENG":
            embed = nextcord.Embed(title=f'**Guess**', description=f"**To start the guessing game choose whether you want to guess a number or a word!** 🤔", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/PytajnikiC.png")
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            view = Zgadywanka_wyborENG(user_id)

        global zgadywanka_msg
        zgadywanka_msg = await ctx.send(embed=embed, view=view)

        statistics = load_statistics()
        if 'zgaduj' in statistics:
            statistics['zgaduj'] += 1
        else:
            statistics['zgaduj'] = 1
        save_statistics(statistics)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Komenda `zgaduj` nie jest włączona dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` The `guess` command is not enabled for this server.", ephemeral=True)

#Waluta
@bot.slash_command(description="Wyświetla ilość waluty botowej!")
async def waluta(ctx):
    user_id = str(ctx.user.id)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    author = ctx.user
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    user_currency = currency_collection.find_one({"_id": server_id})

    user_bank_id = f"{user_id}Bank"
    if lang == "PL":
        if user_currency:
            try:
                currency_amount = round(user_currency[user_id], 2)
            except KeyError:
                currency_amount = 0.0

            try:
                bank_currency_amount = round(user_currency[user_bank_id], 2)
            except KeyError:
                bank_currency_amount = 0.0
                
            embed = nextcord.Embed(title=f"Oto twój portfel!", description=f"**Posiadasz `{currency_amount}` waluty w portfelu!\nOraz `{bank_currency_amount}` w banku**", color=0x009000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Monety.png")
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("`[❌]:` Nie posiadasz jeszcze żadnej waluty! Możesz ją zarobić używając komend 4Fun lub pracując!", ephemeral=True)
    
    elif lang == "ENG":
        if user_currency and user_currency[user_id] or user_currency and user_currency[user_bank_id]:
            try:
                currency_amount = round(user_currency[user_id], 2)
            except KeyError:
                currency_amount = 0.0

            try:
                bank_currency_amount = round(user_currency[user_bank_id], 2)
            except KeyError:
                bank_currency_amount = 0.0
            
            embed = nextcord.Embed(title=f"Here is your wallet!", description=f"**You have `{currency_amount}` currency!\nAnd `{bank_currency_amount}` in the bank**", color=0x009000)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Monety.png")
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed)
        else:
            await ctx.send("`[❌]:` You don't have any currency yet! You can earn it using 4Fun commands or working!", ephemeral=True)

#Notes
@bot.slash_command(description="Notes")
async def notes(ctx):
    await ctx.send("XDX")

#Sprawdz
@notes.subcommand(description="Wyświetla twój notes!")
async def sprawdz(ctx):
    user_id = str(ctx.user.id)
    notes_data = notes_collection.find_one({"_id": user_id})
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    author = ctx.user
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"
    
    if notes_data:

        if lang == "PL":
            embed = nextcord.Embed(title="Twoje notatki:", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://hhaker.pl/wp-content/uploads/2023/08/Notes2.png")
            embed.set_footer(text=f"Invoked by {author} | {current_time}")

        elif lang == "ENG":
            embed = nextcord.Embed(title="Your notes:", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://hhaker.pl/wp-content/uploads/2023/08/Notes2.png")
            embed.set_footer(text=f"Invoked by {author} | {current_time}")

        for key, value in notes_data.items():
            if key != "_id":
                embed.add_field(name=f"*{key}:*", value=value, inline=False)
        await ctx.send(embed=embed)

        statistics = load_statistics()
        if 'notes' in statistics:
            statistics['notes'] += 1
        else:
            statistics['notes'] = 1
            save_statistics(statistics)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie masz żadnych notatek! Możesz je napisać pod `/notes napisz`", ephemeral=True)
        elif lang == "Eng":
            await ctx.send("`[❌]:` You have no notes! You can write them under `/notes napisz`", ephemeral=True)    

#Napisz
@notes.subcommand(description="Dodaje nową notatkę!")
async def napisz(ctx, nazwa: str, *, notatka: str):
    user_id = str(ctx.user.id)
    notes_data = notes_collection.find_one({"_id": user_id})
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"
    
    if notes_data:
        if nazwa in notes_data:
            if lang == "PL":
                await ctx.send("`[❌]:` Notatka o tej nazwie już istnieje.", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` A note with this name already exists.", ephemeral=True)
        else:
            notes_data[nazwa] = notatka
            notes_collection.update_one({"_id": user_id}, {"$set": notes_data})
            if lang == "PL":
                await ctx.send(f"`[✅]:` Dodano nową notatkę: `{nazwa}`! Sprawdzisz je pod `/notes sprawdz`", ephemeral=True)
            if lang == "ENG":
                await ctx.send(f"`[✅]:` New note added: `{nazwa}`! You can check them under `/notes sprawdz`", ephemeral=True)
    else:
        notes_collection.insert_one({"_id": user_id, nazwa: notatka})
        if lang == "PL":
            await ctx.send(f"`[✅]:` Dodano nową notatkę: `{nazwa}`! Sprawdzisz je pod `/notes sprawdz`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` New note added: `{nazwa}`! You can check them under `/notes sprawdz`", ephemeral=True)

    statistics = load_statistics()
    if 'notes' in statistics:
        statistics['notes'] += 1
    else:
        statistics['notes'] = 1
        save_statistics(statistics)

#Usun
@notes.subcommand(description="Usuwa notatkę o podanej nazwie")
async def usun(ctx, nazwa: str):
    user_id = str(ctx.user.id)
    notes_data = notes_collection.find_one({"_id": user_id})
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"
    
    if notes_data and nazwa in notes_data:
        del notes_data[nazwa]
        notes_collection.update_one({"_id": user_id}, {"$unset": {nazwa: ""}})
        if lang == "PL":
            await ctx.send(f"`[✅]:` Notatka o nazwie `{nazwa}` została usunięta!", ephemeral=True)
        elif lang == "PL":
            await ctx.send(f"`[✅]:` Note named `{nazwa}` has been deleted!", ephemeral=True)

        statistics = load_statistics()
        if 'notes' in statistics:
            statistics['notes'] += 1
        else:
            statistics['notes'] = 1
            save_statistics(statistics)
    else:
        if lang == "PL":
            await ctx.send(f"`[❌]:` Notatka o nazwie `{nazwa}` nie istnieje!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[❌]:` Note named `{nazwa}` does not exist!", ephemeral=True)

#Add waluta
@add.subcommand(description="Dodaje waluty")
async def waluta(ctx, uzytkownik: nextcord.Member, ilosc: int):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.administrator:
        user_id = str(uzytkownik.id)
        bank_user_id = f"{user_id}Bank"
        user_currency = currency_collection.find_one({"_id": server_id})

        if user_currency:
            try:
                new_currency = user_currency[bank_user_id] + ilosc
                currency_collection.update_one({"_id": server_id}, {"$set": {bank_user_id: new_currency}})
            except KeyError:
                currency_collection.update_one({"_id": server_id}, {"$set": {bank_user_id: ilosc}})
        else:
            currency_collection.insert_one({"_id": server_id, bank_user_id: ilosc})

        if lang == "PL":
            await ctx.send(f"`[✅]:` Dodano {ilosc} waluty użytkownikowi {uzytkownik.mention}!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` Added {ilosc} of currency to {uzytkownik.mention}!", ephemeral=True)

        statistics = load_statistics()
        if 'add' in statistics:
            statistics['add'] += 1
        else:
            statistics['add'] = 1
            save_statistics(statistics)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `administrator` dodać `waluty`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `administrator` permission to add `currencies`!", ephemeral=True)

#Remove waluta
@remove.subcommand(description="Usuwa walutę")
async def waluta(ctx, uzytkownik: nextcord.Member, ilosc: int):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.administrator:
        user_id = str(uzytkownik.id)
        bank_user_id = f"{user_id}Bank"
        user_currency = currency_collection.find_one({"_id": server_id})

        if user_currency:
            try:
                new_currency = user_currency[bank_user_id] - ilosc
                currency_collection.update_one({"_id": server_id}, {"$set": {bank_user_id: new_currency}})
            except KeyError:
                currency_collection.update_one({"_id": server_id}, {"$set": {bank_user_id: ilosc}})
        else:
            currency_collection.insert_one({"_id": server_id, bank_user_id: 0})

        if lang == "PL":
            await ctx.send(f"`[✅]:` Usunięto `{ilosc}` waluty użytkownikowi {uzytkownik.mention}!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` Removed `{ilosc}` currency from {uzytkownik.mention}!", ephemeral=True)

        statistics = load_statistics()
        if 'remove' in statistics:
            statistics['remove'] += 1
        else:
            statistics['remove'] = 1
            save_statistics(statistics)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `administrator` aby dodać `waluty`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `administrator` permission to add `currencies`!", ephemeral=True)

#Lang
@bot.slash_command(description="Sets the preferred language / Ustawia preferowany język")
async def lang(ctx, lang = nextcord.SlashOption(name="lang", choices={"PL", "ENG"})):
    if ctx.user.guild_permissions.manage_messages:
        if lang == "PL":
            server_id = str(ctx.guild.id)
            server_settings = settings_collection.find_one({'_id': server_id})
            if server_settings is None:
                server_settings = {'_id': server_id}

            server_settings['language'] = "PL"

            settings_collection.update_one({'_id': server_id}, {'$set': server_settings}, upsert=True)

            language = lang.upper()
            await ctx.send(f"`[✅]:` Język serwera został ustawiony na: `{language}`", ephemeral=True)

        elif lang == "ENG":
            server_id = str(ctx.guild.id)
            server_settings = settings_collection.find_one({'_id': server_id})
            if server_settings is None:
                server_settings = {'_id': server_id}

            server_settings['language'] = "ENG"

            settings_collection.update_one({'_id': server_id}, {'$set': server_settings}, upsert=True)

            language = lang.upper()
            await ctx.send(f"`[✅]:` The server language has been set to: `{language}`", ephemeral=True)

    else:
        await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby ustawić `język`!", ephemeral=True)

#Translate
@bot.slash_command(description="Tłumacz")
async def translate(ctx, language = nextcord.SlashOption(description="Język z którego chcesz przetłumaczyć / The language you want to translate from"), to = nextcord.SlashOption(description="Język na który chcesz przetłumaczyć / The language you want to translate into"), *, text):
    try:
        server_id = str(ctx.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            if 'language' in settings_document:
                lang = settings_document['language']
            else:
                lang = "PL"
        else:
            lang = "PL"

        translator = Translator(from_lang=language, to_lang=to)
        translated_text = translator.translate(text)
        if lang == "PL":
            embed = nextcord.Embed(title="Wynik tłumaczenia", color=0x00ff00)
            embed.add_field(name=f"{language} ➡️ {to}\n", value=f"**Oryginał:** `{text}`\n**Tłumaczenie:** `{translated_text}`", inline=False)
        elif lang == "ENG":
            embed = nextcord.Embed(title="Translation result", color=0x00ff00)
            embed.add_field(name=f"{language} ➡️ {to}\n", value=f"**Original:** `{text}`\n**Translation:** `{translated_text}`", inline=False)
        
        embed.set_thumbnail(url=bot.user.avatar.url)
        await ctx.send(embed=embed)

    except Exception as e:
        if lang == "PL":
            await ctx.send(f"`[❌]:` Wystąpił błąd podczas tłumaczenia: `{str(e)}`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[❌]:` An error occurred while translating: `{str(e)}`", ephemeral=True)

#Ocena
@bot.slash_command(description="Oceń naszego bota od 1 do 10!")
async def ocena(ctx, ocena: int, opis: str, zrodlo = nextcord.SlashOption(name="zrodlo", description="Skąd dowiedziałeś się o naszym bocie? / How did you hear about our bot?")):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.user.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    verification_document = users_collection.find_one({"_id": user_id})
    if verification_document and verification_document.get("Voted", False):
        await ctx.send("`[❌]:` Już wystawiłeś ocenę o naszym bocie!", ephemeral=True)
        return

    if ocena <= 10 and ocena >= 1:
        if verification_document:
            users_collection.update_one({'_id': user_id}, {'$set': {'Voted': True}})
        else:
            verification_document = {'_id': user_id, 'Voted': True}
            users_collection.insert_one(verification_document)

        author = ctx.user
        server_name = ctx.guild.name
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        channel = bot.get_channel(kanalOcen)

        if author.avatar:
            avatar_url = ctx.user.avatar.url
        else:
            avatar_url = no_avatar

        if lang == "PL":
            await ctx.send("`[✅]:` Dziękujemy za opinię! Została ona wysłana na kanał ocen na naszym Discordzie! Jeżeli chcesz nam jeszcze bardziej pomóc użyj `/vote`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[✅]:` Thank you for your opinion! It has been posted to the ratings channel on our Discord! If you want to help us even more, use `/vote`", ephemeral=True)

        embed = nextcord.Embed(title=f'**{ocena}/10**', description=f"**Opis:**\n{opis}\n\n**Źródło:**\n{zrodlo}", color=0xffd700)
        embed.set_author(name=author.display_name, icon_url=avatar_url)
        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Gwiazdki.png")
        embed.set_footer(text=f"{server_name} | {current_time}")
        msg = await channel.send(embed=embed)
        await msg.add_reaction("❤")

    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Ocena musi być w skali od 1 do 10! (1, 2... 9, 10)", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` The rating must be on a scale of 1 to 10! (1, 2... 9, 10)", ephemeral=True)

#Vote
@bot.slash_command(description="Zagłosuj na naszego bota na top.gg!")
async def vote(ctx):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    author = ctx.user
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"
        
    if lang == "PL":
        embed = nextcord.Embed(title=f'Zagłosuj na naszego bota', description="Aby zagłosować kliknij w tekst powyżej! Przekieruje cię do `top.gg`", url="https://top.gg/bot/1146885724721905744/vote", color=0xffd700)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        await ctx.send(embed=embed)

#Kalkulator
@bot.slash_command(description="Prosty kalkulator matematyczny")
async def kalkulator(ctx, dzialanie):
    try:
        server_id = str(ctx.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            if 'language' in settings_document:
                lang = settings_document['language']
            else:
                lang = "PL"
        else:
            lang = "PL"

        if settings_document and settings_document.get("kalkulator", False):
            dzialanie_replaced = dzialanie.replace(',', '.')
            dzialanie_replaced = re.sub(r'(\+|-|\*|/)', r' \1 ', dzialanie_replaced)
            wynik = eval(dzialanie_replaced)
            wynik_replaced = str(wynik).replace('.', ',')

            await ctx.send(f"{dzialanie_replaced} = {wynik_replaced}")

            statistics = load_statistics()
            if 'kalkulator' in statistics:
                statistics['kalkulator'] += 1
            else:
                statistics['kalkulator'] = 1
            save_statistics(statistics)
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Komenda `kalkulator` nie jest włączona dla tego serwera.", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` The `kalkulator` command is not enabled for this server.", ephemeral=True)
        
    except Exception as e:
        if lang == "PL":
            await ctx.send(f"`[❌]:` Wystąpił błąd: {str(e)}", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[❌]:` An error occured: {str(e)}", ephemeral=True)

#Work
@bot.slash_command(description="Zarabiaj pieniądze!")
async def work(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.user.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    user_currency = currency_collection.find_one({"_id": server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    wmin = False
    wmax = False
    wt = False
    if settings_document:
        if 'workMin' in settings_document:
            workMin = settings_document['workMin']
            wmin = True
        if 'workMax' in settings_document:
            workMax = settings_document['workMax']
            wmax = True
        if 'workTime' in settings_document:
            workTime = settings_document['workTime']
            wt = True

    if not settings_document or not settings_document.get("ekonomia", False):
        if lang == "PL":
            await ctx.send("`[❌]:` Aby użyć tej komendy, włącz `ekonomie` używając `/settingsekonomia config`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` To use that command, enable `ekonomia` using `/settingsekonomia config`", ephemeral=True)
        return
    
    if wmin == False or wmax == False or wt == False:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie dokonano konfiguracji! Pierw użyj `/settingsekonomia work`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` No configuration completed! First use `/settingsekonomia work`", ephemeral=True)
        return
    
    can = False
    cooldown_data = cooldowns_collection.find_one({"_id": user_id})
    if cooldown_data and "workCD" in cooldown_data:
        last_usage = cooldown_data["workCD"]
        current_time = datetime.datetime.now()
        cooldown_duration = datetime.timedelta(seconds=workTime)
                    
        time_difference = current_time - last_usage
                    
        if time_difference < cooldown_duration:
            time_left = cooldown_duration - time_difference
            await ctx.send(f"`[❌]:` Cooldown trwa! Spróbuj ponowanie za `{time_left.seconds}` sekund", ephemeral=True)
        else:
            can = True
    else:
        can = True

    if can == True:
        income = round(random.uniform(workMin, workMax), 2)

        await ctx.send(f"`[✅]:` Pracując zarobiłeś `{income}` waluty!")

        current_time = datetime.datetime.now()
        if cooldown_data:
            cooldowns_collection.update_one({"_id": user_id}, {"$set": {"workCD": current_time}}, upsert=True)
        else:
            cooldowns_collection.insert_one({"_id": user_id, "workCD": current_time})

        if user_currency:
            if user_id in user_currency:
                new_currency = user_currency[str(ctx.user.id)] + income
                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
            else:
                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: income}})
        else:
            currency_collection.insert_one({"_id": server_id, user_id: income})

        statistics = load_statistics()
        if 'work' in statistics:
            statistics['work'] += 1
        else:
            statistics['work'] = 1
        save_statistics(statistics)

#Sklep
@bot.slash_command(description="Wyświetla sklep serwerowy")
async def sklep(ctx):
    server_id = str(ctx.guild.id)
    server_name = ctx.guild.name
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document:
        settings_document = {'_id': server_id, 'shop': []}

    shop_list = settings_document.get('shop', [])

    if not shop_list:
        if lang == "PL":
            await ctx.send(f"`[❌]:` Sklep jest pusty!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[❌]:` The shop is empty!", ephemeral=True)
        return

    if lang == "PL":
        embed = nextcord.Embed(title=f"Sklep {server_name}", color=0x6A5ACD)

        for idx, item in enumerate(shop_list, start=1):
            nazwa = item['nazwa']
            cena = item['cena']
            opis = item['opis']

            embed.add_field(name=f"ID: *{idx}* - *{nazwa}*\nOpis: *{opis}*", value=f"Cena: {cena} 💵", inline=False)

    elif lang == "ENG":
        embed = nextcord.Embed(title=f"{server_name} shop", color=0x6A5ACD)

        for idx, item in enumerate(shop_list, start=1):
            nazwa = item['nazwa']
            cena = item['cena']
            opis = item['opis']

            embed.add_field(name=f"ID: *{idx}* - *{nazwa}*\nDescription: *{opis}*", value=f"Price: {cena} 💵", inline=False)

    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
    embed.set_thumbnail(url=bot.user.avatar.url)
    embed.set_footer(text=f"Invoked by {ctx.user} | {current_time}")
    await ctx.send(embed=embed)

#Buy
@bot.slash_command(description="Używana do kupna przedmiotów z sklepu")
async def buy(ctx, id: int, nazwa: str = None):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.user.id)

    settings_document = settings_collection.find_one({'_id': server_id})
    user_document = users_collection.find_one({'_id': user_id})
    user_currency = currency_collection.find_one({"_id": server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document:
        if lang == "PL":
            await ctx.send(f"`[❌]:` Sklep jest pusty.", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[❌]:` The shop is empty.", ephemeral=True)
        return

    shop_list = settings_document.get('shop', [])

    found_item = None
    if id <= len(shop_list):
        found_item = shop_list[id - 1]

    if not found_item and nazwa:
        for item in shop_list:
            if item['nazwa'] == nazwa:
                found_item = item
                break

    if not found_item:
        if lang == "PL":
            await ctx.send(f"`[❌]:` Przedmiot o ID `{id}` lub nazwie `{nazwa}` nie istnieje w sklepie!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[❌]:` The item with ID `{id}` or name `{nazwa}` does not exist in the shop!", ephemeral=True)
        return

    nazwa = found_item['nazwa']
    cena = found_item['cena']

    afford = True
    if user_currency:
        if user_id in user_currency:
            if 'equipment' in user_document and user_document['equipment'].get(nazwa, False):
                if lang == "PL":
                    await ctx.send(f"`[❌]:` Posiadasz już ten przedmiot!", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[❌]:` You already have this item!", ephemeral=True)
                return

            new_currency = user_currency[str(ctx.user.id)] - cena
            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
            if user_currency[str(ctx.user.id)] < cena:
                afford = False
        else:
            afford = False
    else:
        afford = False

    if afford == False:
        if lang == "PL":
            await ctx.send(f"`[❌]:` Nie stać cię na to!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[❌]:` You can't afford it!", ephemeral=True)
        return

    if 'equipment' not in user_document:
        user_document['equipment'] = {}

    equipment = user_document['equipment']
    equipment[nazwa] = True

    users_collection.update_one({'_id': user_id}, {'$set': {'equipment': equipment}}, upsert=True)

    if lang == "PL":
        await ctx.send(f"`[✅]:` Kupiono przedmiot `{nazwa}` za {cena} waluty.", ephemeral=True)
    elif lang == "ENG":
        await ctx.send(f"`[✅]:` Bought item `{nazwa}` for {cena} currency.", ephemeral=True)

#Use
@bot.slash_command(description="Używana do użycia przedmiotu z ekwipunku")
async def use(ctx, id: int, nazwa: str = None):
    try:
        server_id = str(ctx.guild.id)
        user_id = str(ctx.user.id)

        user_document = users_collection.find_one({'_id': user_id})
        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            if 'language' in settings_document:
                lang = settings_document['language']
            else:
                lang = "PL"
        else:
            lang = "PL"

        if not user_document or 'equipment' not in user_document:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Nie masz żadnego przedmiotu w ekwipunku!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` You have no item in your inventory!", ephemeral=True)
            return

        equipment = user_document['equipment']

        if id < 1 or id > len(equipment):
            if lang == "PL":
                await ctx.send(f"`[❌]:` Nieprawidłowe ID przedmiotu!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` Invalid item ID!", ephemeral=True)
            return

        nazwa = list(equipment.keys())[id - 1]

        if nazwa not in equipment or not equipment[nazwa]:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Nie masz przedmiotu o nazwie `{nazwa}` w ekwipunku!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` You do not have an item named `{nazwa}` in your inventory!", ephemeral=True)
            return

        guild = ctx.guild
        if settings_document.get("kategoriaOtwieraniaTicketow", False):
            kategoriaID = settings_document.get("kategoriaOtwieraniaTicketow", False)
            kategoria = guild.get_channel(kategoriaID)
        else:
            kategoria = guild

        channel_name = f"sklep-{ctx.user.name}"
        ticket_channel = nextcord.utils.get(guild.channels, name=channel_name)
                    
        if not ticket_channel:
            users_collection.update_one({'_id': user_id}, {'$set': {f'equipment.{nazwa}': False}}, upsert=True)
            user_id = ctx.user.id

            guild = bot.get_guild(ctx.guild.id)
            user = await guild.fetch_member(user_id)
            overwrites = {}

            if kategoria != guild:
                for target, overwrite in kategoria.overwrites.items():
                    overwrites[target] = overwrite

            if settings_document and settings_document.get("weryfikacja", False):
                idroli = settings_document.get("rolaWeryfikacji", False)
                rola = ctx.guild.get_role(idroli)
            else:
                rola = None

            if 'ticketWLRoles' in settings_document:
                for role_id in settings_document['ticketWLRoles']:
                    role = guild.get_role(int(role_id))
                    if role:
                        overwrites[role] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)

            if 'ticketBLRoles' in settings_document:
                for role_id in settings_document['ticketBLRoles']:
                    role = guild.get_role(int(role_id))
                    if role:
                        overwrites[role] = nextcord.PermissionOverwrite(read_messages=False)

            overwrites[user] = nextcord.PermissionOverwrite(read_messages=True, send_messages=True)
            if rola != None:
                overwrites[rola] = nextcord.PermissionOverwrite(read_messages=False)
            overwrites[guild.default_role] = nextcord.PermissionOverwrite(read_messages=False)

            ticket_channel = await kategoria.create_text_channel(f"sklep-{ctx.user.name}", overwrites=overwrites)

            current_time = time.strftime("%Y-%m-%d %H:%M:%S")
            stworzył = f"<t:{int(ctx.user.created_at.timestamp())}:R>"
            dołączył = f"<t:{int(ctx.user.joined_at.timestamp())}:R>"

            if lang == "PL":
                embed = nextcord.Embed(title=f'**Odebranie przedmiotu**', description=f"**Aby zamknąć ticket kliknij przycisk `🔒 Zamknij`**\n\n**Autorem jest {ctx.user.mention} (*{ctx.user.id}*)**\n**Na serwer dołączył** {dołączył}\n**Na Discord dołączył** {stworzył}\n\n\n**INFORMACJA:**\n*Ten ticket został stworzony aby odebrać przedmiot o nazwie `{nazwa}`!*", color=0x00ff00)
                embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                embed.set_thumbnail(url=bot.user.avatar.url)
                embed.set_footer(text=f"{current_time}")
                view = Zamykanie_ticketu()
                await ticket_channel.send(embed=embed, view=view)

            elif lang == "ENG":
                embed = nextcord.Embed(title=f'**Item withdrawal**', description=f"**To close the ticket, click the `🔒 Close` button**\n\n**Author {ctx.user.mention} (*{ctx.user.id}*)**\n**Joined the server** {dołączył}\n**Joined on Discord** {stworzył}\n\n\n**INFORMATION:**\n*This ticket was created to claim an item called `{nazwa}`!", color=0x00ff00)
                embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
                embed.set_thumbnail(url=bot.user.avatar.url)
                embed.set_footer(text=f"{current_time}")
                view = Zamykanie_ticketuENG()
                await ticket_channel.send(embed=embed, view=view)

        else:
            if lang == "PL":
                await ctx.send(f"`[✅]:` Masz już jeden ticket! {ticket_channel.mention}", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` You already have one ticket! {ticket_channel.mention}", ephemeral=True)
            return

        if lang == "PL":
            await ctx.send(f"`[✅]:` Użyto przedmiot `{nazwa}`! Stworzono kanał do odebrania {ticket_channel.mention}!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` Item `{nazwa}` used! A channel for receiving {ticket_channel.mention} has been created!", ephemeral=True)

    except Exception as e:
        if lang == "PL":
            await ctx.send(f"`[❌]:` Wystąpił błąd! Przedmiot mógł ci zostać odebrany! Powiadom o poniższym błędzie administracje (nie jest on spowodowany technicznie) \n\n`{e}`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[❌]:` An error occurred! The item may have been taken away from you! Please notify the administration of the error below (not technical) \n\n`{e}`", ephemeral=True)

#Ekwipunek
@bot.slash_command(description="Wyświetla wszystkie przedmioty w ekwipunku")
async def ekwipunek(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.user.id)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    user_document = users_collection.find_one({'_id': user_id})
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not user_document or 'equipment' not in user_document:
        if lang == "PL":
            await ctx.send(f"`[❌]:` Twój ekwipunek jest pusty!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[❌]:` Your inventory is empty!", ephemeral=True)
        return

    equipment = user_document['equipment']
    items = []

    for id, (nazwa, status) in enumerate(equipment.items(), start=1):
        if status:
            items.append(f"{id} - {nazwa}")

    if not items:
        if lang == "PL":
            await ctx.send(f"`[❌]:` Twój ekwipunek jest pusty!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[❌]:` Your inventory is empty!", ephemeral=True)
        return

    items_text = "\n".join(items)

    if lang == "PL":
        embed = nextcord.Embed(title="Ekwipunek", description=items_text, color=0x00ff00)
    elif lang == "ENG":
        embed = nextcord.Embed(title="Equipment", description=items_text, color=0x00ff00)

    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
    embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Plecak.png")
    embed.set_footer(text=f"Invoked by {ctx.user} | {current_time}")
    await ctx.send(embed=embed)

#Crime
@bot.slash_command(description="Zarabiaj pieniądze! (niezbyt legalnie...)")
async def crime(ctx):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.user.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    user_currency = currency_collection.find_one({"_id": server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    wmin = False
    wmax = False
    wt = False
    if settings_document:
        if 'crimeMin' in settings_document:
            crimeMin = settings_document['crimeMin']
            wmin = True
        if 'crimeMax' in settings_document:
            crimeMax = settings_document['crimeMax']
            wmax = True
        if 'crimeTime' in settings_document:
            crimeTime = settings_document['crimeTime']
            wt = True

    if not settings_document or not settings_document.get("ekonomia", False):
        if lang == "PL":
            await ctx.send("`[❌]:` Aby użyć tej komendy, włącz `ekonomie` używając `/settingsekonomia config`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` To use that command, enable `ekonomia` using `/settingsekonomia config`", ephemeral=True)
        return
    
    if wmin == False or wmax == False or wt == False:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie dokonano konfiguracji! Pierw użyj `/settingsekonomia crime`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` No configuration completed! First use `/settingsekonomia crime`", ephemeral=True)
        return
    
    can = False
    cooldown_data = cooldowns_collection.find_one({"_id": user_id})
    if cooldown_data and "crimeCD" in cooldown_data:
        last_usage = cooldown_data["crimeCD"]
        current_time = datetime.datetime.now()
        cooldown_duration = datetime.timedelta(seconds=crimeTime)
                    
        time_difference = current_time - last_usage
                    
        if time_difference < cooldown_duration:
            time_left = cooldown_duration - time_difference
            if lang == "PL":
                await ctx.send(f"`[❌]:` Cooldown trwa! Spróbuj ponowanie za `{time_left.seconds}` sekund", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` Cooldown continues! Please try again in `{time_left.seconds}` seconds", ephemeral=True)
        else:
            can = True
    else:
        can = True

    if can == True:
        income = round(random.uniform(crimeMin, crimeMax), 2)

        if income > 0:
            if lang == "PL":
                await ctx.send(f"`[✅]:` Pracując nielegalnie zarobiłeś `{income}` waluty!")
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` By working illegally you earned `{income}` of currency!")
        else:
            loss = abs(income)
            if lang == "PL":
                await ctx.send(f"`[❌]:` Pracując nielegalnie straciłeś `{loss}` waluty!")
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` By working illegally you lost your `{loss}` currency!")

        current_time = datetime.datetime.now()
        if cooldown_data:
            cooldowns_collection.update_one({"_id": user_id}, {"$set": {"crimeCD": current_time}}, upsert=True)
        else:
            cooldowns_collection.insert_one({"_id": user_id, "crimeCD": current_time})

        if user_currency:
            if user_id in user_currency:
                new_currency = user_currency[str(ctx.user.id)] + income
                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
            else:
                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: income}})
        else:
            currency_collection.insert_one({"_id": server_id, user_id: income})

        statistics = load_statistics()
        if 'crime' in statistics:
            statistics['crime'] += 1
        else:
            statistics['crime'] = 1
        save_statistics(statistics)

#Deposit
@bot.slash_command(description="Wpłaca pieniądze na konto bankowe")
async def deposit(ctx, ilosc: float):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.user.id)
    bank_user_id = f"{user_id}Bank"
    amount = ilosc

    settings_document = settings_collection.find_one({'_id': server_id})
    user_currency = currency_collection.find_one({"_id": server_id})
    
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if amount <= 0:
        if lang == "PL":
            await ctx.send("`[❌]:` Ilość wpłaty musi być dodatnia!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` Deposit quantity must be positive!", ephemeral=True)
        return

    if not user_currency:
        user_currency = {}

    if user_currency.get(user_id, 0) >= amount:
        user_currency[user_id] -= amount
        user_currency[bank_user_id] = user_currency.get(bank_user_id, 0) + amount
        currency_collection.update_one({"_id": server_id}, {"$set": user_currency}, upsert=True)
        if lang == "PL":
            await ctx.send(f"`[✅]:` Zrealizowano wpłatę `{amount}` na twoje konto bankowe!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` The `{amount}` payment has been made to your bank account!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie masz wystarczającej ilości środków na koncie!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You don't have enough funds in your account!", ephemeral=True)

#Withdraw
@bot.slash_command(description="Wypłaca pieniądze z konta bankowego")
async def withdraw(ctx, ilosc: float):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.user.id)
    bank_user_id = f"{user_id}Bank"
    amount = ilosc

    settings_document = settings_collection.find_one({'_id': server_id})
    user_currency = currency_collection.find_one({"_id": server_id})
    
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if amount <= 0:
        if lang == "PL":
            await ctx.send("`[❌]:` Ilość wypłaty musi być dodatnia!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` Withdrawal amount must be positive!", ephemeral=True)
        return

    if not user_currency:
        user_currency = {}

    if user_currency.get(bank_user_id, 0) >= amount:
        try:
            user_currency[user_id] += amount
        except KeyError:
            currency_collection.update_one({"_id": server_id}, {"$set": {user_id: amount}})

        user_currency[bank_user_id] -= amount
        currency_collection.update_one({"_id": server_id}, {"$set": user_currency}, upsert=True)
        if lang == "PL":
            await ctx.send(f"`[✅]:` Zrealizowano wypłatę `{amount}` z twojego konta bankowego!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` The `{amount}` withdrawal has been made from your bank account!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie masz wystarczającej ilości środków na koncie bankowym!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You don't have enough funds in your bank account!", ephemeral=True)

#Rob
@bot.slash_command(description="Zarabiaj pieniądze okradając!")
async def rob(ctx, osoba: nextcord.Member):
    server_id = str(ctx.guild.id)
    user_id = str(ctx.user.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    user_currency = currency_collection.find_one({"_id": server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    osoba_id = str(osoba.id)
    wmin = False
    wmax = False
    wt = False
    if settings_document:
        if 'robMin' in settings_document:
            robMin = settings_document['robMin']
            wmin = True
        if 'robMax' in settings_document:
            robMax = settings_document['robMax']
            wmax = True
        if 'robTime' in settings_document:
            robTime = settings_document['robTime']
            wt = True

    if not settings_document or not settings_document.get("ekonomia", False):
        if lang == "PL":
            await ctx.send("`[❌]:` Aby użyć tej komendy, włącz `ekonomie` używając `/settingsekonomia config`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` To use that command, enable `ekonomia` using `/settingsekonomia config`", ephemeral=True)
        return
    
    if wmin == False or wmax == False or wt == False:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie dokonano konfiguracji! Pierw użyj `/settingsekonomia work`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` No configuration completed! First use `/settingsekonomia work`", ephemeral=True)
        return
    
    if not osoba_id in user_currency or 0 > user_currency[osoba_id]:
        if lang == "PL":
            await ctx.send("`[❌]:` Ten użytkownik nie ma żadnych pieniędzy w portfelu!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` This user has no money in his wallet!", ephemeral=True)
        return
    
    can = False
    cooldown_data = cooldowns_collection.find_one({"_id": user_id})
    if cooldown_data and "robCD" in cooldown_data:
        last_usage = cooldown_data["robCD"]
        current_time = datetime.datetime.now()
        cooldown_duration = datetime.timedelta(seconds=robTime)
                    
        time_difference = current_time - last_usage
                    
        if time_difference < cooldown_duration:
            time_left = cooldown_duration - time_difference
            if lang == "PL":
                await ctx.send(f"`[❌]:` Cooldown trwa! Spróbuj ponowanie za `{time_left.seconds}` sekund", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` Cooldown continues! Please try again in `{time_left.seconds}` seconds", ephemeral=True)
        else:
            can = True
    else:
        can = True

    if can == True:
        income = round(random.uniform(robMin, robMax), 2)
        if 0 < income and income < user_currency[osoba_id]:
            if lang == "PL":
                await ctx.send(f"`[✅]:` Okradłeś {osoba}, zarobiłeś `{income}` waluty!")
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` You robbed {osoba}, you earned `{income}` currency!")
        else:
            loss = abs(income)
            if lang == "PL":
                await ctx.send(f"`[❌]:` Przy próbie okradnięcia {osoba}, straciłeś `{loss}` waluty!")
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` When trying to rob {osoba}, you lost `{loss}` currency!")

        current_time = datetime.datetime.now()
        if cooldown_data:
            cooldowns_collection.update_one({"_id": user_id}, {"$set": {"robCD": current_time}}, upsert=True)
        else:
            cooldowns_collection.insert_one({"_id": user_id, "robCD": current_time})

        if user_currency:
            if user_id in user_currency:
                new_currency = user_currency[str(ctx.user.id)] + income
                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: new_currency}})
            else:
                currency_collection.update_one({"_id": server_id}, {"$set": {user_id: income}})

            new_currency = user_currency[str(osoba.id)] - income
            currency_collection.update_one({"_id": server_id}, {"$set": {osoba_id: new_currency}})
        
        else:
            currency_collection.insert_one({"_id": server_id, user_id: income})

        statistics = load_statistics()
        if 'rob' in statistics:
            statistics['rob'] += 1
        else:
            statistics['rob'] = 1
        save_statistics(statistics)

#Ruletka
@settingsekonomia.subcommand(description="Ustawia komendę ruletka")
async def ruletka(ctx, odstep: str, minkwota: int = 1, maxkwota: int = 99999999, mnoznikczerwone: int = 2, mnoznikczarne: int = 2, mnoznikzielone: int = 5):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document or not settings_document.get("ekonomia", False):
        if lang == "PL":
            await ctx.send("`[❌]:` Aby użyć tej komendy, włącz `ekonomie` używając `/settingsekonomia config`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` To use that command, enable `ekonomia` using `/settingsekonomia config`", ephemeral=True)
        return

    if ctx.user.guild_permissions.manage_messages:
        time = odstep
        work_time_seconds = parse_duration(time)
        if work_time_seconds is None:
            if lang == "PL":
                await ctx.send("`[❌]:` Niepoprawny format czasu, przykład poprawnych formatów: 10s, 20m, 10h!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` Incorrect time format, example of valid formats: 10s, 20m, 10h", ephemeral=True)
            return

        if settings_document:
            update_data = {
                "$set": {
                    "_id": server_id,
                    "ruletkaTime": work_time_seconds,
                    "ruletkaMin": minkwota,
                    "ruletkaMax": maxkwota,
                    "ruletkaCzerwone": mnoznikczerwone,
                    "ruletkaCzarne": mnoznikczarne,
                    "ruletkaZielone": mnoznikzielone
                }
            }
            settings_collection.update_one({'_id': server_id}, update_data)

        else:
            data = {
                "_id": server_id,
                "ruletkaTime": work_time_seconds,
                "ruletkaMin": minkwota,
                "ruletkaMax": maxkwota,
                "ruletkaCzerwone": mnoznikczerwone,
                "ruletkaCzarne": mnoznikczarne,
                "RuletkaZielone": mnoznikzielone
            }
            settings_collection.insert_one({'_id': server_id}, data)

        if lang == "PL":
            await ctx.send(f"`[✅]:` Pomyślnie ustawiono komendę `ruletka`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` `ruletka` command successfully set!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby ustawić `work`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to set `work` command!", ephemeral=True)

#Ruletka
@bot.slash_command(description="Postaw na jedno i wygraj!")
async def ruletka(ctx, kwota: int):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    server_id = str(ctx.guild.id)
    user_id = str(ctx.user.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    user_currency = currency_collection.find_one({"_id": server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    rt = False
    if settings_document:
        if 'ruletkaTime' in settings_document:
            ruletkaTime = settings_document['ruletkaTime']
            rt = True
        if 'ruletkaMin' in settings_document:
            ruletkaMin = settings_document['ruletkaMin']
        else:
            ruletkaMin = 1

        if 'ruletkaMax' in settings_document:
            ruletkaMax = settings_document['ruletkaMax']
        else:
            ruletkaMax = 99999999999

    if not settings_document or not settings_document.get("ekonomia", False):
        if lang == "PL":
            await ctx.send("`[❌]:` Aby użyć tej komendy, włącz `ekonomie` używając `/settingsekonomia config`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` To use that command, enable `ekonomia` using `/settingsekonomia config`", ephemeral=True)
        return
    
    if rt == False:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie dokonano konfiguracji! Pierw użyj `/settingsekonomia ruletka`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` No configuration completed! First use `/settingsekonomia ruletka`", ephemeral=True)
        return
    
    if kwota < ruletkaMin or kwota > ruletkaMax:
        if lang == "PL":
            await ctx.send(f"`[❌]:` Maksymalnie możesz postawić *{ruletkaMax}*, a minimalnie *{ruletkaMin}*", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[❌]:` You can bet maximum *{ruletkaMax}* and minimum *{ruletkaMin}*", ephemeral=True)
        return

    can = False
    cooldown_data = cooldowns_collection.find_one({"_id": user_id})
    if cooldown_data and "ruletkaCD" in cooldown_data:
        last_usage = cooldown_data["ruletkaCD"]
        current_time = datetime.datetime.now()
        cooldown_duration = datetime.timedelta(seconds=ruletkaTime)
                    
        time_difference = current_time - last_usage
                    
        if time_difference < cooldown_duration:
            time_left = cooldown_duration - time_difference
            if lang == "PL":
                await ctx.send(f"`[❌]:` Cooldown trwa! Spróbuj ponowanie za `{time_left.seconds}` sekund", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` Cooldown continues! Please try again in `{time_left.seconds}` seconds", ephemeral=True)
        else:
            can = True
    else:
        can = True

    if can == True:
        user_money = user_currency.get(user_id, 0)
        if kwota <= 0:
            if lang == "PL":
                await ctx.send("`[❌]:` Kwota musi być większa niż `0`!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` The amount must be greater than `0`!", ephemeral=True)
            return

        if user_money < kwota:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Nie masz wystarczająco dużo pieniędzy. Aktualny stan konta: `{user_money}`", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` You don't have enough money. Current account balance: `{user_money}`", ephemeral=True)
            return
        
        teksty = ["Na co chciałbyś postawić?", "Wybierz dobrze!", "Zawsze możesz wrócić!", "Powodzenia!", "99% hazardzistów odchodzi od stołu przed wielką wygraną!", "Zawsze możesz się zapożyczyć!"]
        tekstyENG = ["What would you like to bet on?", "Choose well!", "You can always come back!", "Good luck!", "99% of gamblers leave the table before big win!", "You can always borrow!"]

        if lang == "PL":
            tekst = random.choice(teksty)
            embed = nextcord.Embed(title="Ruletka 🎲", description=tekst, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {ctx.user} | {current_time}")
            view = Ruletka(kwota, ctx.user.id)

        elif lang == "ENG":
            tekst = random.choice(tekstyENG)
            embed = nextcord.Embed(title="Roulette 🎲", description=tekst, color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Ruletka.png")
            embed.set_footer(text=f"Invoked by {ctx.user} | {current_time}")
            view = RuletkaENG(kwota, ctx.user.id)

        global ruletkamsg
        ruletkamsg = await ctx.send(embed=embed, view=view)

        current_time = datetime.datetime.now()
        if cooldown_data:
            cooldowns_collection.update_one({"_id": user_id}, {"$set": {"ruletkaCD": current_time}}, upsert=True)
        else:
            cooldowns_collection.insert_one({"_id": user_id, "ruletkaCD": current_time})

        statistics = load_statistics()
        if 'ruletka' in statistics:
            statistics['ruletka'] += 1
        else:
            statistics['ruletka'] = 1
        save_statistics(statistics)

#Blackjack
@settingsekonomia.subcommand(description="Ustawia komendę blackjack")
async def blackjack(ctx, odstep: str, minkwota: int = 1, maxkwota: int = 99999999):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document or not settings_document.get("ekonomia", False):
        if lang == "PL":
            await ctx.send("`[❌]:` Aby użyć tej komendy, włącz `ekonomie` używając `/settingsekonomia config`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` To use that command, enable `ekonomia` using `/settingsekonomia config`", ephemeral=True)
        return

    if ctx.user.guild_permissions.manage_messages:
        time = odstep
        work_time_seconds = parse_duration(time)
        if work_time_seconds is None:
            if lang == "PL":
                await ctx.send("`[❌]:` Niepoprawny format czasu, przykład poprawnych formatów: 10s, 20m, 10h!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` Incorrect time format, example of valid formats: 10s, 20m, 10h", ephemeral=True)
            return

        if settings_document:
            update_data = {
                "$set": {
                    "_id": server_id,
                    "blackjackTime": work_time_seconds,
                    "blackjackMin": minkwota,
                    "blackjackMax": maxkwota,
                }
            }
            settings_collection.update_one({'_id': server_id}, update_data)

        else:
            data = {
                "_id": server_id,
                "blackjackTime": work_time_seconds,
                "blackjackMin": minkwota,
                "blackjackMax": maxkwota,
            }
            settings_collection.insert_one({'_id': server_id}, data)

        if lang == "PL":
            await ctx.send(f"`[✅]:` Pomyślnie ustawiono komendę `blackjack`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` `blackjack` command successfully set!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby ustawić `blackjack`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to set `blackjack` command!", ephemeral=True)

#Blackjack
@bot.slash_command(description="Spróbuj szczęścia!")
async def blackjack(ctx, kwota: int):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    server_id = str(ctx.guild.id)
    user_id = str(ctx.user.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    user_currency = currency_collection.find_one({"_id": server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    bt = False
    if settings_document:
        if 'blackjackTime' in settings_document:
            blackjackTime = settings_document['blackjackTime']
            bt = True
        if 'blackjackMin' in settings_document:
            blackjackMin = settings_document['blackjackMin']
        else:
            blackjackMin = 1

        if 'blackjackMax' in settings_document:
            blackjackMax = settings_document['blackjackMax']
        else:
            blackjackMax = 99999999999

    if not settings_document or not settings_document.get("ekonomia", False):
        if lang == "PL":
            await ctx.send("`[❌]:` Aby użyć tej komendy, włącz `ekonomie` używając `/settingsekonomia config`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` To use that command, enable `ekonomia` using `/settingsekonomia config`", ephemeral=True)
        return
    
    if bt == False:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie dokonano konfiguracji! Pierw użyj `/settingsekonomia blackjack`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` No configuration completed! First use `/settingsekonomia blackjack`", ephemeral=True)
        return
    
    if kwota < blackjackMin or kwota > blackjackMax:
        if lang == "PL":
            await ctx.send(f"`[❌]:` Maksymalnie możesz postawić *{blackjackMax}*, a minimalnie *{blackjackMin}*", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[❌]:` You can bet maximum *{blackjackMax}* and minimum *{blackjackMin}*", ephemeral=True)
        return

    can = False
    cooldown_data = cooldowns_collection.find_one({"_id": user_id})
    if cooldown_data and "blackjackCD" in cooldown_data:
        last_usage = cooldown_data["blackjackCD"]
        current_time = datetime.datetime.now()
        cooldown_duration = datetime.timedelta(seconds=blackjackTime)
                    
        time_difference = current_time - last_usage
                    
        if time_difference < cooldown_duration:
            time_left = cooldown_duration - time_difference
            if lang == "PL":
                await ctx.send(f"`[❌]:` Cooldown trwa! Spróbuj ponowanie za `{time_left.seconds}` sekund", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` Cooldown continues! Please try again in `{time_left.seconds}` seconds", ephemeral=True)
        else:
            can = True
    else:
        can = True

    if can == True:
        user_money = user_currency.get(user_id, 0)
        if kwota <= 0:
            if lang == "PL":
                await ctx.send("`[❌]:` Kwota musi być większa niż `0`!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` The amount must be greater than `0`!", ephemeral=True)
            return

        if user_money < kwota:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Nie masz wystarczająco dużo pieniędzy. Aktualny stan konta: `{user_money}`", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` You don't have enough money. Current account balance: `{user_money}`", ephemeral=True)
            return
        
        karty = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        kartaG = random.choice(karty)
        karty.remove(kartaG)
        kartaK = random.choice(karty)
        karty.remove(kartaK)
        if lang == "PL":
            embed = nextcord.Embed(title="Blackjack 🃏", description=f"Wylosowałeś kartę z wartością {kartaG}, grasz dalej?", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
            embed.set_footer(text=f"Invoked by {ctx.user} | {current_time}")
            view = Blackjack(karty, kwota, kartaG, kartaK, ctx.user.id)

        elif lang == "ENG":
            embed = nextcord.Embed(title="Blackjack 🃏", description=f"You have drawn a card with the value {kartaG}, are you still playing?", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Karty.png")
            embed.set_footer(text=f"Invoked by {ctx.user} | {current_time}")
            view = BlackjackENG(kwota, karty, kartaG, kartaK, ctx.user.id)

        global blackjackmsg
        blackjackmsg = await ctx.send(embed=embed, view=view)

        current_time = datetime.datetime.now()
        if cooldown_data:
            cooldowns_collection.update_one({"_id": user_id}, {"$set": {"blackjackCD": current_time}}, upsert=True)
        else:
            cooldowns_collection.insert_one({"_id": user_id, "blackjackCD": current_time})

        statistics = load_statistics()
        if 'blackjack' in statistics:
            statistics['blackjack'] += 1
        else:
            statistics['blackjack'] = 1
        save_statistics(statistics)

#Random IMG
@bot.slash_command(description="Wyślij losową grafikę z internetu")
async def randomimg(ctx):
    try:
        server_id = str(ctx.guild.id)
        settings_document = settings_collection.find_one({'_id': server_id})

        if settings_document:
            if 'language' in settings_document:
                lang = settings_document['language']
            else:
                lang = "PL"
        else:
            lang = "PL"

        if settings_document and settings_document.get("randomIMG", False):
            response = requests.get("https://source.unsplash.com/random")
            if response.status_code == 200:
                img_url = response.url
                if lang == "PL":
                    embed = nextcord.Embed(title="*Losowa grafika*", color=0x00FF00, url=img_url)
                elif lang == "ENG":
                    embed = nextcord.Embed(title="*Random image*", color=0x00FF00, url=img_url)

                embed.set_image(url=img_url)
                await ctx.send(embed=embed)
            else:
                await ctx.send("`[❌]:` Nie udało się pobrać losowej grafiki!", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Komenda `random img` nie jest włączona dla tego serwera.", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` The `random img` command is not enabled for this server.", ephemeral=True)
    except Exception as e:
        await ctx.send(f"Wystąpił błąd: {str(e)}")

#Invites
@bot.slash_command(description="Sprawdza zaproszenia danego użytkownika")
async def invites(ctx, osoba: nextcord.Member):
    user_id = str(osoba.id)
    server_id = str(ctx.guild.id)
    user_document = users_collection.find_one({'_id': user_id})
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if user_document and 'invites' in user_document:
        if server_id in user_document['invites']:
            data = user_document['invites'][server_id]
            invites = data.get('Invites', 0)
            left = data.get('Left', 0)
            real = invites - left
            user = ctx.user

            if user.avatar:
                avatar_url = osoba.avatar.url
            else:
                avatar_url = no_avatar

            if lang == "PL":
                embed = nextcord.Embed(title=f"Zaproszenia", description=f"Dołączenia: `{invites}`\nWyjścia: `{left}`\n\n__**Prawdziwe:**__ `{real}`", color=0x00ff00)
            elif lang == "ENG":
                embed = nextcord.Embed(title=f"Invites", description=f"Join: `{invites}`\nLeaves: `{left}`\n\n__**Real:**__ `{real}`", color=0x00ff00) 
            embed.set_author(name=osoba.display_name, icon_url=avatar_url)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Plus.png")
            await ctx.send(embed=embed)
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Ten użytkownik nie ma zaproszeń na tym serwerze!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` User has no invite data on this server!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Ten użytkownik nie ma zaproszeń na tym serwerze!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` User has no invite data on this server!", ephemeral=True)

#Add invites
@add.subcommand(description='Dodaje zaproszenia')
async def invites(ctx, osoba: nextcord.Member, ilosc: int):
    user_id = str(osoba.id)
    server_id = str(ctx.guild.id)
    user_document = users_collection.find_one({'_id': user_id})
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.administrator:
        if user_document and 'invites' in user_document:
            if server_id not in user_document['invites']:
                user_document['invites'][server_id] = {
                    'Invites': 0,
                    'Left': 0
                }

            user_document['invites'][server_id]['Invites'] += ilosc

            users_collection.update_one({'_id': user_id}, {'$set': {'invites': user_document['invites']}})
            if lang == "PL":
                await ctx.send(f"`[✅]:` Pomyślnie dodano zaproszenia `{ilosc}` dla {osoba.display_name} na tym serwerze!")
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Successfully added `{ilosc}` invites for {osoba.display_name} on this server!")
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Ten użytkownik nie ma zaproszeń na tym serwerze! (Musi pierw kogoś zaprosić)", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` User has no invite data on this server! (He has to invite someone first)", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnień `administratora` aby dodać partnerstwa!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have 'administrator' permission to add partnerships!", ephemeral=True)

#Remove invites
@remove.subcommand(description='Usuwa zaproszenia')
async def invites(ctx, osoba: nextcord.Member, ilosc: int):
    user_id = str(osoba.id)
    server_id = str(ctx.guild.id)
    user_document = users_collection.find_one({'_id': user_id})
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.administrator:
        if user_document and 'invites' in user_document:
            if server_id not in user_document['invites']:
                user_document['invites'][server_id] = {
                    'Invites': 0,
                    'Left': 0
                }

            user_document['invites'][server_id]['Invites'] -= ilosc

            users_collection.update_one({'_id': user_id}, {'$set': {'invites': user_document['invites']}})
            if lang == "PL":
                await ctx.send(f"`[✅]:` Pomyślnie usunięto zaproszenia `{ilosc}` dla {osoba.display_name} na tym serwerze!")
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Successfully removed `{ilosc}` invites for {osoba.display_name} on this server!")
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Ten użytkownik nie ma zaproszeń na tym serwerze!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` User has no invite data on this server!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnień `administratora` aby usunąć partnerstwa!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have 'administrator' permission to remove partnerships!", ephemeral=True)

#Ticket WL Add
@whitelista.subcommand(description="Dodaje rolę, która ma mieć dostęp do ticketów")
async def ticketadd(ctx, rola: nextcord.Role):
    server_id = str(ctx.guild.id)
    role_id = str(rola.id)

    settings_document = settings_collection.find_one({'_id': server_id})

    if not settings_document:
        settings_document = {
            '_id': server_id,
            'ticketWLRoles': []
        }

    if 'ticketWLRoles' not in settings_document:
        settings_document['ticketWLRoles'] = []

    if role_id not in settings_document['ticketWLRoles']:
        settings_document['ticketWLRoles'].append(role_id)
        settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)
        await ctx.send(f"`[✅]:` Dodano rolę {rola.mention} do listy ról z dostępem do ticketów.", ephemeral=True)

#Ticket WL Remove
@whitelista.subcommand(description="Usuwa rolę, która ma mieć dostęp do ticketów")
async def ticketremove(ctx, rola: nextcord.Role):
    server_id = str(ctx.guild.id)
    role_id = str(rola.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        if not settings_document or 'ticketWLRoles' not in settings_document:
            if lang == "PL":
                await ctx.send("`[❌]:` Na tym serwerze nie ma zdefiniowanych ról z dostępem do ticketów!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` There are no roles defined on this server with access to tickets!", ephemeral=True)
            return

        if role_id in settings_document['ticketWLRoles']:
            settings_document['ticketWLRoles'].remove(role_id)
            settings_collection.update_one({'_id': server_id}, {'$set': settings_document})
            if lang == "PL":
                await ctx.send(f"`[✅]:` Usunięto rolę {rola.mention} z listy ról z dostępem do ticketów!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` The {rola.mention} role has been removed from the list of roles with ticket access!", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Rola {rola.mention} nie jest na liście ról z dostępem do ticketów!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` The {rola.mention} role is not on the list of roles with ticket access!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby włączyć/wyłączyć `clear`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to enable/disable `clear`!", ephemeral=True)

#Ticket BL Add
@blacklista.subcommand(description="Dodaje rolę, która nie ma mieć dostępu do ticketów")
async def ticketadd(ctx, rola: nextcord.Role):
    server_id = str(ctx.guild.id)
    role_id = str(rola.id)

    settings_document = settings_collection.find_one({'_id': server_id})

    if not settings_document:
        settings_document = {
            '_id': server_id,
            'ticketWLRoles': []
        }

    if 'ticketBLRoles' not in settings_document:
        settings_document['ticketBLRoles'] = []

    if role_id not in settings_document['ticketBLRoles']:
        settings_document['ticketBLRoles'].append(role_id)
        settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)
        await ctx.send(f"`[✅]:` Dodano rolę {rola.mention} do listy ról z brakiem dostępu do ticketów.", ephemeral=True)

#Ticket BL Remove
@blacklista.subcommand(description="Usuwa rolę, która nie ma mieć dostępu do ticketów")
async def ticketremove(ctx, rola: nextcord.Role):
    server_id = str(ctx.guild.id)
    role_id = str(rola.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        if not settings_document or 'ticketBLRoles' not in settings_document:
            if lang == "PL":
                await ctx.send("`[❌]:` Na tym serwerze nie ma zdefiniowanych ról z dostępem do ticketów!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` There are no roles defined on this server with access to tickets!", ephemeral=True)
            return

        if role_id in settings_document['ticketBLRoles']:
            settings_document['ticketBLRoles'].remove(role_id)
            settings_collection.update_one({'_id': server_id}, {'$set': settings_document})
            if lang == "PL":
                await ctx.send(f"`[✅]:` Usunięto rolę {rola.mention} z listy ról z brakiem dostępu do ticketów!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` The {rola.mention} role has been removed from the list of roles without ticket access!", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Rola {rola.mention} nie jest na liście ról z brakiem dostępu do ticketów!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` The {rola.mention} role is not on the list of roles with ticket access!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby usunąć rolę", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to remove the role", ephemeral=True)

#Selfchannel
@settingsconfig.subcommand(description="Wyświetla konfigurację własnych kanałów")
async def selfchannel(ctx):
    author = ctx.user
    server_id = str(ctx.guild.id)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    settings_document = settings_collection.find_one({'_id': server_id})

    if not settings_document:
        settings_document = {'_id': server_id}

    if settings_document.get('selfchannel', False):
        ticket_status = "on"
    else:
        ticket_status = "off"

    idkanalu = settings_document.get('KanalSelfchannel')

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if lang == "PL":
        view = Wylaczanie_Wlaczanie_selfchannel()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Selfchannel settings**', description=f"\n**Status `{ticket_status}`**\n**Kanał: <#{idkanalu}>**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Selfchannel settings**', description=f"**Status `{ticket_status}`**\n**Channel: <#{idkanalu}>**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Selfchannel settings**', description=f"**Status `{ticket_status}`**\n**Channel: `None`**\n\n**Command `/settingsConfig kanal selfchannel`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
    elif lang == "ENG":
        view = Wylaczanie_Wlaczanie_selfchannelENG()
        if idkanalu and ticket_status == "on":
            embed = nextcord.Embed(title=f'**Selfchannel settings**', description=f"\n**Status `{ticket_status}`**\n**Channel: <#{idkanalu}>**", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        elif idkanalu:
            embed = nextcord.Embed(title=f'**Selfchannel settings**', description=f"**Status `{ticket_status}`**\n**Channel: <#{idkanalu}>**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)
        else:
            embed = nextcord.Embed(title=f'**Selfchannel settings**', description=f"**Status `{ticket_status}`**\n**Channel: `None`**\n\n**Command `/settingsConfig kanal selfchannel`**", color=0xe40c0c)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")
            await ctx.send(embed=embed, view=view)

#Selfchannel
@kanal.subcommand(description="Ustawia kanał własnych kanałów")
async def selfchannel(ctx, kanał: nextcord.VoiceChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:
        if not settings_document:
            settings_document = {'_id': server_id}

        settings_document['KanalSelfchannel'] = kanał.id

        settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

        if lang == "PL":
            await ctx.send(f"`[✅]:` Kanał funkcji `selfchannel`: <#{kanał.id}>", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` Channel of the `selfchannel` function: <#{kanał.id}>", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić kanał dla `selfchannel`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set up a channel for `selfchannel`!", ephemeral=True)

#Selfchannel
@bot.slash_command(description="Tak")
async def selfchannel(ctx):
    await ctx.send("Tak")

#Selfchannel max
@selfchannel.subcommand(description="Ustawia max użytkowników na własnym kanale")
async def max(ctx, kanal: nextcord.VoiceChannel, max: int):
    channel_id = kanal.id
    user_id = ctx.user.id
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    users_document = users_collection.find_one({'_id': "Info"})
    if "selfchannels" in users_document:
        for channel_info in users_document["selfchannels"]:
            if channel_info["id"] == channel_id and channel_info["author"] == user_id:
                await kanal.edit(user_limit=max)
                if lang == "PL":
                    await ctx.send(f"`[✅]:` Pomyślnie ustawiono maksymalną liczbę użytkowników na kanale {kanal.mention} na `{max}`!", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send(f"`[✅]:`You have successfully set the maximum number of users on {kanal.mention} to `{max}`!", ephemeral=True)
                return

    if lang == "PL":
        await ctx.send(f"`[❌]:` Podany kanał nie jest *własnym kanałem* lub nie jesteś jego właścicielem!", ephemeral=True)
    elif lang == "ENG":
        await ctx.send(f"`[❌]:` The specified channel is not *your own channel* or you do not own it!", ephemeral=True)

#Role
@add.subcommand(description="Nadaje rolę użytkownikowi")
async def role(ctx, rola: nextcord.Role, uzytkownik: nextcord.Member = None):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"
    if ctx.user.guild_permissions.manage_roles and uzytkownik == None:
        members_without_role = [member for member in ctx.guild.members if rola not in member.roles]
        if lang == "PL":
            await ctx.send(f'`[✅]:` Dodano rolę *{rola.mention}* wszystkim użytkownikom!')
        elif lang == "ENG":
            await ctx.send(f'`[✅]:` Added *{rola.mention}* role to all users!')
        for member in members_without_role:
            await member.add_roles(rola)

    elif ctx.user.guild_permissions.manage_roles:
        if ctx.user.top_role > rola:
            await uzytkownik.add_roles(rola)
            if lang == "PL":
                await ctx.send(f'`[✅]:` Dodano rolę *{rola.mention}* użytkownikowi *{uzytkownik.mention}*!')
            elif lang == "ENG":
                await ctx.send(f'`[✅]:` Added *{rola.mention}* role to user *{uzytkownik.mention}*!')
        else:
            if lang == "PL":
                await ctx.send('`[❌]:` Nie masz odpowiednich uprawnień, aby dodać tę rolę!', ephemeral=True)
            elif lang == "ENG":
                await ctx.send('`[❌]:` You do not have the appropriate permissions to add this role!', ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send('`[❌]:` Nie masz uprawnień do zarządzania rolami!', ephemeral=True)
        elif lang == "ENG":
            await ctx.send('`[❌]:` You do not have permission to manage roles!', ephemeral=True)

#Role
@remove.subcommand(description="Usuwa rolę użytkownikowi")
async def rola(ctx, rola: nextcord.Role, uzytkownik: nextcord.Member):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_roles:
        if ctx.user.top_role > rola:
            await uzytkownik.remove_roles(rola)
            if lang == "PL":
                await ctx.send(f'`[✅]:` Usunięto rolę *{rola.mention}* użytkownikowi *{uzytkownik.mention}*!')
            elif lang == "ENG":
                await ctx.send(f'`[✅]:` Removed *{rola.mention}* role from user *{uzytkownik.mention}*!')
        else:
            if lang == "PL":
                await ctx.send('`[❌]:` Nie masz odpowiednich uprawnień, aby usunąć tę rolę!', ephemeral=True)
            elif lang == "ENG":
                await ctx.send('`[❌]:` You do not have the appropriate permissions to remove this role!', ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send('`[❌]:` Nie masz uprawnień do zarządzania rolami!', ephemeral=True)
        elif lang == "ENG":
            await ctx.send('`[❌]:` You do not have permission to manage roles!', ephemeral=True)

#Boty
@kanal.subcommand(description="Ustawia kanał wyświetlający ilość botów!")
async def statyboty(ctx, kanal: nextcord.VoiceChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:
        if kanal.permissions_for(ctx.guild.me).manage_channels:

            if not settings_document:
                settings_document = {'_id': server_id}

            settings_document['kanalStatystykiBoty'] = kanal.id

            settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

            if lang == "PL":
                await ctx.send(f"`[✅]:` Kanał funkcji `statyboty`: <#{kanal.id}>", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Channel of the `statyboty` function: <#{kanal.id}>", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Bot nie posiada uprawnień do edycji!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` The bot does not have permission to edit!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić kanał dla `statyboty`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set up a channel for `statyboty`!", ephemeral=True)

#Osoby
@kanal.subcommand(description="Ustawia kanał wyświetlający ilość użytkowników!")
async def statyosoby(ctx, kanal: nextcord.VoiceChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:
        if kanal.permissions_for(ctx.guild.me).manage_channels:

            if not settings_document:
                settings_document = {'_id': server_id}

            settings_document['kanalStatystykiOsoby'] = kanal.id

            settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

            if lang == "PL":
                await ctx.send(f"`[✅]:` Kanał funkcji `statyosoby`: <#{kanal.id}>", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Channel of the `statyosoby` function: <#{kanal.id}>", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Bot nie posiada uprawnień do edycji!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` The bot does not have permission to edit!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić kanał dla `statyosoby`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set up a channel for `statyosoby`!", ephemeral=True)

#Kanaly
@kanal.subcommand(description="Ustawia kanał wyświetlający ilość kanałów!")
async def statykanaly(ctx, kanal: nextcord.VoiceChannel):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_channels:
        if kanal.permissions_for(ctx.guild.me).manage_channels:

            if not settings_document:
                settings_document = {'_id': server_id}

            settings_document['kanalStatystykiKanaly'] = kanal.id

            settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

            if lang == "PL":
                await ctx.send(f"`[✅]:` Kanał funkcji `statykanaly`: <#{kanal.id}>", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Channel of the `statykanaly` function: <#{kanal.id}>", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send(f"`[❌]:` Bot nie posiada uprawnień do edycji!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` The bot does not have permission to edit!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage channels` aby ustawić kanał dla `statykanaly`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage channels` permission to set up a channel for `statykanaly`!", ephemeral=True)

#Statystyki
@settingsconfig.subcommand(description="Wyświetla konfigurację statystyk!")
async def statystyki(ctx):
    server_id = str(ctx.guild.id)
    author = ctx.user
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document:
        settings_document = {'_id': server_id}

    if settings_document.get('statystyki', False):
        statystyki_status = "on"
        color = 0x00ff00
    else:
        statystyki_status = "off"
        color = 0xe40c0c

    if settings_document.get('kanalStatystykiOsoby'):
        kanalstatyOsoby = settings_document.get('kanalStatystykiOsoby')
        kanalstatyOsoby = bot.get_channel(kanalstatyOsoby)
        kanalstatyOsoby = f"{kanalstatyOsoby.mention}"
    else:
        kanalstatyOsoby = "`Brak - /settingsconfig kanal osoby`"

    if settings_document.get('kanalStatystykiBoty'):
        kanalstatyBoty = settings_document.get('kanalStatystykiBoty')
        kanalstatyBoty = bot.get_channel(kanalstatyBoty)
        kanalstatyBoty = f"{kanalstatyBoty.mention}"
    else:
        kanalstatyBoty = "`Brak - /settingsconfig kanal statyboty`"

    if settings_document.get('kanalStatystykiKanaly'):
        kanalstatyKanaly = settings_document.get('kanalStatystykiKanaly')
        kanalstatyKanaly = bot.get_channel(kanalstatyKanaly)
        kanalstatyKanaly = f"{kanalstatyKanaly.mention}"
    else:
        kanalstatyKanaly = "`Brak - /settingsconfig kanal statykanaly`"

    if lang == "PL":
        view = Wylaczanie_Wlaczanie_statystyk()
        embed = nextcord.Embed(title=f'**Ustawienia statystyk**', description=f"\n**Status `{statystyki_status}`**\n\n**Osoby - {kanalstatyOsoby}**\n**Boty - {kanalstatyBoty}**\n**Kanały - {kanalstatyKanaly}**", color=color)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        await ctx.send(embed=embed, view=view)
    elif lang == "ENG":
        view = Wylaczanie_Wlaczanie_statystykENG()
        embed = nextcord.Embed(title=f'**Statistics settings**', description=f"\n**Status `{statystyki_status}`**\n\n**Members - {kanalstatyOsoby}**\n**Bots - {kanalstatyBoty}**\n**Channels - {kanalstatyKanaly}**", color=color)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        await ctx.send(embed=embed, view=view)

#Premium
@bot.slash_command(description="Pokazuje korzyści i możliwość zakupu premium! ⭐")
async def premium(ctx):
    server_id = str(ctx.guild.id)
    author = ctx.user
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    settings_document = settings_collection.find_one({'_id': server_id})
    
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"
    
    if lang == "PL":
        embed = nextcord.Embed(title=f'Premium ⭐', description="**CENA - 10ZŁ/SERWER (Perm.)**\n\nKorzyści z premium:\n- własne przyciski na ticketach\n- dodatkowa kolejka na autoad\n- reklama na autoad w embedzie\n- przycisk do dołączania na autoad\n- możliwość ustawienia kategorii do której lecą zamknięte tickety\n- własna wiadomość powitalna/pożegnalna\n- Radio", color=0xffe600)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        view = Premium()
    elif lang == "ENG":
        embed = nextcord.Embed(title=f'Premium ⭐', description="**PRICE - 10ZŁ**\n\nPremium benefits:\n- own buttons on tickets\n- additional queue for autoadd\n- advertising on autoad in embed\n- button to join autoad\n- ability to set the category to which closed tickets are sent\n- your own welcome/goodbye message\n- Radio", color=0xffe600)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        view = PremiumENG()

    await ctx.send(embed=embed, view=view)

#Premiumconfig
@bot.slash_command(description="Konfiguracja premium")
async def premiumconfig(ctx):
    await ctx.send("XDX")

#Ticket
@premiumconfig.subcommand(description="Konfiguracja ticketów")
async def ticket(ctx):
    await ctx.send("XDX")

#Ticket Addbutton
@ticket.subcommand(description="Dodaje przycisk do otwierania ticketów! (Premium ⭐)")
async def addbutton(ctx, tekst: str, kolor = nextcord.SlashOption(name="kolor", choices={"czerwony / red", "zielony / green", "niebieski / blue", "szary / gray"}), ping: nextcord.Role = None, uprawnienia: nextcord.Role = None):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if not settings_document:
        settings_document = {'_id': server_id}

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    premium_status = get_status_text(settings_document.get("premium", False))
    if premium_status == "on":
        if ctx.user.guild_permissions.manage_messages:            
            if not settings_document:
                settings_document = {'_id': server_id, 'ticketButtons': []}

            button_list = settings_document.get('ticketButtons', [])

            for item in button_list:
                if item['tekst'] == tekst:
                    if lang == "PL":
                        await ctx.send(f"`[❌]:` Taki przycisk już istnieje!", ephemeral=True)
                    elif lang == "ENG":
                        await ctx.send(f"`[❌]:` Such an button already exists!", ephemeral=True)
                    return
                
            if kolor == "czerwony / red":
                kolordb = "czerwony"

            if kolor == "zielony / green":
                kolordb = "zielony"

            if kolor == "niebieski / blue":
                kolordb = "niebieski"

            if kolor == "szary / gray":
                kolordb = "szary"
                
            if uprawnienia != None and ping != None:
                new_item = {'tekst': tekst, 'kolor': kolordb, 'uprawnienia': uprawnienia.id, 'ping': ping.id}
            elif uprawnienia != None:
                new_item = {'tekst': tekst, 'kolor': kolordb, 'uprawnienia': uprawnienia.id}
            elif ping != None:
                new_item = {'tekst': tekst, 'kolor': kolordb, 'ping': ping.id}
            else:
                new_item = {'tekst': tekst, 'kolor': kolordb}
            button_list.append(new_item)

            settings_collection.update_one({'_id': server_id}, {'$set': {'ticketButtons': button_list}}, upsert=True)

            if lang == "PL":
                await ctx.send(f"`[✅]:` Dodano przycisk `{tekst}` z pingiem `{ping}` i kolorem `{kolor}` (Ponownie ustaw kanał ticketów przy pomocy `/settingsconfig kanal tickety`)", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Added button `{tekst}` with ping `{ping}` and color `{kolor}` (Reset the ticket channel using `/settingsconfig ticket channel`)", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby dodać przycisk do ticketów!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` You do not have the `manage messages` permission to add an button to tickets!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz premium! Możesz je zakupić i sprawdzić co daje przy pomocy `/premium`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You don't have premium! You can purchase them and see what they offer using `/premium`", ephemeral=True)

#Ticket Showbuttons
@ticket.subcommand(description="Wyświetla wszystkie przyciski ticketów! (Premium ⭐)")
async def showbuttons(ctx):
    guild = ctx.guild
    author = ctx.user
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if not settings_document:
        settings_document = {'_id': server_id}

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    premium_status = get_status_text(settings_document.get("premium", False))
    if premium_status == "on":
        button_list = settings_document.get('ticketButtons', [])

        if not button_list:
            if lang == "PL":
                await ctx.send("`[❌]:` Brak przycisków do ticketów!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` No ticket buttons available!", ephemeral=True)
            return

        if lang == "PL":
            embed = nextcord.Embed(title="Przyciski Ticketów", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")

            for index, item in enumerate(button_list, start=1):
                button_text = item['tekst']
                ping_id = item.get('ping')
                color = item.get('kolor')
                uprawnienia = item.get('uprawnienia')
                if ping_id:
                    ping_mention = guild.get_role(ping_id)
                else:
                    ping_mention = "Brak"
                if uprawnienia:
                    uprawnienia_mention = guild.get_role(uprawnienia)
                else:
                    uprawnienia_mention = "Brak"
                embed.add_field(name=f"ID: {index}", value=f"**Tekst:** {button_text}\n**Ping:** {ping_mention}\n**Kolor:** {color}\n**Uprawnienia:** {uprawnienia_mention}", inline=False)
        elif lang == "ENG":
            embed = nextcord.Embed(title="Ticket buttons", color=0x00ff00)
            embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
            embed.set_thumbnail(url=bot.user.avatar.url)
            embed.set_footer(text=f"Invoked by {author} | {current_time}")

            for index, item in enumerate(button_list, start=1):
                button_text = item['tekst']
                ping_id = item.get('ping')
                color = item.get('kolor')
                uprawnienia = item.get('uprawnienia')
                if ping_id:
                    ping_mention = guild.get_role(ping_id)
                else:
                    ping_mention = "None"
                if uprawnienia:
                    uprawnienia_mention = guild.get_role(uprawnienia)
                else:
                    uprawnienia_mention = "None"
                embed.add_field(name=f"ID: {index}", value=f"**Text:** {button_text}\n**Ping:** {ping_mention}\n**Color:** {color}\n**Permissions:** {uprawnienia_mention}", inline=False)

        await ctx.send(embed=embed)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz premium! Możesz je zakupić i sprawdzić co daje przy pomocy `/premium`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You don't have premium! You can purchase them and see what they offer using `/premium`", ephemeral=True)

#Ticket Removebutton
@ticket.subcommand(description="Usuwa przycisk ticketów! (Premium ⭐)")
async def removebutton(ctx, id: int):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if not settings_document:
        settings_document = {'_id': server_id}

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    premium_status = get_status_text(settings_document.get("premium", False))
    if premium_status == "on":
        button_list = settings_document.get('ticketButtons', [])

        if not button_list:
            if lang == "PL":
                await ctx.send("`[❌]:` Brak przycisków do ticketów!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` No ticket buttons available!", ephemeral=True)
            return

        if 1 <= id <= len(button_list):
            removed_button = button_list.pop(id - 1)
            settings_collection.update_one({'_id': server_id}, {'$set': {'ticketButtons': button_list}}, upsert=True)

            if lang == "PL":
                await ctx.send(f"`[✅]:` Usunięto przycisk {id} o tekście `{removed_button['tekst']}`.", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` Removed button {id} with text `{removed_button['tekst']}`.", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Podano nieprawidłowy numer przycisku.", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` Invalid button number provided.", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz premium! Możesz je zakupić i sprawdzić co daje przy pomocy `/premium`", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You don't have premium! You can purchase them and see what they offer using `/premium`", ephemeral=True)

#Rekrutacja
@bot.slash_command(description="Pokazuje jak możesz do nas dołączyć!")
async def rekrutacja(ctx):
    server_id = str(ctx.guild.id)
    author = ctx.user
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    settings_document = settings_collection.find_one({'_id': server_id})
    
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"
    
    if lang == "PL":
        embed = nextcord.Embed(title='Rekrutacja', description="Aktualnie rekrutacja trwa na:\n\n- Social Manager\n- Trial support\n\nJeżeli jesteś zainteresowany dołącz na [naszego discorda!](https://discord.gg/wwtXdvtyKG)", color=0xffe600)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
    elif lang == "ENG":
        embed = nextcord.Embed(title='Recruitment', description="Currently, recruitment is ongoing for:\n\n- Social Manager\n- Trial support\n\nIf you are interested, join [our discord!](https://discord.gg/wwtXdvtyKG)", color=0xffe600)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url=bot.user.avatar.url)
        embed.set_footer(text=f"Invoked by {author} | {current_time}")

    await ctx.send(embed=embed)

#Giveaway
@bot.slash_command(description="Tworzy giveaway!")
async def giveaway(ctx, czas, nagroda: str, wiadomosc = None, wygrani: int = 1):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    current_time = datetime.datetime.now()

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if settings_document and settings_document.get("giveaway", False):
        channel_id = ctx.channel.id
        duration = parse_duration(czas)
        if duration == 0:
            await ctx.send("`[❌]:` Zły format czasu, podaj np. 1m 2h", ephemeral=True)
            return
        
        channel = ctx.channel
        end_time = (current_time + timedelta(seconds=duration))
        await ctx.send("`[✅]:` Rozpoczęto!", ephemeral=True)

        existing_giveaways = guilds_collection.find_one({"_id": server_id}, {"giveaways": 1})
        if not existing_giveaways:
            existing_giveaways = {"giveaways": []}

        giveaways_count = len(existing_giveaways.get("giveaways", []))
        unikalneid = giveaways_count + 1

        if wiadomosc == None:
            if lang == "PL":
                embed = nextcord.Embed(
                    title="🎉 Giveaway wystartował!",
                    description=f"Nagroda: **{nagroda}**\nWygrani: **{wygrani}**\n\nKończy się **<t:{int(end_time.timestamp())}:R>**",
                    color=0x00ff00
                )
                embed.set_footer(text=f"Zareaguj 🎉 aby dołączyć!  |  ID: {unikalneid}")

            elif lang == "ENG":
                embed = nextcord.Embed(
                    title="🎉 Giveaway has started!",
                    description=f"Prize: **{nagroda}**\nWinners: **{wygrani}**\n\nIt's ending **<t:{int(end_time.timestamp())}:R>**",
                    color=0x00ff00
                )
                embed.set_footer(text=f"React 🎉 to join!  |  ID: {unikalneid}")

        else:
            wiadomosc = wiadomosc.replace('\\n', '\n')
            if lang == "PL":
                embed = nextcord.Embed(
                    title="🎉 Giveaway wystartował!",
                    description=f"Nagroda: **{nagroda}**\nWygrani: **{wygrani}**\n\n{wiadomosc}\n\nKończy się **<t:{int(end_time.timestamp())}:R>**",
                    color=0x00ff00
                )
                embed.set_footer(text=f"Zareaguj 🎉 aby dołączyć!  |  ID: {unikalneid}")

            elif lang == "ENG":
                embed = nextcord.Embed(
                    title="🎉 Giveaway has started!",
                    description=f"Prize: **{nagroda}**\nWinners: **{wygrani}**\n\n{wiadomosc}\n\nIt's ending **<t:{int(end_time.timestamp())}:R>**",
                    color=0x00ff00
                )
                embed.set_footer(text=f"React 🎉 to join!  |  ID: {unikalneid}")

        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Konfetti.png")
        message = await channel.send(embed=embed)
        await message.add_reaction("🎉")

        end_time = datetime.datetime.now() + timedelta(seconds=duration)
        existing_giveaway = guilds_collection.find_one({"_id": server_id})
        if existing_giveaway:
            guilds_collection.update_one(
                {"_id": server_id},
                {"$push": {"giveaways": {"id": unikalneid, "channel_id": channel_id, "message_id": message.id, "prize": nagroda, "winners": wygrani, "end_time": end_time, "ended": False}}}
            )
        else:
            guilds_collection.insert_one(
                {"_id": server_id, "giveaways": [{"id": unikalneid, "channel_id": channel_id, "message_id": message.id, "prize": nagroda, "winners": wygrani,"end_time": end_time, "ended": False}]}
            )
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Komenda `giveaway` nie jest włączona dla tego serwera.", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` The `giveaway` command is not enabled for this server.", ephemeral=True)

#Reroll
@bot.slash_command(description="Ponownie losuje giveaway!")
async def reroll(ctx, id: int, ilosc: int = 1):
    server_id = str(ctx.guild.id)
    server_data = guilds_collection.find_one({"_id": server_id})
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if server_data and "giveaways" in server_data:
        for giveaway in server_data["giveaways"]:
            if id == giveaway.get("id"):
                channel_id = giveaway.get("channel_id")
                message_id = giveaway.get("message_id")
                prize = giveaway.get("prize")
                ended = giveaway.get("ended")

                if ended:
                    try:
                        channel = bot.get_channel(int(channel_id))
                        message = await channel.fetch_message(int(message_id))
                    except (nextcord.NotFound, nextcord.HTTPException):
                        if lang == "PL":
                            await ctx.send(f"`[❌]:` Nie można znaleźć wiadomości giveaway'a z id `{id}`!", ephemeral=True)
                        elif lang == "ENG":
                            await ctx.send(f"`[❌]:` Could not find giveaway message with id `{id}`!", ephemeral=True)
                        return

                    reactions = message.reactions
                    if reactions:
                        non_bot_users = [user for user in await reactions[0].users().flatten() if not user.bot]

                        if non_bot_users:
                            winners = random.sample(non_bot_users, min(ilosc, len(non_bot_users)))
                            winners_mentions = ', '.join(winner.mention for winner in winners)

                            if lang == "PL":
                                await ctx.send(f"🎉 Ponowne losowanie na **{prize}**! Gratulacje dla {winners_mentions}!")
                            elif lang == "ENG":
                                await ctx.send(f"🎉 Another draw for **{prize}**! Congratulations to {winners_mentions}!")
                        else:
                            if lang == "PL":
                                await ctx.send(f"🎉 Ponowne losowanie na **{prize}**! Niestety nikt nie wziął udziału. 😢")
                            elif lang == "ENG":
                                await ctx.send(f"🎉 Another draw for **{prize}**! Unfortunately, no one took part. 😢")
                    else:
                        if lang == "PL":
                            await ctx.send("`[❌]:` Brak reakcji w wiadomości giveaway'a!", ephemeral=True)
                        elif lang == "ENG":
                            await ctx.send("`[❌]:` No reaction in the giveaway message!", ephemeral=True)
                else:
                    if lang == "PL":
                        await ctx.send("`[❌]:` Ten giveaway się nie zakończył!", ephemeral=True)
                    elif lang == "ENG":
                        await ctx.send("`[❌]:` This giveaway is not over!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Brak aktywnych giveaway'ów na tym serwerze!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` There are no active giveaways on this server!", ephemeral=True)

#Ranking
@bot.slash_command(description="tak")
async def ranking(ctx):
    await ctx.send("tak")

#Partnerstwa
@ranking.subcommand(description="Wyświetla serwerowy ranking partnerstw!")
async def partnerstwa(ctx):
    server_id = str(ctx.guild.id)
    author = ctx.user
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    server_data = guilds_collection.find_one({'_id': server_id})
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if server_data:
        if lang == "PL":
            embed = nextcord.Embed(title="Top 10 partnerstw", color=0x00ff00)
        elif lang == "ENG":
            embed = nextcord.Embed(title="Top 10 partnerships", color=0x00ff00)

        sorted_users = sorted(server_data["partnerships"].items(), key=lambda x: int(x[1]), reverse=True)[:10]
        for index, (user_id, partnership_count) in enumerate(sorted_users, start=1):
            member = ctx.guild.get_member(int(user_id))
            if member:
                if lang == "PL":
                    embed.add_field(name=f"{index}. {member.display_name}", value=f"Partnerstwa: {partnership_count}", inline=False)
                elif lang == "ENG":
                    embed.add_field(name=f"{index}. {member.display_name}", value=f"Partnerships: {partnership_count}", inline=False)

        thumbnail_url = bot.user.avatar.url
        embed.set_thumbnail(url=thumbnail_url)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        await ctx.send(embed=embed)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Brak danych partnerstw na tym serwerze!")
        elif lang == "ENG":
            await ctx.send("`[❌]:` No partnership data found for this server!")

#Radio
@bot.slash_command(description="Dodaje bota na określony kanał głosowy! (Premium ⭐)")
async def radio(ctx, kanal: nextcord.VoiceChannel, stacja = nextcord.SlashOption(name="stacja", choices={"RMF MAXXX", "ESKA", "Radio ZET", "Radio złote przeboje"})):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    premium_status = get_status_text(settings_document.get("premium", False))
    if premium_status == False:
        if lang == "PL":
            await ctx.send("`[❌]:` Do tej funkcji wymagane jest premium ⭐!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` Premium ⭐ required for this feature!", ephemeral=True)
        return

    try:
        voice_channel = await kanal.connect()
        await voice_channel.guild.change_voice_state(channel=kanal, self_deaf=True)
    except Exception as e:
        if lang == "PL":
            await ctx.send(f'`[❌]:` Trwa już dołączanie do kanału {kanal.mention}! Proszę o cierpliwość!\n\n{e}', ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f'`[❌]:` Joining the {kanal.mention} channel is already in progress! Please be patient!\n\n{e}', ephemeral=True)
        return

    if lang == "PL":
        await ctx.send(f'`[✅]:` Trwa dołączanie do: {kanal.mention} i łączenie się z radiem. Może to chwile potrwać!', ephemeral=True)
    elif lang == "ENG":
        await ctx.send(f'`[✅]:` Joining: {kanal.mention} and connecting to the radio. This may take a while!', ephemeral=True)

    if stacja == "Radio złote przeboje":
        url = 'http://poznan7.radio.pionier.net.pl:8000/tuba9-1.mp3'
        voice_channel.play(FFmpegPCMAudio(url))

    elif stacja == "Radio ZET":
        url = 'http://zt01.cdn.eurozet.pl/ZET090.mp3?redirected=01'
        voice_channel.play(FFmpegPCMAudio(url))

    elif stacja == "RMF MAXXX":
        url = 'http://217.74.72.3:8000/rmf_maxxx'
        voice_channel.play(FFmpegPCMAudio(url))

    elif stacja == "ESKA":
        url = 'https://ic1.smcdn.pl/2380-1.mp3'
        voice_channel.play(FFmpegPCMAudio(url))

    if not settings_document:
        settings_document = {'_id': server_id}

    settings_document['kanalRadia'] = kanal.id
    settings_document['stacjaRadia'] = url
    settings_collection.update_one({'_id': server_id}, {'$set': settings_document}, upsert=True)

#UnRadio
@bot.slash_command(description="Usuwa ustawiony kanał radia! (Bot nie będzie cały czas dołączał na dany kanał)")
async def unradio(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if not settings_document or 'kanalRadia' not in settings_document:
        if lang == "PL":
            await ctx.send("`[❌]:` Bot nie jest połączony z żadnym kanałem głosowym!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` The bot is not connected to any voice channel!", ephemeral=True)
        return

    voice_channel_id = settings_document['kanalRadia']
    voice_channel = ctx.guild.get_channel(voice_channel_id)
    if voice_channel:
        if lang == "PL":
            await ctx.send("`[✅]:` Wyczyszczono kanał radia. Wyrzuć teraz bota z niego!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[✅]:` Radio channel cleared. Kick the bot out of it now!", ephemeral=True)

        settings_collection.update_one({'_id': server_id}, {'$unset': {'kanalRadia': 1}})

#Stacja
@bot.slash_command(description="Stacja radiowa")
async def stacja(ctx, kanal: nextcord.VoiceChannel):
    await ctx.send("XDX")

#Radio
@stacja.subcommand(description="Ustawia własne radio! (Premium ⭐)")
async def radio(ctx, kanal: nextcord.VoiceChannel, stacja: str = nextcord.SlashOption(description="Link do stacji (np. http://217.74.72.3:8000/rmf_maxxx)")):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if ctx.user.guild_permissions.manage_messages:
        premium_status = get_status_text(settings_document.get("premium", False))
        if premium_status == False:
            if lang == "PL":
                await ctx.send("`[❌]:` Do tej funkcji wymagane jest premium ⭐!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` Premium ⭐ required for this feature!", ephemeral=True)
            return

        if settings_document:
            settings_collection.update_one({'_id': server_id}, {'$set': {'stacjaRadia': stacja}})
        else:
            settings_document = {'_id': server_id, 'stacjaRadia': stacja}
            settings_collection.insert_one(settings_document)

        if lang == "PL":
            await ctx.send(f"`[✅]:` Ustawiono własną stację jako {stacja}!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send(f"`[✅]:` You have set your own station as {stacja}!", ephemeral=True)

        voice_channel = await kanal.connect()
        await voice_channel.guild.change_voice_state(channel=kanal, self_deaf=True)
        voice_channel.play(FFmpegPCMAudio(stacja))
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie posiadasz uprawnienia `manage messages` aby ustawić `radio`!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` You do not have the `manage messages` permission to set `radio`!", ephemeral=True)

#Support
@bot.slash_command(description="Wysyła link do serwera support")
async def support(ctx):
    await ctx.send("https://discord.gg/dreambot", ephemeral=True)

#DreamShield
@settingsconfig.subcommand(description="Wyświetla konfigurację systemu DreamShield")
async def dreamshield(ctx):
    author = ctx.user
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})

    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    global antyshieldmsg
    if lang == "PL":
        embed=nextcord.Embed(title="🛡 DreamShield", description="DreamShield jest systemem Anty-Raid", color=0x008000)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        view = DreamShieldView(author.id)
        antyshieldmsg = await ctx.send(embed=embed, view=view)

    elif lang == "ENG":
        embed=nextcord.Embed(title="🛡 DreamShield", description="DreamShield is an Anti-Raid system", color=0x008000)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Tarcza.png")
        embed.set_footer(text=f"Invoked by {author} | {current_time}")
        view = DreamShieldViewENG(author.id)
        antyshieldmsg = await ctx.send(embed=embed, view=view)

#Reminder
@bot.slash_command(description="Reminder")
async def reminder(ctx):
    await ctx.send("Create")

#Create
@reminder.subcommand(description="Tworzy reminder")
async def create(ctx, tekst, ping: nextcord.Role, kanal: nextcord.TextChannel, powtarzanie = nextcord.SlashOption(name="powtarzanie", choices={"24h", "12h", "1h"})):
    await ctx.send("Create")

#Fish
@bot.slash_command(description="Fish")
async def fish(ctx):
    await ctx.send("Fish")

#Fish help
@fish.subcommand(description="Komenda pomocy fish")
async def help(ctx):
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if lang == "PL":
        embed = nextcord.Embed(title='Ryby', description="Witaj podróżniku! Chcesz zacząć swoją fascynującą historię z rybami? Poniżej masz wszystkie komendy!", color=0xe40c0c)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Fish.png")
        embed.add_field(name="`/fish work`", value="*Idź łowić ryby!*", inline=False)
        embed.add_field(name="`/fish ekwipunek`", value="*Pokazuje wszystkie twoje ryby, wędki i pieniądze.*", inline=False)
        embed.add_field(name="`/fish sell`", value="*Sprzedaj złowione ryby.*", inline=False)
        embed.add_field(name="`/fish shop`", value="*Sklep w którym można kupić lepsze wędki.*", inline=False)
        embed.add_field(name="`/fish buy [id]`", value="*Kupuje przedmiot z sklepu.*", inline=False)
        embed.add_field(name="`/fish quest`", value="*Wyświetla dostępne zadania.*", inline=False)
        embed.add_field(name="`/fish help`", value="*Wyświetla tę pomoc.*", inline=False)
    elif lang == 'ENG':
        embed = nextcord.Embed(title='Fish', description="Hello traveler! Do you want to start your fascinating fish story? Below you have all the commands!", color=0xe40c0c)
        embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Fish.png")
        embed.add_field(name="`/fish work`", value="*Go fishing!*", inline=False)
        embed.add_field(name="`/fish ekwipunek`", value="*Shows all your fish, rods and money.*", inline=False)
        embed.add_field(name="`/fish sell`", value="*Sell ​​the fish you catch.*", inline=False)
        embed.add_field(name="`/fish shop`", value="*A shop where you can buy better fishing rods.*", inline=False)
        embed.add_field(name="`/fish buy [id]`", value="*Buys an item from the store.*", inline=False)
        embed.add_field(name="`/fish quest`", value="*Displays available tasks.*", inline=False)
        embed.add_field(name="`/fish help`", value="*Displays this help.*", inline=False)
    await ctx.send(embed=embed)

def get_user_wedka_and_prestige(user_id):
    user_document = users_collection.find_one({'_id': user_id})
    user_wedka_name = "drewniana"
    user_wedka_prestige = 1
    upgradeName = None

    if user_document and 'fishShop' in user_document:
        fish_shop = user_document['fishShop']
        for item in fish_shop:
            shop_data = fish_collection.find_one({'_id': 'Info'})
            if shop_data and 'Shop' in shop_data:
                shop_items = shop_data['Shop']
                if item in shop_items:
                    item_data = shop_items[item]
                    item_prestige = item_data.get('Prestige', 1)
                    item_wedka_name = item_data.get('Name', 'drewniana').lower()

                    if item_prestige > user_wedka_prestige:
                        user_wedka_name = item_wedka_name
                        user_wedka_prestige = item_prestige

            if 'ShopUpgrades' in shop_data:
                shop_items = shop_data['ShopUpgrades']
                if item in shop_items:
                    item_data = shop_items[item]
                    item_upgrade_name = item_data.get('Name', 'drewniana').lower()
                    upgradeName = item_upgrade_name

    return user_wedka_name, user_wedka_prestige, upgradeName

#Fish work
@fish.subcommand(description="Pozwala połowić trochę ryb")
async def work(ctx):
    user_id = str(ctx.user.id)
    fish_info_document = fish_collection.find_one({'_id': 'Info'})
    user_document = users_collection.find_one({'_id': user_id})
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    cooldown_data = cooldowns_collection.find_one({"_id": user_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if cooldown_data and "fishCD" in cooldown_data:
        last_usage = cooldown_data["fishCD"]
        current_time = datetime.datetime.now()
        time_difference = current_time - last_usage
        cooldown_duration = datetime.timedelta(seconds=fishcd)
        
        if time_difference >= cooldown_duration:
            cooldowns_collection.update_one({"_id": user_id}, {"$set": {"fishCD": current_time}})

            if fish_info_document and 'Fish' in fish_info_document:
                fish_data = fish_info_document['Fish']

                if fish_data:
                    available_fish = []
                    user_wedka = get_user_wedka_and_prestige(user_id)
                    user_wedka_name, user_wedka_prestige, user_upgrade = user_wedka

                    for fish_name, fish_info in fish_data.items():
                        fish_prestige = fish_info.get('Prestige', 1)

                        gold = False
                        if user_wedka_prestige == 3:
                            if fish_prestige == user_wedka_prestige:
                                available_fish.append(fish_name)
                                gold = True
                        elif user_upgrade != None:
                            if user_upgrade == "ulepszony kołowrotek" and random.randint(1, 5) == 1:
                                if fish_prestige == user_wedka_prestige + 1:
                                    available_fish.append(fish_name)
                                else:
                                    if fish_prestige <= user_wedka_prestige:
                                        available_fish.append(fish_name)
                            else:
                                if fish_prestige <= user_wedka_prestige:
                                    available_fish.append(fish_name)
                        else:
                            if fish_prestige <= user_wedka_prestige:
                                available_fish.append(fish_name)

                    if available_fish:
                        los = random.randint(1, 4)
                        if los == 1 or los == 2:
                            selected_fish = random.choice(available_fish)
                            if lang == "PL":
                                fish_description = fish_data[selected_fish].get('Description', 'Brak opisu')
                                response = f"🎣 Wyłowiono rybę:\n\n**{selected_fish}** - *{fish_description}*"
                            elif lang == "ENG":
                                fish_description = fish_data[selected_fish].get('Description', 'No description')
                                response = f"🎣 Fish caught:\n\n**{selected_fish}** - *{fish_description}*"

                            user_id = str(ctx.user.id)
                            user_document = users_collection.find_one({'_id': user_id})

                            if user_document is None:
                                user_document = {'_id': user_id}

                            if 'Fish' not in user_document:
                                user_document['Fish'] = {}

                            if selected_fish in user_document['Fish']:
                                user_document['Fish'][selected_fish] += 1
                            else:
                                user_document['Fish'][selected_fish] = 1

                            if 'Quests' not in user_document:
                                user_document['Quests'] = {}

                            if 'Fish' in user_document['Quests']:
                                user_document['Quests']['Fish'] += 1
                            else:
                                user_document['Quests']['Fish'] = 1

                            all_fish = user_document['Quests']['Fish']
                            if 'Completed' not in user_document['Quests']:
                                user_document['Quests']['Completed'] = {}

                            if all_fish == 20:
                                if not 'Początkujący1' in user_document['Quests']['Completed'] or user_document['Quests']['Completed']['Początkujący1'] == False:
                                    user_document['Quests']['Completed']['Początkujący1'] = True
                                    if 'fishMoney' in user_document:
                                        user_document['fishMoney'] += 500
                                    else:
                                        user_document['fishMoney'] = 500

                                    if lang == "PL":
                                        response = f"🎣 Wyłowiono rybę:\n\n**{selected_fish}** - *{fish_description}*\n\nZrobiłeś zadanie *Początkujący I* i otrzymałeś *500* <:Moneta:1165730228652494968>"
                                    elif lang == "ENG":
                                        response = f"🎣 Fish caught:\n\n**{selected_fish}** - *{fish_description}*\n\nYou completed *Beginner I* and received *500* <:Moneta:1165730228652494968>"
                            if all_fish == 50:
                                if not 'Początkujący2' in user_document['Quests']['Completed'] or user_document['Quests']['Completed']['Początkujący2'] == False:
                                    user_document['Quests']['Completed']['Początkujący2'] = True
                                    if 'fishMoney' in user_document:
                                        user_document['fishMoney'] += 1000
                                    else:
                                        user_document['fishMoney'] = 1000
                                    
                                    if lang == "PL":
                                        response = f"🎣 Wyłowiono rybę:\n\n**{selected_fish}** - *{fish_description}*\n\nZrobiłeś zadanie *Początkujący II* i otrzymałeś *1000* <:Moneta:1165730228652494968>"
                                    elif lang == "ENG":
                                        response = f"🎣 Fish caught:\n\n**{selected_fish}** - *{fish_description}*\n\nYou completed *Beginner II* and received *1000* <:Moneta:1165730228652494968>"

                            if gold == True:
                                if not 'Złoto' in user_document['Quests']['Completed'] or user_document['Quests']['Completed']['Złoto'] == False:
                                    user_document['Quests']['Completed']['Złoto'] = True
                                    if 'fishMoney' in user_document:
                                        user_document['fishMoney'] += 300
                                    else:
                                        user_document['fishMoney'] = 300
                                    if lang == "PL":
                                        response = f"🎣 Wyłowiono rybę:\n\n**{selected_fish}** - *{fish_description}*\n\nZrobiłeś zadanie *Złoto 🥇* i otrzymałeś *300* <:Moneta:1165730228652494968>"
                                    elif lang == "ENG":
                                        response = f"🎣 Fish caught:\n\n**{selected_fish}** - *{fish_description}*\n\nYou completed the *Gold 🥇* task and received *300* <:Moneta:1165730228652494968>"
                            
                            users_collection.update_one({'_id': user_id}, {'$set': user_document}, upsert=True)
                        elif los == 3:
                            if lang == "PL":
                                response = "Niestety ryba uciekła ci 😢"
                            elif lang == "ENG":
                                response = "Unfortunately, the fish escaped you 😢"
                        else:
                            if lang == "PL":
                                response = "Ryby teraz nie biorą! Zmień miejsce lub poczekaj!"
                            elif lang == "ENG":
                                response = "The fish aren't biting now! Change your seat or wait!"

                        await ctx.send(response)
                        statistics = load_statistics()
                        if 'work' in statistics:
                            statistics['work'] += 1
                        else:
                            statistics['work'] = 1
                        save_statistics(statistics)
                    else:
                        if lang == "PL":
                            await ctx.send("`[❌]:` Niestety, nie udało się złowić żadnej ryby dostępnej dla twojej wędki!", ephemeral=True)
                        elif lang == "ENG":
                            await ctx.send("`[❌]:` Unfortunately, no fish available for your rod were caught!", ephemeral=True)
                else:
                    if lang == "PL":
                        await ctx.send("`[❌]:` Brak danych dotyczących szans na ryby!", ephemeral=True)
                    elif lang == "ENG":
                        await ctx.send("`[❌]:` No data on fishing chances!", ephemeral=True)
            else:
                if lang == "PL":
                    await ctx.send("`[❌]:` Brak danych dotyczących szans na ryby!", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send("`[❌]:` No data on fishing chances!", ephemeral=True)
        else:
            time_left = cooldown_duration - time_difference
            if lang == "PL":
                await ctx.send(f"`[❌]:` Musisz poczekać jeszcze `{time_left.seconds} sekund` przed kolejnym użyciem komendy.", ephemeral=True)
            elif lang == "ENG":
                await ctx.send(f"`[❌]:` You must wait `{time_left.seconds} seconds` before using the command again.", ephemeral=True)
    else:
        current_time = datetime.datetime.now()
        if cooldown_data:
            cooldowns_collection.update_one({"_id": user_id}, {"$set": {"fishCD": current_time}}, upsert=True)
        else:
            cooldowns_collection.insert_one({"_id": str(ctx.user.id), "fishCD": current_time})

        if fish_info_document and 'Fish' in fish_info_document:
            fish_data = fish_info_document['Fish']

            if fish_data:
                available_fish = []
                user_wedka = get_user_wedka_and_prestige(user_id)
                user_wedka_name, user_wedka_prestige, user_upgrade = user_wedka

                for fish_name, fish_info in fish_data.items():
                    fish_prestige = fish_info.get('Prestige', 1)

                    gold = False
                    if user_wedka_prestige == 3:
                        if fish_prestige == user_wedka_prestige:
                            available_fish.append(fish_name)
                            gold = True
                    elif user_upgrade != None:
                        if user_upgrade == "ulepszony kołowrotek" and random.randint(1, 5) == 1:
                            if fish_prestige == user_wedka_prestige + 1:
                                available_fish.append(fish_name)
                            else:
                                if fish_prestige <= user_wedka_prestige:
                                    available_fish.append(fish_name)
                        else:
                            if fish_prestige <= user_wedka_prestige:
                                available_fish.append(fish_name)
                    else:
                        if fish_prestige <= user_wedka_prestige:
                            available_fish.append(fish_name)

                if available_fish:
                    los = random.randint(1, 4)
                    if los == 1 or los == 2:
                        selected_fish = random.choice(available_fish)
                        if lang == "PL":
                            fish_description = fish_data[selected_fish].get('Description', 'Brak opisu')
                            response = f"🎣 Wyłowiono rybę:\n\n**{selected_fish}** - *{fish_description}*"
                        elif lang == "ENG":
                            fish_description = fish_data[selected_fish].get('Description', 'No description')
                            response = f"🎣 Fish caught:\n\n**{selected_fish}** - *{fish_description}*"

                        user_id = str(ctx.user.id)
                        user_document = users_collection.find_one({'_id': user_id})

                        if user_document is None:
                            user_document = {'_id': user_id}

                        if 'Fish' not in user_document:
                            user_document['Fish'] = {}

                        if selected_fish in user_document['Fish']:
                            user_document['Fish'][selected_fish] += 1
                        else:
                            user_document['Fish'][selected_fish] = 1

                        if 'Quests' not in user_document:
                            user_document['Quests'] = {}

                        if 'Fish' in user_document['Quests']:
                            user_document['Quests']['Fish'] += 1
                        else:
                            user_document['Quests']['Fish'] = 1

                        all_fish = user_document['Quests']['Fish']
                        if 'Completed' not in user_document['Quests']:
                            user_document['Quests']['Completed'] = {}

                        if all_fish == 20:
                            if not 'Początkujący1' in user_document['Quests']['Completed'] or user_document['Quests']['Completed']['Początkujący1'] == False:
                                user_document['Quests']['Completed']['Początkujący1'] = True
                                if 'fishMoney' in user_document:
                                    user_document['fishMoney'] += 500
                                else:
                                    user_document['fishMoney'] = 500

                                if lang == "PL":
                                    response = f"🎣 Wyłowiono rybę:\n\n**{selected_fish}** - *{fish_description}*\n\nZrobiłeś zadanie *Początkujący I* i otrzymałeś *500* <:Moneta:1165730228652494968>"
                                elif lang == "ENG":
                                    response = f"🎣 Fish caught:\n\n**{selected_fish}** - *{fish_description}*\n\nYou completed *Beginner I* and received *500* <:Moneta:1165730228652494968>"
                        if all_fish == 50:
                            if not 'Początkujący2' in user_document['Quests']['Completed'] or user_document['Quests']['Completed']['Początkujący2'] == False:
                                user_document['Quests']['Completed']['Początkujący2'] = True
                                if 'fishMoney' in user_document:
                                    user_document['fishMoney'] += 1000
                                else:
                                    user_document['fishMoney'] = 1000
                                    
                                if lang == "PL":
                                    response = f"🎣 Wyłowiono rybę:\n\n**{selected_fish}** - *{fish_description}*\n\nZrobiłeś zadanie *Początkujący II* i otrzymałeś *1000* <:Moneta:1165730228652494968>"
                                elif lang == "ENG":
                                    response = f"🎣 Fish caught:\n\n**{selected_fish}** - *{fish_description}*\n\nYou completed *Beginner II* and received *1000* <:Moneta:1165730228652494968>"

                        if gold == True:
                            if not 'Złoto' in user_document['Quests']['Completed'] or user_document['Quests']['Completed']['Złoto'] == False:
                                user_document['Quests']['Completed']['Złoto'] = True
                                if 'fishMoney' in user_document:
                                    user_document['fishMoney'] += 300
                                else:
                                    user_document['fishMoney'] = 300
                                if lang == "PL":
                                    response = f"🎣 Wyłowiono rybę:\n\n**{selected_fish}** - *{fish_description}*\n\nZrobiłeś zadanie *Złoto 🥇* i otrzymałeś *300* <:Moneta:1165730228652494968>"
                                elif lang == "ENG":
                                    response = f"🎣 Fish caught:\n\n**{selected_fish}** - *{fish_description}*\n\nYou completed the *Gold 🥇* task and received *300* <:Moneta:1165730228652494968>"
                            
                        users_collection.update_one({'_id': user_id}, {'$set': user_document}, upsert=True)
                    elif los == 3:
                        if lang == "PL":
                            response = "Niestety ryba uciekła ci 😢"
                        elif lang == "ENG":
                            response = "Unfortunately, the fish escaped you 😢"
                    else:
                        if lang == "PL":
                            response = "Ryby teraz nie biorą! Zmień miejsce lub poczekaj!"
                        elif lang == "ENG":
                            response = "The fish aren't biting now! Change your seat or wait!"

                    await ctx.send(response)
                    statistics = load_statistics()
                    if 'work' in statistics:
                        statistics['work'] += 1
                    else:
                        statistics['work'] = 1
                    save_statistics(statistics)
                else:
                    if lang == "PL":
                        await ctx.send("`[❌]:` Niestety, nie udało się złowić żadnej ryby dostępnej dla twojej wędki!", ephemeral=True)
                    elif lang == "ENG":
                        await ctx.send("`[❌]:` Unfortunately, no fish available for your rod were caught!", ephemeral=True)
            else:
                if lang == "PL":
                    await ctx.send("`[❌]:` Brak danych dotyczących szans na ryby!", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send("`[❌]:` No data on fishing chances!", ephemeral=True)
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Brak danych dotyczących szans na ryby!", ephemeral=True)
            elif lang == "ENG":
                await ctx.send("`[❌]:` No data on fishing chances!", ephemeral=True)

#Fish ekwipunek
@fish.subcommand(description="Pokazuje twoje złowione ryby")
async def ekwipunek(ctx):
    user_id = str(ctx.user.id)
    user_document = users_collection.find_one({'_id': user_id})
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if user_document and 'Fish' in user_document:
        fish_inventory = user_document['Fish']
    else:
        fish_inventory = None

    if lang == "PL":
        embed = nextcord.Embed(title='Ekwipunek Rybaka', color=0x3498db)
    elif lang == "ENG":
        embed = nextcord.Embed(title='Fishermans equipment', color=0x3498db)
    embed.set_author(name="DreamBot", icon_url=bot.user.avatar.url)
    total_coins = 0
    money = 0

    if 'fishMoney' in user_document:
        money = user_document['fishMoney']

    can = False
    if fish_inventory:
        if lang == "PL":
            embed.add_field(name="\u200B", value=f"Oto twoje złowione ryby:", inline=False)
        elif lang == "ENG":
            embed.add_field(name="\u200B", value=f"Here are your catches:", inline=False)
        for fish_name, fish_quantity in fish_inventory.items():
            fish_info_document = fish_collection.find_one({'_id': 'Info'})
            fish_data = fish_info_document['Fish']
            fish_description = fish_data[fish_name].get('Description', 'Brak opisu')
            fish_price = fish_data[fish_name].get('Price', 0)

            total_price = fish_price * fish_quantity
            total_coins += total_price

            if lang == "PL":
                embed.add_field(name=fish_name, value=f"Ilość: *{fish_quantity}*\nOpis: *{fish_description}*\nCena za 1 rybę: *{fish_price} <:Moneta:1165730228652494968>*", inline=False)
            elif lang == "ENG":
                embed.add_field(name=fish_name, value=f"Amount: *{fish_quantity}*\nDescription: *{fish_description}*\nPrice for 1 fish: *{fish_price} <:Moneta:1165730228652494968>*", inline=False)
            can = True

    if can:
        if lang == "PL":
            embed.add_field(name="Całkowita Wartość", value=f"{total_coins} <:Moneta:1165730228652494968>", inline=False)
        elif lang == "ENG":
            embed.add_field(name="Total Value", value=f"{total_coins} <:Moneta:1165730228652494968>", inline=False)

    if 'fishShop' in user_document:
        fish_shop = user_document['fishShop']
        if fish_shop:
            shop_data = fish_collection.find_one({'_id': 'Info'})
            if shop_data and 'Shop' in shop_data:
                shop_items = shop_data['Shop']
                if lang == "PL":
                    embed.add_field(name='\u200B', value='*Oto twoje wędki i ulepszenia:*', inline=False)
                elif lang == "ENG":
                    embed.add_field(name='\u200B', value='*Here are your fishing rods and upgrades:*', inline=False)
                for item_name in fish_shop:
                    item_data = next((item for item in shop_items.values() if item.get('Name') == item_name), None)
                    if item_data:
                        item_description = item_data.get('Description', 'Brak opisu')
                        embed.add_field(name=item_name, value=f"Opis: {item_description}", inline=False)

                shop_items = shop_data['ShopUpgrades']
                for item_name in fish_shop:
                    item_data = next((item for item in shop_items.values() if item.get('Name') == item_name), None)
                    if item_data:
                        item_description = item_data.get('Description', 'Brak opisu')
                        embed.add_field(name=item_name, value=f"Opis: {item_description}", inline=False)

    embed.add_field(name='\u200B', value='\u200B', inline=False)
    if lang == "PL":
        embed.add_field(name="Portfel", value=f"{money} <:Moneta:1165730228652494968>", inline=False)
    elif lang == "ENG":
        embed.add_field(name="Wallet", value=f"{money} <:Moneta:1165730228652494968>", inline=False)

    if ctx.user.avatar:
        avatar_url = ctx.user.avatar.url
    else:
        avatar_url = no_avatar
    embed.set_author(name="DreamBot", icon_url=avatar_url)
    embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Fish.png")
    await ctx.send(embed=embed)

#Fish sell
@fish.subcommand(description="Sprzedaje wszystkie ryby w ekwipunku")
async def sell(ctx):
    user_id = str(ctx.user.id)
    user_document = users_collection.find_one({'_id': user_id})
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if user_document and 'Fish' in user_document:
        fish_inventory = user_document['Fish']

        if fish_inventory:
            fish_info_document = fish_collection.find_one({'_id': 'Info'})
            fish_data = fish_info_document['Fish']
            total_coins = 0

            for fish_name, fish_quantity in fish_inventory.items():
                if fish_name in fish_data:
                    fish_price = fish_data[fish_name].get('Price', 0)
                    total_price = fish_price * fish_quantity
                    total_coins += total_price

            if 'fishMoney' in user_document:
                user_document['fishMoney'] += total_coins
            else:
                user_document['fishMoney'] = total_coins

            user_document['Fish'] = {}

            users_collection.update_one({'_id': user_id}, {'$set': user_document})
            if lang == "PL":
                await ctx.send(f"`[✅]:` Sprzedałeś wszystkie ryby w ekwipunku za *{total_coins}* <:Moneta:1165730228652494968>!")
            elif lang == "ENG":
                await ctx.send(f"`[✅]:` You sold all fish in your inventory for *{total_coins}* <:Moneta:1165730228652494968>!")
        else:
            if lang == "PL":
                await ctx.send("`[❌]:` Twój ekwipunek ryb jest pusty!")
            elif lang == "ENG":
                await ctx.send("`[❌]:` Your fish inventory is empty!")
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie znaleziono informacji o twoim ekwipunku ryb!")
        elif lang == "ENG":
            await ctx.send("`[❌]:` Your fish inventory information was not found!")


#Fish shop
@fish.subcommand(description="Wyświetla sklep")
async def shop(ctx):
    shop_data = fish_collection.find_one({'_id': 'Info'})
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if shop_data and 'Shop' in shop_data:
        shop_items = shop_data['Shop']
        star = "<:Star:1166383827820748940>"

        if lang == "PL":
            embed = nextcord.Embed(title="Sklep z wędkami", description="Oto dostępne przedmioty w sklepie:", color=0x3498db)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Fish.png")
            embed.add_field(name=f"Drewniana wędka (ID: 0) {1 * star}", value=f"Cena: 0 <:Moneta:1165730228652494968>\nOpis: Podstawowa wędka", inline=False)
            for item_name, item_data in shop_items.items():
                item_id = item_data.get('ID', 'Brak ID')
                item_price = item_data.get('Price', 'Nie podano ceny')
                item_prestige = item_data.get('Prestige', '1')
                item_description = item_data.get('Description', 'Brak opisu')
                embed.add_field(name=f"{item_name} (ID: {item_id}) {item_prestige * star}", value=f"Cena: {item_price} <:Moneta:1165730228652494968>\nOpis: {item_description}", inline=False)
            view = FishShopWedki()
        elif lang == "ENG":
            embed = nextcord.Embed(title="Fishing Shop", description="Here are the available items in the store:", color=0x3498db)
            embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Fish.png")
            embed.add_field(name=f"Wooden fishing rod (ID: 0) {1 * star}", value=f"Price: 0 <:Moneta:1165730228652494968>\nOpis: Basic fishing rod", inline=False)
            for item_name, item_data in shop_items.items():
                item_id = item_data.get('ID', 'None ID')
                item_price = item_data.get('Price', 'None')
                item_prestige = item_data.get('Prestige', '1')
                item_description = item_data.get('Description', 'None')
                embed.add_field(name=f"{item_name} (ID: {item_id}) {item_prestige * star}", value=f"Price: {item_price} <:Moneta:1165730228652494968>\Description: {item_description}", inline=False)
            view = FishShopWedkiENG()
        global Fishmsg
        Fishmsg = await ctx.send(embed=embed, view=view)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Brak dostępnych przedmiotów w sklepie.", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` No items available in the store.", ephemeral=True)

#Fish buy
@fish.subcommand(description="Kupuje przedmiot ze sklepu")
async def buy(ctx, id: int):
    user_id = str(ctx.user.id)
    shop_data = fish_collection.find_one({'_id': 'Info'})
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if shop_data and 'Shop' in shop_data:
        shop_items = shop_data['Shop']
        item_data = next((item for item in shop_items.values() if item.get('ID') == id), None)
        if not item_data:
            shop_items = shop_data['ShopUpgrades']
            item_data = next((item for item in shop_items.values() if item.get('ID') == id), None)

        if item_data:
            item_name = item_data.get('Name', 'Brak nazwy')
            item_price = item_data.get('Price', 0)

            user_document = users_collection.find_one({'_id': user_id})

            if user_document:
                user_money = user_document.get('fishMoney', 0)

                if user_money >= item_price:
                    total = user_money - item_price
                    users_collection.update_one({'_id': user_id}, {'$set': {'fishMoney': total}})
                    fish_shop = user_document.get('fishShop', [])

                    if item_name not in fish_shop:
                        fish_shop.append(item_name)

                        users_collection.update_one({'_id': user_id}, {'$set': {'fishShop': fish_shop}})

                        if lang == "PL":
                            await ctx.send(f"`[✅]:` Kupiono przedmiot *{item_name}* za *{item_price}* <:Moneta:1165730228652494968>.")
                        elif lang == "ENG":
                            await ctx.send(f"`[✅]:` Bought item *{item_name}* for *{item_price}* <:Moneta:1165730228652494968>.")
                    else:
                        if lang == "PL":
                            await ctx.send("`[❌]:` Posiadasz już ten przedmiot!", ephemeral=True)
                        elif lang == "ENG":
                            await ctx.send("`[❌]:` You already own this item!", ephemeral=True)
                else:
                    if lang == "PL":
                        await ctx.send("`[❌]:` Nie masz wystarczająco monet na zakup tego przedmiotu!", ephemeral=True)
                    elif lang == "ENG":
                        await ctx.send("`[❌]:` You don't have enough coins to purchase this item!", ephemeral=True)
            else:
                if lang == "PL":
                    await ctx.send("`[❌]:` Błąd odczytu danych użytkownika!", ephemeral=True)
                elif lang == "ENG":
                    await ctx.send("`[❌]:` Error reading user data!", ephemeral=True)
        else:
            if lang == "PL":
                if id == 0:
                    await ctx.send("`[❌]:` Posiadasz już ten przedmiot!", ephemeral=True)
                else:
                    await ctx.send("`[❌]:` Przedmiot o podanym ID nie istnieje w sklepie!", ephemeral=True)
            elif lang == "ENG":
                if id == 0:
                    await ctx.send("`[❌]:` You already own this item!", ephemeral=True)
                else:
                    await ctx.send("`[❌]:` The item with the given ID does not exist in the store!", ephemeral=True)
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Brak dostępnych przedmiotów w sklepie!", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` No items available in the store!", ephemeral=True)

#Fish quest
@fish.subcommand(description="Wyświetla tablicę zadań!")
async def quest(ctx):
    star = "<:Star:1166383827820748940>"
    user_id = str(ctx.user.id)
    fish_info_document = fish_collection.find_one({'_id': 'Info'})
    user_document = users_collection.find_one({'_id': user_id})
    server_id = str(ctx.guild.id)
    settings_document = settings_collection.find_one({'_id': server_id})
    if settings_document:
        if 'language' in settings_document:
            lang = settings_document['language']
        else:
            lang = "PL"
    else:
        lang = "PL"

    if fish_info_document and 'Quests' in fish_info_document:
        quests_data = fish_info_document['Quests']
        embed = nextcord.Embed(title="Questy", description="Oto dostępne zadania dla ciebie:", color=0x3498db)
        embed.set_thumbnail(url="https://dreambot.pl/DreamBotImages/Fish.png")
        user_quests = quests_data
        num = 0

        for quest_id, quest_info in user_quests.items():
            if lang == "PL":
                quest_name = quest_info.get('Name', 'Nieznane zadanie')
                quest_prize = quest_info.get('Prize', 'Brak')
                quest_description = quest_info.get('Description', 'Brak opisu zadania')
                quest_type = quest_info.get('Type', 1)

                if quest_name == "Początkujący I":
                    if not 'Quests' in user_document or not 'Completed' in user_document['Quests'] or not 'Początkujący1' in user_document['Quests']['Completed'] or user_document['Quests']['Completed']['Początkujący1'] == False:
                        embed.add_field(
                            name=f"Początkujący I",
                            value=f"*{quest_description}*\nNagroda: *{quest_prize}* <:Moneta:1165730228652494968>\nTrudność: {star * quest_type}",
                            inline=False
                        )
                        num =+ 1
                        
                elif quest_name == "Początkujący II":
                    if not 'Quests' in user_document or not 'Completed' in user_document['Quests'] or not 'Początkujący2' in user_document['Quests']['Completed'] or user_document['Quests']['Completed']['Początkujący2'] == False:
                        embed.add_field(
                            name=f"Początkujący II",
                            value=f"*{quest_description}*\nNagroda: *{quest_prize}* <:Moneta:1165730228652494968>\nTrudność: {star * quest_type}",
                            inline=False
                        )
                        num =+ 1
                        
                elif quest_name == "Złoto 🥇":
                    if not 'Quests' in user_document or not 'Completed' in user_document['Quests'] or not 'Złoto' in user_document['Quests']['Completed'] or user_document['Quests']['Completed']['Złoto'] == False:
                        embed.add_field(
                            name=f"Złoto 🥇",
                            value=f"*{quest_description}*\nNagroda: *{quest_prize}* <:Moneta:1165730228652494968>\nTrudność: {star * quest_type}",
                            inline=False
                        )
                        num =+ 1

                else:
                    embed.add_field(
                        name=f"{quest_name}",
                        value=f"*{quest_description}*\nNagroda: *{quest_prize}* <:Moneta:1165730228652494968>\nTrudność: {star * quest_type}",
                        inline=False
                    )
                    num =+ 1
            elif lang == "ENG":
                quest_name = quest_info.get('Name', 'None')
                quest_prize = quest_info.get('Prize', 'None')
                quest_description = quest_info.get('Description', 'None')
                quest_type = quest_info.get('Type', 1)

                if quest_name == "Początkujący I":
                    if not 'Quests' in user_document or not 'Completed' in user_document['Quests'] or not 'Początkujący1' in user_document['Quests']['Completed'] or user_document['Quests']['Completed']['Początkujący1'] == False:
                        embed.add_field(
                            name=f"Begginer I",
                            value=f"*{quest_description}*\nPrize: *{quest_prize}* <:Moneta:1165730228652494968>\nDifficulty: {star * quest_type}",
                            inline=False
                        )
                        num =+ 1
                        
                elif quest_name == "Początkujący II":
                    if not 'Quests' in user_document or not 'Completed' in user_document['Quests'] or not 'Początkujący2' in user_document['Quests']['Completed'] or user_document['Quests']['Completed']['Początkujący2'] == False:
                        embed.add_field(
                            name=f"Begginer II",
                            value=f"*{quest_description}*\nPrize: *{quest_prize}* <:Moneta:1165730228652494968>\nDifficulty: {star * quest_type}",
                            inline=False
                        )
                        num =+ 1
                        
                elif quest_name == "Złoto 🥇":
                    if not 'Quests' in user_document or not 'Completed' in user_document['Quests'] or not 'Złoto' in user_document['Quests']['Completed'] or user_document['Quests']['Completed']['Złoto'] == False:
                        embed.add_field(
                            name=f"Gold 🥇",
                            value=f"*{quest_description}*\nPrize: *{quest_prize}* <:Moneta:1165730228652494968>\nDifficulty: {star * quest_type}",
                            inline=False
                        )
                        num =+ 1

                else:
                    embed.add_field(
                        name=f"{quest_name}",
                        value=f"*{quest_description}*\nPrize: *{quest_prize}* <:Moneta:1165730228652494968>\nDifficulty: {star * quest_type}",
                        inline=False
                    )
                    num =+ 1

        if num > 0:
            await ctx.send(embed=embed)
        else:
            if lang == "PL":
                await ctx.send("Witaj rybaku! 🎣 Niestety aktualnie nie mam żadnych zadań dla Ciebie! Przyjdź do mnie za 2 księżyce! 🌕")
            elif lang == "ENG":
                await ctx.send("Hello fisherman! 🎣 Unfortunately, I currently don't have any tasks for you! Come to me in 2 moons! 🌕")
    else:
        if lang == "PL":
            await ctx.send("`[❌]:` Nie udało się znaleźć informacji o zadaniach. Spróbuj ponownie później.", ephemeral=True)
        elif lang == "ENG":
            await ctx.send("`[❌]:` Could not find task information. Please try again later.", ephemeral=True)



#Globalban
@bot.slash_command(description="Globalbanuje serwer (Tylko właściciele bota)")
async def globalban(ctx, serverid):
    if any(ctx.user.id == owner_id for owner_id in właściciele):
        server = bot.get_guild(int(serverid))
        server_id = str(serverid)
        try:
            settings_document = settings_collection.find_one({'_id': server_id})
            if settings_document:
                current_status = settings_document.get("globalBan", False)
                new_status = not current_status

                settings_collection.update_one({'_id': server_id}, {'$set': {'globalBan': new_status}})
            else:
                new_status = True
                settings_document = {'_id': server_id, 'globalBan': new_status}
                settings_collection.insert_one(settings_document)

            await server.leave()
            await ctx.send(f"`[✅]:` Pomyślnie zglobalbanowano serwer z ID `{serverid}` i nazwą `{server.name}`!", ephemeral=True)
        except Exception as e:
            await ctx.send(f"`[❌]:` Wystąpił błąd podczas opuszczania serwera:\n\n{str(e)}", ephemeral=True)
    else:
        await ctx.send("`[❌]:` Tej komendy mogą jedynie używać właściciele bota!", ephemeral=True)



if DEV == True:
    bot.run(DEVToken)

    @bot.slash_command(description='apply')
    async def apply(ctx, choice = nextcord.SlashOption(name="choice", choices={"one", "two", f"three"})):
        if choice.lower() == 'one':
            await ctx.send('Wybrano opcję 1!')
        elif choice.lower() == 'two':
            await ctx.send('Wybrano opcję 2!')
        elif choice.lower() == 'three':
            await ctx.send('Wybrano opcję 3!')
else:
    bot.run(Token)