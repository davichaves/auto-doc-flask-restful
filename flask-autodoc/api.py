from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

from flask.ext.autodoc import Autodoc

app = Flask(__name__)
api = Api(app)
auto = Autodoc(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):

    @auto.doc(groups=['private'])
    def get(self, todo_id):
        """GET a single TODO"""
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    @auto.doc(groups=['private'])
    def delete(self, todo_id):
        """DELET a single TODO"""
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    @auto.doc(groups=['private'])
    def put(self, todo_id):
        """PUT a single TODO"""
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):

    @auto.doc(groups=['public'])
    def get(self):
        """GET method for TODO LIST"""
        return TODOS

    @auto.doc(groups=['public'])
    def post(self):
        """POST method for a todo"""
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201


class PublicDoc(Resource):

    def get(self):
        """GET the public API"""
        return auto.html(groups=['public'], title='Blog Documentation with Custom template', template="autodoc_custom.html")

# @api.route('/doc/')
# @api.route('/doc/public')
# def public_doc():
#     return auto.html(groups=['public'], title='Blog Documentation with Custom template', template="autodoc_custom.html")


class PrivateDoc(Resource):

    def get(self):
        """GET the private API"""
        return auto.html(groups=['private'], title='Private Documentation with Custom template', template="autodoc_custom.html")

# @api.route('/doc/private')
# def private_doc():
#     return auto.html(groups=['private'], title='Private Documentation with Custom template', template="autodoc_custom.html")

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(PublicDoc, '/doc/public')
api.add_resource(PrivateDoc, '/doc/private')


if __name__ == '__main__':
    app.run(debug=True)
