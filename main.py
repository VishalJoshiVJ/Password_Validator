import hashlib
import requests

# function to get the response of password, good:200 and bad:400
def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching {res.status_code}, check your password...')
    else:
        return res

# get the number of times password hacked/leaked
def get_hacked_count(hashes, hash_to_check):
    hashes = (line.split(":") for line in hashes.text.splitlines())

    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

# utility function to hash the password and process it
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5, tail = sha1password[:5], sha1password[5:]
    responce = request_api_data(first5)
    return get_hacked_count(responce, tail)


def main():
    password = input("Enter your password : ")
    count = pwned_api_check(password)
    if count:
        print(f'Warning : {password} was found to be leaked {count} times, check your password')
    else:
        print(f'{password} is fine, Carry on...')


if __name__ == '__main__':
    main()


