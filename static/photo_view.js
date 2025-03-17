let scale = 1;
let translateX = 0, translateY = 0;
let isDragging = false;
let startX, startY;

const modalImg = document.getElementById("fullscreenImg");
const modal = document.getElementById("fullscreenModal");

function openFullscreen(imgElement) {
    modalImg.src = imgElement.src;
    modal.classList.add("show");
    document.body.classList.add("modal-open");

    // Сбрасываем трансформации
    scale = 1;
    translateX = 0;
    translateY = 0;
    updateTransform();
}

function closeFullscreen() {
    modal.classList.remove("show");
    document.body.classList.remove("modal-open");
}

function updateTransform() {
    modalImg.style.transform = `translate(${translateX}px, ${translateY}px) scale(${scale})`;
}

/* Зум колесиком мыши */
modalImg.addEventListener("wheel", function (event) {
    event.preventDefault();
    let newScale = scale + event.deltaY * -0.01;
    scale = Math.min(Math.max(1, newScale), 3); // Ограничение зума от 1 до 3
    updateTransform();
});

/* Перемещение при нажатой кнопке мыши */
modalImg.addEventListener("mousedown", (event) => {
    event.preventDefault(); // Предотвращаем действие ссылки
    if (scale > 1) { // Перемещение только при зуме
        isDragging = true;
        startX = event.clientX - translateX;
        startY = event.clientY - translateY;
        modalImg.style.cursor = "grabbing"; // Меняем курсор
    }
});

document.addEventListener("mousemove", (event) => {
    if (isDragging) {
        translateX = event.clientX - startX;
        translateY = event.clientY - startY;
        updateTransform();
    }
});

document.addEventListener("mouseup", () => {
    isDragging = false; // Выход из состояния перетаскивания
    modalImg.style.cursor = "grab"; // Возвращаем курсор
});

/* Предотвращаем закрытие модального окна при клике на изображение */
modalImg.addEventListener("click", (event) => {
    event.stopPropagation(); // Останавливаем всплытие события
});

/* Поддержка мобильных устройств */
modalImg.addEventListener("touchstart", (event) => {
    event.preventDefault(); // Предотвращаем действие ссылки
    if (scale > 1 && event.touches.length === 1) {
        isDragging = true;
        const touch = event.touches[0];
        startX = touch.clientX - translateX;
        startY = touch.clientY - translateY;
    }
});

modalImg.addEventListener("touchmove", (event) => {
    if (isDragging && event.touches.length === 1) {
        const touch = event.touches[0];
        translateX = touch.clientX - startX;
        translateY = touch.clientY - startY;
        updateTransform();
    }
});

modalImg.addEventListener("touchend", () => {
    isDragging = false;
});
