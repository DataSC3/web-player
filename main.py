from quart import Quart, render_template, request, send_from_directory
from src.tools import ToolsTrack, YouTubeDL
from src.config import (
    MUSIC_PATH, STATUS_TEXT, 
    STATUS_YT, HOST, PORT)


app = Quart(__name__)

# ------------------------------------------
# Работа с файовой системой
TOOLS = ToolsTrack(directory_path=MUSIC_PATH)

# Работа со сторонними модулям (YouTube)
YOUTUBE = YouTubeDL(directory_path=MUSIC_PATH)

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
        music_size=TOOLS.get_tracks_data()[0])

# Маршрут для перемешивания треков
@app.route('/mix-track')
async def mix():
    songs = TOOLS.get_tracks(user_agent=request.headers.get("User-Agent"), mix=True)
    return await render_template('index.html', 
        songs=songs, status_text=STATUS_TEXT, 
        status_yt=STATUS_YT, music_count=TOOLS.get_tracks_data()[1],
        music_size=TOOLS.get_tracks_data()[0])

# Выдача доступа к хранилищу
@app.route('/music/<path:filename>')
async def music(filename: str):
    return await send_from_directory(directory=MUSIC_PATH, file_name=filename)
    
# Выдача доступа к хранилищу
@app.route('/search/')
async def search():
    # Объявление использования глобальной переменной
    global TEMP_VAR  
    link = request.args.get('link') 

    # Если ссылка уже была скачена то чтобы она не повторял скачивание
    if link == TEMP_VAR:
        songs = TOOLS.get_tracks(user_agent=request.headers.get("User-Agent"))
        return await render_template('index.html', 
            songs=songs, status_text=F"Треки ({TOOLS.count_new_tracks()}) уже установились.", 
            status_yt=STATUS_YT, music_count=TOOLS.get_tracks_data()[1], music_size=TOOLS.get_tracks_data()[0])
    
    # Скачивание и сохранение трека из ссылки
    TEMP_VAR = link
    YOUTUBE.main(link=link)    
    songs = TOOLS.get_tracks(user_agent=request.headers.get("User-Agent"))
    return await render_template('index.html', 
        songs=songs, status_text=F"Треки ({TOOLS.count_new_tracks()}) установились успешно!!", 
        status_yt=STATUS_YT, music_count=TOOLS.get_tracks_data()[1], music_size=TOOLS.get_tracks_data()[0])

# Удаление трека с хранилище
@app.route('/delete/<path:filename>')
async def delete(filename: str):
    songs = TOOLS.remove_tack(filename=filename, user_agent=request.headers.get("User-Agent"))
    return await render_template('index.html', 
        songs=songs, status_text=F"Трек ({filename}) успешно удалён!", status_yt=STATUS_YT,
        music_count=TOOLS.get_tracks_data()[1], music_size=TOOLS.get_tracks_data()[0])

        

if __name__ == '__main__':
    app.run(debug=True, host=HOST, port=PORT)
