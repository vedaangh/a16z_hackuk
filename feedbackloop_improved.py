import asyncio
from pyppeteer import launch
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv
import os
from mistralai import Mistral
import base64
import tools 





load_dotenv()
api_key = os.getenv('MISTRAL_API_KEY') # Replace with your actual API key
model = "mistral-large-latest"
model2 = "pixtral-12b-2409"

client = Mistral(api_key=api_key)

hackathon_description = "Mistral AI hackathon! Make a mistral ai project. "

brave_api_key = os.getenv("BRAVE_API_KEY")

search_tool = tools.SearchTooling(brave_api_key)
results = search_tool.search_web_information("Mistral AI hackathon")
print("Search Results:")
print(results)


def clean_output(output):
    return output.replace("```python", "").replace("```", "").replace("\n", "").replace("    ", "")

def use_search(results):
        prompt = f""" These are results given by search tools {results}, extract useful information about the event or company given by the user from {hackathon_description} and compile into an informative block of text"""
    
        chat_response = client.chat.complete(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=100
        )
    
        cleaned_response = clean_output(chat_response.choices[0].message.content)
        return str(cleaned_response)


useful_information = use_search(results)








def generate_website_code():

    prompt = f"""
    Generate HTML, JS, and CSS code for a website for the MISTRAL AI HACKATHON.
    Include text explaining what Mistral AI is and what people can build with the Mistral API.
    Use an orange, white, and black aesthetic for the web design.
    Use tailwind.css for sure. 
    The hackathon description is: {hackathon_description}
    Additional text to integrate into the website: {useful_information}
    Format your response as a Python dictionary with keys "html", "js", and "css".
    DO NOT ADD ANY OTHER TEXT, ONLY THE CODE DICTIONARY SHOWN.
    DO NOT ADD ```PYTHON``` OR ANY OTHER MARKDOWN.
    DO NOT ADD ANY EXCESS SPACES.
    The response will be put into a Python eval() function.
    """
    
    chat_response = client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    
    cleaned_response = clean_output(chat_response.choices[0].message.content)
    return eval(cleaned_response)

async def render_and_screenshot(html_content, css_content, js_content, output_path):
    browser = await launch()
    page = await browser.newPage()

    with NamedTemporaryFile(mode='w', suffix='.html', delete=False) as temp_file:
        temp_file.write(f"""
        <html>
        <head>
            <style>{css_content}</style>
        </head>
        <body>
            {html_content}
            <script>{js_content}</script>
        </body>
        </html>
        """)
        temp_file_path = temp_file.name

    await page.goto(f'file://{temp_file_path}')
    await page.waitFor(1000)
    await page.screenshot({'path': output_path, 'fullPage': True})
    await browser.close()

def get_feedback(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Evaluate this screenshot of a website for the Mistral AI Hackathon. Make sure to comment on the density of text and stuff. Provide specific, actionable feedback to improve the design, user-friendliness, and aesthetics. Consider the hackathon description: {hackathon_description} and this additional information: {useful_information}. Focus on layout, color scheme, typography, and overall user experience. Do not generate code, only provide feedback."
                },
                {
                    "type": "image_url",
                    "image_url": f"data:image/png;base64,{encoded_image}" 
                }
            ]
        }
    ]

    chat_response = client.chat.complete(
        model=model2,
        messages=messages
    )

    return chat_response.choices[0].message.content

def improve_website_code(original_code, feedback):
    prompt = f"""
    Improve the design of the following website code for the Mistral AI Hackathon based on this feedback:
    {feedback}
    
    Original code:
    {original_code}
    
    Provide your response as a Python dictionary with keys "html", "js", and "css".
    DO NOT ADD ANY OTHER TEXT, ONLY THE CODE DICTIONARY SHOWN.
    DO NOT ADD ```PYTHON``` OR ANY OTHER MARKDOWN.
    DO NOT ADD ANY EXCESS SPACES.
    The response will be put into a Python eval() function.
    Maintain the overall structure and content, but implement the suggested improvements.
    Focus on enhancing the layout, color scheme, typography, and user experience.
    """
    
    chat_response = client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    
    cleaned_response = clean_output(chat_response.choices[0].message.content)
    return eval(cleaned_response)

async def main():
    # Generate initial website code
    initial_code = generate_website_code()
    
    # Render and screenshot the initial website
    n = 5
    await render_and_screenshot(initial_code["html"], initial_code["css"], initial_code["js"], 'improved_output_-1.png')
    for x in range(n):


        
        # Get feedback on the initial design
        feedback = get_feedback('improved_output_{0}.png'.format(str(x-1)))
        print("Feedback:", feedback)
        
        # Improve the website code based on feedback
        improved_code = improve_website_code(initial_code, feedback)
        
        # Render and screenshot the improved website
        await render_and_screenshot(improved_code["html"], improved_code["css"], improved_code["js"], 'improved_output_{0}.png'.format(str(x)))
        initial_code = improved_code
    final_code = initial_code

        # Create the "website" directory
    os.makedirs("website", exist_ok=True)

    # Save CSS
    css_path = os.path.join("website", "styles.css")
    with open(css_path, 'w') as css_file:
        css_file.write(final_code["css"])

    # Save HTML
    html_path = os.path.join("website", "index.html")
    with open(html_path, 'w') as html_file:
        html_file.write(final_code["html"])

    # Save JavaScript
    js_path = os.path.join("website", "script.js")
    with open(js_path, 'w') as js_file:
        js_file.write(final_code["js"])

    print("Website generation process completed. Check 'initial_output.png' and 'improved_output.png' for results. Also check the directory - website")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())