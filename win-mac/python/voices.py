# Импорт библиотек
import platform
import sys
import pyttsx3 # type: ignore
import configparser

# Импорт функции воспроизведения речи
from scripts.tts import text_to_speech

# Определяем операционную систему хоста и устанавливаем
# соответствующие значения переменных для поиска "голосов".
print("\nОпределение операционной системы...")
if platform.system() == "Windows":
    ru_code = 'RU'
    en_code = 'EN'
    print("Операционная система: Windows")
elif platform.system() == "Darwin":
    ru_code = 'ru'
    en_code = 'en-'
    print("Операционная система: MacOS")
else:
    print("Эта операционная система не поддерживается")
    sys.exit()
    
# Инициализация текстового инетерпретатора 
engine = pyttsx3.init()

# Определяем, какие русские "голоса" установлены в операционной системе.
print("\nПоиск русских голосов..." )
voices = engine.getProperty('voices')
ru_voices_list = []
for voice in voices:
    if ru_code in voice.id:
        ru_voices_list.append(voices.index(voice))
        print(voices.index(voice), voice.id)
        if ru_voices_list == []:
            print("В операционной системе нет установленных русских голосов.")
            sys.exit()


# Выбираем русский "голос" из получившегося списка и проверяем
# его звучание.
print()
set_ru_voice = False
text = "Проверим, как звучит этот голос"
while set_ru_voice == False:
    ru_index = input("Введите индекс выбранного русского голоса: ")
    try:
        if int(ru_index) in ru_voices_list:
            ru_voice_id = voices[int(ru_index)].id
            print("Выбран русский голос:", ru_voice_id)    
        else:
            print("Введено некорректное значение индекса русского голоса.")
            print("Попробуйте еще раз.")
            continue
    except:
        print("Введено некорректное значение индекса.")
        print("Попробуйте еще раз.")
        continue        
    text_to_speech(text,
                   voice = ru_voice_id,
                   rate=150,
                   volume=1.0)                
    if input("Подтверждаете выбор этого голоса? (y/n): ").lower().strip()[:1] == "y":
        set_ru_voice = True
    else:
        print("Попробуйте выбрать другой русский голос.")


# Определяем, какие английские "голоса" установлены в операционной системе.
print("\nПоиск английских голосов..." )
en_voices_list = []
for voice in voices:
    if en_code in voice.id:
        en_voices_list.append(voices.index(voice))
        print(voices.index(voice), voice.id)
        if en_voices_list == []:
            print("В операционной системе нет установленных английских голосов.")
            sys.exit()

# Выбираем английский "голос" из получившегося списка и проверяем
# его звучание.
print()
set_en_voice = False
text = "Let's check the sound of this voice"
while set_en_voice == False:
    en_index = input("Введите индекс выбранного английского голоса: ")
    try:
        if int(en_index) in en_voices_list:
            en_voice_id = voices[int(en_index)].id
            print("Выбран английский голос:", en_voice_id)         
        else:
            print("Введено некорректное значение индекса русского голоса.")
            print("Попробуйте еще раз.")
            continue
    except:
        print("Введено некорректное значение индекса.")
        print("Попробуйте еще раз.")
        continue
    text_to_speech(text,
                   voice = en_voice_id,
                   rate=150,
                   volume=1.0)
    if input("Подтверждаете выбор этого голоса? (y/n): ").lower().strip()[:1] == "y":
        set_en_voice = True
    else:
        print("Попробуйте выбрать другой английский голос.")

# Запись конфигурационного файла "голосов".
config = configparser.ConfigParser()

config['Voices'] = {'ru_voice_id': voices[int(ru_index)].id,
                    'en_voice_id': voices[int(en_index)].id}

with open('config.ini', 'w') as configfile:
   config.write(configfile)
   
# Остановка текстового интерпретатора    
engine = None
print("\nУстановка голосов завершена.")
print("Можно запускать скрипт main.py") 