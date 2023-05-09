from ..util import Backend
from datamodels import trace

# backend for starrail station.
class SRSBackend(Backend):
    def fetch_traces(self) -> list[trace.Trace]:
        # return the traces as HsrClient's data model in stead of
        # SRS's data model

        # do backend get request.
        # feed the json to @validator and transform it into HsrCleint's model.
        return []
    
    def fetch_image(self):
        return "srs image"