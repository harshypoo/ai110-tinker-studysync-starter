"""
StudySync -- Find a Study Spot (Ticket 3, Tinker 3B).

TICKET: none of the ranking logic is implemented yet -- every function
below is a stub.
"""

import csv

NOISE_ORDER = {"quiet": 0, "moderate": 1, "loud": 2}


def load_study_spots(csv_path: str) -> list:
    """
    Load study spots from a CSV into a list of dicts, converting
    "distance_miles" to float and "seats_available" to int.
    """
    with open(csv_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        spots = []
        for row in reader:
            # Convert distance_miles to float and seats_available to int
            row["distance_miles"] = float(row["distance_miles"])
            row["seats_available"] = int(row["seats_available"])
            spots.append(row)
    return spots

def score_study_spot(profile: dict, spot: dict) -> tuple:
    """
    Score one study spot against a student profile.

    profile example: {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}

    Return (score, reasons) where reasons is a list of short strings
    explaining what contributed to the score, e.g. ["quiet enough", "close enough"].
    """
    # TODO: implement additive/weighted scoring using at least noise_level
    # (compare using NOISE_ORDER), distance_miles vs max_distance, and
    # seats_available vs min_seats. Append a short string to `reasons` for
    # each factor that contributed, whether it helped or hurt the score.
    score = 0.0
    reasons = []
    for matches, weight, positive, negative in (
        (NOISE_ORDER[spot["noise_level"]] <= NOISE_ORDER[profile["max_noise"]], 3.0, "quiet enough", "too noisy"),
        (spot["distance_miles"] <= profile["max_distance"], 2.0, "close enough", "too far"),
        (spot["seats_available"] >= profile["min_seats"], 1.0, "enough seats", "not enough seats"),
    ):
        score += weight if matches else -weight
        reasons.append(positive if matches else negative)
    return score, reasons


def rank_study_spots(profile: dict, spots: list, k: int = 3) -> list:
    """
    Score every study spot, then return the top k as (spot, score, reasons)
    tuples, sorted by score descending.
    """
    # TODO: score every spot with score_study_spot(), then use
    # sorted(..., key=..., reverse=True)[:k] to keep only the top k.
    scored = [(spot, *score_study_spot(profile, spot)) for spot in spots]
    return sorted(scored, key=lambda result: result[1], reverse=True)[:k]
    

def format_results(ranked: list) -> None:
    """Print each ranked study spot with its score and reasons, one line each."""
    # TODO: for each (spot, score, reasons) tuple, print a readable line, e.g.:
    # "1. Innovation Commons -- Score: 5.0 -- Because: quiet enough, close enough"
    for i, (spot, score, reasons) in enumerate(ranked, start=1):
        print(f"{i}. {spot['name']} -- Score: {score:.1f} -- Because: {', '.join(reasons)}")


def render_study_spot_tab():
    import streamlit as st

    st.subheader("Find a Study Spot")
    max_noise = st.selectbox("Max noise level", ["quiet", "moderate", "loud"], index=1)
    max_distance = st.slider("Max distance (miles)", 0.0, 3.0, 1.0)
    min_seats = st.number_input("Minimum seats needed", min_value=1, value=4, step=1)

    if st.button("Find spots"):
        profile = {"max_noise": max_noise, "max_distance": max_distance, "min_seats": min_seats}
        try:
            spots = load_study_spots("data/study_spots.csv")
            ranked = rank_study_spots(profile, spots, k=3)
            for spot, score, reasons in ranked:
                st.write(f"**{spot['name']}** -- Score: {score:.1f} -- Because: {', '.join(reasons)}")
        except NotImplementedError:
            st.warning("🚧 Ranking isn't implemented yet -- that's Tinker 3B's ticket.")


if __name__ == "__main__":
    spots = load_study_spots("data/study_spots.csv")
    profile = {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}
    ranked = rank_study_spots(profile, spots, k=3)
    format_results(ranked)

# Because noise has a higher weight than distance (3 versus 2), 
# the ranking can consistently bury nearby but loud spots such as 
# Student Union Tables and Courtyard Cafe, creating a filter bubble 
# that narrows the options users ever see.