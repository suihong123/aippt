from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

class TaskScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.setup_tasks()
        
    def setup_tasks(self):
        # 每天凌晨备份数据
        self.scheduler.add_job(
            self.backup_data,
            'cron',
            hour=0,
            minute=0
        )
        
        # 每小时清理过期session
        self.scheduler.add_job(
            self.cleanup_sessions,
            'interval',
            hours=1
        )
        
        # 每5分钟检查系统状态
        self.scheduler.add_job(
            self.check_system_status,
            'interval',
            minutes=5
        )
    
    def start(self):
        self.scheduler.start()
    
    def stop(self):
        self.scheduler.shutdown() 

    def backup_data(self):
        """数据备份任务"""
        try:
            from utils.backup import RedisBackup
            backup = RedisBackup(redis_client)
            backup_file = backup.backup()
            self.logger.info(f"数据备份成功: {backup_file}")
        except Exception as e:
            self.logger.error(f"数据备份失败: {str(e)}")

    def cleanup_sessions(self):
        """清理过期会话"""
        try:
            current_time = datetime.now().timestamp()
            for key in redis_client.scan_iter("session:*"):
                expire_time = float(redis_client.hget(key, 'expire_time') or 0)
                if expire_time < current_time:
                    redis_client.delete(key)
            self.logger.info("清理过期会话完成")
        except Exception as e:
            self.logger.error(f"清理会话失败: {str(e)}") 