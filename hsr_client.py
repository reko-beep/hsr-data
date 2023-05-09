from abc import ABC
from backend import BackendAdapter
from datamodels import trace


# Public facing api client.
class HsrClient:
    def __init__(self):
      
        # abstract away multiple backends. with a single backend adapter. 
        # i guess this is too much.
        # just using SRSBackend here would have been enough.
        self.adapter = BackendAdapter()
    
        # our own api related logic goes here
        # in this case, looping and searching.
        # here we have the convinience of working with our own data models. (ex: Trace)
    def find_trace(self, trace_name) -> trace.Trace:
        for trace in self.adapter().fetch_traces():
            if trace.name  == trace_name:
                return trace
        
        


    def fetch_image(self):
        return self.adapter().fetch_image()  
        # or use a different backend.
        return self.adapter(HoyolabBackend).fetch_image()

if __name__ == "__main__":
    client = HsrClient()
    print(client.find_trace("abc"))
    print(client.fetch_image())
