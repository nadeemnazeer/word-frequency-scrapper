from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import re


def get_page_html(url):
    try:
        print("Fetching..",url)
        payload = {}
        headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        }

        response = requests.request("GET", url, headers=headers, data = payload)

        return response.text
    except Exception as e:
        return ""

def clean_normalize_string(string):
    #find and replace alphanumeric chars with single spaces
    string = re.sub(r'[^a-zA-Z0-9\s]', ' ', string)
    return string.lower()


def compose_ngrams(string, n):
    
    string = clean_normalize_string(string)
    
    #Remove empty tokens
    tokens = list(filter(None, string.split(" ")))

    
    # Use the zip function to help us generate n-grams
    # Concatentate the tokens into ngrams and return
    ngrams = zip(*[tokens[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]


def get_visible_tag(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta','[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def get_internal_links(soup, scrap_domains):
    link_list = set()
    for link in soup.find_all('a', href=True):
        href = link['href']
        for domain in scrap_domains:
            if domain in href:
                link_list.add(link['href'])
    return link_list
    
url_visited = []
def get_sentence_ngrams_list(url,scrap_domains, ngram=1,max_level=4, level=1):
    url_visited.append(url)
    ngramlist = []
    #TODO: Can be improved by checking if url already fetched
    
    body = get_page_html(url)
    body = body.replace("<br />","")
    soup = BeautifulSoup(body, 'html.parser')
    #print(get_internal_links(soup))

    texts = soup.findAll(text=True)
    texts_visible_tags = filter(get_visible_tag, texts)
    sentences = []
    for text in  filter(None, texts_visible_tags):
        sub_sentences = text.strip().lower().split(".")
        sentences.extend(sub_sentences)

    
    for sentence in sentences:
        ngramlist.extend(compose_ngrams(sentence, ngram))
    for link in get_internal_links(soup,scrap_domains):
        if level > max_level:
            return ngramlist
        else:
            level += 1
            if link not in url_visited:
                ngramlist.extend(get_sentence_ngrams_list(link,scrap_domains, ngram, level, max_level))
    return ngramlist



def get_freq_words(url, scrap_domains, ngram=1,top=10, max_level=4):
    sentence_ngrams_list = get_sentence_ngrams_list(url,scrap_domains, ngram,max_level)
    ngramfreq = [sentence_ngrams_list.count(ngram) for ngram in sentence_ngrams_list]
    unique_ngram_freq = set(zip(sentence_ngrams_list, ngramfreq))
    sorted_by_freq = sorted(unique_ngram_freq, key=lambda tup:tup[1], reverse=True)
    print(sorted_by_freq[:top])
    
    

    
get_freq_words('https://www.nytimes.com/',["nytimes.com"], ngram=2,top=10, max_level=4)
#Test data to check against view:source via browser
#[('know more', 6), ('healthcare it', 5), ('cures act', 5), ('ehr help', 4), ('go live', 4)