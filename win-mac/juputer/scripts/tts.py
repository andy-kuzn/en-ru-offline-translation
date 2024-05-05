import pyttsx3

# Функция воспроизведения речи
def text_to_speech(text, voice=None, rate=150, volume=1.0):
    try:
        # Инициализация текстового интерпретатора
        engine = pyttsx3.init()

        # Установка параметров
        engine.setProperty('voice', voice) # Голос
        engine.setProperty('rate', rate)  # Скорость речи
        engine.setProperty('volume', volume)  # Уровень громкости

        # Воспроизведение речи
        engine.say(text)
        # Ожидание окончания воспроизведения речи
        engine.runAndWait()
        
        # Остановка текстового интерпретатора    
        engine = None
        
    # Обработка ошибок
    except Exception as e:
        print(f"An error occurred: {str(e)}")