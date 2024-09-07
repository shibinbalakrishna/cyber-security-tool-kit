def clean_url(url):
    url = url.strip()  # Remove leading and trailing whitespaces
    url = url.replace("https://", "").replace("http://", "")  # Remove https:// and http://
    url = url.rstrip("/")  # Remove trailing /
    return url
