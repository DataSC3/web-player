import os
import random
import logging
import platform
import subprocess
from typing import List
from secrets import token_hex
from src.config import STATUS_COUNT_FILE, STATUS_YT

# СТОРОННИЕ ИМПОРТЫ (3)
from requests_html import HTMLSession
from pydub import AudioSegment
from yt_dlp import YoutubeDL 


# -----------------------------------
# Отключение логирования у yt_dlp 
class YtCustomLogger:
    """Отключение логирования у yt_dlp"""
    def debug(self, msg): pass
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

# РАБОТА С ИНСТРУМЕНТАМИ ПОДДЕРЖКИ СОФТА
class ToolsTrack:
    """:attr: `MAX_MOBILE_NAME_LENGTH` - Значение требуется для установки 
    длины названии трека ДЛЯ МОБИЛЬНЫХ УСТРОЙСТВ. (20)\n

    :attr: `MAX_PC_NAME_LENGTH` - Значение требуется для установки 
    длины названии трека ДЛЯ ПК. (50)"""

    MAX_MOBILE_NAME_LENGTH: int = 20
    MAX_PC_NAME_LENGTH: int = 50
    
    # Установка логирования 
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    def __init__(self, directory_path: str, logging_mode: bool = False) -> None:
        """Работа с модулям треков.\n
        :param: `directory_path | STR` - Путь к хранилище треков. (path/to/folder/) \n\n
        :param: `logging_mode | BOOL` - Режим логирования.\n
        :modul: `get_tracks` - Получение треков из хранилища в виде списка.\n
        """
        self.directory_path: str = directory_path
        self.logging_mode: bool = logging_mode

    # Получение списка треков
    def _tracks_list(self, user_agent: str = None, mix: bool = False) -> List[list]:
        """Получение треков из хранилища в виде списка.\n
        _Для телефонов, строка Имени трека имеет длину не более 20 символов._\n
        _Для ПК, строка Имени трека имеет длину не более 50 символов._\n\n

        :param: `user_agent | STR` - User-Agent пользователя, чтобы узнать какое устройство у посетителя сайта.\n
        :param: `mix | BOOL` - Перемешивает список треков.\n
        
        :return: `songs | LIST` - Список треков: [[имя, трек]..] 
        """

        try: 
            # Список с треками (с расширением .mp3)
            # .replace(YouTubeDL.TRACK_YOUTUBE_DOWNLOADED_FLAG, "")
            songs_list: list = [song for song in os.listdir(self.directory_path) if ".mp3" in song or ".webm" in song]
        
        # Если позникла ошибка из-за пути к хранилищу треков | режим логирования
        except (NotADirectoryError, FileNotFoundError) as NotDirectoryError:
            
            # Режим логирования
            if self.logging_mode: 
                logging.error(F"Ошибка пути или указанный путь не является директорией: {NotDirectoryError}")
            
            return list()

        # Если user_agent существует
        if user_agent:

            # Вы зашли с мобильного устройства
            if "Mobile" in user_agent or "Android" in user_agent:
                
                # Если нужно перемешать треки
                if mix: random.shuffle(songs_list)
                
                # Режим логирования
                if self.logging_mode: 
                    logging.info(F"Найдено: {len(songs_list)}, треков в директории: {self.directory_path}")
                
                # Имя трека не имеет расширение (.mp3) и содержит не более [self.MAX_MOBILE_NAME_LENGTH] символов (Для мобильных устройств)
                songs: list = [[F"{song.replace('.mp3', '').replace(STATUS_YT, '')[0:self.MAX_MOBILE_NAME_LENGTH]}..", song] if not STATUS_YT in song else
                              [F"{STATUS_YT}{song.replace('.mp3', '')[0:self.MAX_MOBILE_NAME_LENGTH]}..", song] for song in songs_list]
                

                # songs = [["JONY, EMIN - Лунная..", "JONY, EMIN - Лунная ночь.mp3"]]
                return songs
            
            # Вы зашли с ПК
            else:
                # Если нужно перемешать треки
                if mix: random.shuffle(songs_list)
                
                # Режим логирования
                if self.logging_mode: 
                    logging.info(F"Найдено: {len(songs_list)}, треков в директории: {self.directory_path}")
                    
                # Имя трека не имеет расширение (.mp3) и содержит не более [self.MAX_PC_NAME_LENGTH] символов (Для ПК)
                songs: list = [[F"{song.replace('.mp3', '').replace(STATUS_YT, '')[0:self.MAX_PC_NAME_LENGTH]}..", song] if not STATUS_YT in song else
                              [F"{STATUS_YT}{song.replace('.mp3', '')[0:self.MAX_PC_NAME_LENGTH]}..", song] for song in songs_list]
                
                # songs = [["JONY, EMIN - Лунная ночь", "JONY, EMIN - Лунная ночь.mp3"]]
                return songs
        
        else:
            # Если нужно перемешать треки
            if mix: random.shuffle(songs_list)

            # Имя трека не имеет расширение (.mp3) и содержит не более [self.MAX_PC_NAME_LENGTH] символов (Для ПК)
            songs: list = [[F"{song.replace('.mp3', '')}", song] for song in songs_list]
            
            # songs = [["JONY, EMIN - Лунная ночь", "JONY, EMIN - Лунная ночь.mp3"]]
            return songs

    # Получение данных о треках
    def get_tracks_data(self, user_agent: str = None) -> tuple:
        """Получение данных о треков из хранилища (SIZE, QUANTITY)
        1. Выдает размер всех треков в хранилище
        2. Выдает количество всех треков в хранилище

        :param: `user_agent | STR` - User-Agent пользователя, чтобы узнать какое устройство у посетителя сайта.\n
        :module: self._tracks_list() - Получение списка треков
        :return: tuple - SIZE, QUANTITY
        """

        # Список файлов
        all_tracks: list = self._tracks_list(user_agent=user_agent)

        # Суммарный размера в байтах
        total_size_bytes: int = 0  

        # Итерируемся по каждому треку и получаем его размер
        for track in all_tracks:

            # Получаем путь к треку
            file_path: str = os.path.join(self.directory_path, track[1]) 
            
            # Получаем размер файла и добавляем его к общему размеру
            if os.path.isfile(file_path):
                total_size_bytes += os.path.getsize(file_path)

        # Переводим размер из байтов в мегабайты и гигабайты
        # Количество байтов в мегабайте
        total_size_mb = round(float(total_size_bytes / (1024 * 1024)), 2)  
        
        # Количество мегабайтов в гигабайте
        total_size_gb = round(float(total_size_mb / 1024), 2)  

        # Если размер файлов более 1000 МБ то будет показывать результат в ГБ
        if total_size_mb > 1000:
            return F"{total_size_gb} GB", len(all_tracks)
        
        return F"{total_size_mb} MB", len(all_tracks)

    # Удаление трека и вывод списка треков (GETTER)
    def remove_tack(self, filename: str, user_agent: str = None) -> List[list]:
        """Удаление трека и получение треков из хранилища в виде списка.\n
        _Для телефонов, строка Имени трека имеет длину не более 20 символов._\n
        _Для ПК, строка Имени трека имеет длину не более 50 символов._\n\n

        :param: `filename | STR` - Название трека.\n
        :param: `user_agent | STR` - User-Agent пользователя, чтобы узнать какое устройство у посетителя сайта.\n
        :return: `songs | LIST` - Список треков: [[имя, трек]..] 
        """

        # Удаление трека и вывод логирования (Если ВКЛ.)
        try: os.remove(path=self.directory_path + filename)
        except FileNotFoundError as error: 
            if self.logging_mode: logging.error("Ошибка удаления трека с названием:", filename, error)
        else:
            if self.logging_mode: logging.info("Удалён трек с названием:", filename)

        # Возвращаем список треков из хранилища
        return self._tracks_list(user_agent=user_agent)

    # Сохраняет и выдает количество треков из файла src.config.STATUS_COUNT_FILE
    def count_new_tracks(self, new_tracks: int = 0) -> int:
        """Сохраняет и выдает количество треков и файла src.config.STATUS_COUNT_FILE
        :param: `new_tracks | INT` - Количество новых треков 
        :return: `new_tracks_count | INT` - Количество недавно сохраненных треков 
        """

        # Если получено количество новых треков
        if new_tracks:
            try:
                # Сохроняем скаченное кол-во треков в файл для дальнейшей работе с Front.
                with open(STATUS_COUNT_FILE, "w") as new_count: 
                    new_count.write(str(new_tracks)) 

                return True

            except Exception as error:
                logging.error(F"Не удалось получить количество недавно сохраненных треков: {error}")
                return False

        # Иначе выдаем количество новых треков
        else:
            try:
                # Проверяем установились сколько установилось новыех треков
                with open(STATUS_COUNT_FILE, "r") as read_count: 
                    new_tracks_count = read_count.read() 
                    
                    # Если файл с треками пуст (def=0)
                    if not new_tracks_count: 
                        new_tracks_count = "0"

                    return new_tracks_count

            except Exception as error:
                logging.error(F"Не удалось получить количество недавно сохраненных треков: {error}")
                return "0"


    # Выдача треков (GETTER)
    def get_tracks(self, user_agent: str = None, mix: bool = False) -> List[list]:
        """Получение треков из хранилища в виде списка.\n
        _Для телефонов, строка Имени трека имеет длину не более 20 символов._\n
        _Для ПК, строка Имени трека имеет длину не более 50 символов._\n\n

        :param: `user_agent | STR` - User-Agent пользователя, чтобы узнать какое устройство у посетителя сайта.\n
        :param: `mix | BOOL` - Перемешивает список треков.\n
        :param: `logging_mode | BOOL` - Режим логирования.\n
        :return: `songs | LIST` - Список треков: [[имя, трек]..] 
        """
        return self._tracks_list(user_agent=user_agent, mix=mix)
    
