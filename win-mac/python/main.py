import os
import sys
import configparser

print("Загрузка системы устного перевода...")

import sounddevice as sd # type: ignore
from scipy.io.wavfile import write # type: ignore
import whisper # type: ignore
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM # type: ignore

# Импорт функции воспроизведения речи
from scripts.tts import text_to_speech

# Чтение конфигурационного файла "голосов"
config = configparser.ConfigParser()
try:
    config.read('config.ini')
    ru_voice_id = config['Voices']['ru_voice_id']
    en_voice_id = config['Voices']['en_voice_id']
except:
    print('Не установлены "голоса" для воспроизведения речи.')
    sys.exit()

# Настройки записи речи с микрофона
sd.default.dtype='int32', 'int32'
fs = 44100  # Частота дискретизации звукового потока - 44,1 КГц
seconds = 30  # Длительность записи (Меняем по необходимости.
               # В данном случае установлено предельное значение.)
if not os.path.exists('audio'):  # Проверяем наличие папки
   os.makedirs('audio')

# Модель распознавания речи Whisper (базовая)
whisper_model = whisper.load_model("base")

# Модель перевода с английского языка на русский Helsinki-NLP/opus-mt-en-ru
en_ru_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-ru",
                                          padding_side='left')
en_ru_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-en-ru")

# Модель перевода с русского языка на английский Helsinki-NLP/opus-mt-ru-en
ru_en_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ru-en",
                                          padding_side='left')
ru_en_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-ru-en")

# Функция завершения записи и перевода 
def stop_recording(myrecording):
    # Останвливаем запись.
    sd.stop()
    # display("Запись закончена. Думаю...") # type: ignore
    # Сохраняем запись в аудиофайл.
    write('audio/file.wav', fs, myrecording)
        
    # Загружаем аудиозапись в модель, увеличиваем ее длительность
    # или обрезаем до 30 секунд.
    audio = whisper.load_audio("audio/file.wav")
    audio = whisper.pad_or_trim(audio)
        
    # Построим лог-мел спектрограмму и перенесем ее на то же устройство,
    # что и модель
    mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)

    # Определим язык, на котором говорят.
    _, probs = whisper_model.detect_language(mel)
    detected_lang = next(iter({max(probs, key=probs.get)}))
    print("Detected language: ", detected_lang)
        
    # Декодируем аудиозапись.
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(whisper_model, mel, options)
    text = result.text
    print(text)
    print('')
        
    if detected_lang == 'en':
        # Перевод с английского языка на русский
        input_ids = en_ru_tokenizer.encode(text, return_tensors="pt")
        outputs = en_ru_model.generate(input_ids)
        translated = en_ru_tokenizer.decode(outputs[0],
                                        skip_special_tokens=True)
        voice_id = ru_voice_id
        print(translated)
                       
    elif detected_lang == 'ru':
        # Перевод с русского языка на английский. 
        input_ids = ru_en_tokenizer.encode(text, return_tensors="pt")
        outputs = ru_en_model.generate(input_ids)
        translated = ru_en_tokenizer.decode(outputs[0],
                                            skip_special_tokens=True)
        voice_id = en_voice_id
        print(translated)
        
    else:
        translated = None   

    # Воспроизведение переведенного текста
    if translated:
        text_to_speech(translated,
                       voice = voice_id,
                       rate=150,
                       volume=1.0)
    else:
        text = "Этот язык не поддерживается"
        print(text)
        text_to_speech(text,
                       voice = ru_voice_id,
                       rate=150,
                       volume=1.0)


# Запись речи и перевод
while True:
    print()
    result = input("Нажмите Enter, чтобы начать запись, "
                   "или введите любой символ, чтобы выйти из программы: ")
    if result == "":
        print ("Записываю...")
        myrecording = sd.rec(int(seconds * fs),
                             samplerate=fs,
                             channels=1)
        print()
        if input("Нажмите Enter, чтобы закончить запись и начать перевод: ") == "":
            print("Запись закончена. Думаю...")
            stop_recording(myrecording)
        else: continue
    else: sys.exit()