import os
import json
from datetime import datetime

LOG_PATH = 'query_log.jsonl'

def log_query(query: str, structured: dict, decision: dict):
    entry = {
        'timestamp': datetime.utcnow().isoformat(),
        'query': query,
        'structured': structured,
        'decision': decision
    }
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(json.dumps(entry) + '\n') 