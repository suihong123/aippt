const CACHE_NAME = 'aippt-v1';
const ASSETS = [
    '/',
    '/index.html',
    '/login.html',
    '/register.html',
    '/activate.html',
    '/static/css/main.css',
    '/static/css/auth.css',
    '/static/js/main.js',
    '/static/js/auth.js',
    '/static/js/api.js',
    '/static/js/utils.js',
    '/static/js/security.js',
    '/favicon.ico',
    '/icon.png'
];

// 安装 Service Worker
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(ASSETS))
    );
});

// 激活新版本
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys => Promise.all(
            keys.map(key => {
                if (key !== CACHE_NAME) {
                    return caches.delete(key);
                }
            })
        ))
    );
});

// 处理请求
self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
}); 