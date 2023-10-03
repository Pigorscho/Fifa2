import os
import json
import shutil
import zipfile
import requests
from time import sleep


class Driver:
    def __init__(self, version):
        self.version = version
        self.base_dir = r'C:\\Chromedriver'
        self.base_file = r'C:\\Chromedriver\chromedriver.exe'
        self.download_dir = r'C:\\Chromedriver\download'
        self.download_zip = r'C:\\Chromedriver\download\chrome_driver.zip'
        self.download_file = r'C:\\Chromedriver\download\chromedriver-win64\chromedriver.exe'

    def run(self):
        download_url = self.get_download_url(self.version)
        self.get_file(download_url)
        self.extract_file()
        self.replace_file()
        self.clean_up()

    def get_download_url(self, version):
        # Endpoint to get the JSON data
        endpoint = 'https://googlechromelabs.github.io/chrome-for-testing/last-known-good-versions-with-downloads.json'
        response = requests.get(endpoint)

        if response.status_code != 200:
            print("Error fetching data from the endpoint.")
            return

        data = json.loads(response.text)

        for channel, details in data["channels"].items():
            if details["version"].startswith(version):
                for download in details["downloads"]["chromedriver"]:
                    if download["platform"] == "win64":  # Adjust based on your needs
                        return download["url"]

    def get_file(self, url):
        print(f"downloading '{url}'")
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
        r = requests.get(url)
        with open(self.download_zip, 'wb') as f:
            f.write(r.content)
        sleep(2)

    def extract_file(self):
        with zipfile.ZipFile(self.download_zip, 'r') as zip_ref:
            zip_ref.extractall(self.download_dir)
        sleep(1)

    def replace_file(self):
        os.remove(self.base_file)
        shutil.move(self.download_file, self.base_dir)

    def clean_up(self):
        shutil.rmtree(self.download_dir)


if __name__ == '__main__':
    handler = Driver('116')
    handler.run()