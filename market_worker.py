# workers/market_worker.py
import json, os

def get_market(molecule):
    """Reads mock market data for the given molecule."""
    path = os.path.join("mock_data", "iqvia_mock.json")
    with open(path) as f:
        data = json.load(f)

    # If molecule not found, return default structure
    return data.get(molecule, {
        "molecule": molecule,
        "therapy_area": "Unknown",
        "market_size_patients_india": 0,
        "cagr": 0.0,
        "top_competitors": [],
        "notes": ""
    })
