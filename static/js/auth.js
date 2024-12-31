// 处理登录和注册的通用函数
async function handleAuth(formData, endpoint) {
    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        return data;
    } catch (err) {
        console.error('认证失败:', err);
        return { success: false, message: '请求失败，请重试' };
    }
}

// 表单验证
function validateForm(formData) {
    const password = formData.get('password');
    const confirmPassword = formData.get('confirm_password');
    
    if (confirmPassword && password !== confirmPassword) {
        return { valid: false, message: '两次输入的密码不一致' };
    }
    
    return { valid: true };
}

// 处理登录
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/api/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                phone: formData.get('phone'),
                password: formData.get('password')
            })
        });
        
        const data = await response.json();
        if (data.success) {
            localStorage.setItem('userToken', data.token);
            window.location.href = 'index.html';
        } else {
            // 显示具体的错误信息
            alert(data.message || '登录失败，请检查账号密码');
        }
    } catch (err) {
        console.error('登录失败:', err);
        alert('登录失败，请检查网络连接');
    }
});

// 处理注册
if (document.getElementById('registerForm')) {
    document.getElementById('registerForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        
        // 验证密码
        if (formData.get('password') !== formData.get('confirm_password')) {
            alert('两次输入的密码不一致');
            return;
        }
        
        try {
            const response = await fetch('https://api.docmee.cn/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    phone: formData.get('phone'),
                    password: formData.get('password')
                })
            });
            
            const data = await response.json();
            if (data.success) {
                alert('注册成功！请登录');
                window.location.href = 'login.html';
            } else {
                alert(data.message);
            }
        } catch (err) {
            console.error('注册失败:', err);
            alert('注册失败，请重试');
        }
    });
} 