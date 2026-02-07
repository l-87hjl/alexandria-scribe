import uuid, datetime, re
from runtime.storage.fragment_store import FragmentStore
from runtime.logging.logger import log_event

def ingest_text(text, source_id):
    log_event("ingestion.start","info","ingestion","start",{"source":source_id})
    store = FragmentStore()
    for part in re.split(r"[.!?]\s+", text):
        if part.strip():
            store.append({
                "fragment_id": str(uuid.uuid4()),
                "raw_text": part.strip(),
                "source_id": source_id,
                "timestamp": datetime.datetime.utcnow().isoformat()
            })
    log_event("ingestion.complete","info","ingestion","done")
