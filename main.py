import mimetypes
import logging, os
from pathlib import Path
from quart import Quart, render_template, request, send_from_directory
from src.tools import ToolsTrack, YouTubeDL
from src.config import (
    MUSIC_PATH, STATUS_TEXT, 
    STATUS_YT, HOST, PORT, VERSION, console_banner)


app = Quart(__name__)

# Отключение логирования
# ------------------------------------------
logging.disable(logging.CRITICAL)
logging.getLogger("urllib3").propagate = False
logging.getLogger('quart.app').setLevel(logging.CRITICAL)
# ------------------------------------------

# Работа с файлвой системой
# ------------------------------------------
TOOLS = ToolsTrack(directory_path=MUSIC_PATH)

# Работа со сторонними модулям (YouTube)
YOUTUBE = YouTubeDL(directory_path=MUSIC_PATH)
# ------------------------------------------

# Данные о треках (РАЗМЕР) >
# TOOLS.get_tracks_data()[0]

# Данные о треках (КОЛИЧЕСТВО) >
# TOOLS.get_tracks_data()[1]

# ВРЕМЕННОЕ ХРАНИЛИЩЕ ВРЕМЕННЫХ ДАННЫХ (НЕ УДАЛЯТЬ | def search())
TEMP_VAR = "TEMP-VARIABLE"
# ------------------------------------------


# Маршрут для главной страницы
@app.route('/')
async def index():
    songs = TOOLS.get_tracks(user_agent=request.headers.get("User-Agent"))
    return await render_template('index.html', 
        songs=songs, status_text=STATUS_TEXT, 
        status_yt=STATUS_YT, music_count=TOOLS.get_tracks_data()[1],
        music_size=TOOLS.get_tracks_data()[0], version=VERSION)

# Маршрут для перемешивания треков
@app.route('/mix-track')
async def mix():
    songs = TOOLS.get_tracks(user_agent=request.headers.get("User-Agent"), mix=True)
    return await render_template('index.html', 
        songs=songs, status_text=STATUS_TEXT, 
        status_yt=STATUS_YT, music_count=TOOLS.get_tracks_data()[1],
        music_size=TOOLS.get_tracks_data()[0], version=VERSION)

# Изменения аккаунта
@app.route('/user/<path:account_name>')
async def account(account_name: str):
    music_path: str = F"{MUSIC_PATH}{account_name}/"

    # Создает директорию, если не существует
    if not Path(music_path).exists(): os.makedirs(music_path)

    TOOLS = ToolsTrack(directory_path=music_path)
    songs = TOOLS.get_tracks(user_agent=request.headers.get("User-Agent"))
    return await render_template('index.html', 
        songs=songs, status_text=STATUS_TEXT, 
        status_yt=STATUS_YT, music_count=TOOLS.get_tracks_data()[1],
        music_size=TOOLS.get_tracks_data()[0], version=VERSION)

# Выдача доступа к хранилищу
@app.route('/music/<path:filename>')
async def music(filename: str):
    # Определение MIME-типа
    mime_type, _ = mimetypes.guess_type(filename)
    
    # MIME-тип по умолчанию, если тип не распознан
    if mime_type is None: mime_type = 'application/octet-stream'  
    
    # Файл для передачи клиенту 
    response_file = await send_from_directory(directory=MUSIC_PATH, file_name=filename, mimetype=mime_type)
    
    # Кэширование на 1 день
    response_file.headers['Cache-Control'] = 'public, max-age=86400'  

    return response_file
    
# Поиск треков через YouTube
@app.route('/search/')
async def search():
    # Объявление использования глобальной переменной
    global TEMP_VAR  
    link: str = request.args.get("link")
    account_path = request.args.get('account')
    if account_path: account_path: str = F"{MUSIC_PATH}{account_path}"

    # Если ссылка уже была скачена то чтобы она не повторял скачивание
    if link == TEMP_VAR:
        songs = TOOLS.get_tracks(user_agent=request.headers.get("User-Agent"))
        return await render_template('index.html', 
            songs=songs, status_text=F"Треки ({TOOLS.count_new_tracks()}) уже установились.", version=VERSION, 
            status_yt=STATUS_YT, music_count=TOOLS.get_tracks_data()[1], music_size=TOOLS.get_tracks_data()[0])
    
    # Скачивание и сохранение трека из ссылки
    TEMP_VAR = link
    YOUTUBE.main(link=link, account_path=account_path)
    
    if account_path:
        songs = TOOLS.get_tracks(user_agent=request.headers.get("User-Agent"))
        return await render_template('index.html', 
            songs=songs, status_text=F"Треки ({TOOLS.count_new_tracks()}) установились успешно ({account_path})!!", version=VERSION, 
            status_yt=STATUS_YT, music_count=TOOLS.get_tracks_data()[1], music_size=TOOLS.get_tracks_data()[0])
    
    songs = TOOLS.get_tracks(user_agent=request.headers.get("User-Agent"))
    return await render_template('index.html', 
        songs=songs, status_text=F"Треки ({TOOLS.count_new_tracks()}) установились успешно!!", version=VERSION, 
        status_yt=STATUS_YT, music_count=TOOLS.get_tracks_data()[1], music_size=TOOLS.get_tracks_data()[0])

# Удаление трека с хранилище
@app.route('/delete/<path:filename>')
async def delete(filename: str):
    songs = TOOLS.remove_tack(filename=filename, user_agent=request.headers.get("User-Agent"))
    return await render_template('index.html', 
        songs=songs, status_text=F"Трек ({filename}) успешно удалён!", status_yt=STATUS_YT, version=VERSION,
        music_count=TOOLS.get_tracks_data()[1], music_size=TOOLS.get_tracks_data()[0])

# Показ баннера в консоль
console_banner(
    music_count = TOOLS.get_tracks_data()[1],
    music_size = TOOLS.get_tracks_data()[0])

# Точка входа
if __name__ == '__main__':
    app.run(host=HOST, port=PORT)

