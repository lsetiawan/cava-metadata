import os
from flask import Flask
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask("cava-metadata-api", instance_relative_config=True)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY="dev", DATABASE=os.path.join("/opt/app", "CAVA_Assets.db")
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db

    db.init_app(app)

    from . import creator
    creator.init_metadata(app)

    from . import metadata

    app.register_blueprint(metadata.bp)

    return app
