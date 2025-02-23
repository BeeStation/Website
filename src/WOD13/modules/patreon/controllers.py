from WOD13 import cfg
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request

bp_patreon = Blueprint("patreon", __name__)


@bp_patreon.route("/linkpatreon")
def page_patreon_link():
    ckey = request.args.get("ckey")

    if ckey is not None:
        return redirect(
            "http://www.patreon.com/oauth2/authorize?response_type={}&client_id={}&redirect_uri={}&scope={}&state={}".format(  # noqa: E501
                "code",
                cfg.WEBSITE["patreon"]["client-id"],
                "https://api.WOD13.com/patreonauth",
                "identity identity.memberships",
                str(ckey),
            )
        )

    return render_template("patreonlink.html")
