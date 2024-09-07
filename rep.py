import string
import requests
import hashlib,socket
from bs4 import BeautifulSoup as bs
from bs4 import BeautifulSoup
import re
import textwrap
import time
from urllib.parse import urljoin
import sys


API_KEY = '5f2174dcd5bbd7be427f4d400e500dba31afb2527aa53e25bc50cdcad1757e40'
SCAN_URL = 'https://www.virustotal.com/vtapi/v2/url/scan'
REPORT_URL = 'https://www.virustotal.com/vtapi/v2/url/report'

def scan_url1(url):
    params = {'apikey': API_KEY, 'url': url}
    response = requests.post(SCAN_URL, data=params)
    json_response = response.json()
    if 'scan_id' in json_response:
        scan_id = json_response['scan_id']
        return get_report(scan_id)
    else:
        return None

# Function to get scan report from VirusTotal API
def get_report(scan_id):
    params = {'apikey': API_KEY, 'resource': scan_id}
    response = requests.get(REPORT_URL, params=params)
    return response.json()


# username
def is_username_leaked(username):
    api_url = f"https://leakcheck.io/api/public?check={username}"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            found_count = data.get("found", 0)
            if found_count > 0:
                return {
                    "message": f"The username '{username}' has been found in {found_count} leaked databases.",
                    "sources": data.get("sources", [])
                }
            else:
                return {"message": f"The username '{username}' has not been found in any leaked databases."}
        else:
            return {"error": f"Failed to fetch data. Status code: {response.status_code}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}
    

    # password

def check_password_strength(password):
    # Minimum requirements
    min_length = 8
    min_uppercase = 1
    min_lowercase = 1
    min_digits = 1
    min_special_chars = 1

    # Check length
    if len(password) < min_length:
        return "Password should be at least {} characters long.".format(min_length)

    # Check uppercase letters
    if sum(1 for c in password if c.isupper()) < min_uppercase:
        return "Password should contain at least {} uppercase letter(s).".format(min_uppercase)

    # Check lowercase letters
    if sum(1 for c in password if c.islower()) < min_lowercase:
        return "Password should contain at least {} lowercase letter(s).".format(min_lowercase)

    # Check digits
    if sum(1 for c in password if c.isdigit()) < min_digits:
        return "Password should contain at least {} digit(s).".format(min_digits)

    # Check special characters
    special_chars = string.punctuation
    if sum(1 for c in password if c in special_chars) < min_special_chars:
        return "Password should contain at least {} special character(s).".format(min_special_chars)

    return "Password is strong."

def request_api_data(char):
    url = 'https://api.pwnedpasswords.com/range/'+char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(
            f'Error fetching: {res.status_code}, check the api and try again')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)


# whois
def ip_address_tracker(ip_address):
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "success":
        country = data["country"]
        city = data["city"]
        isp = data["isp"]
        longitude = data["lon"]
        latitude = data["lat"]
        zip_code = data["zip"]
        region = data["regionName"]
        timezone= data["timezone"]

        return {
            'is_fetched': True,
            'ip_address': ip_address,
            'country': country,
            'city': city,
            'isp': isp,
            'longitude': longitude,
            'latitude': latitude,
            'zip_code': zip_code,
            'region': region,
            'timezone': timezone
        }
    else:
        return {'is_fetched': False}

def url_to_ip(url1):
    try:
        ip_address1 = socket.gethostbyname(url1)
        return ip_address1
    except socket.gaierror:
        return "Error: Unable to resolve host."
    

# urlrobo

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

# vuln scan

def clickjacking_scan(domain):
    headers = requests.get(domain).headers
    if 'X-Frame-Options' in headers:
        return "Not Vulnerable to clickjacking"
    else:
        return "Vulnerable to Clickjacking vulnerability"

def get_all_forms(url):
    soup = bs(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    details = {}
    details["action"] = form.attrs.get("action", "").lower()
    details["method"] = form.attrs.get("method", "get").lower()
    details["inputs"] = [{"type": input_tag.attrs.get("type", "text"),
                          "name": input_tag.attrs.get("name")} for input_tag in form.find_all("input")]
    return details

def submit_form(form_details, url, value):
    target_url = urljoin(url, form_details["action"])
    data = {input["name"]: value for input in form_details["inputs"]}
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    else:
        return requests.get(target_url, params=data)

def xss_scan(url):
    forms = get_all_forms(url)
    js_script = "<Script>alert('hi')</script>"
    is_vulnerable = False
    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, js_script).content.decode()
        if js_script in content:
            is_vulnerable = True
            break
    if is_vulnerable:
        return "Vulnerable to Cross-Site Scripting (XSS)"
    else:
        return "Not Vulnerable to XSS"

def is_sql_injection_vulnerable(response, payload, url):
    errors = {"you have an error in your sql syntax;",
              "warning: mysql",
              "unclosed quotation mark after the character string",
              "quoted string not properly terminated"}
    for error in errors:
        if error in response.content.decode().lower():
            return True
    return False

def sql_injection_scan(url):
    for c in "\"'":
        new_url = f"{url}{c}"
        res = requests.get(new_url)
        if is_sql_injection_vulnerable(res, c, new_url):
            return "Vulnerable to SQL Injection"
    return "Not Vulnerable to SQL Injection"

def rce_scan(url):
    forms = get_all_forms(url)
    is_vulnerable = False
    for form in forms:
        form_details = get_form_details(form)
        content = submit_form(form_details, url, "test; echo vulnerable").content.decode()
        if "vulnerable" in content:
            is_vulnerable = True
            break
    if is_vulnerable:
        return "Vulnerable to Remote Code Execution (RCE)"
    else:
        return "Not Vulnerable to RCE"

def csrf_scan(url):
    res = requests.get(url)
    soup = bs(res.content, "html.parser")
    csrf_element = soup.find("input", attrs={"name": "csrf_token"})
    if csrf_element:
        return "Vulnerable to Cross-Site Request Forgery (CSRF)"
    else:
        return "Not Vulnerable to CSRF"

def lfi_scan(url):
    lfi_payloads = ["../../../../../../../../../../../etc/passwd",
                    "../../../../../../../../../../../etc/passwd",
                    "/..././..././..././..././..././..././..././etc/passwd%00",
                    "../../../../../../../../../../../etc/passwd"]
    for payload in lfi_payloads:
        r = requests.get(url + payload, timeout=5)
        if "root:x" in r.text:
            return "Vulnerable to Local File Inclusion (LFI)"
    return "Not Vulnerable to LFI"

# Utility function to generate timestamp
def generate_timestamp():
    return time.strftime("%Y%m%d%H%M%S")

sys.stdout.reconfigure(encoding='utf-8')

# Function to crawl a web page and extract all text-based HTML tags
# Function to crawl a web page and extract all text-based HTML tags
def crawl_and_extract(url):
    try:
        # Check if the URL starts with 'http://' or 'https://'
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url  # Add 'https://' prefix if not present
        
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find all text-based HTML tags and extract their text content
            text_tags = [tag.get_text(strip=True) for tag in soup.find_all(text=True)]
            # Remove empty strings and dots
            text_tags = [text.strip() for text in text_tags if text.strip() and text.strip() != '.']
            return text_tags
        else:
            return None
    except Exception as e:
        print(f"An error occurred while crawling {url}: {str(e)}")
        return None
