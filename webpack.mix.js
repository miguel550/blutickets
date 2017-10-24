const mix = require('laravel-mix');

mix.styles(
    [
        'resources/css/app/global.css',
        'resources/css/app/accounts.css',
        'resources/css/app/tickets.css',
    ],
    'assets/css/app.css'
);

mix.styles(
    [
        'resources/css/vendor/custom-style.css',
        'resources/css/vendor/owl.carousel.css',
        'resources/css/vendor/responsive.css',
    ],
    'assets/css/vendor.css'
);

mix.babel(
    [
        'resources/js/vendor/jquery.easing.1.3.min.js',
        'resources/js/vendor/jquery.sticky.js',
        'resources/js/vendor/main.js',
        'resources/js/vendor/owl.carousel.min.js',
    ],
    'assets/js/vendor.js'
);

mix.babel(
    [
        'resources/js/app/functions.js',
        'resources/js/app/sales.js',
    ],
    'assets/js/app.js'
);