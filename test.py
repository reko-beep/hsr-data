from main import SRSClient
from constants import Types



client = SRSClient()
r = client.get_all_items('cn')
print(r)