# workers/internal_worker.py

def get_internal_insights(molecule):
    """Returns mock insights from internal reports."""
    notes = {
        "molecule_x": {
            "sales_team_note": "Low uptake of current inhaled generics.",
            "field_feedback": "Doctors want once-daily dosing options."
        },
        "molecule_y": {
            "sales_team_note": "Strong demand in dermatology segments.",
            "field_feedback": "Need formulations with better tolerability."
        }
    }

    return notes.get(molecule, {})
