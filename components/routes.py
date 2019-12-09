from io import BytesIO
from random import choice

from flask import render_template, send_file
from werkzeug.exceptions import HTTPException

from components.image.generate import search, retrieve_random, distort, NOUNS


def register(app, request):
    @app.route('/')
    def index():
        return render_template('/home.html')

    @app.route('/generate', methods=['get', 'post'])
    def generate():
        query = ' '.join(choice(NOUNS) for i in range(app.config['NOUN_COUNT']))
        results = search(app.config['GOOGLE_API_KEY'],
                         app.config['GOOGLE_CSE_CX'],
                         request.args.get('query', query))
        img = retrieve_random(results)
        img = distort(img, app.config['EFFECT_COUNT'])
        stream = BytesIO()
        img.save(stream, 'png')
        stream.seek(0)
        return send_file(stream, mimetype='image/png')

    @app.errorhandler(HTTPException)
    def error(e):
        return render_template('error.html', num=e.code, text=e.description, title=e.code), e.code