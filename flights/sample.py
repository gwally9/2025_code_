
import http.client

conn = http.client.HTTPSConnection( "https://api.aviationstack.com")

conn.request("GET", "/v1/flights?access_key={9eaf52939d98d90572d2de9e64f0bbc4}")

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))