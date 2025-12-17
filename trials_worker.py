# workers/trials_worker.py
import json, os

def get_trials(molecule):
    """Reads mock clinical trial data for the given molecule."""
    path = os.path.join("mock_data", "trials_mock.json")
    with open(path) as f:
        data = json.load(f)

    return [t for t in data if t.get("molecule") == molecule]
