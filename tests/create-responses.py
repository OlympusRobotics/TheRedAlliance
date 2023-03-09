# create a batch of responses for a form.

if __name__ != "__main__":
    exit()

import requests
import time
import json
import random

url = input("Enter form URL ")

code = url.split("/")[-1]

url = f"https://{''.join(url.split('/')[2])}/api/respond/{code}"
print(url)

responses = input("Enter response payload for form ")

payload = {
    "teamNum": 1,
    "name": "",
    "responses": json.loads(responses)
}

headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
}

num_res = int(input("How many teams? "))
team_num_res = int(input("How many responses per team"))

for i in range(num_res):
    payload["teamNum"] = i * random.randint(1, 7)
    for j in range(team_num_res):
        req = requests.post(url, json=payload, headers=headers)
        print(req.status_code, req.text)
        payload["name"] = str(j) + "th response"
        time.sleep(.03)


print("Done")
