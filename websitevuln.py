import requests
from bs4 import BeautifulSoup
import re
import socket



def get_title(url):
    data = read_contents(url).decode('utf-8')
    title_pattern = re.compile(r'<title[^>]*>(.*?)<\/title>', re.I | re.S)
    title = title_pattern.search(data)
    return title.group(1) if title else None

def web_server(url):
    wsheaders = requests.head(url).headers
    ws = wsheaders.get('Server', '')
    return ws if ws else None

def cloudflare_detect(url):
    urlhh = 'http://api.hackertarget.com/httpheaders/?q={}'.format(url)
    resulthh = requests.get(urlhh).text.lower()
    return 'cloudflare' in resulthh

def robots_dot_txt(url):
    rbturl = '{}/robots.txt'.format(url)
    rbthandle = requests.get(rbturl)
    if rbthandle.status_code == 200:
        rbtcontent = rbthandle.text
        return rbtcontent if rbtcontent else None
    else:
        return None

def get_http_header(url):
    hdr = requests.head(url).headers
    return hdr

def extract_links(url):
    elsc = read_contents(url)
    if elsc:
        eldom = BeautifulSoup(elsc, 'html.parser')
        links = eldom.find_all('a')
        return [link['href'] for link in links]
    else:
        return None

def read_contents(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None

def check_open_ports(url):
    ports = [80, 443, 8080, 21, 22, 23]  # Example list of ports to check
    open_ports = []

    for port in ports:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex((url, port))

                if result == 0:
                    open_ports.append(port)
        except Exception as e:
            pass

    return open_ports

def analyze_website(url):
    if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url  # Add 'https://' prefix if not present
    results = {}

    results['Title'] = get_title(url)
    results['Web Server'] = web_server(url)
    results['Cloudflare Detected'] = cloudflare_detect(url)
    results['robots.txt'] = robots_dot_txt(url)
    results['HTTP Headers'] = get_http_header(url)
    results['Links'] = extract_links(url)
    results['Open Ports'] = check_open_ports(url)

    return results
