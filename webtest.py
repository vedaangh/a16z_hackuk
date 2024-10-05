import os
import requests
from tempfile import NamedTemporaryFile
from pyppeteer import launch
import asyncio

async def download_resource(url, local_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, 'wb') as f:
            f.write(response.content)

async def process_external_resources(html_content):
    # Parse for external resources (This is a simple example and might need improvement)
    resources = []
    
    # Example of finding <link> and <script> tags in the HTML
    # You could use BeautifulSoup for more complex parsing
    if '<link ' in html_content:
        # Extract link hrefs
        # (Implement parsing logic here to extract actual URLs)
        resources.append("https://example.com/external.css")
    
    if '<script ' in html_content:
        # Extract script srcs
        # (Implement parsing logic here to extract actual URLs)
        resources.append("https://example.com/external.js")

    # Download resources
    for resource in resources:
        filename = os.path.basename(resource)
        local_path = os.path.join('local_resources', filename)
        download_resource(resource, local_path)
        html_content = html_content.replace(resource, local_path)  # Update the HTML to use local path

    return html_content

async def render_and_screenshot(html_content, css_content, js_content, output_path):
    browser = await launch()
    page = await browser.newPage()

    # Combine HTML, CSS, and JS
    full_html_content = f"""
    <html>
    <head>
        <style>{css_content}</style>
    </head>
    <body>
        {html_content}
        <script>{js_content}</script>
    </body>
    </html>
    """

    # Process external resources
    processed_html = await process_external_resources(full_html_content)

    with NamedTemporaryFile(mode='w', suffix='.html', delete=False) as temp_file:
        temp_file.write(processed_html)
        temp_file_path = temp_file.name

    await page.goto(f'file://{temp_file_path}')
    await page.waitFor(1000)
    await page.screenshot({'path': output_path, 'fullPage': True})
    await browser.close()

# Example usage
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image from the Internet</title>
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f0f0f0;
        }
        img {
            max-width: 100%;
            height: auto;
            border: 2px solid #ccc;
            border-radius: 8px;
        }
    </style>
</head>
<body>
    <img src="https://via.placeholder.com/600" alt="Placeholder Image">
</body>
</html>


"""


css_content = ""
js_content = ""
output_file = 'screenshot.png'


async def main():
    await render_and_screenshot(html_content, css_content, js_content, output_file)

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())