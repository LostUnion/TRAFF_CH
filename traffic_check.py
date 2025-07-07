import argparse
from abc import ABC
from urllib.parse import urlparse

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
        self.check_format_link()

    def check_format_link(self):
        try:
            url = self.site_name.lower()

            if not url.startswith("http://") and not url.startswith("https://"):
                url = "http://" + url

            parsed = urlparse(url)

            self.site_name = parsed.netloc

            if ':' in self.site_name:
                self.site_name = self.site_name.split(':')[0]


        except Exception as err:
            print(f"An error occurred in the block TRAFFIC_CHECKER.check_format_link: {err}")
            return False

    def get_traffic(self):
        try:
            full_url = f"https://www.similarsites.com/api/site/{self.site_name}"
            res = self.session.get(url=full_url, headers=self.headers)
            res_json = res.json()
            if res_json is None:
                print('This site is not in the database!')
                return False
            
            total_visits = res_json['TotalVisits']
            return total_visits
        except Exception as err:
            print(f"An error occurred in the block TRAFFIC_CHECKER.get_traffic: {err}")
            return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Checking the monthly traffic on the site.')
    parser.add_argument('-s', '--site_name', type=str, required=True, help='Enter site-name')
    args = parser.parse_args()

    check = TRAFFIC_CHECKER(args.site_name)
    print(check.get_traffic())