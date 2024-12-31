import os
from werkzeug.utils import secure_filename
import magic

class FileUpload:
    ALLOWED_EXTENSIONS = {'ppt', 'pptx', 'doc', 'docx', 'pdf', 'jpg', 'png'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)

    def allowed_file(self, filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS

    def check_file_type(self, file):
        """使用 python-magic 检查文件类型"""
        mime = magic.from_buffer(file.read(2048), mime=True)
        file.seek(0)  # 重置文件指针
        return mime in [
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'application/pdf',
            'image/jpeg',
            'image/png'
        ]

    def save_file(self, file):
        if file and self.allowed_file(file.filename):
            if file.content_length > self.MAX_FILE_SIZE:
                return None, "文件大小超过限制"
            
            if not self.check_file_type(file):
                return None, "不支持的文件类型"
            
            filename = secure_filename(file.filename)
            file_path = os.path.join(self.upload_folder, filename)
            file.save(file_path)
            return file_path, None
        
        return None, "无效的文件" 