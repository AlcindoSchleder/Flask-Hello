import os
from flask import Flask

COMMON_DIRECTORY = os.path.abspath(os.path.dirname(__file__))

class FlaskServer:
    """
        Classe que initialize API Server, Application Server or both
        * class      ICompanyServer
        * requires   python 3.7
        * version    1.0.0
        * developer  Alcindo Schleder <alcindo.schleder@amcom.com.br>
    """

    def __init__(self):
        # Create a instance of Flask and get api configuration
        self.server_app = Flask(__name__)

        self.server_app.config['FLASK_ENV'] = os.environ.get("FLASK_ENV", default="development")
        self.set_environment_config()

    def set_environment_config(self):
        from server.config import config_by_name

        mode = config_by_name[self.server_app.config['FLASK_ENV']]

        self.server_app.config['DEBUG'] = mode.DEBUG
        self.server_app.config['TESTING'] = mode.TESTING
        self.server_app.config['HOST_SERVER'] = mode.HOST_SERVER
        self.server_app.config['SERVER_PORT'] = mode.SERVER_PORT

    def run(self):
        self.server_app.run(
            self.server_app.config['HOST_SERVER'],
            self.server_app.config['SERVER_PORT'],
            debug=self.server_app.config['DEBUG']
        )
        print('endpoints: ', self.server_app.url_map)
