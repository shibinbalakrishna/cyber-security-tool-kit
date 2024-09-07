import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
import time
import textwrap



# Vulnerability scanning functions
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