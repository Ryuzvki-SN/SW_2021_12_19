from flask import make_response

from api import app
from api.elector.model import Elector


@app.route("/api/changement/<cni>", methods=["GET", "POST"], strict_slashes=False)
def changement(cni):
    user = Elector.query.filter_by(cni=cni).first()

    if not user:
        # returns 401 if user does not exist
        return make_response(
            'User does not exist !!',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )
