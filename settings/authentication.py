from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_jwt_extended.exceptions import NoAuthorizationError

class Authentication :
    def __init__(self,app):
        self.app = app
        app.config['JWT_SECRET_KEY'] = 'your-secret-key'
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)  # Token expires in 15 minutes
        # app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)  # Refresh token expires in 30 days
        jwt = JWTManager(app)

        @jwt.expired_token_loader
        def expired_token_callback(jwt_header, jwt_payload):
            return {
                "message": "The token has expired",
                "status" : 400
            }

        @app.errorhandler(NoAuthorizationError)
        def handle_missing_authorization(error):
            return {
                "message": "must include token!!!",
                "status" : 400
            }