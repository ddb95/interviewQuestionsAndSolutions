from flask import Flask
from flask.globals import request
from flask_restplus import Api, Resource, fields, inputs, reqparse
from werkzeug.contrib.fixers import ProxyFix
from datetime import datetime
import sqlite3
import logging

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='TodoMVC API',
    description='A popular simple TodoMVC API',
)
parser = reqparse.RequestParser()
parser.add_argument('due_date', type=inputs.date, help="Add Due Date")

ns = api.namespace('todos', description='TODO operations')

# Database Connection
def db_conn():
    try:
        conn = sqlite3.connect('task.db')
        c = conn.cursor()
        # Create Table
        c.execute(
            """CREATE TABLE tasks (
                id integer,
                todoName text,
                todoDetails text,
                status text,
                dueDate text
            )""")
        return c,conn
    except Exception as e:
        logging.warning(e)
        conn = sqlite3.connect('task.db')
        c = conn.cursor()
        print("Connection Successful")
        return c,conn

# Converting a tuple returned from DB to a dictionary for easy access 
def tupleToObject(arrayOfTuple):
    arrayOfObjects = []
    detailsObject = {}
    for item in arrayOfTuple:
        detailsObject["id"],detailsObject["todoName"],detailsObject["todoDetails"], detailsObject["status"], detailsObject["dueDate"] = item
        # detailsObject['dueDate'] = datetime.strptime(detailsObject['dueDate'], '%Y-%m-%d %H:%M:%S')
        arrayOfObjects.append(detailsObject)
        detailsObject = {}
    return arrayOfObjects

# Model
LIST_MODEL = {
    'id': fields.Integer(readonly=True, description='The task unique identifier'),
    'todoName': fields.String(required=True, description='The task Name'),
    'todoDetails': fields.String(required=False, description='The task details'),
    'status': fields.String(required=True, description='The task status'),
    'dueDate': fields.String(required=True,description='Due Date'),
}

# Model to List view
todo = ns.model(
    "listversion",
    LIST_MODEL
)
# TODO class with class methods
class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        dbquery, conn = db_conn()
        todoList = []
        try:
            with conn:
                todoData = dbquery.execute('select * from tasks where id={id}'.format(id=id)).fetchall()
                todoList = tupleToObject(todoData)
                if len(todoList) > 0:
                    return todoList
                else:
                    raise Exception("Todo {} doesn't exist".format(id))
        except Exception as e:
            logging.warning(e)
            api.abort(404, "Todo {} doesn't exist".format(id))
    
    def getbyDuedate(self, date):
        for todo in self.todos:
            if todo['dueDate'] == date:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))
    
    def getbyStatus(self, status):
        for todo in self.todos:
            if todo['status'] == status:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        try:
            todo = data
            getNumberOfDataAvailable = TodoList().get()
            self.counter = len(getNumberOfDataAvailable)
            todo['id'] = self.counter = self.counter + 1
            dbConn, conn = db_conn()
            try:
                print('INSERT INTO tasks VALUES ({id}, "{todoName}", "{todoDetails}", "{status}", "{dueDate}")'.format(id =todo["id"], todoName= todo["todoName"], todoDetails= todo["todoDetails"], status= todo["status"],dueDate=todo["dueDate"]))
                dbConn.execute('INSERT INTO tasks VALUES ({id}, "{todoName}", "{todoDetails}", "{status}", "{dueDate}")'.format(id =todo["id"], todoName= todo["todoName"], todoDetails= todo["todoDetails"], status= todo["status"],dueDate=todo["dueDate"]))
                conn.commit()
                conn.close()
            except Exception as e:
                logging.warning(e)
                conn.close()
            self.todos.append(todo)
            return self.todos
        except KeyError as e:
            ns.abort(500, e.__doc__, status = "Could not parse information", statusCode = "500")
        except Exception as e:
            ns.abort(400, e.__doc__, status = "Could not parse information", statusCode = "400")

    def update(self, id, todo):
        dbquery, conn = db_conn()
        if(dbquery.execute('select 1 from tasks where id={id}'.format(id=id)).fetchone()):
            try:
                dbquery.execute('update tasks set todoName="{todoName}", todoDetails="{todoDetails}", status="{status}",dueDate="{dueDate}" where id={id}'.format(id =id, todoName= todo["todoName"], todoDetails= todo["todoDetails"], status= todo["status"],dueDate=todo["dueDate"]))
                conn.commit()
                conn.close()
                return "Successfully Updated Todo with Id-{id}".format(id=id)
            except Exception as e:
                logging.warning(e)
                conn.close()
                return "Error"      
        else:
            return "Not Found "
          

    def delete(self, id):
        dbConn, conn = db_conn()
        try:
            with conn:
                dbConn.execute('DELETE from tasks WHERE id = {id}'.format(id=id))
                if dbConn.rowcount>0:
                    conn.commit()
                    return "Delete Successfully"
                else:
                    return "No data found with ID->{id}".format(id=id)
        except Exception as e:
            logging.warning(e)
            return e

    def getByStatusFinished(self):
        dbquery, conn = db_conn()
        todoList = []
        try:
            with conn:
                todoData = dbquery.execute('select * from tasks where status="Finished"').fetchall()
                todoList = tupleToObject(todoData)
                if len(todoList) > 0:
                    return todoList
                else:
                    raise Exception("No task marked as finished")
        except Exception as e:
            logging.warning(e)
            api.abort(404, "Error in getting tasks")
            return todoList
        
    def getTasksByOverdue(self):
        dbQuery, conn = db_conn()
        currentDateTime = datetime.now().strftime("%Y-%m-%d")
        todoList = []
        try:
            with conn:
                print('select * from tasks where dueDate<\"{currentdatetime}\"'.format(currentdatetime = currentDateTime))
                todoData = dbQuery.execute('select * from tasks where dueDate<\"{currentdatetime}\"'.format(currentdatetime = currentDateTime)).fetchall()
                todoList = tupleToObject(todoData)
                return todoList
        except Exception as e:
            logging.warning(e)
            api.abort(404, "Error in getting tasks")
            return todoList
    
    def getTasksByDueDate(self, dueDate):
        dbQuery, conn = db_conn()
        dateVal = datetime.strftime(dueDate, "%Y-%m-%d")
        todoList = []
        try:
            with conn:
                print('select * from tasks where dueDate=\"{currentdatetime}\"'.format(currentdatetime = dateVal))
                todoData = dbQuery.execute('select * from tasks where dueDate=\"{currentdatetime}\"'.format(currentdatetime = dateVal)).fetchall()
                todoList = tupleToObject(todoData)
                return todoList
        except Exception as e:
            logging.warning(e)
            api.abort(404, "Error in getting tasks")
            return todoList

