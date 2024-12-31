// 工具函数
const utils = {
    // 格式化日期
    formatDate(date) {
        if (typeof date === 'string' || typeof date === 'number') {
            date = new Date(date);
        }
        return date.toLocaleString('zh-CN', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    },
    
    // 格式化数字
    formatNumber(num) {
        return new Intl.NumberFormat('zh-CN').format(num);
    },
    
    // 验证输入
    validateInput(input, type) {
        const rules = {
            phone: /^1[3-9]\d{9}$/,
            password: /^.{6,20}$/,
            code: /^[A-Z0-9]{8,16}$/
        };
        return rules[type]?.test(input) || false;
    },
    
    // 错误处理
    handleError(error) {
        console.error('Error:', error);
        if (error.response) {
            alert(error.response.message || CONFIG.ERROR_MESSAGES.default);
        } else {
            alert(CONFIG.ERROR_MESSAGES.NETWORK_ERROR);
        }
    },
    
    // 处理API错误
    handleApiError(error, defaultMessage = '操作失败') {
        console.error('API Error:', error);
        if (error.response) {
            return error.response.message || CONFIG.ERROR_MESSAGES.default;
        }
        return defaultMessage;
    },
    
    // 显示错误消息
    showError(message) {
        alert(message);
    }
}; 