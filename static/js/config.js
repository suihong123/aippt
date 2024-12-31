// 全局配置
const CONFIG = {
    API_BASE_URL: 'https://api.docmee.cn',
    BASE_URL: '/aippt',
    ASSETS_URL: './static',
    SDK_URL: './wenduoduo',
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
        REGISTER_FAILED: '注册失败，请稍后重试',
        SERVER_ERROR: '服务器错误，请稍后重试',
        default: '操作失败，请重试'
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