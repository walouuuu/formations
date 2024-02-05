from scrapy import cmdline    

import requests

def get_ip_address():
    response = requests.get("https://httpbin.org/ip")
    ip_data = response.json()
    ip_address = ip_data.get("origin")
    return ip_address

if __name__ == '__main__':
    ip_address = get_ip_address()
    print(f"Your IP address: {ip_address}")

    cmdline.execute("scrapy crawl linkedinSpider -o ./data/jobs.json".split())