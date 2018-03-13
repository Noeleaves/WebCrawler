ICS 221 Infor Retrieval Assignment2

	yimingc9,28328800
	vaibhap1,36008056
	tzucl2,48964286
	llin20,38645610


This file is about the analytics for space cralwer.

Analytics

1. Keep track of all the subdomains that it visited, and count how many different URLs it has
processed from each of those subdomains

	All the subdomains are recorded in subdomain.txt file. There are total 4311 pages are successfully crawled with total 93 distict domain

2. Count how many invalid links it received from the frontier, if any

	As every links were checked before adding to the frontier, there is no invalids in the frontier_summary.txt file. All the links are succeffully crawled.

3. Find the page with the most out links (of all pages given to your crawler)

	The page with the most out links is shown as below. 
	['https://sli.ics.uci.edu/Site/AllRecentChanges', 424]

4. Any additional things you may find interesting to keep track



Correctness
a) Did you successfully download at least 3,000 pages?

	There are total 4311 pages are crawled.

b) Did you extract the links correctly?
	
	all the links are extracted correctly and converted to absolute url path if necssary

c) Does your crawler validate the URLs that is given and that is sends back to the frontier?

	Yes, the detail about how to avoid are explained at is_valid function in crawler_frame.py

d) How does your program handle bad URLs?

	Convert to absolute link if available. If it causes the crawler to be trapped then we simply ignore it	
	
e) Does your crawler avoid traps?

	The crawler avoid the traps by validating the links.