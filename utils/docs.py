from flask import jsonify
import inspect

class APIDocGenerator:
    def __init__(self, app):
        self.app = app
        self.endpoints = []
        self.collect_endpoints()
    
    def collect_endpoints(self):
        """收集所有API端点信息"""
        for rule in self.app.url_map.iter_rules():
            if rule.endpoint.startswith('api'):
                view_func = self.app.view_functions[rule.endpoint]
                doc = inspect.getdoc(view_func)
                self.endpoints.append({
                    'path': rule.rule,
                    'methods': list(rule.methods),
                    'description': doc,
                    'name': rule.endpoint
                })
    
    def generate_docs(self):
        """生成API文档"""
        return jsonify({
            'api_version': '1.0',
            'endpoints': self.endpoints
        }) 