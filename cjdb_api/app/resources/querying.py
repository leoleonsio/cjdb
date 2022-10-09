from flask_restful import Resource
from flask import Flask, render_template, make_response, url_for, request, redirect
from model.sqlalchemy_models import CjObjectModel
from cjdb_api.app.schemas import CityJsonSchema
from cjdb_api.app.db import session, engine
from sqlalchemy.sql import text
cityjson_schema = CityJsonSchema()
cityjson_list_schema = CityJsonSchema(many=True)

def parse_table(parse):
    # convert cityjson schema to a list of headers and a list of lists of values
    headings = list(parse[0].keys())
    data = []
    for item in parse:
        data.append(list(item.values()))
       
    return headings, data
    
##working

#Select all objects in the database
class all(Resource):
    @classmethod
    def get(cls):
        all = session.query(CjObjectModel).all()
        headings, data = parse_table(cityjson_list_schema.dump(all))

        if not all:
            return {"message": "Object not found"}, 404

        return make_response(render_template("all.html", headings=headings, data=data))
    
##Get all the information of an object, given a certain value: So for instance, select building with object_id NL.IMBAG.Pand.0518100000213709-0, or select building with id 2
class QueryByAttribute(Resource):
    @classmethod
    def get(cls, attrib: str, value: str):
        cj_object = session.query(CjObjectModel).filter(getattr(CjObjectModel, attrib) == str(value))

        if not cj_object:
            return {"message": "Object not found"}, 404

        return cityjson_list_schema.dump(cj_object)

## Get the attribute info of an object, given the object_id, so for instance, get the children, parents, or attributes of NL.IMBAG.Pand.0518100000213709-0
class GetInfo(Resource):
    @classmethod
    def get(cls, attrib: str, object_id: str):
        cj_object = session.query(CjObjectModel).filter(CjObjectModel.object_id == object_id).first()
        attribute = getattr(cj_object, attrib)

        if not attribute:
            return {"message": "Object not found"}, 404

        return attribute

class FilterAttributes(Resource):
    @classmethod
    def get(cls, attrib: str, operator:str, value: str):
        if operator == "smaller":
            cj_object = session.query(CjObjectModel).filter(CjObjectModel.attributes[attrib] < value).all()
        if operator == "equals":
            cj_object = session.query(CjObjectModel).filter(CjObjectModel.attributes[attrib] < value).all()
        if operator == "bigger":
            cj_object = session.query(CjObjectModel).filter(CjObjectModel.attributes[attrib] > value).all()

        if not cj_object:
            return {"message": "Object not found"}, 404

        return cityjson_list_schema.dump(cj_object)


class CalculateFootprint(Resource):
    @classmethod
    def get(cls, object_id: str):
        cj_object = session.query(CjObjectModel).filter(CjObjectModel.object_id == object_id).first()

        if not cj_object:
            return {"message": "Object not found"}, 404

        with engine.connect() as connection:
            area_pointer = connection.execute(cj_object.bbox.ST_Area())
            # the pointer is "<sqlalchemy.engine.cursor.LegacyCursorResult object at 0x000002322DFAA2B0>" 
            
            for row in area_pointer:
                area = row[0]

            if not area:
                return {"message": "Object not found"}, 404

        return area


##in progress
class AddAttribute(Resource):
    @classmethod
    def get(cls):
        objects = session.query(CjObjectModel).all()
        for object in objects:
            listObj = object.attributes
            listObj["test_attribute"] = "test_value"
            object.attributes = listObj
            session.commit() # This is supposed to save the changes to the DB, but it doesn't

        return cityjson_list_schema.dump(objects)

#attempt to use raw sequel
# class Sequel(Resource):
#     @classmethod
#     def get(cls):
#         objects = session.query(CjObjectModel).all()
#
#         sql = text(("UPDATE objects SET attributes = jsonb_set(attributes::jsonb, ’{roof_area}’, ’123’)::json WHERE type = ’Building’;"))
#
#
#         for object in objects:
#             # session.execute(sql, **object)
#             session.execute(("UPDATE objects SET attributes = jsonb_set(attributes::jsonb, ’{roof_area}’, ’123’)::json WHERE type = ’Building’;"))
#         # objects.session.exectute("UPDATE objects SET attributes = jsonb_set(attributes::jsonb, ’{roof_area}’, ’123’)::json WHERE type = ’Building’;")
#         # for object in objects:
#         #     listObj = object.attributes
#         #     listObj["test_attribute"] = "test_value"
#         #     object.attributes = listObj
#         #     session.commit()  # This is supposed to save the changes to the DB, but it doesn't
#
#         return cityjson_list_schema.dump(objects)


#todo


class CalculateVolume (Resource):
    pass

class Geometry(Resource):
    @classmethod
    def get(cls):
        all = session.query(CjObjectModel).all()

        if not all:
            return {"message": "Object not found"}, 404

        return cityjson_list_schema.dump(all)

