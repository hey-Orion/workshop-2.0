import requests

response = requests.get("https://httpbin.org/status/200", timeout=2)

if response == 200:
        print("System Online")
   
else:
    print("System Offline")



