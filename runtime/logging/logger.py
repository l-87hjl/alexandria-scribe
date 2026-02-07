import json, sys, uuid, datetime

def log_event(event_type, severity, source, message, context=None):
    sys.stdout.write(json.dumps({
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "event_type": event_type,
        "severity": severity,
        "source": source,
        "message": message,
        "context": context or {}
    }) + "\n")
