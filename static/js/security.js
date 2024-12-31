const security = {
    // Token管理
    token: {
        get() {
            return localStorage.getItem('userToken');
        },
        set(token) {
            localStorage.setItem('userToken', token);
        },
        clear() {
            localStorage.removeItem('userToken');
        }
    },
    
    // 请求拦截器
    interceptors: {
        request(config) {
            const token = security.token.get();
            if (token) {
                config.headers = {
                    ...config.headers,
                    'Authorization': `Bearer ${token}`
                };
            }
            return config;
        },
        response(response) {
            if (response.status === 401) {
                security.token.clear();
                window.location.href = 'login.html';
            }
            return response;
        }
    }
}; 