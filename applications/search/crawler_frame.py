import logging
from datamodel.search.Yimingc9Vaibhap1Tzucl2Llin20_datamodel import Yimingc9Vaibhap1Tzucl2Llin20Link, OneYimingc9Vaibhap1Tzucl2Llin20UnProcessedLink, add_server_copy, get_downloaded_content
from spacetime.client.IApplication import IApplication
from spacetime.client.declarations import Producer, GetterSetter, Getter, ServerTriggers
from lxml import html,etree
import re, os
from time import time
from uuid import uuid4

import lxml
import analytics_calc as ac
from lxml import html
from urlparse import urlparse, parse_qs
from uuid import uuid4

logger = logging.getLogger(__name__)
LOG_HEADER = "[CRAWLER]"

@Producer(Yimingc9Vaibhap1Tzucl2Llin20Link)
@GetterSetter(OneYimingc9Vaibhap1Tzucl2Llin20UnProcessedLink)
@ServerTriggers(add_server_copy, get_downloaded_content)
class CrawlerFrame(IApplication):

    def __init__(self, frame):
        self.starttime = time()
        self.app_id = "Yimingc9Vaibhap1Tzucl2Llin20"
        self.frame = frame


    def initialize(self):
        self.count = 0
        l = Yimingc9Vaibhap1Tzucl2Llin20Link("http://www.ics.uci.edu/")
        print l.full_url
        self.frame.add(l)

    def update(self):
        unprocessed_links = self.frame.get(OneYimingc9Vaibhap1Tzucl2Llin20UnProcessedLink)
        if unprocessed_links:
            link = unprocessed_links[0]
            print "Got a link to download:", link.full_url
            downloaded = link.download()
            links = extract_next_links(downloaded)

            # counter for the page with the most out link
            cnt = 0
            for l in links:
                if is_valid(l):
                    self.frame.add(Yimingc9Vaibhap1Tzucl2Llin20Link(l))
                    cnt += 1

            # update the page with the most out link 
            ac.max_outgoing(link.full_url, cnt)

            # print the page with the most out link
            print ac.analytics_result['max_outgoing']


    def shutdown(self):
        print (
            "Time time spent this session: ",
            time() - self.starttime, " seconds.")
    
def extract_next_links(rawDataObj):
    try :
        tree = lxml.html.fromstring(rawDataObj.content)
        elements = tree.xpath('//a/@href')
        out = []
        for i in elements:
            parsed = urlparse(i)

            # if domain not in url
            if parsed.netloc != "":
                out.append(i)
            else:
                # ignore the anchor tag
                if i.startswith("#"):
                    continue

                # adding the domain of source link and converts to the absolute url
                nexturl =urlparse(rawDataObj.url).netloc
                combine=""
                if i.startswith("/"):
                    combine=nexturl+i
                else :
                    combine=nexturl+"/"+i
                out.append(combine)
        return out
    except:
        return []
    '''
    rawDataObj is an object of type UrlResponse declared at L20-30
    datamodel/search/server_datamodel.py
    the return of this function should be a list of urls in their absolute form
    Validation of link via is_valid function is done later (see line 42).
    It is not required to remove duplicates that have already been downloaded. 
    The frontier takes care of that.
    
    Suggested library: lxml
    '''

def is_valid(url):
    '''
    Function returns True or False based on whether the url has to be
    downloaded or not.
    Robot rules and duplication rules are checked separately.
    This is a great place to filter out crawler traps.
    '''
    parsed = urlparse(url)

    # if url is not http/https then return false
    if parsed.scheme not in set(["http", "https"]):
        return False

    # If the url contains to many subpath and also using http get/post for download file, ID varification, then return false;
    if parsed.path.count("/")>7 or parsed.query.lower().find("action=download")>=0 or parsed.query.lower().find("action=login")>=0 or parsed.query.lower().find("action=edit")>=0:
        return False

    # ignore the query which are too long
    if len(parsed.query)>20:
        return False 

    # avoid the specific calendar/Pagination query at wics.ics.uci and also the share to Facebook ,Twitter, etc
    if url.lower().find("wics.ics.uci.edu/events/")>=0 or parsed.query.lower().find("_page_id")>=0 or parsed.query.lower().find("share=")>=0:
        return False

    # check every element in url
    elements=parsed.path.lower().split("/")
    unique=set()
    idx=0
    for element in elements:
        idx += 1
        if element=="":
            continue

        # if element repeated again, contains query at wrong position, with mail to tag, and calendar then return false
        if element in unique or len(element)>30  or (idx != len(elements) and element.find("?")>=0 or element.find("calendar")>=0) or element.find("..")>=1 or element.find("mailto")>=1:
            return False
        unique.add(element)
        
    
    try:
        return ".ics.uci.edu" in parsed.hostname \
            and not re.match(".*\.(css|js|bmp|gif|jpe?g|jpg|ico" + "|png|tiff?|mid|mp2|mp3|mp4"\
            + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
            + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
            + "|thmx|mso|arff|rtf|jar|csv"\
            + "|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        return False
    
    return True