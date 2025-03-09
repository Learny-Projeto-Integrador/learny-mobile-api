def init_app(app):
    @app.route('/')
    def home():
        return 'Rota Inicial'