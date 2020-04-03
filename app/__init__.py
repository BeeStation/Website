from app import cfg
from app import db
from app import util

from flask import Flask
from flask import session

from flask_cors import CORS


app = Flask(__name__, static_url_path=cfg.WEBSITE["static-url-path"])


app.url_map.strict_slashes = False

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.context_processor
def context_processor():
	return dict(cfg=cfg, db=db, util=util, session=dict(session))


from app.modules.api.controllers import bp_api
app.register_blueprint(bp_api)

from app.modules.bans.controllers import bp_bans
app.register_blueprint(bp_bans)

from app.modules.index.controllers import bp_index
app.register_blueprint(bp_index)

from app.modules.leaderboard.controllers import bp_leaderboard
app.register_blueprint(bp_leaderboard)

from app.modules.library.controllers import bp_library
app.register_blueprint(bp_library)

from app.modules.maps.controllers import bp_maps
app.register_blueprint(bp_maps)

from app.modules.meta.controllers import bp_meta
app.register_blueprint(bp_meta)

from app.modules.patreon.controllers import bp_patreon
app.register_blueprint(bp_patreon)

from app.modules.redirects.controllers import bp_redirects
app.register_blueprint(bp_redirects)

from app.modules.rules.controllers import bp_rules
app.register_blueprint(bp_rules)

from app.modules.stats.controllers import bp_stats
app.register_blueprint(bp_stats)

