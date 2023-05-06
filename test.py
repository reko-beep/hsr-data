from main import SRSClient
from constants import Types, Languages

from json import dump

client = SRSClient()
r = client.get_all_items(Types.CHARACTERS)[0]
c = client.get_all_character_details(r)
print(c)