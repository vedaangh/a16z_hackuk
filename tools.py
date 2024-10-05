import requests
import os
from dotenv import load_dotenv
from pprint import pprint
from typing import List, Dict, Any
from urllib.parse import urlparse
from pathlib import Path

load_dotenv()

brave_api_key = os.getenv("BRAVE_API_KEY")

class VisualTooling:

    def render_website(self, directory: str):
        pass

class SearchTooling:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        self.image_search_url = "https://api.search.brave.com/res/v1/images/search"

    def search_web_information(self, query: str): # search the web for information
        """
        Fetches search results from Brave Search API using Python with specific headers.
        
        Args:
        - api_key (str): Your Brave Search API key.
        - query (str): The search query.
        
        Returns:
        - dict: Search results as a dictionary.
        """
        
        # API endpoint
        url = self.base_url

        # Query parameters
        params = {
            'q': query,
            'count': 10  # Number of results to return
        }

        # Headers to match the curl request
        headers = {
            'Accept': 'application/json',
            'X-Subscription-Token': self.api_key  # API Key passed here
        }

        # Make the GET request
        response = requests.get(url, headers=headers, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()  # Return the search results as a JSON dictionary
        else:
            # If the request fails, raise an error with the status and error message
            return f"Error: {response.status_code} - {response.text}"
        
    def search_web_screenshots(self, query: str, save_dir: str) -> List[Dict[str, Any]]:
        """
        Search for images using the Brave API's image search endpoint and save them to a directory.

        Args:
        - query (str): The search query for images.
        - save_dir (str): The directory to save the downloaded images.

        Returns:
        - List[Dict[str, Any]]: A list of image results with local file paths.
        """
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key
        }
        params = {
            "q": query,
            "count": 10  # Number of results to return
        }
        response = requests.get(self.image_search_url, headers=headers, params=params)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            # Create the save directory if it doesn't exist
            Path(save_dir).mkdir(parents=True, exist_ok=True)
            
            for i, result in enumerate(results):
                image_url = result.get('thumbnail', {}).get('src')
                if image_url:
                    # Download and save the image
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image_path = os.path.join(save_dir, f"image_{i}.jpg")
                        with open(image_path, 'wb') as f:
                            f.write(image_response.content)
                        print(f"Saved image to {image_path}")
                    else:
                        print(f"Failed to download image: {image_response.status_code}")
            return results
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []

    def search_web_pictures(self, query: str): # search the web for pictures
        results = self.search_web_information(query)

    def extract_website_code(self, url: str): # extract the code from a website
        pass

# Example usage with pretty printing
if __name__ == "__main__":
    search_tool = SearchTooling(brave_api_key)
    results = search_tool.search_web_information("dog")
    print("Search Results:")
    pprint(results, indent=2, width=100)
    
    # Image search example
    image_results = search_tool.search_web_screenshots("cute puppies", "/images")
    print("\nImage Search Results:")
    pprint(image_results, indent=2, width=100)