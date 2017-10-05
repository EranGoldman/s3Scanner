"""Simple Python 3 web crawler, to be scan for s3 buckets in sites.

Prerequisites:
pip install requests
pip install beautifulsoup4
"""
import collections
import string

from timeit import default_timer
from urllib.parse import urldefrag, urljoin, urlparse

import bs4
import requests

import redis
import re

#------------------------------------------------------------------------------
def crawler(maxpages=1000000):
    """Crawl the web starting from specified page.

    1st parameter = URL of starting page
    maxpages = maximum number of pages to crawl
    singledomain = whether to only crawl links within startpage's domain
    """

    r = redis.Redis(
        host='localhost',
        port=6379)

    pages = 0 # number of pages succesfully crawled so far
    failed = 0 # number of links that couldn't be crawled

    sess = requests.session() # initialize the session
    requests.packages.urllib3.disable_warnings()
    lastKey = int(r.get('lastKey'))
    firstKey = int(r.get('firstKey'))
    while lastKey > firstKey:
        url = r.get(firstKey).decode("utf-8")

        firstKey += 1
        r.set('firstKey',firstKey)
        try:
            flag = forbiddenDomains(url)
        except:
            continue
        if flag:
            print("PASS :",url)
            continue
        # read the page
        try:
            headers = {'Accept-Encoding': 'deflate'}
            response = sess.get(url,verify=False, headers=headers)
        except (requests.exceptions.MissingSchema,
                requests.exceptions.InvalidSchema):
            print("*FAILED*:", url)
            failed += 1
            continue
        if 'content-type' in response.headers and not response.headers['content-type'].startswith('text/html'):
            continue # don't crawl non-HTML content

        # Note that we create the Beautiful Soup object here (once) and pass it
        # to the other functions that need to use it
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        # process the page
        r.set(url,1)
        pages += 1
        if pagehandler(url, response, soup) and lastKey < maxpages:
            # get the links from this page and add them to the crawler queue
            links = getlinks(url, soup)
            for link in links:
                if not url_in_db(link):
                    r.set(lastKey,link)
                    lastKey += 1
                    r.set('lastKey',lastKey)

    print('{0} pages crawled, {1} links failed.'.format(pages, failed))

#-------------------------------------------------------------------------------
def forbiddenDomains(url):
    """Checks if a domain is in the do not crawl list
    The domain are in the db under the forbiddenDomains key
    It's a list of domains separated by comma (,)
    """
    r = redis.Redis(
        host='localhost',
        port=6379)
    fd = r.get("forbiddenDomains").decode("utf-8")
    d = getDomainOnly(url)
    return d in fd

#------------------------------------------------------------------------------
def getlinks(pageurl, soup):
    """Returns a list of links from from this page to be crawled.

    pageurl = URL of this page
    domain = domain being crawled (None to return links to *any* domain)
    soup = BeautifulSoup object for this page
    """

    # get target URLs for all links on the page
    links = [a.attrs.get('href') for a in soup.select('a[href]')]

    # remove fragment identifiers
    links = [urldefrag(link)[0] for link in links]

    # remove any empty strings
    links = [link for link in links if link]

    # if it's a relative link, change to absolute
    links = [link if bool(urlparse(link).netloc) else urljoin(pageurl, link) \
        for link in links]

    return links

#------------------------------------------------------------------------------
def pagehandler(pageurl, pageresponse, soup):
    """Function to be customized for processing of a single page.

    pageurl = URL of this page
    pageresponse = page content; response object from requests module
    soup = Beautiful Soup object created from pageresponse

    Return value = whether or not this page's links should be crawled.
    """
    print('Crawling:' + pageurl + ' ({0} bytes)'.format(len(pageresponse.text)))
    # wordcount(soup) # display unique word counts
    searchBuckets(soup,pageurl)
    return True

def searchBuckets(soup,pageurl):
    rawtext = soup.get_text()
    regex = re.compile('https*://(\S*)\.s3.amazonaws.com')
    buckets =  re.findall(regex, rawtext)
    # print ("buckets : ",buckets)
    if len(buckets) > 0 :
        for i in range(len(buckets)):
            b = buckets[i]
            if b.rfind('//') >= 0:
                buckets[i] = b[b.rfind('//')+2:]
        buckets = set(buckets)
        with open("buckets.txt","a") as f:
            for b in buckets:
                f.write(b)
                f.write("\n")
            # f.write("\n")
        # if "s3.amazonaws.com" in rawtext:
        #     buckets.write(pageurl)
        #     buckets.write('\n')


#------------------------------------------------------------------------------
def samedomain(netloc1, netloc2):
    """Determine whether two netloc values are the same domain.

    This function does a "subdomain-insensitive" comparison. In other words ...

    samedomain('www.microsoft.com', 'microsoft.com') == True
    samedomain('google.com', 'www.google.com') == True
    samedomain('api.github.com', 'www.github.com') == True
    """
    domain1 = netloc1.lower()
    if '.' in domain1:
        domain1 = domain1.split('.')[-2] + '.' + domain1.split('.')[-1]

    domain2 = netloc2.lower()
    if '.' in domain2:
        domain2 = domain2.split('.')[-2] + '.' + domain2.split('.')[-1]

    return domain1 == domain2

#------------------------------------------------------------------------------
def url_in_db(url):
    """Determine whether a URL is in the db.

    This function checks whether the URL is contained in the db with either
    an http:// or https:// prefix. It is used to avoid crawling the same
    page separately as http and https.
    """
    r = redis.Redis(
        host='localhost',
        port=6379)

    http_version = url.replace('https://', 'http://')
    https_version = url.replace('http://', 'https://')

    return (r.get(http_version)) or (r.get(https_version))

#-------------------------------------------------------------------------------
def getDomainOnly(url):
    """Return the domain out from a url
    url = the url
    """
    # print ("getDomainOnly : ", url)
    tmp = url.split('.')[-2] + '.' + url.split('.')[-1]
    tmp = tmp.split('/')[0]

    return tmp

#------------------------------------------------------------------------------
if __name__ == "__main__":
    crawler(1000000)
