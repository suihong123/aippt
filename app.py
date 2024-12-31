from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
import redis
from config import APP_CONFIG, DB_CONFIG, SECURITY_CONFIG, API_CONFIG
from utils.security import hash_password, verify_password
from utils.backup import RedisBackup
from middleware.rate_limit import RateLimit
from utils.upload import FileUpload
from middleware.security import SecurityMiddleware
from utils.monitor import PerformanceMonitor
import schedule

app = Flask(__name__)
app.secret_key = APP_CONFIG['SECRET_KEY']

# Redis连接
redis_client = redis.Redis(
    host=DB_CONFIG['host'],
    port=DB_CONFIG['port'],
    decode_responses=True
)

# 路由导入
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.main import main_bp

# 注册蓝图
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(main_bp)

# 初始化各个组件
rate_limiter = RateLimit(redis_client)
security = SecurityMiddleware()
monitor = PerformanceMonitor()
file_upload = FileUpload('uploads')

# 设置定时备份
backup = RedisBackup(redis_client)
schedule.every().day.at("00:00").do(backup.backup)

# 使用中间件
@app.before_request
@security.check_security
@monitor.monitor
def before_request():
    pass

# 在路由中使用
@app.route('/api/upload', methods=['POST'])
@rate_limiter.limit(requests=10, window=60)
def upload_file():
    file = request.files.get('file')
    path, error = file_upload.save_file(file)
    if error:
        return jsonify({'success': False, 'message': error})
    return jsonify({'success': True, 'path': path})

if __name__ == '__main__':
    app.run(debug=APP_CONFIG['DEBUG'])
