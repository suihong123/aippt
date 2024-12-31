// 全局配置
window.CONFIG = {
    API_BASE_URL: 'https://api.docmee.cn',
    BASE_URL: '/aippt',
    ASSETS_URL: './static',
    SDK_URL: './wenduoduo',
    DEFAULT_TOKEN: 'ak_u_loy5FsT35FvozDKZ',
    LANG: 'zh',
    MODE: 'light',
    ENDPOINTS: {
        LOGIN: '/api/login',
        REGISTER: '/api/register',
        ACTIVATE: '/api/activate',
        USER_STATUS: '/api/user/status'
    },
    API_HEADERS: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Origin': 'https://suihong123.github.io'
    }
};

// 添加调试模式
CONFIG.DEBUG = true;

// 添加日志函数
CONFIG.log = function(message, data) {
    if (CONFIG.DEBUG) {
        console.log(`[AIPPT] ${message}`, data || '');
    }
}; 