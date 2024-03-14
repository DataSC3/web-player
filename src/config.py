# НАСТРОЙКИ
# Путь к хранилище треков 
MUSIC_PATH = "static/music/" 
if MUSIC_PATH[-1] != "/": MUSIC_PATH + "/"

# Настройки сети (Хост, Порт)
HOST, PORT = "localhost", 9000

# ------------------------------------------
# Путь к файлу где сохраняються результаты установок треков через YouTube
STATUS_COUNT_FILE = "src/.status_count.txt"

# Текст для FRONTEND (class="status-text")
STATUS_TEXT = "Песни автоматически переключаются и загружаются через YouTube."

# Текст для распознования песни что он загружен из YouTube для FRONTEND
STATUS_YT = " -YT9"
# ------------------------------------------
