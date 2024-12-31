import logging
from logging.handlers import RotatingFileHandler
import os
import json
from datetime import datetime
from flask import request

class Logger:
    def __init__(self, name, log_dir='logs'):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # 创建日志目录
        os.makedirs(log_dir, exist_ok=True)
        
        # 添加文件处理器
        file_handler = RotatingFileHandler(
            f'{log_dir}/{name}.log',
            maxBytes=1024 * 1024,  # 1MB
            backupCount=5
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(file_handler)
        
        # 添加控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(console_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def log_user_action(self, user_id, action, details=None):
        """记录用户操作"""
        log_data = {
            'user_id': user_id,
            'action': action,
            'details': details,
            'timestamp': datetime.now().timestamp(),
            'ip': request.remote_addr
        }
        
        # 存储到Redis
        redis_client.lpush('user_actions', json.dumps(log_data))
        # 同时写入日志文件
        self.info(f"User Action: {json.dumps(log_data)}") 