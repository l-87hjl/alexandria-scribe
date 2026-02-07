from fastapi import FastAPI
from pydantic import BaseModel
from runtime.ingestion.minimal_ingest import ingest_text

app = FastAPI()

class IngestRequest(BaseModel):
    text: str
    source_id: str

@app.post("/ingest")
def ingest(req: IngestRequest):
    fragments = ingest_text(req.text, req.source_id)
    return {"fragments_created": len(fragments)}
