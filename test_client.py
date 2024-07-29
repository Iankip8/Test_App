import requests

url = 'http://127.0.0.1:5000/predict'
data = {'input': ["I love this product!", "I hate this service."]}

response = requests.post(url, json=data)

print("Response status code:", response.status_code)
print("Response JSON:", response.json())
