# ЗАПУСК WSG СЕРВЕРА
from src.config import HOST, PORT, COLOR_CODE, AUDIO_EXTENSIONS, LOGGING_MODE, MUSIC_PATH, console_clear
import subprocess


# Выбор пользователя об установке модуля
console_clear()
print(F"[{COLOR_CODE['ORANGE']}*{COLOR_CODE['RESET']}] {COLOR_CODE['ORANGE']}{COLOR_CODE['BOLD']}MY{COLOR_CODE['RESET']} {COLOR_CODE['BOLD']}PLAYEER")

try:
    choice = input(F"[{COLOR_CODE['ORANGE']}*{COLOR_CODE['RESET']}] Вы хотите увидеть настройки? (y/n): ")

    # Пользователь решил посмотреть на настройки
    if choice.lower() == 'y' or choice.lower() == 'н':
        
        # Доступные расширения
        print(F" {COLOR_CODE['ORANGE']}|{COLOR_CODE['RESET']}")
        print(F"[*] Разрешенные рассширения: {COLOR_CODE['DARK']}{', '.join(AUDIO_EXTENSIONS)}{COLOR_CODE['RESET']}")
        
        # Статус режима логирования
        print(F"[*] Режим логирования: {COLOR_CODE['URL_L']}{LOGGING_MODE}{COLOR_CODE['RESET']}")

        # Путь к хранилище треков
        print(F"[*] Путь к трекам: {COLOR_CODE['GREEN']}{MUSIC_PATH}{COLOR_CODE['RESET']}")

        # Настройки сети
        print(F"[*] Настройки сети: {COLOR_CODE['UNDERLINE']}{COLOR_CODE['URL_L']}{HOST}:{PORT}{COLOR_CODE['RESET']}")

        print(F" {COLOR_CODE['ORANGE']}|{COLOR_CODE['RESET']}")
        print(F"[{COLOR_CODE['ORANGE']}?{COLOR_CODE['RESET']}] {COLOR_CODE['BLUE']}Чтобы изменить настройки, перейдите в src/config.py{COLOR_CODE['RESET']}")

        choice = input(F"[{COLOR_CODE['ORANGE']}*{COLOR_CODE['RESET']}] Запустить сервер? (y/n): ")
        
        # Пользователь решил запустить сервер
        if choice.lower() == 'y' or choice.lower() == 'н':
            # hypercorn main:app --bind HOST:PORT
            subprocess.check_call(["hypercorn", "main:app", "--bind", F"{HOST}:{PORT}"])

        # Если пользователь ничего не выбрал
        else:
            print(F"[{COLOR_CODE['RED']}!{COLOR_CODE['RESET']}] Операция запуска сервера была отменена.")
            exit()


    elif choice.lower() == 'n' or choice.lower() == 'т':
        choice = input(F"[{COLOR_CODE['ORANGE']}*{COLOR_CODE['RESET']}] Запустить сервер? (y/n): ")
        
        # Пользователь решил запустить сервер
        if choice.lower() == 'y' or choice.lower() == 'н':
            # hypercorn main:app --bind HOST:PORT
            subprocess.check_call(["hypercorn", "main:app", "--bind", F"{HOST}:{PORT}"])

        # Если пользователь ничего не выбрал
        else:
            print(F"[{COLOR_CODE['RED']}!{COLOR_CODE['RESET']}] Операция запуска сервера была отменена.")
            exit()

    # Если пользователь ничего не выбрал
    else:
        print(F"[{COLOR_CODE['RED']}!{COLOR_CODE['RESET']}] Операция выбора отменена.")
        exit()


# ОБРАБОТКА CRTL + C
except KeyboardInterrupt as keyError: 
    print(F"\n[{COLOR_CODE['RED']}!{COLOR_CODE['RESET']}] Процесс отключен.")
    exit()


