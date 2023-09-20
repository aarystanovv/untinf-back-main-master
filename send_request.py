import requests

response = requests.post('http://localhost:8000/update-answers/')

if response.status_code == 302:
    redirect_url = response.headers['Location']

    response = requests.get(redirect_url)

    print(response.text)
