$(document).ready(function() {
    var body = $('body');

    // Check if a theme is saved in localStorage
    if (localStorage.getItem('theme')) {
        // Apply saved theme
        body.addClass(localStorage.getItem('theme'));
    } else {
        // Check user preference in OS/user-agent
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            body.addClass('dark-mode');
            localStorage.setItem('theme', 'dark-mode');
        } else {
            body.addClass('light-mode');
            localStorage.setItem('theme', 'light-mode');
        }
    }

    $('#darkModeToggle').click(function() {
        // Theme switching code
        if (body.hasClass('light-mode')) {
            body.removeClass('light-mode');
            body.addClass('dark-mode');
            localStorage.setItem('theme', 'dark-mode');
        } else if (body.hasClass('dark-mode')) {
            body.removeClass('dark-mode');
            body.addClass('light-mode');
            localStorage.setItem('theme', 'light-mode');
        }
    });

    $('.slider').owlCarousel({
        loop: true,
        margin: 20,
        responsiveClass: true,
        responsive: {
            0: {
                items: 1,
                nav: false,
                autoplay: true,
            },
            600: {
                items: 3,
                nav: true,
                autoplay: true,
            },
            1000: {
                items: 5,
                nav: true,
                loop: true,
                autoplay: true,
            }
        }
    });
});