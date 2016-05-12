import os
import re

from bs4 import BeautifulSoup
from multiprocessing import Pool
import multiprocessing
import requests

BASE_URL = "http://developer.openstack.org/"
response = requests.get(BASE_URL+"api-ref.html")
soup = BeautifulSoup(response.text, "lxml")
regex = re.compile("^api\-ref.*", re.IGNORECASE)
links = dict()
for link in soup.find_all('a'):
    if regex.search(link["href"]):
        links[link["href"][8:-5]] = BASE_URL+"{0}{1}".format("/", link["href"])

print "Downloading all files.."


def make_all_files(uri):
    filename = "./links/{}.html".format(uri)
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError:
            raise


def download_all_links(uri):
    filename = "./links/{}.html".format(uri)
    with open(filename, 'w') as f:
        f.writelines(requests.get(links[uri]).text)


map(make_all_files, links)

number_of_pools = multiprocessing.cpu_count()
print "Number of processes launched {}".format(number_of_pools)
p = Pool(number_of_pools)
p.map(download_all_links, links)
print "All resources downloaded to directory {}".format("./links/")
