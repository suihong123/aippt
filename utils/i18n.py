from flask_babel import Babel
from flask import request, session

def get_locale():
    if 'language' in session:
        return session['language']
    return request.accept_languages.best_match(['zh', 'en'])

babel = Babel(app, locale_selector=get_locale) 