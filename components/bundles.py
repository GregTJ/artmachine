from flask_assets import Bundle, Environment
from webassets.filter import get_filter

assets = None


def register(app):
    global assets
    assets = Environment(app)

    scripts = Bundle(
        "js/helpers.js",
        filters='jsmin', output='gen/packed.js')

    styles = Bundle(
        "scss/reset.scss",
        "scss/error.scss",
        "scss/base.scss",
        filters=get_filter('libsass', as_output=True, style='compressed'),
        output='gen/packed.css')

    assets.register('scripts', scripts)
    assets.register('styles', styles)
