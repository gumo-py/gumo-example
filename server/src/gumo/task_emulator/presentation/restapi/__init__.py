from logging import getLogger

import flask.views

logger = getLogger(__name__)
emulator_api_blueprint = flask.Blueprint('task-emulator', __name__)


class TasksView(flask.views.MethodView):
    def get(self):
        return 'ok'

    def post(self):
        return 'ok'


emulator_api_blueprint.add_url_rule(
    '/',
    view_func=TasksView.as_view(name='tasks'),
    methods=['GET', 'POST']
)
