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

def get_token():
    return "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzQ5NzA5NTc2LCJpYXQiOjE3NDk3MDkyNzYsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjNjZTQ3YjRhLWM0ZGMtNGIxNS1iMzI5LTIxMmQ5NzBmNTIyZiIsInN1YiI6IjIyMDNhNTEyOTFAc3J1LmVkdS5pbiJ9LCJlbWFpbCI6IjIyMDNhNTEyOTFAc3J1LmVkdS5pbiIsIm5hbWUiOiJnb3R0aW11a2t1bGEgc2hpdmEga3Jpc2huYSByZWRkeSIsInJvbGxObyI6IjIyMDNhNTEyOTEiLCJhY2Nlc3NDb2RlIjoiTVZHd0VGIiwiY2xpZW50SUQiOiIzY2U0N2I0YS1jNGRjLTRiMTUtYjMyOS0yMTJkOTcwZjUyMmYiLCJjbGllbnRTZWNyZXQiOiJFVVRVZ1F0eGRTbXdraGhjIn0.hklGo4XQ1PlXmjdhf3ygaD9ntFPtVii1jbrLFmM0UX0"

def fetch_numbers_from_api(identifier):
    token = get_token()
    if not token:
        return []
    try:
        url = VALID_IDS[identifier]
        headers = {
            'Authorization':f'Bearer {token}'
        }
        res = requests.get(url, headers=headers, timeout=2)
        if res.status_code==200:
            return res.json().get("numbers", [])
    except:
        pass
    return []

def calculate_average(numbers):
    return round(sum(numbers)/len(numbers), 2) if numbers else 0.0

@api_view(['GET'])
def number_handler_view(request, identifier):
    if identifier not in VALID_IDS:
        return Response({"error": "Invalid ID"}, status=status.HTTP_400_BAD_REQUEST)

    previous_state = list(number_windows[identifier])
    new_numbers = fetch_numbers_from_api(identifier)

    for num in new_numbers:
        if num not in number_windows[identifier]:
            number_windows[identifier].append(num)
        if len(number_windows[identifier]) == WINDOW_SIZE:
            break

    current_state = list(number_windows[identifier])
    average_value = calculate_average(current_state)

    return Response({
        "windowPrevState": previous_state,
        "windowCurrState": current_state,
        "avg": average_value
    }, status=status.HTTP_200_OK)
