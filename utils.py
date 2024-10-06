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

def generate_event_details(user_input):
    # Generate event details from user input

    prompt = f"""
    You are an AI assistant helping to create a website for an event based on a user's input. The input might be vague or minimal. Your task is to expand on this input and provide rich context for website generation.

    Given the user input: "{user_input}"

    1. Interpret the core idea of the event.
    2. Imagine and describe key aspects that would be relevant for creating a website.
    3. Suggest a theme, style, or mood that would suit this event.
    4. If any specific details are mentioned (like date, location, etc.), include them. If not, do not mention them, or add TBD.
    5. If no specific design details are given, feel free to creatively fill in gaps that would help in website design.

    Provide your response as a concise paragraph or two, focusing on elements that would inspire and guide the creation of a spectacular, modern website. Your output will be used directly in further prompts for website generation, so make it rich and descriptive.
    """

    messages = [
        {"role": "system", "content": "You are a creative event planner and web designer, skilled at interpreting client needs and expanding on minimal information."},
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

def _encode_image(image_path: str) -> str:
    # Encode image to base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_website_theme(event_details, reference_images, image_dir="/screenshots"):
    image_paths = [f"{image_dir}/{image_name}" for image_name in reference_images]
    images = [{"type": "image_url", "image_url": f"data:image/jpeg;base64,{_encode_image(path)}"} for path in image_paths]

    base_css = """
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@200;300;400;500;600;700;800&display=swap');

    :root {
        --primary-color: #4a90e2;
        --secondary-color: #50e3c2;
        --text-color: #333333;
        --background-color: #f5f5f5;
    }

    body {
        font-family: 'Manrope', sans-serif;
        margin: 0;
        padding: 0;
        background-color: var(--background-color);
        color: var(--text-color);
    }

    .header {
        background-color: #ffffff;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        padding: 1rem 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .header nav a {
        margin-left: 1rem;
        text-decoration: none;
        color: var(--text-color);
        font-weight: 500;
    }

    .main-content {
        max-width: 1200px;
        margin: 2rem auto;
        padding: 0 2rem;
    }

    .hero {
        text-align: center;
        padding: 4rem 0;
    }

    .hero h1 {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .cta-button {
        display: inline-block;
        background-color: var(--primary-color);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 5px;
        text-decoration: none;
        font-weight: 600;
        transition: background-color 0.3s ease;
    }

    .cta-button:hover {
        background-color: var(--secondary-color);
    }
    """

    base_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{event_name}</title>
        <link rel="stylesheet" href="styles.css">
    </head>
    <body>
        <header class="header">
            <div class="logo">{event_name}</div>
            <nav>
                <a href="#about">About</a>
                <a href="#schedule">Schedule</a>
                <a href="#register">Register</a>
            </nav>
        </header>
        <main class="main-content">
            <section class="hero">
                <h1>{event_headline}</h1>
                <p>{event_description}</p>
                <a href="#register" class="cta-button">Register Now</a>
            </section>
            <!-- Additional sections to be generated dynamically -->
        </main>
    </body>
    </html>
    """

    messages = [
        {
            "role": "system",
            "content": "You are a web designer tasked with customizing and enhancing a base website theme for an event."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""Customize and enhance the following base CSS and HTML for this event: {event_details}

                    Base CSS:
                    {base_css}

                    Base HTML:
                    {base_html}

                    Instructions:
                    1. Modify the color scheme to suit the event theme.
                    2. Add additional CSS for creative layouts and modern design elements.
                    3. Enhance the HTML structure with more sections relevant to the event.
                    4. Incorporate subtle animations or transitions for interactive elements.
                    5. Ensure the design is responsive and works well on all devices.

                    Provide the following:

                    [CSS]
                    (Your enhanced CSS code here, including the base CSS with your modifications)
                    [/CSS]

                    [HTML]
                    (Your enhanced HTML structure here, based on the base HTML with your additions)
                    [/HTML]

                    [DESIGN_TOKENS]
                    (Your design tokens here in JSON format, including color schemes, typography, spacing, and breakpoints)
                    [/DESIGN_TOKENS]

                    Ensure the design is visually appealing, modern, and aligns with the event's theme while maintaining usability and accessibility."""
                },
                *images
            ]
        }
    ]

    chat_response = client.chat.complete(
        model=MODELS["image"],
        messages=messages
    )
    
    return chat_response.choices[0].message.content
    

def generate_pages(website_theme, event_details, asset_images, html_structure=["index.html","contact.html","register.html","about.html"]):
    # Generate individual pages based on the theme
    # html structure accepts a list of page names e.g. ["index.html","contact.html","register.html","about.html"]
    # asset images accepts a list of asset image names (i.e. the list of files in the directory "images"), let the image names be descriptive
    html_list = [generate_page_content(website_theme, page, event_details, asset_images) for page in html_structure]
    return html_list

def generate_page_content(website_theme, html_example, page, event_details, asset_images):
    # Generate content for a single page
    prompt = f"""
    We are trying to build a single page {page} for a website for an event in html based upon the template of {html_example}. 
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