# РАБОТА С МОДУЛЕМ YOUTUBE
class YouTubeDL:
    """:attr: `TRACK_YOUTUBE_DOWNLOADED_FLAG` - Флаг означает, что трек был загружен с YouTube. (Требуеться для фронтенда)"""

    TRACK_YOUTUBE_DOWNLOADED_FLAG: str = STATUS_YT

    # Установка логирования 
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

    def __init__(self, directory_path: str = None, logging_mode: bool = False) -> None:
        """Инициализация объекта класса YouTube.
        :param: `directory_path | STR` - Путь к хранилище треков. (path/to/folder/) \n\n
        :param: `logging_mode | BOOL` - Режим логирования.\n"""

        self.logging_mode: bool = logging_mode
        self.directory_path: str = directory_path

    # Получение всех ссылок на песни из плейлиста YouTube
    def _get_playlist(self, link: str, rending_count: int = 5, rending_timeout: int = 60) -> list:
        """Получение всех ссылок песен из плейлиста YouTube.\n\n

        :param: `link | STR` - Ссылка на плейлист.\n
        :param: `rending_count | INT` - Количество повторных ренгингов на случае случайных ошибок на YouTube (def. 5).\n
        :param: `rending_timeout | INT` - Время ожидания конца рендинга страницы во избежания случайных ошибок на (def. 60).\n
        :return: Список ссылок на песни из плейлиста.
        """
    
        # Начало сканирования плейлиста
        if self.logging_mode: logging.info("Начинаем сканирование плейлиста:%s", link)
        
        while rending_count:
            try: 
                # Инициализация сессии и получение страницы
                session = HTMLSession()
                response = session.get(link)
                
                # Рендеринг JavaScript на странице
                response.html.render(timeout=rending_timeout)

                # Получение ссылок на песни из плейлиста
                music_url_list: list = ["https://www.youtube.com" + music_url 
                    for music_url in response.html.links 
                    if '/watch' in music_url]
                
                if self.logging_mode: logging.info("Успешный рендеринг страницы, получено %s%s", len(music_url_list), "треков.")
                return music_url_list

            except Exception as error:
                # Обработка ошибок при рендеринге страницы
                logging.error(F"Ошибка рендеринга страницы, делаем повтор. {error}")
                rending_count -= 1
                continue
    
    # Скачивание трека с YouTube по ссылке
    def _download_youtube_audio(self, link: str) -> bool:
        """
        Скачивание трека с YouTube по ссылке. | modul: yt-dlp | .webm (Format)

        :param: `track_name | STR` - Имя трека по умолчанию, иначе 
        записывается стандартное - название трека с YouTube (Название трека).
        
        :param: `link | STR` - Ссылка на видео.
        :return: bool
        """
        
        try:
            # Опции для YTDLP + Отключение логирования
            youtube_options: dict = {'format': 'ba',
            'outtmpl': self.directory_path + '%(title)s.%(ext)s',
            'logger': YtCustomLogger()}

            # Запускаем загрузку трек явно и ожидаем ее завершения
            with YoutubeDL(params=youtube_options) as ydl:
                ydl.extract_info(link, download=False)
                ydl.download([link])
        
            # Логирование результата 
            if self.logging_mode: logging.info(F"Трек (-и) успешно установились в: {self.directory_path}")    
            return True
            
        # Если возникла ошибка
        except Exception as error:
            logging.error(F"Ошибка при работе: {__name__} {error}")
            return False

    # Проверяет установлен ли FFmpeg на устройство
    def _check_ffmpeg_installed(self) -> bool:
        """Проверяет установлен ли FFmpeg на устройство в \n
        зависимости от операционной системы (Linux, MacOS, Windows)"""

        # Определяем операционную систему
        system_platform = platform.system()

        # Проверяем установку FFmpeg на LINUX
        if system_platform == 'Linux':
            result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
            
            # Если FFmpeg установлен
            if result.returncode == 0:
                if self.logging_mode: logging.info("FFmpeg доступен в вашей операционной системе [Linux]")
                return True
            
            # Если FFmpeg НЕ установлен
            else:
                if self.logging_mode: 
                    logging.error("FFmpeg НЕ доступен в вашей операционной системе [Linux]")
                    logging.info("Пожалуйста, установите FFmpeg на вашу систему [Linux] для использовании %s", self.__class__.__name__)
                
                return False

        # Проверяем установку FFmpeg на MACOS
        elif system_platform == 'Darwin':  # MacOS
            result = subprocess.run(['which', 'ffmpeg'], capture_output=True, text=True)
            
            # Если FFmpeg установлен
            if result.returncode == 0:
                if self.logging_mode: logging.info("FFmpeg доступен в вашей операционной системе [MacOS]")
                return True
            
            # Если FFmpeg НЕ установлен
            else:
                if self.logging_mode: 
                    logging.error("FFmpeg НЕ доступен в вашей операционной системе [MacOS]")
                    logging.info("Пожалуйста, установите FFmpeg на вашу систему [MacOS] для использовании %s", self.__class__.__name__)
                
                return False

        # Проверяем установку FFmpeg на WINDOWS
        elif system_platform == 'Windows':
            result = subprocess.run('where ffmpeg', shell=True, capture_output=True, text=True)
            
            # Если FFmpeg установлен
            if result.returncode == 0:
                if self.logging_mode: logging.info("FFmpeg доступен в вашей операционной системе [Windows]")
                return True
            
            # Если FFmpeg НЕ установлен
            else:
                if self.logging_mode: 
                    logging.error("FFmpeg НЕ доступен в вашей операционной системе [Windows]")
                    logging.info("Пожалуйста, установите FFmpeg на вашу систему [Windows] для использовании %s", self.__class__.__name__)
                
                return False
        
        # Если система не поддерживает FFmpeg
        else:
            if self.logging_mode: 
                logging.error("Ваша система НЕ поддерживает FFmpeg!")
                logging.info("Пожалуйста, прочтите документацию по установке FFmpeg на вашу систему. Фунция %s %s", self.__class__.__name__, "не доступна.")
                
            return False

    # Конвертирует .wedm файл в .mp3
    def _conver_webm_to_mp3(self) -> bool:
        """Конвертирует .wedm файл в .mp3
        При создании файла даеться рандомное HEX имя с флагом self.TRACK_YOUTUBE_DOWNLOADED_FLAG (
            Важно: Данный флаг требуется для распознования ФРОНТЕНДОМ,
                    на выдачу ему иконки о доп. установки трека с YouTube)
        
        :param: `filename | STR` - Название файла который нужно конвертировать.\n
        :return: bool
        """
        try:
            # Получаем все скаченные треки из папки которые имеют расширение .webm
            tracks_list = [track for track in os.listdir(self.directory_path) if ".webm" in track]

            # Сохроняем скаченное кол-во треков в файл для дальнейшей работе с Front.
            trackToolsClass = ToolsTrack(directory_path=self.directory_path)
            trackToolsClass.count_new_tracks(new_tracks=len(tracks_list))

            # Если список треков имеються:
            if tracks_list:
                for webm_file in tracks_list:
                    webm_file_path = self.directory_path + webm_file
                    
                    audio = AudioSegment.from_file(file=webm_file_path, format="webm")

                    for symbols in ["?", '"', "'", "/", ":", "#", "|", ",", " | ", "<", ">", "*"]:                         
                        webm_file = webm_file.replace(symbols, "")
                    
                    new_file_name: str = self.directory_path + self.TRACK_YOUTUBE_DOWNLOADED_FLAG + webm_file + ".mp3"

                    # Сохранение файла как .mp3
                    audio.export(new_file_name.replace(".webm", ""), format="mp3")

                    # Вывод логирования и удаление .webm
                    if self.logging_mode: logging.info("Конвертация / удаление .webm файла, прошла успешно и сохранен в %s", new_file_name)
                    os.remove(webm_file_path)
            
            # Если треки в папке не найдены
            else:
                if self.logging_mode: logging.info(F"Не найдено треков в папке: {self.directory_path}")
                return False

            if self.logging_mode: logging.info(F"Все треки {len(tracks_list)} из плейлиста успешно загрузились!")
            return True

        # Вывод логирования об ошибке при конвертации
        except Exception as error:
            logging.error(F"Ошибка при конвертации, по причине: {self.directory_path}, {error}")
            return False

    # Точка входа в сервис по получении, установке и конвертации треков
    def main(self, link: str = None, rending_count: int = 5, rending_timeout: int = 60) -> bool:
        """Точка входа в сервис по получении, установке и конвертации треков

        :param: `link | STR` - Ссылка на трек или плейлист
        :param: `rending_count | INT` - Количество повторных попыток получения ссылок-треков из плейлист (def. 5)
        :param: `rending_timeout | INT` - Время ожидания конца рендинга страницы во избежания случайных ошибок на (def. 60).\n
        :param: `track_name | STR` - Название трека если его нету в YouTube (def. Неизвестный исполнитель)
        :return: bool
        """
        
        # 1. Проверка что ссылка введет на плейлист
        # 2. Проверяет установлен ли FFmpeg на устройство
        if '/playlist' in link and self._check_ffmpeg_installed() and link != None:
            
            # Логирование
            if self.logging_mode: logging.info("Ссылка введет на плейлист:%s ", link)

            # Получение всех ссылок на песни из плейлиста YouTube НЕ ТРЕБУЕТЬСЯ (YT-DLP САМ ВСЕ ДЕЛАЕТ)
            # playlist_links: list =  #self._get_playlist(link=link, rending_count=rending_count, rending_timeout=rending_timeout)
            
            # Скачиваем песни из плейлиста
            self._download_youtube_audio(link=link)
            
            # Конвертируем трек (.wbem -> .mp3)
            self._conver_webm_to_mp3()
            

        if link != None:
            # Логирование
            if self.logging_mode: logging.info("Ссылка введет на трек:%s ", link)
            
            # Удаление не нужных символов и получение ID видео
            if '&list' in link: link = link.split("&")[0].split("=")[-1]
            else: link = link.split("=")[-1]

            # Скачивание конвертация (.webm -> .mp3) треков 
            self._download_youtube_audio(link=link)
            self._conver_webm_to_mp3()

        else: 
            if self.logging_mode: logging.info("Передайте ссылку для скачивания!")


if __name__ == "__main__":
    youtube_dl=YouTubeDL(logging_mode=True, directory_path="./static/music/")
    youtube_dl.main(link="https://youtube.com/playlist?list=PLyxTxA__Xf9h4OiMCQs45fdk4VvMobQxh&si=Eyt2LOyhsga9kLXo")

