""" REST API Controllers """
from sw_demo_api import manager
from sw_demo_api.models import Role, User

role_api_blueprint = manager.create_api_blueprint(Role, methods=['GET', 'PATCH', 'POST'])
user_api_blueprint = manager.create_api_blueprint(
    User,
    methods=['GET', 'PATCH', 'POST'],
    include_columns=['id', 'name', 'roles']
)
