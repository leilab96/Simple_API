import json
import pickle

# read JSON file
with open('projects.json', 'r') as f:
    projects = json.load(f)

# save projects as pickle file
with open('projects.pickle', 'wb') as f:
    pickle.dump(projects, f)
