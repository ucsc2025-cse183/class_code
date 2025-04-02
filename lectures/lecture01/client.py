import requests

response = requests.get("https://www.ucsc.edu/")
print(response.content[:100])




