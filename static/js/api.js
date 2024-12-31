// API接口封装
const api = {
    // 用户相关
    user: {
        // 获取用户资料
        getProfile: async () => {
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/user/profile`, {
                headers: {
                    'Authorization': `Bearer ${security.token.get()}`
                }
            });
            return response.json();
        },

        // 更新用户资料
        updateProfile: async (data) => {
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/user/profile`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${security.token.get()}`
                },
                body: JSON.stringify(data)
            });
            return response.json();
        },

        // 获取使用统计
        getUsageStats: async () => {
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/user/stats`, {
                headers: {
                    'Authorization': `Bearer ${security.token.get()}`
                }
            });
            return response.json();
        },

        // 获取生成历史
        getHistory: async () => {
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/user/history`, {
                headers: {
                    'Authorization': `Bearer ${security.token.get()}`
                }
            });
            return response.json();
        }
    },
    
    // 激活码相关
    codes: {
        activate: async (code) => {
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/activate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('userToken')}`
                },
                body: JSON.stringify({ code })
            });
            return response.json();
        },
        
        check: async (code) => {
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/codes/check/${code}`);
            return response.json();
        },
        
        generate: async (options) => {
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/admin/codes/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('adminToken')}`
                },
                body: JSON.stringify(options)
            });
            return response.json();
        }
    },
    
    // 管理员相关
    admin: {
        // 生成激活码
        generateCodes: async (count, options) => {
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/admin/codes/generate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${security.token.get()}`
                },
                body: JSON.stringify({ count, ...options })
            });
            return response.json();
        },

        // 获取用户列表
        listUsers: async () => {
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/admin/users`, {
                headers: {
                    'Authorization': `Bearer ${security.token.get()}`
                }
            });
            return response.json();
        },

        // 获取系统统计
        getStats: async () => {
            const response = await fetch(`${CONFIG.API_BASE_URL}/api/admin/stats`, {
                headers: {
                    'Authorization': `Bearer ${security.token.get()}`
                }
            });
            return response.json();
        }
    }
}; 