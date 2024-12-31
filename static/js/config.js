// 全局配置
const CONFIG = {
    API_BASE_URL: 'https://api.docmee.cn',
    ENDPOINTS: {
        LOGIN: '/api/login',
        REGISTER: '/api/register',
        ACTIVATE: '/api/activate',
        USER_STATUS: '/api/user/status'
    },
    ERROR_MESSAGES: {
        AUTH_FAILED: '认证失败，请重新登录',
        NETWORK_ERROR: '网络错误，请检查连接',
        INVALID_CODE: '无效的激活码'
    }
}; 