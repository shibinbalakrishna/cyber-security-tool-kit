
import requests


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