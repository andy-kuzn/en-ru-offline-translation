import subprocess

# Функция воспроизведения речи
def text_to_speech(text, voice):
    try:
        subprocess.call("echo "+text+"|rhvoice.test -p "+voice, shell=True)
    # Обработка ошибок
    except Exception as e:
        print(f"An error occurred: {str(e)}")