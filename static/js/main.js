// 复制之前提供的JavaScript代码到这里
async function loginUser() {
    const phone = document.getElementById('phone').value;
    const nickname = document.getElementById('nickname').value;
    // ... 其余JavaScript代码 ...
}

// 用户信息处理
async function getUserInfo() {
    try {
        const response = await fetch('/api/user-info');
        const data = await response.json();
        if (data.success) {
            document.getElementById('username').textContent = data.username;
        }
    } catch (err) {
        console.error('获取用户信息失败');
    }
}