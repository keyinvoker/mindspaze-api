from logging import getLogger
from flask import Flask
from flask_apscheduler import APScheduler
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from mindspaze.config import Config

app_logger = getLogger('app')
error_logger = getLogger('error')

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
scheduler = APScheduler()


def create_app(test: bool = False) -> Flask:
    app = Flask("MindSpaze")
    app.config.from_object(Config)

    with app.app_context():
        db.init_app(app)
        ma.init_app(app)
        migrate.init_app(app, db)

        from mindspaze.cli import prediction_cli
        app.cli.add_command(prediction_cli)

        from mindspaze.blueprints.prediction import prediction_bp
        app.register_blueprint(prediction_bp)

        print(f"\Endpoints:\n{app.url_map.iter_rules}\n")

        return app
