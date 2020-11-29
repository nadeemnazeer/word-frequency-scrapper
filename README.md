
#  word-frequency-scrapper

Tool to scrap any website and fetch top ngrams with their frequency. 
# For standalone run
**Install dependencies**

    pip install -r requirements.txt

**Run** 

    python core.py --url="https://www.314e.com/" --scrap_domains="314e.com"  --ngram=1 --top=10 --max_level=4

**Argument(s) description:**

 - **--url**: Base url to scrap. 
 - **--scrap_domains**: For ignoring any external url links; provide a comma separated list of domains to restrict scraping and crawling to. 
 - **--ngrams**: ngrams value, put **ngrams = 1**  for for seeing consolidated top 10 frequent words and put **ngrams = 2** for the top 10 frequent word pairs (two words in the same order) along with their frequency.
 - **--top**: Top limit to return, e.g: 10 to return top to words.
 - **--max_level**: Max level to crawl & scrap; maximum number of levels you want to expand for urls within a url.

**For help:**

    python grpc_client.py --help
It will show all the information needed to run:


    Tool to scrap any website and fetch top ngrams with their frequency. e.g: python grpc_client.py --url="https://www.washingtonpost.com/" --scrap_domains="washingtonpost.com"
    --ngram=1 --top=10 --max_level=4
    
    optional arguments:
      -h, --help            show this help message and exit
      --url URL             Base url to scrap.
      --scrap_domains SCRAP_DOMAINS
                            **For ignoring any external url links; provide a comma seperated list of domains to restrict scraping and cralwing to.
      --ngrams NGRAMS       ngrams value
      --top TOP             Top limit
      --max_level MAX_LEVEL
                            Max level to cralw & scrap; maximum number of levels you want to expand for urls within a url.
      --version             show program's version number and exit

> Put, 
> **ngrams = 1** : For for seeing consolidated top 10 frequent words 
> **ngrams = 2** : For the top 10 frequent word pairs (two words in the same order) along with their frequency

## Example output(s):
With params: --url="https://www.314e.com/" --scrap_domains="314e.com"  --ngram=2 --top=10 --max_level=4
**For the top 10 frequent word pairs:**
    
    INFO:root:Fetched https://www.314e.com/ , Level: 1
    INFO:root:Computing ngram frequency for url https://www.314e.com/ ..
    INFO:root:Fetched https://www.314e.com/services/healthcare-it-staff-augmentation/ , Level: 4
    ...
    cures act 156
    healthcare it 127
    cloud adoption 110
    services ehr 108
    go live 108
    big data 94
    muspell cdr 87
    business intelligence 87
    our team 86
    muspell automaton 84


**For for seeing consolidated top 10 frequent words:** 
With params: --url="https://www.314e.com/" --scrap_domains="314e.com"  --ngram=1 --top=10 --max_level=4

    and 781
    data 574
    the 532
    to 525
    services 475
    ehr 457
    314e 407
    of 391
    it 336
    solutions 313
## To run unit tests

    python -m unittest

## Logging description
Logs are of the format:
INFO: < url > < level >
INFO:Computing ngram frequency for url < url >
e.g:

    INFO:root:Fetched https://www.314e.com/ , Level: 1
    INFO:root:Computing ngram frequency for url https://www.314e.com/ ..


 

# As standalone gRPC service

## Build docker:

    docker build -t freqscrapper .
## Run docker:

    docker run -d -p 50051:50051 freqscrapper
## Run gRPC client:

    python grpc_client.py --url="https://www.314e.com/" --scrap_domains="314e.com"  --ngram=1 --top=10 --max_level=4
    

>   1. Arguments will remain same as that of standalone run as shown above.
>   2. You will need to install dependencies to run this client.

## Code description:

**Core logic of the app:** https://github.com/nadeemnazeer/word-frequency-scrapper/blob/develop/core.py
Entry class/function to code:

    fs = FreqScrapper(url,scrap_domains)
    rows = fs.get_freq_words(ngrams,top, max_level)

## TODO(s):
- Not tested on AJAX/ASP Pages  
- OCR for content that is put as images on the website
- Stopwords
- TFIDF - to get the actual sense of what is mentioned as important on page  
-   There can be other terms of same weight as that of last one - but we are showing only 10
- F1 Scoring to get the sense of how is our extraction doing.
