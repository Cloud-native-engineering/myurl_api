from apiflask import APIFlask
from app.config import Config
from app.extensions import db
from app.security.auth0_service import auth0_service
from app.security.guards import authorization_guard
from app.extensions import QueueFeed

def create_app(config_class=Config):
    app = APIFlask(__name__)
    app.config.from_object(config_class)
    app.security_schemes = {
        'bearerAuth': {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT'
        }
    }

    # Flask Erweiterungen initialisieren
    db.init_app(app)

    # Auth0Service initialisieren
    auth0_service.initialize(app.config['JWKS_URI'], app.config['JWT_AUDIENCE'], app.config['JWT_ISSUER_URL'], app.config['JWT_ALGORITHM'])

    # Init SQS if enabled
    app.queue_feed = QueueFeed(app.config['SQS_QUEUE_URL'])

    # Blueprints registrieren
    from app.users import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/api/users')

    from app.urls import bp as urls_bp
    app.register_blueprint(urls_bp, url_prefix='/api/urls')

    from app.restrictions import bp as restrictions_bp
    app.register_blueprint(restrictions_bp, url_prefix='/api/restrictions')
    
    # Datenbanktabellen anlegen
    with app.app_context():
        db.create_all()

    @app.route('/api/')
    @app.doc(security='bearerAuth')
    @authorization_guard
    def test_page():
        return {'message': 'MyURLs API', 'version': '1.0.0'}

    return app