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
    document.querySelector(".button-description").style.width = "0%";
    document.querySelector(".button-description").style.visibility = "hidden";
    document.querySelector(".button-description").style.fontSize = "0%";
    
    
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
            
            //.replace(/\//g, "#");
            var modificate_input = encodeURIComponent(searchInput.value); 
            const currentPath = window.location.pathname || '';
            
            if (currentPath.includes('/user/')) {
                const userName = currentPath.split('/user/')[1].split('/')[0];
                window.location.href = '/search/?link=' + modificate_input + '&account=' + `${userName}/`;}
            
            else {window.location.href = '/search/?link=' + modificate_input;}
        
        // Если была ошибка в ссылке то цвет текста станет крассным и img будет другим
        } else {
            statusText.innerText = "Ссылка должна перенаправлять на плейлист или на трек с YouTube!!.";
            statusTextIcon.src = "/static/icon/status-false.svg";
            statusText.style.color = "rgb(247, 169, 169)";

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
    document.querySelector(".button-description").style.width = "100%";
    document.querySelector(".button-description").style.visibility = "visible";
    document.querySelector(".button-description").style.fontSize = "90%";


    var statusText = document.querySelector(".status-text");
    if (statusText.style.color === "rgb(247, 169, 169)") {
        statusText.innerText = "Песни автоматически переключаются и загружаются через YouTube."
        statusText.style.color = "rgba(255, 255, 255, 0.72)";
        statusTextIcon.src = "/static/icon/status-true.svg";}

    // Очищаем поле ввода ссылки при закрытии
    document.querySelector(".search-input").value = "";

    // Скрытие кнопок и показ 
    // document.querySelector(".stop-forward").style.display = "block";
    document.querySelector(".music-count").style.display = "flex";
    document.querySelector(".mix-forward").style.display = "flex";
    document.querySelector(".update").style.display = "flex";

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

// Функция для таймера
function timerHandler() {
    const loginElement = document.querySelector(".login");
    const timerElement = document.querySelector(".timer");

    
    // Показывает элемент, если он был скрыт
    if (timerElement.style.display === "none") {
    if (loginElement.style.display === "flex") {loginElement.style.display = "none";}
    timerElement.style.display = "flex";} 
    
    // Скрывает элемент, если он видим
    else {timerElement.style.display = "none";}
}

// Проверяем валидность введенных данных для таймера
function validateTimerInput(input) {
    // Удаляем все нецифровые символы
    input.value = input.value.replace(/\D/g, '');
    
    // Удаляем ведущие нули, если введено больше одной цифры
    if (input.value.length > 0 && input.value.startsWith('0')) {
        input.value = input.value.substring(1);
    }

    // Ограничиваем длину до двух символов
    if (input.value.length > 2) {
        input.value = input.value.slice(0, 2);
    }
}

// Запускаем таймер
function timerStart() {
    // Получаем значение из input
    var timerInput = document.querySelector(".timer-input");
    var timerStatus = document.querySelector(".timer-status");
    var statusText = document.querySelector(".status-text");
    
    // Преобразуем значение в минуты
    var minutes = parseInt(timerInput.value, 10);

    // Проверяем, что значение корректное
    if (isNaN(minutes) || minutes <= 0) {return;}

    // Преобразуем минуты в миллисекунды
    var milliseconds = minutes * 60 * 1000;

    // Меняем текст таймера
    timerStatus.style.color = "#28df28"
    timerStatus.textContent = "Запущен"
    timerInput.disabled = "true"
    statusText.innerHTML = "Таймер сна установлен на " + minutes + 
    " мин.  <span style='margin-left: 5px; cursor: pointer; color: orange;' onclick='location.reload();'>Отменить?.</span>"

    // Запускаем таймер
    setTimeout(function() {
        location.reload(); // Обновляем страницу, когда таймер истек
    }, milliseconds);
}

// Функция для авторизации
function loginHandler() {
    var loginStatus = document.querySelector(".login-status");
    const loginElement = document.querySelector(".login");
    const timerElement = document.querySelector(".timer");
    const currentPath = window.location.pathname || '';

    // Показывает элемент, если он был скрыт
    if (loginElement.style.display === "none") {
        if (timerElement.style.display === "flex") {timerElement.style.display = "none";}
        
        loginElement.style.display = "flex";
        if (currentPath.includes('/user/')) {
            const userName = currentPath.split('/user/')[1].split('/')[0];
            loginStatus.textContent = "Акк. " + userName
        }
            
    }
        
    // Скрывает элемент, если он видим
    else {loginElement.style.display = "none";}
}

// Вход в аккаунт
function loginUser() {
    // Регулярное выражение для проверки латинских букв и цифр
    var regex = /^[a-zA-Z0-9]+$/;
    var accountName = document.querySelector('.login-input').value;
    var loginStatus = document.querySelector(".login-status");

    // Проверка ввода
    if (accountName === "") {} 
    else if (regex.test(accountName)) {
        // Перенаправление на URL
        loginStatus.style.color = "#28df28"
        loginStatus.textContent = "Загрузка.."
        window.location.href = '/user/' + encodeURIComponent(accountName);
    } else {
        // Показать сообщение об ошибке для недопустимых символов
        loginStatus.style.color = "#e91e1e"
        loginStatus.textContent = "Ошибка в имени"
    }
}


// Добавляем обработчик события для каждого аудио-элемента
audioPlayers.forEach(function(player) {
    player.addEventListener('play', loadAudio);});

// Переключение трека по окончании настоящего трека
document.addEventListener('DOMContentLoaded', function() {
    var audioPlayers = document.querySelectorAll('.audioPlayer');
    
    audioPlayers.forEach(function(player) {
        player.addEventListener('ended', function() {
            var nextPlayer = player.closest('.playeer-item').nextElementSibling.querySelector('.audioPlayer');
            if (nextPlayer) {nextPlayer.play();}});});});

// Проверка бразуера
document.addEventListener("DOMContentLoaded", function() {
    const userAgent = navigator.userAgent.toLowerCase();
    const audioPlayers = document.querySelectorAll(".audioPlayer");

    if (userAgent.indexOf('chrome') > -1 && userAgent.indexOf('edg') === -1 && userAgent.indexOf('opr') === -1) {
        audioPlayers.forEach(function(audioPlayer) {audioPlayer.style.background = "rgb(241 243 244)";});}});

// Изменение аккаунта
document.addEventListener("DOMContentLoaded", function() {
    const audioPlayers = document.querySelectorAll('.audioPlayer');
    if (!audioPlayers.length) {return;}

    const currentPath = window.location.pathname || '';
    if (currentPath.includes('/user/')) {
        const userName = currentPath.split('/user/')[1].split('/')[0];
        audioPlayers.forEach(player => {
            const sources = player.querySelectorAll('source');
            sources.forEach(source => {
                let src = source.getAttribute('src') || '';
                if (src.includes('/music/')) {
                    // Обновляем src на основе userName
                    source.setAttribute('src', src.replace('/music/', `/music/${userName}/`));
                }
            });
        });
    }
});


// Блокировка кнопки "Смешать" для аккаунтов
document.addEventListener("DOMContentLoaded", function() {
    const currentPath = window.location.pathname || '';

    if (currentPath.includes('/user/')) {
        const mixForwardElements = document.querySelectorAll('.mix-forward');
        document.getElementById("exit").style.display = "block";

        mixForwardElements.forEach(element => {
            // Добавляем стиль opacity
            element.style.opacity = '0.3';
            
            // Удаляем атрибут onclick
            element.removeAttribute('onclick');
        });
    }
});
