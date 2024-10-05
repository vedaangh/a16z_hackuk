import asyncio
from pyppeteer import launch
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv
import os
from mistralai import Mistral
load_dotenv()
api_key = os.getenv('MISTRAL_API_KEY')
model = "mistral-large-latest"

hackathon_description = "MISTRAL AI hackathon, a hackathon to make projects with mistral ai"
extra_information = "This is the mistral logo: https://www.google.com/url?sa=i&url=https%3A%2F%2Fmedium.com%2Fenrique-dans%2Fmistrals-open-source-approach-a-breath-of-fresh-air-to-ai-while-it-lasts-941fc4a604d5&psig=AOvVaw1DCd93kDuG_qYDCt_1mL0F&ust=1728223938755000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCKDqlYG294gDFQAAAAAdAAAAABAE, mistral is an AI company, heres info from their website: Frontier AI in your hands Open and portable generative AI for devs and businesses. Also the aesthetic for mistral is orange and black so keep that in mind"
client = Mistral(api_key=api_key)
hackathon_description = "Mistral AI hackathon! Make a mistral ai project. Location CodeNode london"#input("Enter a description of your hackathon: ")
chat_response = client.chat.complete(
    model= model,
    messages = [
        {
            "role": "user",
            "content": """Generate html, js and css code for a website for a hackathon/event, including a large amount of text to populate the body of the website that is informative of the nature of the organisers with the description: {hackathon_description} and extra information about the event including images and such: MiSTRAL IS AN AI COMPANY AND STUFF AND LIKE HAS A ORANGE AND BLACK AESTHETIC This is the mistral logo: https://www.google.com/url?sa=i&url=https%3A%2F%2Fmedium.com%2Fenrique-dans%2Fmistrals-open-source-approach-a-breath-of-fresh-air-to-ai-while-it-lasts-941fc4a604d5&psig=AOvVaw1DCd93kDuG_qYDCt_1mL0F&ust=1728223938755000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCKDqlYG294gDFQAAAAAdAAAAABAE - use this extra information to inform the webdesign. Format your response as a dictionary of the sort: {"html"="Html code here", "js":"Js code here", "css":"Css code here"}. DO NOT ADD ANY OTHER TEXT, ONLY THE CODE DICTIONARY SHOWN, DO NOT ADD ```PYTHON``` EITHER. DO NOT ADD ANY EXCESS SPACES. I WILL BE PUTTING THIS INTO A PYTHON EVAL FUNCTION so that htmljscss = eval(code you generate)""",
        },
    ],
    temperature=0.0
)
htmljscss = chat_response.choices[0].message.content.replace("```python","").replace("```","").replace("json","")
html_js_css_code = eval(htmljscss)
print(htmljscss)


async def render_and_screenshot(html_content, css_content, js_content, output_path):
    # Launch the browser
    browser = await launch()
    page = await browser.newPage()

    # Create a temporary HTML file with the provided content
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

    # Navigate to the temporary file
    await page.goto(f'file://{temp_file_path}')

    # Wait for any JavaScript to execute (adjust the wait time as needed)
    await page.waitFor(1000)

    # Take a screenshot
    await page.screenshot({'path': output_path, 'fullPage': True})

    # Close the browser
    await browser.close()

# Example usage
html = html_js_css_code["html"]
css = html_js_css_code["css"]
js = html_js_css_code["js"]

asyncio.get_event_loop().run_until_complete(
    render_and_screenshot(html, css, js, 'firstoutput.png')
)


# NOW LETS GET PIXTRAL TO GIVE THE OTHER MODEL SOME FEEDBACK
import base64


# Retrieve the API key from environment variables


# Specify model
model2 = "pixtral-12b-2409"

# Initialize the Mistral client
client = Mistral(api_key=api_key)
# Define the image path
imgpath = 'firstoutput.png'

# Convert the image to a base64-encoded string
with open(imgpath, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
# Define the messages for the chat
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Evaluate the following screenshot from a websie from the perspective of a UI designer, giving tips to the website designer to make it more user friendly and aesthetically pleasing. This is supposed to be a website for a hackathon/event with the description: {hackathon_description} and extra information about the event including images and such: {extra_information}. PLEASE DONT GENERATE ANY CODE. ONLY GIVE FEEDBACK. NO CODE"
            },
            {
                "type": "image_url",
                "image_url": f"data:image/png;base64,{encoded_image}" 
            }
        ]
    }
]

# Get the chat response
chat_response = client.chat.complete(
    model=model2,
    messages=messages
)

# Print the content of the response
feedback = chat_response.choices[0].message.content

print(feedback)

chat_response = client.chat.complete(
    model= model,
    messages = [
        {
            "role": "user",
            "content": """Improve the given html, js and css code for a website for a hackathon/event with the description: {hackathon_description} and extra information about the event including images and such: {extra_information}. Location CodeNode london. This is the old code that must be improved, given as a python dictionary: {htmljscss}. The feedback is given here: {feedback}. Format your response as a dictionary of the sort: {"html"="Html code here", "js":"Js code here", "css":"Css code here"}. DO NOT ADD ANY OTHER TEXT, ONLY THE CODE DICTIONARY SHOWN, DO NOT ADD ```PYTHON``` EITHER. DO NOT ADD ANY EXCESS SPACES. I WILL BE PUTTING THIS INTO A PYTHON EVAL FUNCTION so that htmljscss = eval(code you generate). PLEASE ABIDE BY THAT LAST STATEMENT I WILL BE PUTTING THIS INTO A PYTHON EVAL ALLOW IT FAM""",
        },
    ],
    temperature=0.0
)


htmljscss = chat_response.choices[0].message.content.replace("```python","").replace("```","").replace("json","")
html_js_css_code = eval(htmljscss)

print("IMPROVED HTML JS CSS CODE!:")
print(htmljscss)

html2 = html_js_css_code["html"]
css2 = html_js_css_code["css"]
js2 = html_js_css_code["js"]


asyncio.get_event_loop().run_until_complete(
    render_and_screenshot(html2, css2, js2, 'improvedoutput.png')
)
