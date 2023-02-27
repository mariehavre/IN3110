import re

## -- Task 2 -- ##

def find_urls(
    html: str,
    base_url: str = "https://en.wikipedia.org",
    output: str = None,
) -> set:
    """Find all the url links in a html text using regex
    Arguments:
        html (str): html string to parse
    Returns:
        urls (set) : set with all the urls found in html text
    """

    a_pat = re.compile(r"<a([^>]+)>", flags=re.IGNORECASE)
    href_pat = re.compile(r'href="([/|http].[^"]+)"', flags=re.IGNORECASE) 
    urls = set()

    for a_tag in a_pat.findall(html):
        match = href_pat.search(a_tag)
        if match:
            urls.add(match.group(1))

    urls = change_urls(urls, pattern='#.*', replacement='')               
    urls = change_urls(urls, pattern='^(//)', replacement='https://')
    urls = change_urls(urls, pattern='^(/)', replacement=base_url + '/')  
   
    if output:
        print(f"Writing to: {output}")
        f = open(output, "w")
        for u in urls:
            f.write(u + "\n")
        f.close()
    
    return urls


def change_urls(urls, pattern, replacement):
    """Reformats the elements in the given set 'urls' using regex.

    Arguments:
        - urls (set): all urls found in the html
        - pattern (str): regex to find the parts of a url that needs to be changed
        - replacement (str): the string to replace that part of the url
    Returns:
        - urls (set): an updated set
    """

    new_urls = set()
    old_urls = set()

    hash_pattern = re.compile(pattern)

    for u in urls:
        match = hash_pattern.search(u)

        if match:
            new_u = re.sub(pattern, replacement, u)
            new_urls.add(new_u)
            old_urls.add(u)
    
    urls -= old_urls
    urls.update(new_urls)

    return urls

def find_articles(html: str, output=None) -> set:
    """Finds all the wiki articles inside a html text. Make call to find urls, and filter
    arguments:
        - text (str) : the html text to parse
    returns:
        - (set) : a set with urls to all the articles found
    """

    urls = find_urls(html)
    pattern = re.compile('(.*(?:wikipedia.org/wiki/(?!.*:|\n)).*)', flags=re.IGNORECASE) 
    articles = set()

    for u in urls:
        match = pattern.search(u)
        if match:
            articles.add(u)
        else:
            print(u)

    if output:
        print(f"Writing to: {output}")
        f = open(output, "w")
        for a in articles:
            f.write(a + "\n")
        f.close()

    return articles

def find_img_src(html: str):
    """Finds all src attributes of img tags in an HTML string

    Args:
        html (str): A string containing some HTML.

    Returns:
        src_set (set): A set of strings containing image URLs

    The set contains every found src attibute of an img tag in the given HTML.
    """
 
    img_pat = re.compile(r"<img[^>]+>", flags=re.IGNORECASE)
    src_pat = re.compile(r'src="([^"]+)"', flags=re.IGNORECASE)
    src_set = set()

    for img_tag in img_pat.findall(html):
        match = src_pat.search(img_tag)

        if match:
            src_set.add(match.group(1))

    return src_set
