from main import SRSClient
from constants import Types, Languages



client = SRSClient()
r = client.get_all_items(Languages.CN, Types.MATERIALS)
print(r)