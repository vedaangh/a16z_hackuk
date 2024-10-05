from mistralai import Mistral
import os

api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

MODELS = {
    "text": "mistral-large-latest",
    "image": "pixtral-12b-2409",
    "code": "codestral-mamba-latest",
}

def main(user_input):
    # Parse user input
    event_details = parse_user_input(user_input)
    
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
    prompt = f"""
    Analyze the following user input for an event webpage and extract key information. Provide a summary of the event details in a structured format. Include any important aspects mentioned by the user, such as event description, date, time, venue, theme, color preferences, or other requirements.

    User Input:
    {user_input}

    Please provide a concise summary of the event details, highlighting the most important aspects. The type of information being provided will be variable depenending on the user input, so don't mention 'not mentioned' for any information. Accept that the user might not have mentioned certain details, and don't bring it up. Write any info that can be inferred from the user input.

    Example output:
    Event Name: Summer Music Festival
    Event Description: A music festival with a bohemian summer theme.
    Date: July 15, 2024
    Time: 12 PM to 10 PM
    Venue: Central Park
    Theme: Bohemian Summer
    Color Preferences: Warm Reds, Teals, Sky Blues
    Decorations: Eco-friendly
    Accessibility: Disabled attendees

    Now, please analyze the user input and provide a similar summary:
    """

    messages = [
        {"role": "user", "content": prompt}
    ]

    response = client.chat.complete(
        model=MODELS["text"],
        messages=messages
    )

    return response.choices[0].message.content

def get_reference_images(event_details):
    # Use Brave API to get screenshots and posters

    # Use Pixtral to process and filter relevant images
    pass

def generate_website_theme(event_details, reference_images):
    # Use Pixtral to generate initial website theme
    pass

def generate_pages(website_theme, event_details, asset_images, html_structure=["index.html","contact.html","register.html","about.html"]):
    # Generate individual pages based on the theme
    # html structure accepts a list of page names e.g. ["index.html","contact.html","register.html","about.html"]
    # asset images accepts a list of asset image names (i.e. the list of files in the directory "images"), let the image names be descriptive
    html_list = [generate_page_content(website_theme, page, event_details, asset_images) for page in html_structure]
    return html_list

def generate_page_content(website_theme, page, event_details, asset_images):
    # Generate content for a single page
    prompt = f"""
    We are trying to build a single page {page} for a website for an event in html. 
    E.g. if the page is index.html it should contain a brief summary of the event, if contact.html generate contact etc.
    These are details of the event: {event_details}, 
    and furthermore the theme is {website_theme}. Also we have a list of images you can use, {" ".join(asset_images)}. make sure when sourcing these images you do images/imagename.png.
    The images are labelled by name so add ones you find relevant to the page. 
    """

    messages = [
        {"role": "user", "content": prompt}
    ]

    chat_response = client.chat.complete(
        model=MODELS["text"],
        messages=messages
    )
    cleaned_response = chat_response.choices[0].message.content
    return cleaned_response

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