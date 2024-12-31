// 处理登录和注册的通用函数
// async function handleAuth(formData, endpoint) {
//     try {
//         const response = await fetch(endpoint, {
//             method: 'POST',
//             body: formData
//         });
//         const data = await response.json();
//         return data;
//     } catch (err) {
//         console.error('认证失败:', err);
//         return { success: false, message: '请求失败，请重试' };
//     }
// }

// 表单验证
// function validateForm(formData) {
//     const password = formData.get('password');
//     const confirmPassword = formData.get('confirm_password');
//     
//     if (confirmPassword && password !== confirmPassword) {
//         return { valid: false, message: '两次输入的密码不一致' };
//     }
//     
//     return { valid: true };
// }

// 处理登录
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const errorMessage = document.getElementById('errorMessage');
            
            // 验证手机号
            const phone = formData.get('phone');
            if (!/^1[3-9]\d{9}$/.test(phone)) {
                errorMessage.textContent = '请输入正确的手机号';
                errorMessage.style.display = 'block';
                return;
            }

            try {
                console.log('Login attempt:', { phone });

                const response = await fetch(`${CONFIG.API_BASE_URL}/api/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        phone: phone,
                        password: formData.get('password')
                    })
                });
                
                const data = await response.json();
                console.log('Login response:', data);
                
                if (data.success && data.token) {
                    // 保存token
                    localStorage.setItem('userToken', data.token);
                    localStorage.setItem('userPhone', phone);
                    
                    // 登录成功提示
                    errorMessage.style.color = '#52c41a';
                    errorMessage.textContent = '登录成功！正在跳转...';
                    errorMessage.style.display = 'block';
                    
                    // 延迟跳转
                    setTimeout(() => {
                        window.location.href = `${CONFIG.BASE_URL}/index.html`;
                    }, 1000);
                } else {
                    errorMessage.style.color = '#ff4444';
                    errorMessage.textContent = data.message || CONFIG.ERROR_MESSAGES.LOGIN_FAILED;
                    errorMessage.style.display = 'block';
                }
            } catch (err) {
                console.error('Login error:', err);
                errorMessage.style.color = '#ff4444';
                errorMessage.textContent = CONFIG.ERROR_MESSAGES.NETWORK_ERROR;
                errorMessage.style.display = 'block';
            }
        });
    }
});

// 处理注册
document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            const errorMessage = document.getElementById('errorMessage');
            
            // 验证手机号
            const phone = formData.get('phone');
            if (!/^1[3-9]\d{9}$/.test(phone)) {
                errorMessage.textContent = '请输入正确的手机号';
                errorMessage.style.display = 'block';
                return;
            }

            // 验证密码强度
            const password = formData.get('password');
            if (password.length < 6) {
                errorMessage.textContent = '密码长度至少6位';
                errorMessage.style.display = 'block';
                return;
            }
            
            // 验证两次密码
            if (password !== formData.get('confirm_password')) {
                errorMessage.textContent = '两次输入的密码不一致';
                errorMessage.style.display = 'block';
                return;
            }

            try {
                console.log('Attempting registration...', { phone });
                
                // 注册请求
                const response = await fetch(`${CONFIG.API_BASE_URL}/api/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        phone: phone,
                        password: password
                    })
                });

                const data = await response.json();
                console.log('Register response:', data);
                
                if (data.success) {
                    // 注册成功，显示提示并延迟跳转
                    errorMessage.style.color = '#52c41a';
                    errorMessage.textContent = '注册成功！正在跳转到登录页面...';
                    errorMessage.style.display = 'block';
                    
                    setTimeout(() => {
                        window.location.href = `${CONFIG.BASE_URL}/login.html`;
                    }, 2000);
                } else {
                    errorMessage.style.color = '#ff4444';
                    errorMessage.textContent = data.message || CONFIG.ERROR_MESSAGES.REGISTER_FAILED;
                    errorMessage.style.display = 'block';
                }
            } catch (err) {
                console.error('Registration error:', err);
                errorMessage.style.color = '#ff4444';
                errorMessage.textContent = CONFIG.ERROR_MESSAGES.NETWORK_ERROR;
                errorMessage.style.display = 'block';
            }
        });
    }
}); 