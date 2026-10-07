import re

US_STATES = {
    "AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas", "CA": "California",
    "CO": "Colorado", "CT": "Connecticut", "DE": "Delaware", "FL": "Florida", "GA": "Georgia",
    "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois", "IN": "Indiana", "IA": "Iowa",
    "KS": "Kansas", "KY": "Kentucky", "LA": "Louisiana", "ME": "Maine", "MD": "Maryland",
    "MA": "Massachusetts", "MI": "Michigan", "MN": "Minnesota", "MS": "Mississippi",
    "MO": "Missouri", "MT": "Montana", "NE": "Nebraska", "NV": "Nevada", "NH": "New Hampshire",
    "NJ": "New Jersey", "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
    "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon", "PA": "Pennsylvania",
    "RI": "Rhode Island", "SC": "South Carolina", "SD": "South Dakota", "TN": "Tennessee",
    "TX": "Texas", "UT": "Utah", "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
    "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming", "DC": "District of Columbia",
}

STATE_CODE = r"\b(" + "|".join(US_STATES) + r")\b"
WASHINGTON = r"(?i)washington|district of columbia"

_STATE_PATTERNS = {
    code: (re.compile(rf"\b{code}\b"), re.compile(rf"\b{re.escape(name)}\b", re.IGNORECASE))
    for code, name in US_STATES.items()
}


def states_mentioned(text):
    return {code for code, (short, full) in _STATE_PATTERNS.items() if short.search(text) or full.search(text)}


def state_of_s1(address):

    parts = [part.strip() for part in address.split(",")]
    positions = [i for i, part in enumerate(parts) if part in US_STATES]
    if not positions:
        return None, ""
    i = positions[-1]
    town = parts[i - 1] if i > 0 else (parts[i + 1] if i + 1 < len(parts) else "")
    return parts[i], town


def record_state(s1_address, record_address):


    code, town = state_of_s1(s1_address)
    if code is None:
        return "unknown"
    if town:
        record_address = re.sub(rf"\b{re.escape(town)}\b", " ", record_address, flags=re.IGNORECASE)
    mentioned = states_mentioned(record_address)
    if code in mentioned:
        return "same"
    return "other" if mentioned else "none"
