import requests
from bs4 import BeautifulSoup

class KickAssAPI():

    def __init__(self):
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}

    def search(self,query) -> dict:

        """ Returns a list of dictionaries with the results of the search """

        url = "https://katcr.to/usearch/" + query + "/"
        results = requests.get(url, headers=self.headers)

        if results.status_code == 200:
            soup = BeautifulSoup(results.text, "html.parser")
            search_results = soup.find_all("a", {"class": "cellMainLink"})
            results.close()

        elif results.status_code == 403:
            print("\nThe URL (\"https://katcr.to\") responded with code 403.\nThis means that the server understood the request but refuses to authorize it.")
            results.close()
            exit()
        elif results.status_code == 404:
            print("\nThe URL (\"https://katcr.to\") responded with code 404.\nThis means that the server cannot find the page you requested. ")
            results.close()
            exit()
        else:
            results.close()
            print("\nThe URL (\"https://katcr.to\") responded with code " + str(results.status_code) + ".\nThis means that the server is not responding to the request.")
        
        return search_results


    def magnet(self,search_dict,index=0) -> str:

        """ Returns the magnet link of the selected torrent """

        magnet_page = requests.get("https://katcr.to"+search_dict[index].get("href"), headers=self.headers)
        magnet_page_bs = BeautifulSoup(magnet_page.text, "html.parser")
        magnet_link = magnet_page_bs.find("a", {"class": "kaGiantButton"}).get("href")
        magnet_page.close()

        return magnet_link 
