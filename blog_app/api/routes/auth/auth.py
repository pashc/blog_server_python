import logging

from flask import request, g
from flask.json import jsonify
from flask_restplus import Resource

from blog_app.api import api
from blog_app.api.exceptions.UserNotFoundException import UserNotFoundException
from blog_app.api.serializers import user
from blog_app.api.services import user_service
from blog_app.auth import auth

log = logging.getLogger(__name__)

ns = api.namespace('auth', description='authentication related operations')


@ns.route('/users/<int:user_id>')
class UserItem(Resource):

    @api.marshal_with(user)
    def get(self, user_id):
        """
        :param user_id: the user to get
        :return: the user for the given id
        """
        return user_service.find(user_id)

    @api.expect(user)
    @api.response(204, 'user successfully updated')
    @auth.login_required
    def put(self, user_id):
        """
        update a user

        use this operation to change the username and password for the given id

        all the fields are mandatory

        * send a JSON object with the fields in the request body

        '''
        {
            "username": "Topsy",
            "password": "Cret"
        }
        '''
        :param user_id: the user to update
        :return: None, status_code=204
        """
        data = request.json
        return user_service.update(user_id, data)

    @api.response(204, 'user successfully deleted')
    @auth.login_required
    def delete(self, user_id):
        """
        deletes the user for the given id
        :param user_id: the user to delete
        :return: None, status_code=204
        """
        return user_service.delete(user_id)


@ns.errorhandler(UserNotFoundException)
def handle_user_not_found(error):
    return error.to_dict(), error.code


@auth.login_required
def get_auth_token():
    """
    generates the authentication token for the current user with a ttl of
    :return:
    """
    token = g.user.generate_auth_token(600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@auth.verify_password
def verify_password(username_or_token, password):
    return user_service.verify_password(username_or_token, password)
