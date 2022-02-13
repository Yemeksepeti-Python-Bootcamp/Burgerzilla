from api.config.config import Config
from flask_restx import Resource,Namespace,fields
from flask import request
from ..models.restaurants import Menu, Restaurant
from http import HTTPStatus
from werkzeug.exceptions import Conflict,BadRequest
from flask_jwt_extended import jwt_required,get_jwt_identity
from ..utils import db
import json

rest_namespace = Namespace('rest',description="a namespace for restaurants")



post_menu_model = rest_namespace.model(
    'Menu', {
        'id': fields.Integer(),
        'title': fields.String(required=True, description="Name of Menu"),
        'list': fields.String(required=True, description="A List of All menus"),

    }
)


menu_model = rest_namespace.model(
    'MenuModel', {
        'id': fields.Integer(),
        'title': fields.String(required=True, description="Name of Menu"),
        'list': fields.String(required=True, description="A List of All menus"),

    }
)

@rest_namespace.route('/menu')
class menu(Resource):

    @rest_namespace.marshal_with(menu_model)
    @rest_namespace.doc(
        description="All Menus"
    )
    def get(self):
        """
            Get all Menus
        """
        results = Menu.query.all()
        # all = get_all_rest(results)
        return results, HTTPStatus.OK

    @rest_namespace.expect(post_menu_model)
    @rest_namespace.marshal_with(menu_model)
    @jwt_required()
    def post(self):
        """
            Create a new Menu
        """
        data = request.get_json()
        try:

            result = Menu(
                id=data.get("id"),
                title=data.get("title"),
                list=str(data.get("list"))
            )
            result.save()
            return result, HTTPStatus.CREATED

        except Exception as e:
            print(str(e))
            raise Conflict(f"Exception  or Error {str(e)}")
@rest_namespace.route('/menu/<int:id>')
class one_menu(Resource):

    @rest_namespace.marshal_with(menu_model)
    def get(self, id):
        """
            Retrieve ane Menus by its id
        """
        result = Menu.get_by_id(id)
        return result, HTTPStatus.OK

    @rest_namespace.marshal_with(menu_model)
    @jwt_required()
    def put(self, id):
        """
            Update a Menu with id
        """

        to_update = Menu.get_by_id(id)

        data = rest_namespace.payload

        to_update.title = data['title']
        to_update.list = str(data['list'])

        to_update.save()

        return to_update, HTTPStatus.OK

    @jwt_required()
    def delete(self, id):
        """
            Delete one Restaurant with id
        """
        order_to_delete = Restaurant.get_by_id(id)

        res = order_to_delete.delete()

        return res, HTTPStatus.OK

@rest_namespace.route('/list_menu/<int:id>')
class list_menu(Resource):

    def get(self, id):
        """
            Retrieve ane List of Menus Products by its id
        """
        result = Menu.get_by_id(id)
        products = {
            "list":result.list
        }
        return products, HTTPStatus.OK

@rest_namespace.route('/add_product_menu/<int:id>')
class add_product_menu(Resource):

    def post(self, id):

        results = Menu.get_by_id(id)
        result = results.list
        products = json.dumps(result)
        data = request.get_json()
        new_product = str(","+str(data))
        products = str(products[:-2]) + new_product + str(products[-2:])

        results.list = str(products)
        results.save()

        return products, HTTPStatus.OK




post_rest_model = rest_namespace.model(
    'Restaurant', {
        'id': fields.Integer(),
        'owner': fields.Integer(),
        'name': fields.String(required=True, description="An unique name of restaurant"),
        'menu': fields.Integer(),

    }
)


rest_model = rest_namespace.model(
    'RestaurantModel', {
        'id': fields.Integer(),
        'owner': fields.Integer(),
        'name': fields.String(required=True, description="An unique name of restaurant"),
        'menu': fields.Integer(),
    }
)


def get_all_rest(results):
    list = []
    for result in results:
        list.append(
            {
        'id': result.id,
        'owner': result.owner,
        'name':result.name,
        'menu':result.menu
    }
        )
    return list
@rest_namespace.route('/restaurant')
class restaurant(Resource):

    def get(self):
        """
            Get all Restaurants
        """
        results = Restaurant.query.all()
        all = get_all_rest(results)
        return all, HTTPStatus.OK

    @rest_namespace.expect(post_rest_model)
    @rest_namespace.marshal_with(rest_model)
    @jwt_required()
    def post(self):
        """
            Create a new Restaurant
        """
        data = request.get_json()
        try:

            result = Restaurant(
                id=data.get("id"),
                owner=data.get("owner"),
                name=data.get("name"),
                menu=data.get("menu")
            )
            result.save()
            return "Message: Created !", HTTPStatus.CREATED

        except Exception as e:
            print(str(e))
            raise Conflict(f"Exception  or Error {str(e)}")
@rest_namespace.route('/restaurant/<int:id>')
class one_restaurant(Resource):

    def get(self, id):
        """
            Retrieve ane Restaurant by its id
        """
        result = Restaurant.get_by_id(id)
        all = {
            'id': result.id,
            'owner': result.owner,
            'name': result.name
        }
        return all, HTTPStatus.OK

    @jwt_required()
    def put(self, id):
        """
            Update a Restaurant with id
        """

        order_to_update = Restaurant.get_by_id(id)

        data = rest_namespace.payload

        order_to_update.name = data['name']
        order_to_update.owner = data['owner']

        order_to_update.save()

        return "Updated", HTTPStatus.OK

    @jwt_required()
    def delete(self, id):
        """
            Delete one Restaurant with id
        """
        order_to_delete = Restaurant.get_by_id(id)

        res = order_to_delete.delete()

        return res, HTTPStatus.OK
