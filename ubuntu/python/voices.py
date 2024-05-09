# Импорт библиотек
import subprocess
import configparser
import sys

# Импорт функции воспроизведения речи 
from scripts.tts import text_to_speech

# Ввод пароля для sudo.
password = input("Введите свой пароль для sudo: ")

# Сгенерируем список всех "голосов", которые могут быть установлены.
subprocess.call("echo "+password+ "| sudo -S rhvoice.vm -a > voices.txt",
                        shell=True)
voices_file = open("voices.txt", "r")
voices_list = voices_file.read().split("\n")
voices_file.close()

# Из полученного общего списка сформируем список всех доступных
# русских и английских "голосов".
ru_voices = []
en_voices = []
for voicename in voices_list:
    if "русский" in voicename:
        voicename = voicename.replace(" (русский)", "")
        ru_voices.append(voicename)
    elif "English" in voicename:
        voicename = voicename.replace(" (English)", "")
        en_voices.append(voicename)
    else:
        continue

# Выведем список всех доступных русских "голосов".      
print("\nВсе доступные русские голоса: ", ru_voices)

# Выведем список всех доступных английских голосов.
print("\nВсе доступные английские голоса: ", en_voices)

# Также проверим, какие "голоса" уже были были установлены.
print("\nВсе ранее установленные голоса:")
subprocess.call("echo "+password+ "| sudo -S rhvoice.vm -l",
                shell=True)

# Выбираем русский "голос" из списка доступных и проверяем
# его звучание.
print("\nВыберите русский голос из списка доступных, например, Aleksandr.")
print("Если он еще не был установлен, он будет установлен сейчас.")
set_ru_voice = False
text = "Проверим, как звучит этот голос"
while set_ru_voice == False:
    ru_voice_name = input("Введите имя выбранного русского голоса: ")
    if ru_voice_name in ru_voices:
        subprocess.call("echo "+password+ "| sudo -S rhvoice.vm -i "+ru_voice_name,
                    shell=True)
    else:
        print("\nВведено некорректное имя.")
        print("Попробуйте еще раз. \n")
        continue
    voice = ru_voice_name
    text_to_speech(text, voice)
    if input("Подтверждаете выбор этого голоса? (y/n): ").lower().strip()[:1] == "y":
        set_ru_voice = True
    else:
        print("Попробуйте выбрать другой русский голос. \n")

# Выбираем английский "голос" из списка доступных и проверяем
# его звучание.
print("\nВыберите английский голос из списка доступных, например, Alan.")
print("Если он еще не был установлен, он будет установлен сейчас.")
set_en_voice = False
text = "Let's test how this voice sounds"
text = text.replace("'", "")
while set_en_voice == False:
    en_voice_name = input("Введите имя выбранного английского голоса: ")
    if en_voice_name in en_voices:
        subprocess.call("echo "+password+ "| sudo -S rhvoice.vm -i "+en_voice_name,
                    shell=True)
    else:
        print("\nВведено некорректное имя.")
        print("Попробуйте еще раз. \n")
        continue
    voice = en_voice_name
    text_to_speech(text, voice)
    if input("Подтверждаете выбор этого голоса? (y/n): ").lower().strip()[:1] == "y":
        set_en_voice = True
    else:
        print("Попробуйте выбрать другой английский голос. \n")

# Запись конфигурационного файла "голосов".
config = configparser.ConfigParser()

config['Voices'] = {'ru_voice_name': ru_voice_name,
                    'en_voice_name': en_voice_name}

with open('config.ini', 'w') as configfile:
   config.write(configfile)
