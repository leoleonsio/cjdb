from flask import Blueprint
from flask_restful import Api
import cjdb_api.app.resources.querying as query

master_blueprint = Blueprint("master", __name__)
master_api = Api(master_blueprint)

# routes
master_api.add_resource(query.Item, "/")
