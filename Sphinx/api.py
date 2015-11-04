from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}


class Hello(Resource):
    """docstring for Hello"""
    def get(self):
        return "Hello, World!"


class TodoSimple(Resource):
    """dosctring for TodoSimple"""
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

api.add_resource(TodoSimple, '/<string:todo_id>')
api.add_resource(Hello, '/hello')

if __name__ == '__main__':
    app.run(debug=True)
