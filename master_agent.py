# master_agent.py

import re
from workers import market_worker, trials_worker, patent_worker, web_worker, internal_worker


def extract_molecule(prompt: str):
    """Extracts the molecule name from user prompt. Defaults to molecule_x."""
    prompt = prompt.lower()
    match = re.findall(r"molecule_[a-z0-9]+", prompt)
    if match:
        return match[0]
    return "molecule_x"  # default


def run_pipeline(prompt: str):
    """Main orchestrator function."""

    molecule = extract_molecule(prompt)

    # Call worker agents
    market_data = market_worker.get_market(molecule)
    trials_data = trials_worker.get_trials(molecule)
    patent_data = patent_worker.get_patents(molecule)
    web_data = web_worker.get_web_snippets(molecule)
    internal_data = internal_worker.get_internal_insights(molecule)

    # Generate summary
    summary = generate_summary(
        molecule,
        market_data,
        trials_data,
        patent_data,
        web_data,
        internal_data
    )

    # Return everything in one dictionary
    return {
        "molecule": molecule,
        "market": market_data,
        "trials": trials_data,
        "patents": patent_data,
        "web": web_data,
        "internal": internal_data,
        "summary": summary
    }


def generate_summary(molecule, market, trials, patents, web, internal):
    """Simple rule-based summary (no LLM required)."""

    # Market
    therapy = market.get("therapy_area")
    market_size = market.get("market_size_patients_india")
    cagr = market.get("cagr")

    # Clinical Trials
    num_trials = len(trials)
    phases = ", ".join(sorted({t["phase"] for t in trials})) if num_trials > 0 else "None"

    # Patents
    num_patents = len(patents)

    # Web insights
    key_web = web[0]["snippet"] if web else "No notable web insights."

    # Internal insights
    field_note = internal.get("field_feedback", "No internal insights found.")

    summary_text = (
        f"{molecule} is positioned in the {therapy} therapy area with an estimated "
        f"market size of approximately {market_size} patients in India and a CAGR of {cagr*100:.1f}%. "
        f"Current landscape shows {num_trials} active or past clinical trials, spanning phases: {phases}. "
        f"A total of {num_patents} relevant patent families were identified. "
        f"Scientific literature suggests: {key_web}. "
        f"Internal field insights indicate: {field_note}. "
        f"Overall, initial evidence indicates potential opportunity for repurposing assessment."
    )

    return summary_text
