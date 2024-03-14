# ПОМОЩЬНИК ПО УСТНАНОВКЕ ЗАВИСИМОСТЕЙ
import platform, os

# ANSI Escape коды для цветов
COLORS = {
    # Крассный
    'RED': '\033[91m', 
    
    # Зеленый 
    'GREEN': '\033[92m', 
    
    # Желтый 
    'YELLOW': '\033[93m', 
    
    # Синий 
    'BLUE': '\033[94m', 
    
    # Сброс цвета
    'ENDC': '\033[0m'}

# Очистка терминала 
def clear_terminal():
    """Очистка терминала (Авт. опрдл. системы)"""
    
    # Определяем операционную систему
    system = platform.system()

    # Если операционная система - Windows
    # Очищаем терминал командой cls
    if system == 'Windows': os.system('cls')
    
    # Если операционная система - Unix/Linux/MacOS
    # Очищаем терминал командой clear
    elif system == 'Linux' or system == 'Darwin': os.system('clear')
    
    # Если не удалось определить операционную систему, выводим сообщение об ошибке
    else: print(F"[!] {COLORS['RED']}Не удалось определить операционную систему.{COLORS['ENDC']}")

# Автоматическая установка зависимостей
def requirements(module: str = None, description: str = None, link: str = None):
    """Автоматическая установка зависимостей"""

    print(F"\n[!] {COLORS['RED']}У вас отсутствует модуль ->{COLORS['YELLOW']} {module}{COLORS['ENDC']}")
    print(F"[&] {COLORS['GREEN']}Ссылка на Pypi:{COLORS['BLUE']} {link}{COLORS['ENDC']}")
    print(F"[?] {COLORS['GREEN']}Описание модуля:{COLORS['ENDC']} {description}\n")


    try:
        # Выбор пользователя об установке модуля
        choice = input(F"[*] {COLORS['YELLOW']}Установить модуль pydub? (y/n):{COLORS['ENDC']} ")
        
        # Пользователь решил установить
        if choice.lower() == 'y' or choice.lower() == 'н':
            try:
                # Установка модуля
                import subprocess
                subprocess.check_call(['pip', 'install', module])
            
            # Обработка ошибки при работе subprocess
            except Exception as error: 
                print(f"[!] {COLORS['RED']}Ошибка при установке модуля:{COLORS['YELLOW']} {error}{COLORS['ENDC']}")
                print(f"[!] {COLORS['RED']}Ошибка при использовании {COLORS['YELLOW']}[subprocess]{COLORS['ENDC']}")
                exit()
        # Если пользователь ничего не выбрал
        else:
            print(F"[*] Операция установки {module} отменена.")
            exit()
    
    # ОБРАБОТКА CRTL + C
    except KeyboardInterrupt as keyError: 
        print(F"\n[*] Операция установки {module} отменена.")
        exit()

