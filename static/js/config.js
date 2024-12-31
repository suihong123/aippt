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
    ERROR_MESSAGES: {
        AUTH_FAILED: '认证失败，请重新登录',
        NETWORK_ERROR: '网络错误，请检查连接',
        INVALID_CODE: '无效的激活码',
        LOGIN_FAILED: '登录失败，请检查账号密码',
        REGISTER_FAILED: '注册失败，请稍后重试'
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