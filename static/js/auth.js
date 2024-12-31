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
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const formData = new FormData(e.target);
            
            try {
                console.log('Login attempt:', {
                    phone: formData.get('phone'),
                    url: `${CONFIG.API_BASE_URL}/api/login`
                });

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
                
                console.log('Raw response:', response);
                const data = await response.json();
                console.log('Login response data:', data);
                
                if (data.success) {
                    if (!data.token) {
                        throw new Error('No token received');
                    }
                    
                    localStorage.setItem('userToken', data.token);
                    console.log('Token saved, redirecting...');
                    
                    window.location.href = `${CONFIG.BASE_URL}/index.html`;
                } else {
                    const errorMessage = document.getElementById('errorMessage');
                    errorMessage.textContent = data.message || '登录失败，请检查账号密码';
                    errorMessage.style.display = 'block';
                }
            } catch (err) {
                console.error('Login error:', err);
                const errorMessage = document.getElementById('errorMessage');
                errorMessage.textContent = '登录失败，请检查网络连接';
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
            
            // 验证密码
            if (formData.get('password') !== formData.get('confirm_password')) {
                const errorMessage = document.getElementById('errorMessage');
                errorMessage.textContent = '两次输入的密码不一致';
                errorMessage.style.display = 'block';
                return;
            }

            const phone = formData.get('phone');
            const password = formData.get('password');
            
            try {
                console.log('Attempting registration...', { phone });
                
                // 注册请求
                const registerResponse = await fetch(`${CONFIG.API_BASE_URL}/api/register`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        phone,
                        password
                    })
                });
                
                const registerData = await registerResponse.json();
                console.log('Register response:', registerData);
                
                if (registerData.success) {
                    // 注册成功后立即登录
                    console.log('Registration successful, attempting auto-login...');
                    
                    const loginResponse = await fetch(`${CONFIG.API_BASE_URL}/api/login`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            phone,
                            password
                        })
                    });
                    
                    const loginData = await loginResponse.json();
                    console.log('Auto-login response:', loginData);
                    
                    if (loginData.success) {
                        // 保存登录信息
                        localStorage.setItem('userToken', loginData.token);
                        localStorage.setItem('userPhone', phone);
                        console.log('Auto-login successful, redirecting...');
                        
                        // 跳转到主页
                        window.location.href = `${CONFIG.BASE_URL}/index.html`;
                    } else {
                        console.error('Auto-login failed:', loginData.message);
                        const errorMessage = document.getElementById('errorMessage');
                        errorMessage.textContent = '注册成功但自动登录失败，请手动登录';
                        errorMessage.style.display = 'block';
                        
                        // 延迟2秒后跳转到登录页
                        setTimeout(() => {
                            window.location.href = `${CONFIG.BASE_URL}/login.html`;
                        }, 2000);
                    }
                } else {
                    console.error('Registration failed:', registerData.message);
                    const errorMessage = document.getElementById('errorMessage');
                    errorMessage.textContent = registerData.message || '注册失败，请重试';
                    errorMessage.style.display = 'block';
                }
            } catch (err) {
                console.error('Registration error:', err);
                const errorMessage = document.getElementById('errorMessage');
                errorMessage.textContent = '注册失败，请检查网络连接';
                errorMessage.style.display = 'block';
            }
        });
    }
}); 