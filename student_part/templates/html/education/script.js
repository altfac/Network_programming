document.addEventListener('DOMContentLoaded', function() {
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');

    dropdownToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const dropdownContent = this.nextElementSibling;
            // Закрываем все остальные открытые dropdown
            document.querySelectorAll('.custom-dropdown-content.open').forEach(content => {
                if (content !== dropdownContent) {
                    content.classList.remove('open');
                }
            });
            dropdownContent.classList.toggle('open');
        });
    });

    // Закрываем dropdown при клике вне его
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.custom-dropdown')) {
            document.querySelectorAll('.custom-dropdown-content.open').forEach(content => {
                content.classList.remove('open');
            });
        }
    });
});