import os
import time
import json
import requests
from argparse import ArgumentParser

class KickFlix():

    def __init__(self):

        print("""

                    
██╗░░██╗██╗░█████╗░██╗░░██╗███████╗██╗░░░░░██╗██╗░░██╗
██║░██╔╝██║██╔══██╗██║░██╔╝██╔════╝██║░░░░░██║╚██╗██╔╝
█████═╝░██║██║░░╚═╝█████═╝░█████╗░░██║░░░░░██║░╚███╔╝░
██╔═██╗░██║██║░░██╗██╔═██╗░██╔══╝░░██║░░░░░██║░██╔██╗░
██║░╚██╗██║╚█████╔╝██║░╚██╗██║░░░░░███████╗██║██╔╝╚██╗
╚═╝░░╚═╝╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚══════╝╚═╝╚═╝░░╚═╝
  Minimal command line based torrent streaming client
        """)
        parser = ArgumentParser(description='KickFlix - Minimal torrent player')
        parser.add_argument('-s', '--stream', type=str, help='Stream a torrent')
        parser.add_argument('-d', '--download', help='Download a torrent')
        parser.add_argument('-m', '--magnet', help='Get the magnet link of a torrent')
        self.args = parser.parse_args()

        self.API = "https://kickass-api-unofficial.herokuapp.com/"
    
    def run(self):
        """ Run the program """

        if self.args.stream:
            search_results = self.search_kickass(self.args.stream)
            magnet = self.get_magnet(search_results["1"]['page_url'])
            print("\nNow streaming:\n",search_results["1"]['title'])
            time.sleep(0.7)
            self.stream(magnet)
            exit()

        elif self.args.download:
            search_results = self.search_kickass(self.args.download)
            magnet = self.get_magnet(search_results["1"]['page_url'])
            print("\nDownloading: \n",search_results["1"]['title'])
            time.sleep(0.7)
            self.download(magnet)
            exit()
        
        elif self.args.magnet:
            search_results = self.search_kickass(self.args.magnet)
            magnet = self.get_magnet(search_results["1"]['page_url'])
            print("\nMagnet for : ",str(search_results["1"]['title'])+ "\n")
            print(magnet)
            exit()  
        
        else:
            query = input('What do you want to search for (q) to quit: ').strip()
            if query.lower() == "q":
                exit()
            else:
                results = self.search_kickass(query)

            for count in results.keys():
                print(f"{count}. {results[count]['title']}\n")

            
            while True:
                try:
                    user_input = input('\nSelect a torrent(s/d/m) (q) to quit (r) to re-search: ').strip()
                    if user_input.lower() == "q":
                        exit()
                    elif user_input.lower() == "r":
                        print("\n-----------------#####-----------------\n")
                        self.run()
                    elif user_input != "":
                        index = user_input[0]
                        mode = user_input[1]
                        magnet = self.get_magnet(results[index]['page_url'])

                        if mode == "s":
                            print("\nNow streaming: ",results[index]['title'])
                            time.sleep(0.7)
                            self.stream(magnet)
                        elif mode == "d":
                            print("\nDownloading: ",results[index]['title'])
                            time.sleep(0.7)
                            self.download(magnet)
                        
                        elif mode == "m":
                            print("\nMagnet for : ",str(results[index]['title'])+ "\n")
                            print(magnet)

                        print("\n-----------------#####-----------------\n")
                        self.run()
                except (IndexError,ValueError):
                    print("""
*****************************************************                   
  Please retry entering mode with torrent selection 
  example: \"1s\" to stream first torrent                
        or \"1d\" to download first torrent
*****************************************************""")               

            

    def get_magnet(self,page_url) -> str:
        """ Get magnet link of selected torrent """ 
        resp = requests.get(self.API + "magnet?page_url=" + page_url)
        resp.close()
        magnet = json.loads(resp.text)
        
        return (magnet['magnet'])
        

    def download(self,magnet):
        """ Download a torrent """

        os.system('webtorrent ' + magnet)
    
    def stream(self,magnet):
        """ Stream a torrent """

        os.system('webtorrent ' + f"\"{magnet}\"" + ' --vlc')

    def search_kickass(self,query) -> dict:
        """ Search for torrents """
        
        print(f"Searching for \"{query}\"")

        resp = requests.get(self.API + "search?torrent=" + query)
        resp.close()
        search_result = json.loads(resp.text)

        if search_result == {}:
            print("0 search results\n")
            print("\n-----------------#####-----------------\n")
            if self.args.stream == None and self.args.download == None:
                self.run()
            exit()
        print(str(len(search_result)) + " search results found\n")
        time.sleep(0.7)
        
        return search_result

def main(): 
    """ Run the program """

    kickflix = KickFlix()
    kickflix.run()

main()

