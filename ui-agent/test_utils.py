from mistralai import Mistral
import os
import base64
import re 
import sys
import json
import traceback

api_key = os.getenv("MISTRAL_API_KEY")
client = Mistral(api_key=api_key)

MODELS = {
    "text": "mistral-large-latest",
    "image": "pixtral-12b-2409",
    "code": "codestral-mamba-latest",
}

def main(user_input):
    try:
        print(f"Received user input: {user_input}")
        
        # Parse user input
        event_details = generate_event_details(user_input)
        print(f"Generated event details: {event_details}")
        
        # Get reference images
        reference_images = get_reference_images(event_details)
        print(f"Got reference images: {reference_images}")
        
        # Generate website structure
        website_theme = generate_website_theme(event_details, reference_images)
        print(f"Generated website theme: {website_theme}")
        
        # Generate individual pages
        pages = generate_pages(website_theme, event_details, reference_images)
        print(f"Generated pages: {pages}")
        
        # Refine and optimize code
        image_dir = "../images"
        image_paths = list_file_names(image_dir)
        print(f"Image paths: {image_paths}")

        theme = generate_website_theme(event_details, image_dir)
        html = theme['html']
        css = theme['css']
        pages = generate_pages(css, html, event_details, image_paths)
        
        result = {
            "pages": pages,
            "css": css
        }
        
        # Publish the website and get the output directory
        output_dir = publish_website(pages, css)
        
        # Add the output directory to the result
        result["output_dir"] = output_dir
        
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({
            "error": str(e),
            "traceback": traceback.format_exc()
        }))
        sys.exit(1)

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


def list_file_names(directory_path):
    try:
        # Get the list of all files and directories in the specified path
        all_items = os.listdir(directory_path)
        
        # Filter out directories, keeping only files
        file_names = [item for item in all_items if os.path.isfile(os.path.join(directory_path, item))]
        
        return file_names
    except FileNotFoundError:
        print(f"Directory not found: {directory_path}")
        return []
    except PermissionError:
        print(f"Permission denied to access directory: {directory_path}")
        return []

def generate_website_theme(event_details, image_dir="/screenshots", html_structure=["index.html","contact.html","register.html","about.html"]):
    # Use Pixtral to generate initial website theme
    reference_images = list_file_names(image_dir)[:7]
    image_paths = [f"{image_dir}/{image_name}" for image_name in reference_images]
    images = [{"type": "image_url", "image_url": f"data:image/jpeg;base64,{_encode_image(path)}"} for path in image_paths]

    messages = [
        {
            "role": "system",
            "content": "You are an exceptionally skilled web designer. Create a modern, spectacular website theme based on requirements and loosely based on the provided images."
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"""Generate a website theme based on these images and the following requirements: {event_details}

                    Please provide:
                    1. A CSS file with very modern, responsive design and cool web design features
                    2. A basic HTML structure for the home page as well as a navbar which links to all of the other pages in {html_structure} (and contains all of those pages)
                    Make sure that the navbar actually links to the other pages, i.e. it has page_name.html as its href
                    3. Design tokens (colors, typography, spacing)
                    4. DO not add ```css or ```html, format only as below/

                    Format your response as follows:

                    [CSS]
                    (Your CSS code here)
                    [/CSS]

                    [HTML]
                    (Your HTML structure here)
                    [/HTML]

                    [DESIGN_TOKENS]
                    (Your design tokens here in JSON format)
                    [/DESIGN_TOKENS]

                    Ensure spectacular and modern design using latest web technologies and trends."""
                },
                *images
            ]
        }
    ]

    response = client.chat.complete(
        model=MODELS["image"],
        messages=messages
    )
    response_content = response.choices[0].message.content
        # Extract CSS, HTML, and design tokens
    css = re.search(r'\[CSS\](.*?)\[/CSS\]', response_content, re.DOTALL)
    html = re.search(r'\[HTML\](.*?)\[/HTML\]', response_content, re.DOTALL)
    design_tokens = re.search(r'\[DESIGN_TOKENS\](.*?)\[/DESIGN_TOKENS\]', response_content, re.DOTALL)
    
    css = css.group(1).strip() if css else ""
    html = html.group(1).strip() if html else ""
  
    
    return {
        "css": css,
        "html": html,
        "design_tokens": design_tokens
    }

def generate_pages(website_theme, html_example, event_details, asset_images, html_structure=["index.html","contact.html","register.html","about.html"]):
    # Generate individual pages based on the theme
    # html structure accepts a list of page names e.g. ["index.html","contact.html","register.html","about.html"]
    # asset images accepts a list of asset image names (i.e. the list of files in the directory "images"), let the image names be descriptive

    html_list = [generate_page_content(website_theme, html_example, page, event_details, asset_images) for page in html_structure]
    return html_list

def generate_page_content(website_theme, html_example, page, event_details, asset_images):
    # Generate content for a single page
    prompt = f"""
    Create a single-page '{page}' for a website based on the template '{html_example}' using HTML.

    - If the page is 'index.html', include a brief summary of the event. For 'contact.html', generate contact information, and so on, depending on the page type.
    - The event details are as follows: '{event_details}'.
    - The website's theme is: '{website_theme}'.
    - You may use the following images, use the full path else they will not work: {' '.join(asset_images)}. Include at least one image on the page, ensuring that images are relevant to the content when possible. Use the format 'images/imagename.png' to reference images.
    - PLEASE DO NOT ADD ANY EXTRA WORDS. DO NOT ADD ```html, DO NOT ADD "Certainly!". ADD NO EXTRA WORDS. 
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


def publish_website(refined_website, design, html_structure=["index.html","contact.html","register.html","about.html"]):
    # Change the output directory to a public folder accessible by Next.js
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'public', 'generated_website')
    os.makedirs(output_dir, exist_ok=True)

    # Save CSS
    css_path = os.path.join(output_dir, "styles.css")
    with open(css_path, 'w') as css_file:
        css_file.write(design)

    # Save HTML files
    for i, page in enumerate(html_structure):
        html_path = os.path.join(output_dir, page)
        with open(html_path, 'w') as html_file:
            html_file.write(refined_website[i])

    # Save JavaScript (empty for now)
    js_path = os.path.join(output_dir, "script.js")
    with open(js_path, 'w') as js_file:
        js_file.write("")

    return output_dir

def generate_images(image_requirements):
    # Use DALL-E API to generate images based on requirements
    # lets leave this one for now...
    pass


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
        main(user_input)
    else:
        print(json.dumps({"error": "No input provided"}))
        sys.exit(1)