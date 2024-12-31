from flask import jsonify
import traceback

class ErrorHandler:
    def __init__(self, app, logger):
        self.app = app
        self.logger = logger
        self.register_handlers()
    
    def register_handlers(self):
        @self.app.errorhandler(404)
        def not_found(error):
            return render_template('404.html'), 404
        
        @self.app.errorhandler(500)
        def internal_error(error):
            self.logger.error(f"500 Error: {traceback.format_exc()}")
            return render_template('500.html'), 500
        
        @self.app.errorhandler(Exception)
        def handle_exception(error):
            self.logger.error(f"Unhandled Exception: {traceback.format_exc()}")
            return jsonify({
                'success': False,
                'message': '服务器内部错误'
            }), 500 