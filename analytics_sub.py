import re

def subdomain_count(url,d):
    link = url.strip().split("/")[0]
    link = link.strip().split("?")[0]

    link = re.sub(".*://", "", link)
    link = re.sub("www.", "", link)

    if link in d.keys():
        d[link] += 1
    else:
        d[link] = 1
    return d

def writeFile(d):
    count = 0
    with open('subdomain.txt', 'w') as f:
        for key, value in d.items():
            count += value
            f.write(key+': '+str(value)+'\n')
        d_len = len(d)
        f.write('\nThere are ' + str(d_len) + ' subdomains.\n')
    #print count

if __name__ == "__main__":
    subdomain = dict()
    with open("frontier_summary.txt",'r') as f:
        for line in f:
            if line.find('incomplete')!=-1:
                continue
            url = line.strip().split("\t")[0]
            if url.find('ics.uci.edu')==-1:
                continue
            subdomain = subdomain_count(url, subdomain)
    writeFile(subdomain)

