import json
from collections import Counter
from typing import List, Dict

LOG_PATH = 'query_log.jsonl'


def load_logs() -> List[Dict]:
    logs = []
    try:
        with open(LOG_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                logs.append(json.loads(line))
    except FileNotFoundError:
        pass
    return logs

def summarize_failures(logs: List[Dict]) -> Dict:
    failures = [log['decision'].get('justification', '') for log in logs if log['decision'].get('decision') == 'rejected']
    counter = Counter(failures)
    return dict(counter.most_common())

def generate_weekly_report() -> Dict:
    logs = load_logs()
    summary = summarize_failures(logs)
    report = {
        'total_queries': len(logs),
        'total_rejections': sum(summary.values()),
        'common_failure_reasons': summary
    }
    return report 