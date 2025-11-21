import httpx
import xml.etree.ElementTree as ET

ARXIV_API_URL = "https://export.arxiv.org/api/query"

import random

async def search_arxiv(query: str, start: int = 0, max_results: int = 10, sort_by: str = "submittedDate", sort_order: str = "descending"):
    params = {
        "search_query": f"all:{query}",
        "start": start,
        "max_results": max_results,
        "sortBy": sort_by,
        "sortOrder": sort_order
    }
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(ARXIV_API_URL, params=params)
        response.raise_for_status()
        
    return parse_arxiv_response(response.text)

async def get_random_paper():
    topics = [
        "Artificial Intelligence", "Climate Change", "Quantum Computing", "Neuroscience", 
        "Astrophysics", "Machine Learning", "Biotechnology", "Robotics", 
        "Cryptography", "Genomics", "Nanotechnology", "Renewable Energy"
    ]
    topic = random.choice(topics)
    
    # Randomize start index to get different papers each time
    start_index = random.randint(0, 100)
    
    # Get a few results and pick one randomly
    papers = await search_arxiv(topic, start=start_index, max_results=5)
    if papers:
        return random.choice(papers)
    return None

def parse_arxiv_response(xml_data: str):
    root = ET.fromstring(xml_data)
    ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
    
    papers = []
    for entry in root.findall('atom:entry', ns):
        paper = {
            "id": entry.find('atom:id', ns).text,
            "title": entry.find('atom:title', ns).text.strip().replace('\n', ' '),
            "summary": entry.find('atom:summary', ns).text.strip().replace('\n', ' '),
            "authors": [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)],
            "published": entry.find('atom:published', ns).text,
            "pdf_url": next((link.attrib['href'] for link in entry.findall('atom:link', ns) if link.attrib.get('title') == 'pdf'), None)
        }
        papers.append(paper)
        
    return papers
