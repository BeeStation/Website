from flask import Blueprint, redirect, render_template, request

from app import cfg, util

bp_patreon = Blueprint("patreon", __name__)


@bp_patreon.route("/linkpatreon")
def page_patreon_link():

    ckey = request.args.get("ckey")

    if ckey != None:
        return redirect(
            "http://www.patreon.com/oauth2/authorize?response_type={}&client_id={}&redirect_uri={}&scope={}&state={}".format(
                "code",
                cfg.WEBSITE["patreon"]["client-id"],
                "https://api.beestation13.com/patreonauth",
                "identity identity.memberships",
                str(ckey),
            )
        )

    return render_template("patreonlink.html")
