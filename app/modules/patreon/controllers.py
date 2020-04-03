from app import cfg
from app import db
from app import util

from flask import Blueprint
from flask import render_template
from flask import redirect
from flask import request

import patreon

bp_patreon = Blueprint('patreon_oauth', __name__)

@bp_patreon.route("/patreonauth")
def page_patreon_oauth():

	try:
		code = request.args.get('code')
		ckey = request.args.get('state')

		if code != None and ckey != None:
			oauth_client = patreon.OAuth(cfg.PRIVATE["patreon"]["client_id"], cfg.PRIVATE["patreon"]["client_secret"])

			tokens = oauth_client.get_tokens(code, 'https://beestation13.com/patreonauth')

			access_token = tokens['access_token']

			api_client = patreon.API(access_token)

			user_identity = api_client.get_identity().data()

			user_id = user_identity.id()

			player = db.Player.from_ckey(ckey)

			if not player:
				return redirect("/linkpatreon?error=invalidckey")
			
			db.site_db.link_patreon(ckey, user_id)

			return redirect("/linkpatreon?success=true")

		else:
			return redirect("/linkpatreon?error=unknown")

	except Exception as E:
		return str(E)
	
	return redirect("/linkpatreon?error=unknown")


@bp_patreon.route("/linkpatreon")
def page_patreon_link():

	ckey = request.args.get("ckey")

	if ckey != None:

		player = db.Player.from_ckey(ckey)

		if player:
			return redirect("http://www.patreon.com/oauth2/authorize?response_type={}&client_id={}&redirect_uri={}&scope={}&state={}".format(
				"code",
				cfg.PRIVATE["patreon"]["client_id"],
				"https://beestation13.com/patreonauth",
				"identity identity.memberships",
				str(ckey)
			))

		else:
			return redirect("/linkpatreon?error=invalidckey")

	return render_template("patreonlink.html")