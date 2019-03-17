""" REST API Controllers """
from sw_demo_api import manager
from sw_demo_api.models import Role, User

ROLE_API_BLUEPRINT = manager.create_api_blueprint(Role, methods=['GET', 'PATCH', 'POST'])
USER_API_BLUEPRINT = manager.create_api_blueprint(
    User,
    methods=['GET', 'PATCH', 'POST'],
    include_columns=['user_id', 'name', 'roles']
)
