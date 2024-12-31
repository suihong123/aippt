from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime
import random
import string
from config import SECURITY_CONFIG
import time
import psutil

admin_bp = Blueprint('admin', __name__)

def require_admin(f):
    """管理员验证装饰器"""
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return jsonify({
                'success': False,
                'message': '需要管理员权限'
            }), 403
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin')
@require_admin
def admin_page():
    return render_template('admin.html')

@admin_bp.route('/api/admin/generate-code', methods=['POST'])
@require_admin
def generate_code():
    data = request.json
    days = data.get('days', 30)
    uses = data.get('uses', 100)
    count = data.get('count', 1)
    
    if not all([isinstance(x, int) and x > 0 for x in [days, uses, count]]):
        return jsonify({
            'success': False,
            'message': '参数无效'
        })
    
    if count > 50:  # 限制批量生成数量
        return jsonify({
            'success': False,
            'message': '单次最多生成50个激活码'
        })
    
    generated_codes = []
    for _ in range(count):
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        
        # 存储激活码
        redis_client.hmset(f"code:{code}", {
            'code': code,
            'days': days,
            'uses': uses,
            'used': '0',
            'create_time': datetime.now().timestamp()
        })
        
        generated_codes.append({
            'code': code,
            'days': days,
            'uses': uses
        })
    
    return jsonify({
        'success': True,
        'data': generated_codes
    })

@admin_bp.route('/api/admin/codes-list')
@require_admin
def list_codes():
    # 获取所有激活码
    codes = []
    for key in redis_client.scan_iter("code:*"):
        code_data = redis_client.hgetall(key)
        if code_data:
            codes.append({
                'code': code_data['code'],
                'days': int(code_data['days']),
                'uses': int(code_data['uses']),
                'used': code_data['used'],
                'create_time': float(code_data['create_time']),
                'used_time': float(code_data['used_time']) if 'used_time' in code_data else None,
                'used_by': code_data.get('used_by')
            })
    
    # 按创建时间倒序排序
    codes.sort(key=lambda x: x['create_time'], reverse=True)
    
    return jsonify({
        'success': True,
        'data': codes
    })

@admin_bp.route('/api/admin/stats')
@require_admin
def get_stats():
    """获取使用统计"""
    total_codes = len(list(redis_client.scan_iter("code:*")))
    used_codes = len([1 for key in redis_client.scan_iter("code:*") 
                     if redis_client.hget(key, 'used') == '1'])
    
    return jsonify({
        'success': True,
        'data': {
            'total_codes': total_codes,
            'used_codes': used_codes,
            'usage_rate': round(used_codes / total_codes * 100, 2) if total_codes > 0 else 0
        }
    })

@admin_bp.route('/monitor')
@require_admin
def monitor_page():
    return render_template('monitor.html')

@admin_bp.route('/api/monitor/stats')
@require_admin
def get_monitor_stats():
    monitor = PerformanceMonitor()
    stats = monitor.get_system_stats()
    
    # 从Redis获取性能数据
    performance_data = redis_client.lrange('performance_logs', 0, -1)
    if performance_data:
        # 计算平均响应时间
        response_times = [float(log.split(':')[1]) for log in performance_data]
        avg_response_time = sum(response_times) / len(response_times)
        
        # 计算请求率（每分钟请求数）
        current_time = time.time()
        recent_requests = len([log for log in performance_data 
                            if current_time - float(log.split(':')[0]) <= 60])
    else:
        avg_response_time = 0
        recent_requests = 0
    
    return jsonify({
        'cpu_percent': stats['cpu_percent'],
        'memory_percent': stats['memory_percent'],
        'disk_usage': stats['disk_usage'],
        'avg_response_time': round(avg_response_time * 1000, 2),  # 转换为毫秒
        'request_rate': recent_requests,
        'memory_used': round(psutil.Process().memory_info().rss / 1024 / 1024, 2)  # MB
    })

@admin_bp.route('/api/admin/users')
@require_admin
def list_users():
    users = []
    for key in redis_client.scan_iter("user:*"):
        user_data = redis_client.hgetall(key)
        if user_data:
            users.append({
                'username': user_data['username'],
                'email': user_data['email'],
                'create_time': datetime.fromtimestamp(float(user_data['create_time'])),
                'last_login': datetime.fromtimestamp(float(user_data.get('last_login', 0))),
                'is_active': bool(int(user_data.get('is_active', 0))),
                'remaining_uses': int(user_data.get('remaining_uses', 0))
            })
    
    return jsonify({
        'success': True,
        'data': users
    })

@admin_bp.route('/api/admin/user/<username>', methods=['PUT'])
@require_admin
def update_user(username):
    data = request.json
    user_key = f"user:{username}"
    
    if not redis_client.exists(user_key):
        return jsonify({
            'success': False,
            'message': '用户不存在'
        })
    
    # 更新用户信息
    redis_client.hmset(user_key, {
        'is_active': int(data.get('is_active', 1)),
        'remaining_uses': data.get('remaining_uses', 0)
    })
    
    return jsonify({
        'success': True,
        'message': '更新成功'
    }) 