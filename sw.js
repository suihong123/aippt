const CACHE_NAME = 'aippt-v1';
const ASSETS = [
    './',
    './index.html',
    './login.html',
    './register.html',
    './activate.html',
    './static/css/main.css',
    './static/css/auth.css',
    './static/js/main.js',
    './static/js/auth.js',
    './static/js/api.js',
    './static/js/utils.js',
    './static/js/security.js',
    './favicon.ico',
    './icon.png'
];

// 安装 Service Worker
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(ASSETS))
    );
});

// 激活Service Worker
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// 处理请求
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // 如果在缓存中找到响应，则返回缓存的响应
        if (response) {
          return response;
        }

        // 克隆请求，因为请求是一个流，只能使用一次
        const fetchRequest = event.request.clone();

        return fetch(fetchRequest).then(
          (response) => {
            // 检查是否收到有效的响应
            if(!response || response.status !== 200 || response.type !== 'basic') {
              return response;
            }

            // 克隆响应，因为响应是一个流，只能使用一次
            const responseToCache = response.clone();

            caches.open(CACHE_NAME)
              .then((cache) => {
                // 不缓存API请求
                if (!event.request.url.includes('/api/')) {
                  cache.put(event.request, responseToCache);
                }
              });

            return response;
          }
        );
      })
  );
});

// 处理推送通知
self.addEventListener('push', (event) => {
  const options = {
    body: event.data.text(),
    icon: '/icon.png',
    badge: '/icon.png'
  };

  event.waitUntil(
    self.registration.showNotification('AIPPT生成器', options)
  );
});

// 处理通知点击
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  event.waitUntil(
    clients.openWindow('/')
  );
}); 