import re
from typing import Dict

def parse_query(query: str) -> Dict:
    """Extracts age, procedure, location, duration, etc. from user query."""
    result = {}
    # Age
    age_match = re.search(r'(\d{2})-year-old', query)
    if age_match:
        result['age'] = int(age_match.group(1))
    # Procedure
    proc_match = re.search(r'(surgery|treatment|procedure|hospitalization|operation|therapy|consultation)', query, re.I)
    if proc_match:
        result['procedure'] = proc_match.group(1)
    # Location
    loc_match = re.search(r'in ([A-Za-z ]+)', query)
    if loc_match:
        result['location'] = loc_match.group(1).strip()
    # Duration (e.g., 3-month-old)
    dur_match = re.search(r'(\d+)-(month|year|day)-old', query)
    if dur_match:
        result['policy_duration'] = f"{dur_match.group(1)} {dur_match.group(2)}"
    return result 