import requests


url = "http://127.0.0.1:5000/test"

while True:
    payload = {}
    payload["prompt"] = input()

    response = requests.post(url, data = payload)
    # print(response.status_code)
    print(response.text)
