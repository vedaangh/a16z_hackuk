import asyncio
from pyppeteer import launch
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv
import os
from mistralai import Mistral
import base64

load_dotenv()
api_key = os.getenv('MISTRAL_API_KEY') # Replace with your actual API key
model = "mistral-large-latest"
model2 = "pixtral-12b-2409"

client = Mistral(api_key=api_key)

hackathon_description = "Mistral AI hackathon! Make a mistral ai project. Location CodeNode london"
extra_information = """
This is the mistral logo: https://www.google.com/url?sa=i&url=https%3A%2F%2Fmedium.com%2Fenrique-dans%2Fmistrals-open-source-approach-a-breath-of-fresh-air-to-ai-while-it-lasts-941fc4a604d5&psig=AOvVaw1DCd93kDuG_qYDCt_1mL0F&ust=1728223938755000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCKDqlYG294gDFQAAAAAdAAAAABAE
Mistral is an AI company. Here's info from their website: Frontier AI in your hands. Open and portable generative AI for devs and businesses.
The aesthetic for Mistral is orange and black, so keep that in mind.
"""

def clean_output(output):
    return output.replace("```python", "").replace("```", "").replace("\n", "").replace("    ", "")

def generate_website_code():
    prompt = f"""
    Generate HTML, JS, and CSS code for a website for the MISTRAL AI HACKATHON.
    Include text explaining what Mistral AI is and what people can build with the Mistral API.
    Use an orange, white, and black aesthetic for the web design.
    The hackathon description is: {hackathon_description}
    Additional information: {extra_information}
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
                    "text": f"Evaluate this screenshot of a website for the Mistral AI Hackathon. Provide specific, actionable feedback to improve the design, user-friendliness, and aesthetics. Consider the hackathon description: {hackathon_description} and this additional information: {extra_information}. Focus on layout, color scheme, typography, and overall user experience. Do not generate code, only provide feedback."
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
    
    print("Website generation process completed. Check 'initial_output.png' and 'improved_output.png' for results.")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())