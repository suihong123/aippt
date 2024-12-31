// 用户仪表板功能
class UserDashboard {
    constructor() {
        this.loadUserStats();
        this.loadHistory();
    }

    async loadUserStats() {
        try {
            const response = await api.user.getUsageStats();
            if (response.success) {
                document.getElementById('remainingUses').textContent = response.data.remaining_uses;
                document.getElementById('expireTime').textContent = utils.formatDate(response.data.expire_time);
                document.getElementById('usedCount').textContent = response.data.used_count;
            }
        } catch (error) {
            utils.handleError(error);
        }
    }

    async loadHistory() {
        try {
            const response = await api.user.getHistory();
            if (response.success) {
                const historyHtml = response.data.map(item => `
                    <div class="history-item">
                        <div class="history-time">${utils.formatDate(item.create_time)}</div>
                        <div class="history-title">${item.title}</div>
                        <div class="history-status">${item.status}</div>
                    </div>
                `).join('');
                document.getElementById('historyList').innerHTML = historyHtml;
            }
        } catch (error) {
            utils.handleError(error);
        }
    }
} 