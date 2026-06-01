import json

def get_saved_data():
    # """Call this function anytime later to retrieve the saved data."""
    try:
        with open('saved_assignments.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return [] # Return empty list if no file exists yet
