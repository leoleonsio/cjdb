from flask import Blueprint
from flask_restful import Api
import cjdb_api.app.resources.querying as query

master_blueprint = Blueprint("master", __name__)
master_api = Api(coll_blueprint)

# routes
coll_api.add_resource(query.Item, "/")
