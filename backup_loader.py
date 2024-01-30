import os
import json
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import datetime

DBAccount = "MainAccount"
DBPassword = "1EfzIeQYvsBvTir3"
uri = f"mongodb+srv://{DBAccount}:{DBPassword}@dreambot.utpybla.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Main']
dbInfo = client['Info']

# Kolekcje
settings_collection = db['settings']
currency_collection = db['currency']
cooldowns_collection = db['cooldowns']
notes_collection = db['notes']
users_collection = dbInfo['Users']
backup_collection = dbInfo['Backup']
fish_collection = dbInfo['Fish']
guilds_collection = dbInfo['Guilds']
website_collection = dbInfo['Website']

# Klasa do obsługi niestandardowego kodowania JSON
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (datetime.datetime, )):
            return o.isoformat()
        return super().default(o)

# Folder z backupami
backup_folder = 'backup'

# Iteracja po kolekcjach w folderze "backup"
for file_name in os.listdir(backup_folder):
    if file_name.endswith('.json'):
        backup_path = os.path.join(backup_folder, file_name)

        # Odczyt danych z pliku JSON
        with open(backup_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        # Ekstrakcja nazwy kolekcji i bazy danych z nazwy pliku
        collection_name, db_name = os.path.splitext(file_name)[0].split('_')

        # Utworzenie bazy danych, jeśli nie istnieje
        db = client[db_name]

        # Utworzenie kolekcji, jeśli nie istnieje
        collection = db[collection_name]

        # Wstawienie dokumentów do kolekcji
        collection.delete_many({})  # Usunięcie istniejących dokumentów w kolekcji
        collection.insert_many(data)

        print(f"Przywrócono dane do kolekcji: {collection_name} w bazie danych: {db_name}")