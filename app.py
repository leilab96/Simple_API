import uuid
import pickle
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

    
def load_data():
    with open('projects.pickle', 'rb') as f:
        data = pickle.load(f)
    return data

# save projects to pickle file
def save_data(data):
    with open('projects.pickle', 'wb') as f:
        pickle.dump(data, f)

projects= load_data()

    

@app.route("/")
def home():
  return render_template("index.html.j2", name="Leila")


@app.route("/projects")
def get_projects():
  return jsonify(projects), 200, {
      # add Access-Control-Allow-Origin header
      'Access-Control-Allow-Origin': '*'
  }


 #create projects modified, it saves the added project into the pickle file
@app.route("/project", methods=['POST'])
def create_project():
    request_data = request.get_json()
    new_project_id = uuid.uuid4().hex[:24]
    new_project = {
        'name': request_data['name'],
        'creation_date': request_data['creation_date'],
        'completed': request_data['completed'],
        'tasks': []
    }
    for task in request_data['tasks']:
        new_task_id = uuid.uuid4().hex[:24]
        new_task = {
            'name': task['name'],
            'completed': task['completed'],
            'task_id': new_task_id,
            'checklist': []
        }
        for item in task['checklist']:
            new_checklist_id = uuid.uuid4().hex[:24]
            new_item = {
                'name': item['name'],
                'completed': item['completed'],
                'checklist_id': new_checklist_id
            }
            new_task['checklist'].append(new_item)
        new_project['tasks'].append(new_task)
    projects['projects'].append(new_project)
    save_data(projects)
    return jsonify({ 'message': f'project created with id: {new_project_id}' }), 201


#note: "projects" is a key itself too so the code will need some modifications for other functions too
#get_project uses project_id to find the project
@app.route("/project/<string:project_id>")
def get_project(project_id):
    for project in projects["projects"]:
        if project['project_id'] == project_id:
            return jsonify(project)
    return jsonify({'message': 'project not found'}), 404
  
  
#change projects key "complete" to true and saves it 
@app.route("/project/<string:project_id>/complete", methods=['POST'])
def complete_project(project_id):
    for project in projects["projects"]:
        if project['project_id'] == project_id:
            if project['completed']:
                return '', 200
            else:
                project['completed'] = True
                save_data(projects)
                return jsonify(project), 200
    return jsonify({'message': 'project not found'}), 404
  

@app.route("/project/<string:project_id>/task", methods=['POST'])
def add_task_to_project(project_id):
    request_data = request.get_json()
    for project in projects['projects']:
        if project['project_id'] == project_id:
            new_task_id = uuid.uuid4().hex[:24]
            new_task = {
                'name': request_data['name'],
                'completed': request_data['completed'],
                'task_id': new_task_id,
                'checklist': []
            }
            if 'checklist' in request_data:
                for item in request_data['checklist']:
                    new_checklist_id = uuid.uuid4().hex[:24]
                    new_item = {
                        'name': item['name'],
                        'completed': item['completed'],
                        'checklist_id': new_checklist_id
                    }
                    new_task['checklist'].append(new_item)
            project['tasks'].append(new_task)
            save_data(projects)
            return jsonify({'task_id': new_task_id}), 201
    return jsonify({'message': 'project not found'}), 404
  
@app.route("/project/<string:name>/tasks")
def get_project_tasks(name):
  for project in projects["projects"]:
    if project['name'] == name:
      return jsonify({'tasks': project['tasks']})
  return jsonify({'message': 'project not found'}), 404