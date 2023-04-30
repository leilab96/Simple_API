import pickle
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)


# read projects from pickle file
with open('projects.pickle', 'rb') as f:
    projects = pickle.load(f)
    




@app.route("/")
def home():
  return render_template("index.html.j2", name="Leila")


@app.route("/projects")
def get_projects():
  return jsonify(projects), 200, {
      # add Access-Control-Allow-Origin header
      'Access-Control-Allow-Origin': '*'
  }


@app.route("/project", methods=['POST'])
def create_project():
  request_data = request.get_json()
  new_project = {'name': request_data['name'], 'tasks': request_data['tasks']}
  projects.append(new_project)
  return jsonify(new_project), 201


@app.route("/project/<string:name>")
def get_project(name):
  print(name)
  for project in projects:
    if project['name'] == name:
      return jsonify(project)
  return jsonify({'message': 'project not found'}), 404


@app.route("/project/<string:name>/tasks")
def get_project_tasks(name):
  for project in projects:
    if project['name'] == name:
      return jsonify({'tasks': project['tasks']})
  return jsonify({'message': 'project not found'}), 404


@app.route("/project/<string:name>/task", methods=['POST'])
def add_task_to_project(name):
  request_data = request.get_json()
  for project in projects:
    if 'name' in project and project['name'] == name:
      if 'completed' not in request_data or type(
          request_data['completed']) is not bool:
        return jsonify(
            {'message': 'completed is required and must be a boolean'}), 400
      new_task = {
          'name': request_data['name'],
          'completed': request_data['completed']
      }
      project['tasks'].append(new_task)
      return jsonify(new_task), 201
  return jsonify({'message': 'project not found'}), 404
