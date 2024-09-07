
import string
import requests
import hashlib


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
    print(response)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} is found {count} times. You should change it')
        else:
            print(f"{password} is not found. You're good to go")

    return 'done'