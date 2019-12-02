from io import BytesIO
from json import dumps
from random import choice

from flask import Response, render_template, send_file
from werkzeug.exceptions import HTTPException

from components.image.generate import search, retrieve_random, distort, NOUNS
from urllib.parse import quote


def register(app, request):
    @app.route('/')
    def index():
        query = ' '.join(choice(NOUNS) for i in range(app.config['NOUN_COUNT']))
        return render_template('/home.html', query=query, query_endpoint=f'/generate?query={quote(query)}')

    @app.route('/generate', methods=['get', 'post'])
    def generate():
        if 'query' in request.args:
            results = search(app.config['GOOGLE_API_KEY'], app.config['GOOGLE_CSE_CX'], request.args['query'])
            img = retrieve_random(results)
            img = distort(img, app.config['EFFECT_COUNT'])
            stream = BytesIO()
            img.save(stream, 'png')
            stream.seek(0)
            return send_file(stream, mimetype='image/png')

        return Response(dumps({}), mimetype='application/json')

    @app.errorhandler(HTTPException)
    def error(e):
        return render_template('error.html', num=e.code, text=e.description, title=e.code), e.code
