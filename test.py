import requests

url = "http://127.0.0.1:8000"

print("POST:")
print("test 1")
response = requests.post(url + "/api/v1/convert", json={"date":"12.20.2021 20:21:05", "tz":"EST", "target_tz":"GMT"})
print("url: " + response.request.url)
print(f"data: {response.request.body}")
print("response: " + response.text)

print("test 2")
response = requests.post(url + "/api/v1/convert", json={"date":"12.20.2021 20:21:05", "tz":"GMT", "target_tz":"EST"})
print("url: " + response.request.url)
print(f"data: {response.request.body}")
print("response: " + response.text)

print("test 3")
json = {"first_date":"12.20.2021 20:21:05",
        "first_tz":"EST",
        "second_date":"01.12.2020 12:30:00",
        "second_tz":"Europe/Moscow"}
response = requests.post(url + "/api/v1/datediff", json=json)
print("url: " + response.request.url)
print(f"data: {response.request.body}")
print("response: " + response.text)

print("GET:")
print("test 4")
response = requests.get(url)
print("url: " + response.request.url)
print(f"data: {response.request.body}")
print("response: " + response.text)

print("test 5")
response = requests.get(url + "/Europe/Moscow")
print("url: " + response.request.url)
print(f"data: {response.request.body}")
print("response: " + response.text)