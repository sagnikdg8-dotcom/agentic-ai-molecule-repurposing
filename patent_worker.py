# workers/patent_worker.py
import json, os

def get_patents(molecule):
    """Reads mock patent data for the given molecule."""
    path = os.path.join("mock_data", "patents_mock.json")
    with open(path) as f:
        data = json.load(f)

    return [p for p in data if p.get("molecule") == molecule]
