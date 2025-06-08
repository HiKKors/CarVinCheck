document.addEventListener('DOMContentLoaded', function() {
    // Переключение между формами
    const switcherLinks = document.querySelectorAll('.form-switcher a');
    
    switcherLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Удаляем активный класс у всех кнопок и форм
            document.querySelectorAll('.form-switcher a').forEach(btn => btn.classList.remove('active'));
            document.querySelectorAll('.form-container').forEach(form => form.classList.remove('active'));
            
            // Добавляем активный класс текущей кнопке и соответствующей форме
            this.classList.add('active');
            const formType = this.textContent.includes('VIN') ? 'vin' : 'body';
            document.getElementById(`${formType}-form`).classList.add('active');
        });
    });
});