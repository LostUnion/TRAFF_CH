import argparse
from abc import ABC

from curl_cffi import Session

class CONFIG(ABC):
    def __init__(self, timeout: int = 15):
        self.session = Session()
        self.headers = {
            'accept': '*/*',
            'accept-language': 'ru,en-US;q=0.9,en;q=0.8',
            'priority': 'u=1, i',
            'referer': 'https://www.similarsites.com/',
            'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        }
        self.timeout = timeout

class TRAFFIC_CHECKER(CONFIG):
    def __init__(self, site_name: str):
        super().__init__()
        self.site_name = site_name

    def get_traffic(self):
        try:
            full_url = f"https://www.similarsites.com/api/site/{self.site_name}"
            print(full_url)
            res = self.session.get(url=full_url, headers=self.headers)
            print(res.content)

        except Exception as err:
            print(f"An error occurred in the block TRAFFIC_CHECKER.get_traffic: {err}")
            return False
        
check = TRAFFIC_CHECKER('ebay.com')
check.get_traffic()