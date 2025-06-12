from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from collections import deque
import requests

WINDOW_SIZE=10
VALID_IDS={
    'p':'http://20.244.56.144/evaluation-service/primes',
    'f':'http://20.244.56.144/evaluation-service/fibo',
    'e':'http://20.244.56.144/evaluation-service/even',
    'r':'http://20.244.56.144/evaluation-service/rand',
}
number_windows={key: deque(maxlen=WINDOW_SIZE) for key in VALID_IDS}

import requests

def get_token():
    url = "http://20.244.56.144/evaluation-service/auth"
    payload = {
        "email": "2203a51291@sru.edu.in",
        "name": "gottimukkula shiva krishna reddy",
        "rollNo": "2203a51291",
        "accessCode": "MVGwEF",
        "clientID": "3ce47b4a-c4dc-4b15-b329-212d970f522f",
        "clientSecret": "EUTUgQtxdSmwkhhc"
    }
    try:
        res = requests.post(url, json=payload, timeout=5)
        print("Status Code:",res.status_code)
        print("Response Text:",res.text)
        if res.status_code==201:
            return res.json().get("access_token")
    except Exception as e:
        print("Error:", e)
    return None


def fetch_numbers_from_api(identifier):
    token=get_token()
    if not token:
        return []
    try:
        url=VALID_IDS[identifier]
        headers={
            'Authorization':f'Bearer {token}'
        }
        res=requests.get(url, headers=headers, timeout=2)
        if res.status_code==200:
            return res.json().get("numbers",[])
    except:
        pass
    return []

def calculate_average(numbers):
    return round(sum(numbers)/len(numbers),2) if numbers else 0.0

@api_view(['GET'])
def number_handler_view(request,identifier):
    if identifier not in VALID_IDS:
        return Response({"error": "Invalid ID"}, status=status.HTTP_400_BAD_REQUEST)

    previous_state=list(number_windows[identifier])
    new_numbers=fetch_numbers_from_api(identifier)

    for num in new_numbers:
        if num not in number_windows[identifier]:
            number_windows[identifier].append(num)
        if len(number_windows[identifier])==WINDOW_SIZE:
            break

    current_state=list(number_windows[identifier])
    average_value=calculate_average(current_state)

    return Response({
        "windowPrevState":previous_state,
        "windowCurrState":current_state,
        "avg":average_value
    }, status=status.HTTP_200_OK)
