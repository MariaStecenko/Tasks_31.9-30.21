import queue
import random
import threading
import time

N = 100       # кількість глядачів
m = 3         # кількість турнікетів
t_open = 60   # турнікети відкривають за t_open секунд до матчу
t1 = 3        # максимальний час проходу через турнікет (1..t1)

# черга глядачів
spectators_queue = queue.Queue()

# час прибуття глядачів 
arrival_times = sorted([random.uniform(-t_open, 0) for _ in range(N)])
for i, arr_t in enumerate(arrival_times):
    spectators_queue.put((arr_t, i))

results = [] 
lock = threading.Lock()

def turnstile_worker():
    current_time = -t_open
    while not spectators_queue.empty():
        try:
            arr_t, spec_id = spectators_queue.get_nowait()
        except queue.Empty:
            break
        
        # турнікет чекає глядача, якщо той ще не прийшов
        start_service = max(current_time, arr_t)
        service_duration = random.uniform(1, t1)
        finish_time = start_service + service_duration
        current_time = finish_time
        
        # встиг, якщо завершив прохід до початку матчу (<= 0)
        success = (finish_time <= 0)
        with lock:
            results.append((arr_t, success))
            
        spectators_queue.task_done()

# запуск m потоків (турнікетів)
threads = [threading.Thread(target=turnstile_worker) for _ in range(m)]
for t in threads:
    t.start()
for t in threads:
    t.join()

results.sort(key=lambda x: x[0])

# рахую ймовірність успіху у ковзному вікні
window_size = 20
found_time = None

for i in range(len(results) - window_size):
    window = results[i:i+window_size]
    prob = sum(1 for _, s in window if s) / window_size
    if prob >= 0.9:
        found_time = window[0][0]
        break

if found_time is not None:
    print(f"Потрібно прийти щонайменше за {abs(found_time):.2f} сек до початку матчу (імовірність 0.9).")
else:
    print("При заданих параметрах досягти імовірності 0.9 не вдалося.")
