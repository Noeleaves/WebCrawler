from urlparse import urlparse
import re
import json
import pprint
ANALYTICS_FILE = "log_analytics.json"

analytics_result = {
        'max_outgoing' : [None,0],
        'sub_domain' : {},
        'invalid_from_frontier' : 0
    }


def cnt_invalid():
    analytics_result['invalid_from_frontier'] += 1


def subdomain_count(url):
    cur_count = analytics_result['sub_domain']
    link = url.strip().split("/")[0]
    link = link.strip().split("?")[0]

    link = re.sub(".*://", "", link)
    link = re.sub("www.", "", link)

    if link in cur_count.keys():
        cur_count[link] += 1
    else:
        cur_count[link] = 1
    analytics_result['sub_domain'] = cur_count


def max_outgoing(url, count_link):
    cur_max = analytics_result['max_outgoing']
    if count_link > cur_max[1]:
        analytics_result['max_outgoing'] = [url, count_link]


def to_file():
    with open(ANALYTICS_FILE, "w") as outfile:
        json.dump(analytics_result, outfile)


def from_file():
    global analytics_result
    with open(ANALYTICS_FILE, "r") as infile:
        analytics_result = json.load(infile)


def file_wrapper(filename):

    with open(filename, "r") as f, open(ANALYTICS_FILE, "w") as outfile:
        for line in f:

            url = line.strip().split("\t")[0]
            analytics_result['sub_domain'] = subdomain_count(url, analytics_result['sub_domain'])
        json.dump(analytics_result, outfile)
    return analytics_result

if __name__ == "__main__":
    pprint.pprint(file_wrapper("frontier_summary.txt"))