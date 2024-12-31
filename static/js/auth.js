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
        console.log('Login response:', data); // 调试日志
        
        if (data.success) {
            localStorage.setItem('userToken', data.token);
            // 使用 CONFIG.BASE_URL 构建完整路径
            window.location.href = `${CONFIG.BASE_URL}/index.html`;
        } else {
            const errorMessage = document.getElementById('errorMessage');
            errorMessage.textContent = data.message || '登录失败，请检查账号密码';
            errorMessage.style.display = 'block';
        }
    } catch (err) {
        console.error('登录失败:', err);
        const errorMessage = document.getElementById('errorMessage');
        errorMessage.textContent = '登录失败，请检查网络连接';
        errorMessage.style.display = 'block';
    }
});

// 处理注册
if (document.getElementById('registerForm')) {
    document.getElementById('registerForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        
        try {
            const registerResponse = await fetch(`${CONFIG.API_BASE_URL}/api/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    phone: formData.get('phone'),
                    password: formData.get('password')
                })
            });
            
            const registerData = await registerResponse.json();
            if (registerData.success) {
                // 注册成功后直接登录
                const loginResponse = await fetch(`${CONFIG.API_BASE_URL}/api/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        phone: formData.get('phone'),
                        password: formData.get('password')
                    })
                });
                
                const loginData = await loginResponse.json();
                if (loginData.success) {
                    localStorage.setItem('userToken', loginData.token);
                    // 使用 CONFIG.BASE_URL 构建完整路径
                    window.location.href = `${CONFIG.BASE_URL}/index.html`;
                } else {
                    alert('登录失败：' + (loginData.message || '请手动登录'));
                    window.location.href = `${CONFIG.BASE_URL}/login.html`;
                }
            } else {
                alert(registerData.message || '注册失败，请重试');
            }
        } catch (err) {
            console.error('注册失败:', err);
            alert('注册失败，请重试');
        }
    });
} 