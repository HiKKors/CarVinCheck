document.getElementById("car-form").addEventListener("submit", async function(event) {
    event.preventDefault(); // Отменяем стандартную отправку формы

    let submitBtn = document.getElementById("submit-btn");
    let loading = document.getElementById("loading");
    let carData = document.getElementById("car-data");
    let vinInput = document.getElementById("vin"); // Поле ввода VIN

    submitBtn.disabled = true; // Деактивируем кнопку
    loading.classList.remove("hidden"); // Показываем индикатор загрузки
    carData.classList.add("hidden"); // Скрываем старые данные

    try {
        let response = await fetch("/", {
            method: "POST",
            body: new FormData(document.getElementById("car-form")), // Отправка VIN
        });

        if (!response.ok) throw new Error("Ошибка при получении данных");

        let html = await response.text(); // Получаем HTML-код с сервера

        // Вставляем новую версию данных
        let parser = new DOMParser();
        let doc = parser.parseFromString(html, "text/html");
        let newCarData = doc.getElementById("car-data");

        if (newCarData) {
            carData.innerHTML = newCarData.innerHTML; // Обновляем только данные
            carData.classList.remove("hidden"); // Показываем данные
        }
    } catch (error) {
        alert("Ошибка загрузки данных: " + error.message);
    } finally {
        loading.classList.add("hidden"); // Скрываем индикатор загрузки
        submitBtn.disabled = false; // Активируем кнопку
    }
});