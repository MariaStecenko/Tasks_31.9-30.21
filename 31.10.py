import os
import threading
import time

TMP_DIR = "temp_files"
os.makedirs(TMP_DIR, exist_ok=True)

t1 = 2  # перевіряти кожні 2 секунди
t2 = 3  # видаляти файли, змінені раніше ніж 3 секунди тому

def daemon_cleanup():
    """Потік-демон для очищення застарілих .tmp файлів"""
    while True:
        time.sleep(t1)
        now = time.time()
        for filename in os.listdir(TMP_DIR):
            if filename.endswith(".tmp"):
                filepath = os.path.join(TMP_DIR, filename)
                mtime = os.path.getmtime(filepath)
                # Якщо файл старіший за t2 секунд
                if now - mtime >= t2:
                    try:
                        os.remove(filepath)
                        print(f"[Демон] Видалено: {filename}")
                    except OSError:
                        pass

# запуск демона
cleaner = threading.Thread(target=daemon_cleanup, daemon=True)
cleaner.start()

# основний потік
print("Основний потік працює. Створюються файли...")
try:
    for i in range(10):
        fname = os.path.join(TMP_DIR, f"file_{i}.tmp")
        with open(fname, "w") as f:
            f.write(f"Дані {i}")
        print(f"[Основний] Створено: file_{i}.tmp")
        time.sleep(0.8)
    time.sleep(5)  
finally:
    for f in os.listdir(TMP_DIR):
        os.remove(os.path.join(TMP_DIR, f))
    os.rmdir(TMP_DIR)
