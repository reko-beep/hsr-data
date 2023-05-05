from main import SRSClient
from routes import MATERIALS
client = SRSClient()
r = client.generate_hash_route('en', MATERIALS,True, 872066)
print(r)
