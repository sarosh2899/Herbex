import requests

url = 'http://127.0.0.1:5001/generate' 

# Data to be sent in the request
data = {
    'name': 'John',
    'surname': 'Doe',
    'age': 25,
    'email': 'john.doe@example.com',
    'city': 'New York',
    'gender': 'Male'
}

image_file_path = 'C:\\Users\\Gagan\\Downloads\\herbex-ignite (1)\\herbex-ignite\\static\\public\\logo.png'
files = {'image': open(image_file_path, 'rb')}

# Make a POST request to the endpoint
response = requests.post(url, data=data, files=files)

# Check the response status
if response.status_code == 200:
    print('Request successful!')
    print(response.json())  # Assuming the response is in JSON format
else:
    print(f'Request failed with status code: {response.status_code}')
    print(response.text)  # Print the response content for debugging purposes
