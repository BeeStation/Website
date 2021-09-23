from os import environ

from flask import Flask
from flask_cors import CORS

from app import cfg

app = Flask(__name__, static_url_path=cfg.WEBSITE["static-url-path"])

if environ.get("DEBUG") == "True":
    from werkzeug.debug import DebuggedApplication

    app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

    app.debug = True

if environ.get("APM") == "True":
    from elasticapm.contrib.flask import ElasticAPM

    apm_url = "http://0.0.0.0:8200"
    apm_debug = False
    apm_token = ""

    # Check for APM envrion variables
    if "APM_URL" in environ:
        apm_url = environ["APM_URL"]
    if "APM_DEBUG" in environ:
        apm_debug = environ["APM_DEBUG"]
    if "APM_TOKEN" in environ:
        apm_token = environ["APM_TOKEN"]

    app.config["ELASTIC_APM"] = {
        # Set required service name. Allowed characters:
        # a-z, A-Z, 0-9, -, _, and space
        "SERVICE_NAME": "beesite",
        # Use if APM Server requires a token
        "SECRET_TOKEN": apm_token,
        # Set custom APM Server URL (default: http://0.0.0.0:8200)
        "SERVER_URL": apm_url,
        "DEBUG": apm_debug,
    }

    apm = ElasticAPM(app)

app.url_map.strict_slashes = False

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.context_processor
def context_processor():
    from app import util

    return dict(cfg=cfg, util=util)


from app.modules.bans.controllers import bp_bans

app.register_blueprint(bp_bans)

from app.modules.index.controllers import bp_index

app.register_blueprint(bp_index)

from app.modules.library.controllers import bp_library

app.register_blueprint(bp_library)

from app.modules.meta.controllers import bp_meta

app.register_blueprint(bp_meta)

from app.modules.patreon.controllers import bp_patreon

app.register_blueprint(bp_patreon)

from app.modules.redirects.controllers import bp_redirects

app.register_blueprint(bp_redirects)

from app.modules.stats.controllers import bp_stats

app.register_blueprint(bp_stats)
