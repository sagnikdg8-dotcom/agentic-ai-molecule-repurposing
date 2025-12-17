# workers/web_worker.py

def get_web_snippets(molecule):
    """Returns mock scientific or guideline snippets."""
    snippets = {
        "molecule_x": [
            {"source": "Guideline X", "snippet": "No targeted therapy exists for post-infectious bronchiectasis."},
            {"source": "Journal Y", "snippet": "Molecule X shows anti-inflammatory activity in airway models."}
        ],
        "molecule_y": [
            {"source": "Dermatology Conference Z", "snippet": "Sustained topical formulations show positive outcomes."}
        ]
    }

    return snippets.get(molecule, [])
