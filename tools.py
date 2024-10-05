import requests
import os
from dotenv import load_dotenv
from pprint import pprint
from typing import List, Dict, Any
from urllib.parse import urlparse
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

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

    def search_web_information(self, query: str):  # search the web for information
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
        params = {"q": query, "count": 10}  # Number of results to return

        # Headers to match the curl request
        headers = {
            "Accept": "application/json",
            "X-Subscription-Token": self.api_key,  # API Key passed here
        }

        # Make the GET request
        response = requests.get(url, headers=headers, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()  # Return the search results as a JSON dictionary
        else:
            # If the request fails, raise an error with the status and error message
            return f"Error: {response.status_code} - {response.text}"

    def search_web_pictures(
        self, query: str, save_dir: str = "images"
    ) -> List[Dict[str, Any]]:
        """
        Search for images using the Brave API's image search endpoint and save them to a directory.

        Args:
        - query (str): The search query for images.
        - save_dir (str): The directory to save the downloaded images. Defaults to 'images'.

        Returns:
        - List[Dict[str, Any]]: A list of image results with local file paths.
        """
        # Get the current working directory and append the save_dir
        print(os.getcwd())
        # Use a relative path instead of an absolute path
        save_dir = os.path.join(os.getcwd(), save_dir.lstrip("/"))
        print(save_dir)
        headers = {"Accept": "application/json", "X-Subscription-Token": self.api_key}
        params = {"q": query, "count": 10}  # Number of results to return
        response = requests.get(self.image_search_url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])

            # Create the save directory if it doesn't exist
            Path(save_dir).mkdir(parents=True, exist_ok=True)

            for i, result in enumerate(results):
                image_url = result.get("thumbnail", {}).get("src")
                if image_url:
                    # Download and save the image
                    image_response = requests.get(image_url)
                    if image_response.status_code == 200:
                        image_path = os.path.join(save_dir, f"image_{i}.jpg")
                        with open(image_path, "wb") as f:
                            f.write(image_response.content)
                        print(f"Saved image to {image_path}")
                    else:
                        print(f"Failed to download image: {image_response.status_code}")
            return results
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []

    def screenshot_web(self, query: str, save_dir: str = "screenshots") -> List[str]:
        """
        Search the web using Brave API and take screenshots of the resulting websites.

        Args:
        - query (str): The search query for websites.
        - save_dir (str): The directory to save the screenshots. Defaults to 'screenshots'.

        Returns:
        - List[str]: A list of file paths where screenshots are saved.
        """
        # Perform a web search to get URLs using Brave API
        search_results = self.search_web_information(query)
        urls = [result["url"] for result in search_results.get("results", [])]
        print(urls)
        # Set up the Selenium WebDriver
        options = Options()
        options.add_argument("--headless")  # Run in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

        # Create the save directory if it doesn't exist
        save_dir = os.path.join(os.getcwd(), save_dir)
        Path(save_dir).mkdir(parents=True, exist_ok=True)

        screenshot_paths = []
        for i, url in enumerate(urls):
            try:
                driver.get(url)
                screenshot_path = os.path.join(save_dir, f"screenshot_{i}.png")
                driver.save_screenshot(screenshot_path)
                screenshot_paths.append(screenshot_path)
                print(f"Saved screenshot to {screenshot_path}")
            except Exception as e:
                print(f"Failed to take screenshot of {url}: {e}")

        driver.quit()
        return screenshot_paths

    def extract_website_code(self, url: str):  # extract the code from a website
        pass


# Example usage with pretty printing
if __name__ == "__main__":
    search_tool = SearchTooling(brave_api_key)
    results = search_tool.search_web_information("dog")
    print("Search Results:")
    pprint(results, indent=2, width=100)

    # Image search example
    image_results = search_tool.search_web_pictures("cute puppies", "/images")
    print("\nImage Search Results:")
    pprint(image_results, indent=2, width=100)

    # Screenshot example
    screenshot_results = search_tool.screenshot_web("cute puppies")
    print("\nScreenshot Results:")
    pprint(screenshot_results, indent=2, width=100)
