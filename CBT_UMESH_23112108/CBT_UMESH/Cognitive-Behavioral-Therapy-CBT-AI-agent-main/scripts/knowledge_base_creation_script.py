import requests
from bs4 import BeautifulSoup
import os
import re

# URLs for CBT knowledge
urls = {
    "verywellmind": "https://www.verywellmind.com/what-is-cognitive-behavioral-therapy-2795747",
    "nhs": "https://www.nhs.uk/mental-health/talking-therapies-medicine-treatments/talking-therapies-and-counselling/cognitive-behavioural-therapy-cbt/",
    "apa": "https://www.apa.org/ptsd-guideline/patients-and-families/cognitive-behavioral",
    "psychologytoday": "https://www.psychologytoday.com/us/therapy-types/cognitive-behavioral-therapy"
}

# Create knowledge base folder
os.makedirs("knowledge_base", exist_ok=True)

def clean_text(text):
    # Remove multiple spaces, newlines, references like [1]
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\[[0-9]+\]', '', text)
    return text.strip()

def scrape_and_save(name, url):
    print(f"Scraping {name}...")
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract paragraphs
    paragraphs = soup.find_all("p")
    content = " ".join([p.get_text() for p in paragraphs])
    content = clean_text(content)

    # Save into text file
    file_path = os.path.join("knowledge_base", f"{name}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Saved {name}.txt")

# Scrape all URLs
for name, url in urls.items():
    scrape_and_save(name, url)

print("✅ Knowledge base created in 'knowledge_base/' folder")
