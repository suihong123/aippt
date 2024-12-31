// 处理激活码
document.getElementById('activateForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const token = localStorage.getItem('userToken');
    
    try {
        const response = await fetch('https://api.docmee.cn/api/activate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                code: formData.get('code')
            })
        });
        
        const data = await response.json();
        if (data.success) {
            alert('激活成功！');
            window.location.href = 'index.html';
        } else {
            alert(data.message);
        }
    } catch (err) {
        console.error('激活失败:', err);
        alert('激活失败，请重试');
    }
});

// 加载用户信息
async function loadUserInfo() {
    const token = localStorage.getItem('userToken');
    try {
        const response = await fetch('https://api.docmee.cn/api/user/status', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('remainingUses').textContent = data.data.remaining_uses;
            document.getElementById('expireTime').textContent = data.data.expire_time;
        }
    } catch (err) {
        console.error('加载用户信息失败:', err);
    }
}

loadUserInfo(); 