# Class initialization
DAO = TodoDAO()

# Completed the api to create a todo, can handle multiple todos
@ns.route('/createTodo')
class CreateTodo(Resource):
    @ns.doc("Create a new Task")
    @ns.expect([todo])
    @ns.marshal_with(todo)
    def post(self):
        for items in api.payload:
            DAO.create(items)

# Sort the Todos which are Finished
@ns.route('/finished')
class GetFinishedData(Resource):
    @ns.doc("Get all task which are finished")
    @ns.response(200, "Finished Tasks")
    def get(self):
        return DAO.getByStatusFinished()

# Delete a particular Todo by id
@ns.route('/deleteTodo/<int:id>')
class DeleteTodo(Resource):
    @ns.doc("Delete a new Task")
    @ns.response(200, "Todo Deleted")
    def delete(self, id):
        return DAO.delete(id)

# Find TODOs which are overdues
@ns.route('/overdue')
class OverdueTodo(Resource):
    @ns.doc("Get all the tasks that are overdue")
    @ns.response(200, "Overdue Tasks")
    def get(self):
        return DAO.getTasksByOverdue()

# Find TODOs which are due on a particular date
@ns.route('/due')
class DueDateTodo(Resource):
    @ns.doc("Get all the task by due date")
    @ns.response(200, "Due Date Task\nSend Due Date in form of YYYY-MM-DD\nExample:2021-06-27")
    @ns.expect(parser)
    def get(self):
        args = parser.parse_args()
        return DAO.getTasksByDueDate(args["due_date"])

# Update a TODO by ID and updated payload
@ns.route('/update/<int:id>')
class UpdateTodo(Resource):
    @ns.doc("Update a new Task")
    @ns.expect([todo])
    @ns.marshal_with(todo)
    def post(self, id):
        if(isinstance(id,int)):
            DAO.update(id,api.payload[0])
        else:
            raise Exception("ID doesn't exist".format(id))

# Base URL to get TODOs
@ns.route('/')
class TodoList(Resource):
    # List of all Todos and lets you POST to add new tasks
    @ns.doc('List all the Todos')
    @ns.marshal_list_with(todo)
    def get(self):
        dbConn, conn = db_conn()
        todoTuple = dbConn.execute("select * from tasks").fetchall()
        todoList = tupleToObject(todoTuple)
        conn.close()
        # List all tasks
        return todoList

# Get Todo by ID
@ns.route('/<int:id>')
@ns.response(404, "Task Not Available")
@ns.param("id", "The task identifier")
class Todo(Resource):
    # Show indivisual Task
    @ns.doc("Get a Task by Id")
    @ns.marshal_with(todo)
    def get(self, id):
        return DAO.get(id)

if __name__ == '__main__':
    app.run(debug=True)