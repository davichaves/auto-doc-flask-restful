from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_restful_swagger import swagger

app = Flask(__name__)
api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url='/api/spec')

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
@swagger.model
class Todo(Resource):
    """Hello, this is my Todo!"""
    def __init__(self):
        pass

    @swagger.operation(
        notes='Hello, Im typing some notes to test this!',
        responseClass='Todo',
        nickname='get',
        parameters=[
            {
              "name": "body",
              "description": "blueprint object that needs to be added. YAML.",
              "required": True,
              "allowMultiple": False,
              "dataType": 'hello data type',
              "paramType": "body"
            }
        ],
        responseMessages=[
            {"code": 201,
             "message": "Created. The URL of the created blueprint should be in the Location header"
             },
            {"code": 405,
             "message": "Invalid input"
             }
        ]
    )
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    @swagger.operation(
        notes='Hello, this should be my delete method!',
        responseClass='Todo',
        nickname='delete',
        parameters=[
            {
              "name": "body",
              "description": "blueprint object that needs to be added. YAML.",
              "required": True,
              "allowMultiple": False,
              "dataType": 'hello data type',
              "paramType": "body"
            }
        ],
        responseMessages=[
            {"code": 201,
             "message": "Created. The URL of the created blueprint should be in the Location header"
             },
            {"code": 405,
             "message": "Invalid input"
             }
        ]
    )
    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    @swagger.operation(
        notes='Hello, this should be my put method!',
        responseClass='Todo',
        nickname='put',
        parameters=[
            {
              "name": "body",
              "description": "blueprint object that needs to be added. YAML.",
              "required": True,
              "allowMultiple": False,
              "dataType": 'hello data type',
              "paramType": "body"
            }
        ],
        responseMessages=[
            {"code": 201,
             "message": "Created. The URL of the created blueprint should be in the Location header"
             },
            {"code": 405,
             "message": "Invalid input"
             }
        ]
    )
    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
@swagger.model
class TodoList(Resource):
    """Hello, this is my TodoList!"""
    def __init__(self):
        pass

    @swagger.operation(
        notes='Hello, this should be my get method!',
        responseClass='TodoList',
        nickname='get',
        parameters=[
            {
              "name": "body",
              "description": "blueprint object that needs to be added. YAML.",
              "required": True,
              "allowMultiple": False,
              "dataType": 'hello data type',
              "paramType": "body"
            }
        ],
        responseMessages=[
            {"code": 201,
             "message": "Created. The URL of the created blueprint should be in the Location header"
             },
            {"code": 405,
             "message": "Invalid input"
             }
        ]
    )
    def get(self):
        return TODOS

    @swagger.operation(
        notes='Hello, this should be my post method!',
        responseClass='TodoList',
        nickname='post',
        parameters=[
            {
              "name": "body",
              "description": "blueprint object that needs to be added. YAML.",
              "required": True,
              "allowMultiple": False,
              "dataType": 'hello data type',
              "paramType": "body"
            }
        ],
        responseMessages=[
            {"code": 201,
             "message": "Created. The URL of the created blueprint should be in the Location header"
             },
            {"code": 405,
             "message": "Invalid input"
             }
        ]
    )
    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


if __name__ == '__main__':
    app.run(debug=True)
