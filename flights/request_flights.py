# import requests
# import json

# url = "https://example.com/api/create"
# headers = {"Content-Type": "application/json"}

url = "https://api.aviationstack.com/v1/flights?access_key=9eaf52939d98d90572d2de9e64f0bbc4"

# response = requests.post(url, headers=headers)


# print(response.status_code)
# print(response.json())  # created resource


import requests

response = requests.get(url)

print(response.status_code)  # 200
print(response.json())  # list of posts
print(f"\n")