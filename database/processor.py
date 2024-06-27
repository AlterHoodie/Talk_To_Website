import json
import requests
from bs4 import BeautifulSoup 
import os
import time
from crawl4ai.web_crawler import WebCrawler
from crawl4ai.chunking_strategy import *
from crawl4ai.extraction_strategy import *
from crawl4ai.crawler_strategy import *
from rich import print
from rich.console import Console
from functools import lru_cache
import json
import re
console = Console()

@lru_cache()
def create_crawler():
    crawler = WebCrawler()
    crawler.warmup()
    return crawler

def cprint(message, press_any_key=False):
    # console.print(message)
    pass

# Function to check if a tag is a link

def is_link(tag,url_links):
    seen=False
    if tag.name == 'a' or tag.name=="span":
        # href = tag.get('href')
        # if href:
        #     if href in url_links:
        #         seen = True
        #     else:
        #         # print(tag.text)
        #         url_links.append(href)
        seen = bool(re.search(r'\d+\.\d+\.\d+',tag.text)) or bool(re.search(r'\d+\.\d+',tag.text)) or bool(re.search(r'Criteria\s+(\d+)\s*',tag.text))
        # if tag.text.replace("\n","")!="":
        #     print(tag.text,bool(re.search(r'Criteria\s+(\d+)\s*',tag.text)))
        # print(tag.get("class")
    if tag.text in ["NAAC","DVV","PESU Academy","About","Campus Life","Criteria","Faculty of Engineering","Admissions","Campuses","Departments","Faculty of Engineering"]:
        ele = tag.NextSibling
        while ele:
            ele.decompose()
            ele=  ele.NextSibling
        seen=True
    return seen or tag.name=="header" or tag.name=="footer"


def is_empty(element):
    return  element.text.replace("\n","")==""

def without_chunking_strategy(url,crawler,html):
    cprint("\n🔍 [bold cyan]Time to explore another chunking strategy: NlpSentenceChunking![/bold cyan]", True)
    result = crawler.run_html(
        url=url,
        # css_selector = "p",
        html=html,
        chunking_strategy=NlpSentenceChunking()
    )
    cprint("[LOG] 📦 [bold yellow]NlpSentenceChunking result:[/bold yellow]")
    # print_result(result)
    return result


def add_chunking_strategy(url,crawler,html):
    cprint("\n🔍 [bold cyan]Time to explore another chunking strategy: NlpSentenceChunking![/bold cyan]", True)
    cprint("NlpSentenceChunking uses NLP techniques to split the text into sentences. Let's see how it performs!")
    result = crawler.run_html(
        url=url,
        # css_selector = "p",
        html=html,
        chunking_strategy=NlpSentenceChunking(),
        extraction_strategy = CosineStrategy(word_count_threshold=10, max_dist=0.2, linkage_method="ward", top_k=3, sim_threshold = 0.1, verbose=True)
    )
    cprint("[LOG] 📦 [bold yellow]NlpSentenceChunking result:[/bold yellow]")
    # print_result(result)
    return result


def processor(url,html,crawler,url_links,token_threshold=150):
        soup = BeautifulSoup(html, 'html.parser')
        # Remove all links
        for link in soup.find_all(lambda tag:is_link(tag,url_links)):
            if link.nextSibling and link.nextSibling.name=="span":
                link.nextSibling.decompose()
            link.decompose()
        for link in soup.find_all(is_empty):
            link.decompose()

        
        html = soup.prettify()
        # print(html)
        # print(result)
        result=add_chunking_strategy(url,crawler,html)
        if result.success==False:
            print("Failed to extract using cosing strategy")
            result = without_chunking_strategy(url,crawler,html)
        extracted_content = json.loads(result.extracted_content)
        chunks=[]
        i=0
        while i<len(extracted_content):
            chunk=""
            while i<len(extracted_content) and len(chunk.split())<token_threshold:
                chunk+=extracted_content[i]['content']
                i+=1
            chunks.append(chunk)
        return chunks





