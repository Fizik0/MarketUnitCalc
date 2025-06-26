"""
Скрипт для запуска приложения в режиме разработки
с автоматической перезагрузкой при изменении кода
"""
import os
import sys
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Цвета для консольного вывода
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_banner():
    """Вывод информационного баннера"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
{BLUE}==========================================================={RESET}
{GREEN}   Калькулятор Юнит-Экономики - Режим Разработки{RESET}
{BLUE}==========================================================={RESET}
{YELLOW}
- Приложение запущено на http://localhost:8501
- Изменения в коде вызовут автоматическую перезагрузку
- Для завершения работы нажмите Ctrl+C
{RESET}
{BLUE}==========================================================={RESET}
""")

class StreamlitHandler(FileSystemEventHandler):
    """Обработчик изменений файлов"""
    def __init__(self, process_func):
        self.process_func = process_func
        self.last_modified = time.time()
    
    def on_modified(self, event):
        # Игнорируем события от директорий и слишком частые события
        if event.is_directory or time.time() - self.last_modified < 1:
            return
        
        # Фильтруем только Python файлы и JSON
        if event.src_path.endswith(('.py', '.json')):
            self.last_modified = time.time()
            print(f"{YELLOW}[DEV] Изменен файл: {event.src_path}{RESET}")
            self.process_func()

def restart_streamlit():
    """Перезапуск процесса Streamlit"""
    global streamlit_process
    
    # Завершаем текущий процесс
    if streamlit_process:
        print(f"{YELLOW}[DEV] Перезапуск сервера...{RESET}")
        streamlit_process.terminate()
        streamlit_process.wait()
    
    # Запускаем новый процесс
    streamlit_process = subprocess.Popen(
        ["streamlit", "run", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )
    print(f"{GREEN}[DEV] Сервер перезапущен{RESET}")

if __name__ == "__main__":
    # Проверка наличия необходимых файлов
    if not os.path.exists("app.py"):
        print(f"{RED}ОШИБКА: app.py не найден. Запустите скрипт из корневой директории проекта.{RESET}")
        sys.exit(1)
    
    # Глобальная переменная для процесса
    streamlit_process = None
    
    try:
        # Вывод баннера
        print_banner()
        
        # Первый запуск
        restart_streamlit()
        
        # Настройка наблюдателя за изменениями файлов
        event_handler = StreamlitHandler(restart_streamlit)
        observer = Observer()
        
        # Наблюдаем за несколькими директориями
        paths_to_watch = [".", "utils", "data", "pages"]
        for path in paths_to_watch:
            if os.path.exists(path):
                observer.schedule(event_handler, path, recursive=True)
        
        observer.start()
        print(f"{BLUE}[DEV] Отслеживание изменений запущено{RESET}")
        
        # Поддерживаем скрипт запущенным и выводим логи Streamlit
        while True:
            if streamlit_process and streamlit_process.poll() is None:
                output = streamlit_process.stdout.readline()
                if output:
                    print(output.strip())
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print(f"\n{YELLOW}[DEV] Завершение работы...{RESET}")
        
        if streamlit_process:
            streamlit_process.terminate()
            
        observer.stop()
        observer.join()
        
        print(f"{GREEN}[DEV] Работа приложения завершена{RESET}")
        sys.exit(0)