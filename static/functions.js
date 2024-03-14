// JS СКРИПТЫ РАБОТЫ ФРОНТЕНДА(20% animation, 80% audio)
const audioPlayers = document.querySelectorAll('.audioPlayer');
let currentTrackIndex = 0;


// Функция показа поле ввода ссылки
function showSearchBlock() {
    var searchInput = document.querySelector(".search-input");
    var statusText = document.querySelector(".status-text");
    var statusTextIcon = document.getElementById("status-text-icon");
    var statusLoading = document.getElementById("status-loading");
    
    // Проверка что поле ввода содержится ссылка на видео (YouTube)
    statusText.innerText = "Укажите ссылку на плейлист или трек для загрузки с YouTube."
    if (searchInput.value) {
        
        // Если все ОК то цвет текста остается белым и img будет другим
        if (
            // Фильтрирует ссылку пользователя чтобы избежать ошибки
            searchInput.value !== "" &&
            searchInput.value.includes("https://") &&(
                (searchInput.value.includes("/playlist") && !searchInput.value.includes("/watch")) ||
                (!searchInput.value.includes("/playlist") && searchInput.value.includes("/watch"))
            ) && searchInput.value.length > 32) {
            

            // Если ссылка введет на плейлист
            if (searchInput.value.includes('/playlist')) {
                statusText.innerText = "Плейлист загружается!. это может занять некоторое время, пожалуйста, подождите..";}
            
            // Если ссылка введет на трек
            if (!searchInput.value.includes('/playlist')) {
                statusText.innerText = "Трек загружается!. Пожалуйста, подождите..";}

            statusTextIcon.style.display = "none";
            statusLoading.style.display = "block";
            searchInput.disabled = true;
            statusText.style.color = "rgba(255, 255, 255, 0.72)";
            
            var modificate_input = encodeURIComponent(searchInput.value); //.replace(/\//g, "#");
            console.log('/search/?link=' + modificate_input)
            window.location.href = '/search/?link=' + modificate_input;

            // https://www.youtube.com/watch?v=JOnEn5Asc6E
        
            console.log("REQUEST YES");
        
        
        // Если была ошибка в ссылке то цвет текста станет крассным и img будет другим
        } else {
            statusText.innerText = "Ссылка должна перенаправлять на плейлист или на трек с YouTube!!.";
            statusTextIcon.src = "/static/icon/status-false.svg";
            statusText.style.color = "rgb(247, 169, 169)";

            console.log("REQUEST NOT");
        }
    }

    // Скрытие кнопок и показ 
    // document.querySelector(".stop-forward").style.display = "none";
    document.querySelector(".music-count").style.display = "none";
    document.querySelector(".mix-forward").style.display = "none";
    document.querySelector(".update").style.display = "none";
    
    // ---------------–-----
    document.querySelector(".close-forward").style.display = "block";
    document.querySelector(".search-input").style.display = "block";
    document.querySelector(".line").style.display = "block";}

// Функция скрытия поле ввода ссылки
function hideSearchBlock() {
    var statusTextIcon = document.getElementById("status-text-icon");
    var statusText = document.querySelector(".status-text");
    if (statusText.style.color === "rgb(247, 169, 169)") {
        statusText.innerText = "Песни автоматически переключаются и загружаются через YouTube."
        statusText.style.color = "rgba(255, 255, 255, 0.72)";
        statusTextIcon.src = "/static/icon/status-true.svg";
    }

    // Очищаем поле ввода ссылки при закрытии
    document.querySelector(".search-input").value = "";

    // Скрытие кнопок и показ 
    // document.querySelector(".stop-forward").style.display = "block";
    document.querySelector(".music-count").style.display = "flex";
    document.querySelector(".mix-forward").style.display = "block";
    document.querySelector(".update").style.display = "block";

    // ---------------–-----
    document.querySelector(".close-forward").style.display = "none";
    document.querySelector(".search-input").style.display = "none";
    document.querySelector(".line").style.display = "none";}

// Анимация при удалении файла
async function deleteFile(element, fileName) {
    element.style.display = "none";
    element.nextElementSibling.style.display = "block";
    
    // Удаление трека (отправка запроса GET)
    window.location.href = '/delete/' + fileName;}

// Функция для загрузки аудиофайла при запуске трека
function loadAudio(event) {
    var audio = event.target;
    var source = audio.querySelector('source');
    if (!source.src) {
        source.src = audio.dataset.src;
        
        // Загружаем аудиофайл
        audio.load(); 
        
        // Автоматически запускаем его
        audio.play();}}

// Добавляем обработчик события для каждого аудио-элемента
audioPlayers.forEach(function(player) {
    player.addEventListener('play', loadAudio);});

// Переключение трека по окончании настоящего трека
document.addEventListener('DOMContentLoaded', function() {
    var audioPlayers = document.querySelectorAll('.audioPlayer');
    
    audioPlayers.forEach(function(player) {
        player.addEventListener('ended', function() {
            var nextPlayer = player.closest('.playeer-item').nextElementSibling.querySelector('.audioPlayer');
            if (nextPlayer) {
                nextPlayer.play();}});});});



