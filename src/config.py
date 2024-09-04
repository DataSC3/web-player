# НАСТРОЙКИ
import os

# Путь к хранилище треков 
# ------------------------------------------
MUSIC_PATH: str = "static/music/" 

try:
    if MUSIC_PATH[-1] != "/": MUSIC_PATH + "/"

# Если будет ошибка, чтобы выбрал путь по умолчанию
except IndexError: MUSIC_PATH = "static/music/"
# ------------------------------------------

# Настройки сети (Хост, Порт)
# ------------------------------------------
HOST, PORT = "localhost", 9090
# ------------------------------------------

# Настройки версии
# ------------------------------------------
VERSION: str = "1.0.1"
# ------------------------------------------

# Логирование в консоль
# ------------------------------------------
LOGGING_MODE: bool = True
# ------------------------------------------

# ------------------------------------------
# Путь к файлу где сохраняються результаты установок треков через YouTube
STATUS_COUNT_FILE: str = "src/.status_count.txt"

# Текст для FRONTEND (class="status-text")
STATUS_TEXT: str = "Песни автоматически переключаются и загружаются через YouTube."

# Текст для распознования песни что он загружен из YouTube для FRONTEND
STATUS_YT: str = " -YT9"

# Аудио рассширения
AUDIO_EXTENSIONS: list = [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma", ".alac", ".aiff", ".opus", ".webm"]
# ------------------------------------------


# (Не редактировать >) ------------------------------------------
# Цветовая политра
COLOR_CODE = {
    "RESET": "\033[0m",      # Сброс цвета [Стиль]
    "UNDERLINE": "\033[04m", # Нижнее подчеркивание [Стиль]
    "GREEN": "\033[32m",     # Зеленый 
    "YELLOW": "\033[93m",    # Желтый
    "RED": "\033[31m",       # Красный
    "CYAN": "\033[36m",      # Светло голубой
    "BOLD": "\033[01m",      # Жирный [Стиль]
    "PINK": "\033[95m",      # Розовое
    "URL_L": "\033[36m",     # Ссылки [Стиль] 
    'BLUE': '\033[94m',      # Синий
    "LI_G": "\033[92m",      
    "F_CL": "\033[0m",
    "DARK": "\033[90m",      # Темный
    "ORANGE": "\033[38;5;208m"  # Оранжевый
}

# Очистка консоли
def console_clear() -> None:
    """Очиска консоли (Windows / Linux)"""
    
    # Очистка для Windows
    if os.sys.platform == "win32": os.system("cls")

    # Очистка для Linux
    else: os.system("clear")

# ———————————————————————————————————————————————————————————————————
# Баннер
def console_banner(music_count: str = "0", music_size: str = "0"):
    """Вывод баннера в консоль

    Args:
        music_count (str, optional): Количество тркеов. Поумолчании "0".
        music_size (str, optional): _description_. Поумолчании "0".
    """
    # Очистка консоли
    console_clear()
    
    # Баннер
    print(F"{COLOR_CODE['ORANGE']} *{COLOR_CODE['RESET']} ———————————————————————— {COLOR_CODE['DARK']}{VERSION}{COLOR_CODE['RESET']}")
    print(F"{COLOR_CODE['ORANGE']} * ╭━┳━┳━┳╮{COLOR_CODE['RESET']} ╭━┳╮╭━━┳━┳┳━┳━┳━╮")
    print(F"{COLOR_CODE['ORANGE']} * ┃┃┃┃┣╮┃┃{COLOR_CODE['RESET']} ┃╋┃┃┃╭╮┣╮┃┃┳┫┳┫╋┃")
    print(F"{COLOR_CODE['ORANGE']} * ┃┃┃┃┣┻╮┃{COLOR_CODE['RESET']} ┃╭┫╰┫┣┫┣┻╮┃┻┫┻┫╮┫")
    print(F"{COLOR_CODE['ORANGE']} * ╰┻━┻┻━━╯{COLOR_CODE['RESET']} ╰╯╰━┻╯╰┻━━┻━┻━┻┻╯")
    print(F"{COLOR_CODE['ORANGE']} *{COLOR_CODE['RESET']} ———————————————————————— \n")

    # Статус логирования
    if LOGGING_MODE: logging_text: str = F"          {COLOR_CODE['GREEN']}Включена{COLOR_CODE['RESET']}"
    else: logging_text: str = F"          {COLOR_CODE['RED']}Отключена{COLOR_CODE['RESET']}"
    
    print(F" ▲  ———————————————————————————————🢖")

    # Количество и размер треков
    print(F"[*] Количество и размер треков:  {COLOR_CODE['GREEN']}{music_count} / {music_size}{COLOR_CODE['RESET']}")
    
    # Доступные расширения
    print(F"[*] Разрешенные рассширения:     {COLOR_CODE['DARK']}{', '.join(AUDIO_EXTENSIONS)}{COLOR_CODE['RESET']}")
    
    # Статус режима логирования
    print(F"[*] Режим логирования: {logging_text}")

    # Путь к хранилище треков
    print(F"[*] Путь к трекам:               {COLOR_CODE['GREEN']}{MUSIC_PATH}{COLOR_CODE['RESET']}")

    # Настройки сети
    print(F"[*] Веб-сайт:                    {COLOR_CODE['UNDERLINE']}{COLOR_CODE['URL_L']}{HOST}:{PORT}{COLOR_CODE['RESET']}")

    print(F" ▼  ———————————————————————————————🢖\n")

# ———————————————————————————————————————————————————————————————————

