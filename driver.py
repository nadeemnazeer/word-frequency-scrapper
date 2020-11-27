from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
import re


def get_page_html(url):
    payload = {}
    headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    return response.text

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


def get_freq_words(url, ngram=1):
    body = get_page_html(url)
    body = body.replace("<br />","")
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    texts_visible_tags = filter(get_visible_tag, texts)
    #filter(texts_visible_tags)
    sentences = []
    for text in  filter(None, texts_visible_tags):
        sub_sentences = text.strip().lower().split(".")
        sentences.extend(sub_sentences)

    wordlist = []
    for sentence in sentences:
        wordlist.extend(compose_ngrams(sentence, ngram))
    wordfreq = [wordlist.count(w) for w in wordlist]
    lt = set(zip(wordlist, wordfreq))
    sorted_by_freq = sorted(lt, key=lambda tup:tup[1], reverse=True)
    print(sorted_by_freq[:15])


    

    
get_freq_words('https://www.314e.com/',3)
#Test data to check against view:source via browser
#[('know more', 6), ('healthcare it', 5), ('cures act', 5), ('ehr help', 4), ('go live', 4)