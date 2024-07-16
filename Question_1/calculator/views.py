import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import time
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class NumberStore:
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.window = []

    def add_numbers(self, numbers):
        for number in numbers:
            if number not in self.window:
                if len(self.window) >= self.window_size:
                    self.window.pop(0)
                self.window.append(number)

    def get_window(self):
        return self.window

    def calculate_average(self):
        if not self.window:
            return 0
        return sum(self.window) / len(self.window)

number_store = NumberStore()

class NumberView(APIView):
    def get(self, request, number_id):
        if number_id not in ['p', 'f', 'e', 'r']:
            return Response({'error': 'Invalid number ID'}, status=status.HTTP_400_BAD_REQUEST)

        test_server_url = {
            'p': 'http://20.244.56.144/test/primes',
            'f': 'http://20.244.56.144/test/fibo',
            'e': 'http://20.244.56.144/test/even',
            'r': 'http://20.244.56.144/test/rand'
        }

        # Use your pre-obtained token here
        access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzIxMTM4OTc2LCJpYXQiOjE3MjExMzg2NzYsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6IjM1M2E1MTZmLWUwZTAtNDBiMS04YWE3LTljYzdmODlhYWE5YiIsInN1YiI6IjEyNTAwMzQ3N0BzYXN0cmEuYWMuaW4ifSwiY29tcGFueU5hbWUiOiJTQVNUUkEgRGVlbWVkIFVuaXZlcnNpdHkiLCJjbGllbnRJRCI6IjM1M2E1MTZmLWUwZTAtNDBiMS04YWE3LTljYzdmODlhYWE5YiIsImNsaWVudFNlY3JldCI6ImlHWndMam95bExmbmVqUlQiLCJvd25lck5hbWUiOiJBbWFybmF0aCBBIiwib3duZXJFbWFpbCI6IjEyNTAwMzQ3N0BzYXN0cmEuYWMuaW4iLCJyb2xsTm8iOiIxMjUwMDM0NzcifQ.sNIgH1zzpvSFS_NFn-0a4QWTHu8ooKXv9h2dv3MTqBs"

        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        numbers = []
        try:
            start_time = time.time()
            response = requests.get(test_server_url[number_id], headers=headers, timeout=0.5)
            response_time = time.time() - start_time
            if response_time > 0.5 or response.status_code != 200:
                logger.debug(f'Test server response too slow or failed. Response time: {response_time}, Status code: {response.status_code}')
                raise Exception('Test server response too slow or failed')
            logger.debug(f'Test server response: {response.json()}')
            numbers = response.json().get('numbers', [])
        except Exception as e:
            logger.error(f'Error fetching numbers from test server: {e}')
            numbers = []

        prev_window = number_store.get_window().copy()
        number_store.add_numbers(numbers)
        curr_window = number_store.get_window()
        avg = number_store.calculate_average()

        result = {
            'numbers': numbers,
            'windowPrevState': prev_window,
            'windowCurrState': curr_window,
            'avg': round(avg, 2)
        }
        logger.debug(f'Response: {result}')
        return Response(result, status=status.HTTP_200_OK)
