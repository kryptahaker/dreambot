#Znaki

#import re
#
#def zamien_polskie_znaki(tekst):
#    zamiany = {
#        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
#        'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
#        'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N',
#        'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
#    }
#    for polski, zastepczy in zamiany.items():
#        tekst = tekst.replace(polski, zastepczy)
#    return tekst
#
#with open('main.py', 'r', encoding='utf-8') as plik:
#    kod = plik.read()
#
#nowy_kod = zamien_polskie_znaki(kod)
#
#with open('main_nowy.py', 'w', encoding='utf-8') as plik_nowy:
#    plik_nowy.write(nowy_kod)


#Emotki
import re

def remove_emojis(input_text):
    # Pattern do identyfikowania emotek
    emoji_pattern = re.compile("["
                              u"\U0001F600-\U0001F64F"  # emotki ogólne
                              u"\U0001F300-\U0001F5FF"  # symbole & pictogramy
                              u"\U0001F680-\U0001F6FF"  # symbole transportu & mapy
                              u"\U0001F700-\U0001F77F"  # symbole narzędzi & ustawień
                              u"\U0001F780-\U0001F7FF"  # karty & terminy
                              u"\U0001F800-\U0001F8FF"  # symbole ogólne
                              u"\U0001F900-\U0001F9FF"  # symbole różnych
                              u"\U0001FA00-\U0001FA6F"  # symbole dodatkowe
                              u"\U0001FA70-\U0001FAFF"  # symbole sportowe
                              u"\U00002702-\U000027B0"  # znaki użycia
                              u"\U000024C2-\U0001F251" 
                              "]+", flags=re.UNICODE)

    # Usuń emotki z tekstu
    return emoji_pattern.sub(r'', input_text)

 #Otwórz plik main.py i przeczytaj jego zawartość
with open('main.py', 'r', encoding='utf-8') as file:
    file_content = file.read()

 #Usuń emotki z zawartości pliku
new_content = remove_emojis(file_content)

 #Zapisz nową zawartość do pliku
with open('main_cleaned.py', 'w', encoding='utf-8') as new_file:
    new_file.write(new_content)
