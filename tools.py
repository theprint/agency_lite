import requests
import datetime
import config
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote

# Method for generating a responce from the LLM
def getResponse(prompt, agent, client):
    print("Getting response from AI ...")
    response = client.chat.completions.create(
                model=agent.model,
                messages=[
                    {"role": "system", "content": agent.role},
                    {"role": "system", "content": agent.description},
                    {"role": "user", "content": prompt}
                ]
            )
    return response.choices[0].message.content

# Shortens text that is larger the max chunk size, defined in config.py
def shorten(text, agent, client):
    if (len(text) > config.MAX_CHUNK_SIZE):
        print(f"Response was {len(text)} characters long. Shortening to max. {config.MAX_CHUNK_SIZE} characters.")
        text = getResponse(f"Shorten the following text while maintaining the link, all main points and arguments. Make sure the summary is under {config.MAX_CHUNK_SIZE} characters. The final output should have: a headline, the summary, and MUST include the link URL to the source story. TEXT TO SHORTEN: {text}", agent, client)
        return text


# Searches duckduckgo.com for something, extracts and cleans the source links from the results.
def simple_web_search(query, limit=10):
    url = f"https://www.duckduckgo.com/html/?q={query}&ia=news"
    headers = {'User-Agent': 'Mozilla/5.0'}

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = soup.findAll('a', class_='result__url', limit=config.MAX_SEARCH_RESULTS)
    urls = [link['href'] for link in links[:limit]]  # Apply limit

    lid = 0
    for link in urls:
        urls[lid] = extract_actual_url(link)
        lid += 1

    return urls


# Converts a search result url to the source it is point to
def extract_actual_url(redirect_url):
    # Ensure the URL starts with http(s):// for urlparse to work correctly
    if not redirect_url.startswith(('http:', 'https:')):
        redirect_url = 'https:' + redirect_url

    parsed_url = urlparse(redirect_url)
    query_string = parse_qs(parsed_url.query)
    actual_url = query_string.get('uddg', [''])[0]  # Extract the URL and default to '' if not found

    # URL-decode the extracted URL
    actual_url_decoded = unquote(actual_url)
    return actual_url_decoded


# Attempts to scrape the content of a given URL, and clean up the returned text.
def scrape(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    content = ""
    try:
        response = requests.get(url, headers=headers)
        print(f" - Status code {response.status_code} for URL: {url}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # List of tuples containing tag names and their possible attributes for main content
            wrappers = [
                ('div', {'id': 'content'}),
                ('div', {'class': 'content'}),
                ('main', {}),
                ('article', {}),
                ('section', {}),
                ('div', {'id': 'main-content'}),
                ('div', {'class': 'main-content'}),
                ('div', {'id': 'page'}),
                ('div', {'class': 'page'}),
            ]


            for tag, attributes in wrappers:
                content_element = soup.find(tag, attributes)
                if content_element:
                    content += content_element.get_text(separator="\n", strip=True)
                    content += f"\n LINK: {url}"
        else:
            content = "Content missing - please ignore this text."
    except:
        print(f" - Bad connection, skipping {url}.")
        pass

    return content


# Saves a timestamped output file.
def save_file(input_string):
    print("Saving ...")
    # Generate a timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"output/output_{timestamp}.txt"

    # Save the input string to a file with the generated filename
    with open(filename, 'w+') as file:
        file.write(input_string)

    return filename
