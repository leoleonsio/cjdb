from flask import Blueprint
from flask_restful import Api
import  cjdb_api.app.resources.querying as query

beta_blueprint = Blueprint("beta", __name__)
beta_api = Api(beta_blueprint)

# Query
beta_api.add_resource(query.show, "/show/<int:lim>")
beta_api.add_resource(query.QueryByPoint, "/point/<string:coor>")
beta_api.add_resource(query.QueryByGroundGeometry, "/ground_geometry/<string:coor>")
beta_api.add_resource(query.AddAttribute, "/add/<string:object_id>/<string:attrib>/<string:new_value>")
beta_api.add_resource(query.FilterAttributes, "/filter/<string:attrib>/<string:operator>/<string:value>")
beta_api.add_resource(query.GetChildren, "/children/<string:object_id>")
beta_api.add_resource(query.GetParent, "/parent/<string:object_id>")
beta_api.add_resource(query.QueryByAttribute, "/select/<string:attrib>/<string:value>")
beta_api.add_resource(query.GetInfo, "/info/<string:attrib>/<string:object_id>")
beta_api.add_resource(query.CQL_query, "/cql")

# Update
beta_api.add_resource(query.UpdateAttrib, "/update/<string:object_id>/<string:attrib>/<string:new_value>")

# Deletion
beta_api.add_resource(query.DelAttrib, "/del/<string:object_id>/<string:attrib>")
beta_api.add_resource(query.DelObject, "/delObject/<string:object_id>")
