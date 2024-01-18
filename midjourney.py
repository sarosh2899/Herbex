import requests
import time

def create_barbie_image(api_key, image_urls):
    """
    Create a Barbie image using the provided API key and image URLs.
    
    Args:
    - api_key (str): The API key for authentication.
    - image_urls (list): List of URLs for creating the image.
    
    Returns:
    - dict: Response from the API containing task information.
    """
    endpoint = "https://api.midjourneyapi.xyz/mj/v2/blend"
    headers = {"X-API-KEY": api_key}
    
    data = {
        "image_urls": image_urls,
        "process_mode": "turbo",
        "webhook_endpoint": "",
        "webhook_secret": ""
    }
    
    response = requests.post(endpoint, headers=headers, json=data)
    return response.json()

def create_ken_image(api_key, image_urls):
    """
    Create a Ken image using the provided API key and image URLs.
    
    Args:
    - api_key (str): The API key for authentication.
    - image_urls (list): List of URLs for creating the image.
    
    Returns:
    - dict: Response from the API containing task information.
    """
    endpoint = "https://api.midjourneyapi.xyz/mj/v2/blend"
    headers = {"X-API-KEY": api_key}
    
    data = {
        "image_urls": image_urls,
        "process_mode": "turbo",
        "webhook_endpoint": "",
        "webhook_secret": ""
    }
    
    response = requests.post(endpoint, headers=headers, json=data)
    return response.json()


def fetch_from_midjourney(task_id):
    """
    Fetch data from Midjourney API based on the provided task ID.
    
    Args:
    - task_id (str): The task ID to fetch data from Midjourney.
    
    Returns:
    - dict: Response from the Midjourney API.
    """
    endpoint = "https://api.midjourneyapi.xyz/mj/v2/fetch"
    data = {"task_id": task_id}
    
    response = requests.post(endpoint, json=data)
    return response.json()

def fetch_image_from_task(task_id):
    """
    Fetches an image from the task ID response within a 5-minute timeframe.
    
    Args:
    - task_id (str): The task ID to fetch the image from.
    
    Returns:
    - bytes/str: Fetched image content if successful, else an error message.
    """
    start_time = time.time()
    end_time = start_time + 300  # 5 minutes
    
    while time.time() < end_time:
        response = fetch_from_midjourney(task_id)
        discord_image_url = response['task_result']['discord_image_url']
        print(response)
        if discord_image_url:
            try:
                image_response = requests.get(discord_image_url)
                if image_response.status_code == 200:
                    return image_response.content
            except requests.RequestException as e:
                print(f"Failed to fetch image: {e}")
        else:
            time.sleep(2)
    
    return "Faced some issue"

# Example usage
api_key = 'YOUR_API_KEY'


barbie_image_path = "https://images.unsplash.com/photo-1563475454428-db1b68095419?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8YmFyYmllJTIwZG9sbHxlbnwwfHwwfHx8MA%3D%3D"

ken_image_path= "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSfCwkjx4URwIaPaHvtOKOjKH0SVXhftMykMA&usqp=CAU"


user_image = "https://images.pexels.com/photos/1391495/pexels-photo-1391495.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"



barbie_image_urls = [
    user_image,
    barbie_image_path
]

ken_image_urls = [
    user_image,
    barbie_image_path
]

key = 'f9f51b8840ad7f99897ccb4d53305335bb0b389260457aedaab05f5d56547cc1'
barbie_response = create_barbie_image(key, barbie_image_urls)
print(barbie_response)
# task_id_barbie = barbie_response['task_id']

task_id_barbie = barbie_response['task_id']

# ken_response = create_ken_image(api_key, ken_image_urls)
# task_id_ken = ken_response['task']

fetch_response = fetch_from_midjourney(task_id_barbie)

print(fetch_response)
