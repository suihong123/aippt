import json
import os
from datetime import datetime
import redis
import schedule
import time

class RedisBackup:
    def __init__(self, redis_client, backup_dir='backups'):
        self.redis_client = redis_client
        self.backup_dir = backup_dir
        os.makedirs(backup_dir, exist_ok=True)

    def backup(self):
        """执行备份"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'{self.backup_dir}/backup_{timestamp}.json'
        
        # 获取所有键
        data = {}
        for key in self.redis_client.scan_iter("*"):
            key_type = self.redis_client.type(key)
            if key_type == 'hash':
                data[key] = {
                    'type': 'hash',
                    'value': self.redis_client.hgetall(key)
                }
            elif key_type == 'string':
                data[key] = {
                    'type': 'string',
                    'value': self.redis_client.get(key)
                }
        
        # 写入文件
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # 只保留最近7天的备份
        self._cleanup_old_backups()
        
        return backup_file

    def _cleanup_old_backups(self, keep_days=7):
        """清理旧备份"""
        for file in os.listdir(self.backup_dir):
            file_path = os.path.join(self.backup_dir, file)
            if (datetime.now() - datetime.fromtimestamp(os.path.getctime(file_path))).days > keep_days:
                os.remove(file_path)

    def restore(self, backup_file):
        """从备份恢复"""
        with open(backup_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        for key, item in data.items():
            if item['type'] == 'hash':
                self.redis_client.hmset(key, item['value'])
            elif item['type'] == 'string':
                self.redis_client.set(key, item['value']) 