from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login_page'))
    return render_template('main.html')

@main_bp.route('/api/user/status')
def user_status():
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': '未登录'
        })
    
    user_id = session['user_id']
    user_data = redis_client.hgetall(f"user:{user_id}")
    
    if not user_data:
        return jsonify({
            'success': False,
            'message': '用户不存在'
        })
    
    # 检查账号状态
    expire_time = user_data.get('expire_time')
    remaining_uses = int(user_data.get('remaining_uses', 0))
    
    return jsonify({
        'success': True,
        'data': {
            'username': user_data['username'],
            'expire_time': datetime.fromtimestamp(float(expire_time)).strftime('%Y-%m-%d %H:%M:%S') if expire_time else None,
            'remaining_uses': remaining_uses,
            'is_active': bool(expire_time and float(expire_time) > datetime.now().timestamp() and remaining_uses > 0)
        }
    })

@main_bp.route('/api/user/use-count', methods=['POST'])
def update_use_count():
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'message': '未登录'
        })
    
    user_id = session['user_id']
    user_key = f"user:{user_id}"
    
    # 检查并更新使用次数
    remaining_uses = int(redis_client.hget(user_key, 'remaining_uses') or 0)
    if remaining_uses <= 0:
        return jsonify({
            'success': False,
            'message': '使用次数已用完'
        })
    
    redis_client.hincrby(user_key, 'remaining_uses', -1)
    
    return jsonify({
        'success': True,
        'data': {
            'remaining_uses': remaining_uses - 1
        }
    })

@main_bp.route('/api/upload/ppt', methods=['POST'])
@login_required
def upload_ppt():
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'message': '未找到文件'
        })
    
    file = request.files['file']
    path, error = file_upload.save_file(file)
    
    if error:
        return jsonify({
            'success': False,
            'message': error
        })
    
    # 记录上传历史
    user_id = session['user_id']
    redis_client.lpush(f"user:{user_id}:uploads", {
        'file_path': path,
        'upload_time': datetime.now().timestamp(),
        'file_type': file.content_type
    })
    
    return jsonify({
        'success': True,
        'path': path
    }) 