# Проверка установки FFmpeg
def ffmpeg_requirements():
    clear_terminal()
    
    # Проверка установки FFmpeg
    ffmpeg_status = YouTubeDL()._check_ffmpeg_installed()
    
    # Если FFmpeg установлен
    if ffmpeg_status: 
        print(F"[+] {COLORS['GREEN']}FFmpeg доступен в вашей системе: {COLORS['ENDC']}{ffmpeg_status=}")
    
    else:
        print(F"[+] {COLORS['RED']}FFmpeg не установлен в вашу систему {COLORS['ENDC']}{ffmpeg_status=}!")
        print(F"[+] {COLORS['BLUE']}Без него, ничего не будет работать..{COLORS['ENDC']}\n")

        try:
            # Выбор пользователя об установке модуля
            choice = input(F"[*] {COLORS['YELLOW']}Показать инструкцию по установке FFMPEG? (y/n):{COLORS['ENDC']} ")
        
            # Подробная инструкция
            if choice.lower() == 'y' or choice.lower() == 'н':
                clear_terminal()
                
                # UBUNTU/DEBIAN
                print(F"{COLORS['BLUE']}[+] UBUNTU/DEBIAN (40-50 МБ).{COLORS['ENDC']}")
                print("[-] sudo apt update")
                print("[-] sudo apt install ffmpeg\n")

                # CENTOS/RHEL
                print(F"{COLORS['BLUE']}[+] CENTOS/RHEL (50-60 МБ).{COLORS['ENDC']}")
                print("[-] sudo yum install epel-release")
                print("[-] sudo yum install ffmpeg\n")
                
                # FEDORA
                print(F"{COLORS['BLUE']}[+] FEDORA (0-0 МБ).{COLORS['ENDC']}")
                print("[-] sudo dnf install ffmpeg\n")

                # MACOS
                print(F"{COLORS['BLUE']}[+] MACOS (40-50 МБ).{COLORS['ENDC']}")
                print("[-] brew install ffmpeg\n")

                # WINDOWS / С помощью установщика
                print(F"{COLORS['BLUE']}[+] WINDOWS / С помощью установщика (50-100 МБ): {COLORS['ENDC']}")
                print(F"[1] Перейдите на официальный сайт FFmpeg: {COLORS['YELLOW']}https://ffmpeg.org/download.html.{COLORS['ENDC']}")
                print("[2] Скачайте статический сборки FFmpeg для Windows.")
                print("[3] Распакуйте архив в удобную для вас директорию.")
                print("[4] Добавьте путь к исполняемым файлам FFmpeg в переменную PATH вашей системы.\n")

                # WINDOWS / С помощью Chocolatey
                print(F"{COLORS['BLUE']}[+] WINDOWS / С помощью Chocolatey (50-100 МБ): {COLORS['ENDC']}")
                print(F"[1] Установите менеджер пакетов Chocolatey, следуя инструкциям на сайте: {COLORS['YELLOW']}https://chocolatey.org/install.{COLORS['ENDC']}")
                print("[2] Установите FFmpeg с помощью Chocolatey:")
                print("[-] choco install ffmpeg\n")

                # Совет
                print(F"{COLORS['BLUE']}[?] Совет:{COLORS['ENDC']} После установки проверьте, что FFmpeg успешно установлен, запустив команду {COLORS['YELLOW']}ffmpeg{COLORS['ENDC']} в вашем терминале или командной строке.\n")

            # Если пользователь ничего не выбрал
            else:
                print(F"[*] Операция установки FFmpeg отменена.")
                exit()


        # ОБРАБОТКА CRTL + C
        except KeyboardInterrupt as keyError: 
            print(F"\n[*] Операция установки FFmpeg отменена.")
            exit()

# МОДУЛЬ PYDUB - Работает с конвертацией аудио
clear_terminal()
try: import pydub
except ImportError: requirements(
    module="pydub",
    link="https://pypi.org/project/pydub",
    description="PYDUB - Работает с конвертацией аудио | "
    "Управляйте звуком с помощью простого и понятного интерфейса высокого уровня.")

# МОДУЛЬ QUART - Асинхронный веб-фреймворк для Python (Альтернатива Flask) 
clear_terminal()
try: import quart
except ImportError: requirements(
    module="Quart", 
    link="https://pypi.org/project/Quart",
    description="Quart - это асинхронный веб-фреймворк для Python (Альтернатива Flask) | " 
    "Построенный поверх асинхронной библиотеки ASGI (Asynchronous Server Gateway Interface). " 
    "Он разработан как альтернатива Flask для асинхронного программирования, "
    "поддерживая множество функций и API, которые делают его очень похожим на Flask, "
    "но предоставляющим асинхронные возможности. ")

# МОДУЛЬ REQUESTS-HTML - Библиотека Python для парсигда JS на сайтах (Альтернатива BeautifullSoup4) 
clear_terminal()
try: import requests_html
except ImportError: requirements(
    module="requests-html", 
    link="https://pypi.org/project/requests-html",
    description="Requests-HTML - это библиотека Python для парсигда JS на сайтах, " 
    "предоставляющая удобный интерфейс "
    "для выполнения HTTP-запросов и парсинга HTML-кода веб-страниц. "
    "Она основана на библиотеке requests, которая предоставляет "
    "простой API для работы с HTTP, и pyquery, который является аналогом jQuery для Python.")

# МОДУЛЬ REQUESTS-HTML - Форк библиотеки youtube-dlc (Установка видео с YouTube)
clear_terminal()
try: import yt_dlp
except ImportError: requirements(
    module="yt_dlp", 
    link="https://pypi.org/project/yt-dlp",
    description="Yt-dlp это форк библиотеки youtube-dlc, "
    "который предоставляет расширенные возможности для загрузки видео "
    "с различных платформ, включая YouTube. Он создан для улучшения " 
    "и расширения функциональности youtube-dl, известной и широко "
    "используемой библиотеки для загрузки видео с Интернета.")

# Проверка установки FFmpeg
from src.tools import YouTubeDL
ffmpeg_requirements()





