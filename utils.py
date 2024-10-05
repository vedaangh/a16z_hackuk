from mistralai import Mistral
import os
import base64

api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

MODELS = {
    "text": "mistral-large-latest",
    "image": "pixtral-12b-2409",
    "code": "codestral-mamba-latest",
}

def main(user_input):
    # Parse user input
    event_details = generate_event_details(user_input)
    
    # Get reference images
    reference_images = get_reference_images(event_details)
    
    # Generate website structure
    website_theme = generate_website_theme(event_details, reference_images)
    
    # Generate individual pages
    pages = generate_pages(website_theme, event_details, reference_images)
    
    # Refine and optimize code
    final_website = refine_website(pages, event_details)
    
    return final_website

def parse_user_input(user_input):
    # Parse user input into structured event details
    # ... implementation ...
    pass

def get_reference_images(event_details):
    # Use Brave API to get screenshots and posters

    # Use Pixtral to process and filter relevant images
    pass

def generate_website_structure(event_details, reference_images):
    # Use Pixtral to generate initial website structure
    # ... implementation ...
    pass

def generate_pages(website_structure, event_details, reference_images):
    # Generate individual pages based on the structure
    pass

def generate_page_content(page, event_details, reference_images):
    # Generate content for a single page
    # ... implementation ...
    pass

def refine_website(pages, design, event_details):
    # Use Codestral to refine and optimize the website
    # pages is a list of html codes

    # need to experiment with codestral to see how it handles a llist of files
    prompt = f"""
    We are trying to build a hackathon website. We have the html code of separate pages in the list {str(pages)} as well as the css design in {design}. 
    Add a navbar to all of the pages to navigate between them and make any other refinements, perhaps according to the design. 
    Output the html code in the same form and order that it was inputted, as a list of strings containing the html code. 

    """
    messages = [
        {"role": "user", "content": prompt}
    ]

    chat_response = client.chat.complete(
        model=MODELS["code"],
        messages=messages
    )
    cleaned_response = chat_response.choices[0].message.content
    return eval(cleaned_response)

def publish_website(refined_website,design, html_structure):
    os.makedirs("website", exist_ok=True)

    # Save CSS
    css_path = os.path.join("website", "styles.css")
    with open(css_path, 'w') as css_file:
        css_file.write(design)

    # Save HTML
    for i in range(len(html_structure)):
        html_path = os.path.join("website", html_structure[i])
        with open(html_path, 'w') as html_file:
            html_file.write(refined_website[i])

    # Save JavaScript
    js_path = os.path.join("website", "script.js")
    with open(js_path, 'w') as js_file:
        js_file.write("")


def generate_images(image_requirements):
    # Use DALL-E API to generate images based on requirements
    # lets leave this one for now...
    pass


if __name__ == "__main__":
    # ... code to output or deploy the website ...
    pass