# Установка библиотек и зависимомтей в вирутуальную среду
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
install("sounddevice==0.4.6")
install("scipy==1.13.0")
install("git+https://github.com/openai/whisper.git")
install("transformers==4.40.1")
install("sentencepiece==0.2.0")
install("sacremoses==0.1.1")
install("torch==2.2.2")
install("torchaudio==2.2.2")
install("huggingface-hub==0.20.3")

print("\nУстановка библиотек и зависимостей завершена.")
print("Далее необходимо запустить скрипт voices.py.")