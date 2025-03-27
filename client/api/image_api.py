import requests
from config import ClientConfig

class ImageAPI:
    def __init__(self):
        self.server_url = ClientConfig.SERVER_URL
        self.headers = {'Authorization': f'Bearer {ClientConfig.API_KEY}'}
        self.timeout = ClientConfig.TIMEOUT

    def check_connection(self):
        try:
            response = requests.get(
                f"{self.server_url}/images",
                headers=self.headers,
                timeout=self.timeout
            )
            return response.status_code == 200
        except (requests.ConnectionError, requests.Timeout):
            return False

    def upload_image(self, file_path, filter_type):
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'filter': filter_type}
            
            response = requests.post(
                f"{self.server_url}/upload",
                files=files,
                data=data,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()

    def get_image(self, image_url):
        response = requests.get(
            f"{self.server_url}/image/{image_url}",
            headers=self.headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.content

    def get_history(self):
        response = requests.get(
            f"{self.server_url}/images",
            headers=self.headers,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()