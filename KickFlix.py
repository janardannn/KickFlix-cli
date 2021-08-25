import os
import time
from argparse import ArgumentParser
from API.KickAssAPI import KickAssAPI

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
        self.args = parser.parse_args()

        self.api = KickAssAPI()
    
    def run(self):
        """ Run the program """

        if self.args.stream:
            search_results = self.search_kickass(self.args.stream)
            magnet = self.get_magnet(search_results,0)
            print("\nNow streaming: ",search_results[0].text)
            time.sleep(0.7)
            self.stream(magnet)
            exit()

        elif self.args.download:
            search_results = self.search_kickass(self.args.download)
            magnet = self.get_magnet(search_results,0)
            print("\nDownloading: ",search_results[0].text)
            time.sleep(0.7)
            self.download(magnet)
            exit()
        
        else:
            query = input('What do you want to search for (q) to quit: ').strip()
            if query.lower() == "q":
                exit()
            else:
                results = self.search_kickass(query)
            r = 1
            for result in results:
                text = result.text.replace("\n","")
                print(f'{r}. {text}\n')
                r += 1
            
            while True:
                try:
                    user_input = input('\nSelect a torrent(s/d) (q) to quit (r) to re-search: ').strip()
                    if user_input.lower() == "q":
                        exit()
                    elif user_input.lower() == "r":
                        print("\n-----------------#####-----------------\n")
                        self.run()
                    elif user_input != "":
                        index = int(user_input[0]) - 1
                        mode = user_input[1]
                        magnet = self.get_magnet(results,index)

                        if mode == "s":
                            print("\nNow streaming: ",results[index].text)
                            time.sleep(0.7)
                            self.stream(magnet)
                        elif mode == "d":
                            print("\nDownloading: ",results[index].text)
                            time.sleep(0.7)
                            self.download(magnet)

                        print("\n-----------------#####-----------------\n")
                        self.run()
                except IndexError:
                    print("""
*****************************************************                   
  Please retry entering mode with torrent selection 
  example: \"1s\" to stream first torrent                
        or \"1d\" to download first torrent
*****************************************************""")               

            

    def get_magnet(self,search_result,index) -> str:
        """ Get magnet link of selected torrent """ 
        try:
            magnet = self.api.magnet(search_result,index)
            return magnet
        except IndexError:
            print("0 search results")
            print("\n-----------------#####-----------------\n")
            self.run()

    def download(self,magnet):
        """ Download a torrent """

        os.system('webtorrent ' + magnet)
    
    def stream(self,magnet):
        """ Stream a torrent """

        os.system('webtorrent ' + f"\"{magnet}\"" + ' --vlc')

    def search_kickass(self,query) -> dict:
        """ Search for torrents """
        
        print(f"Searching for \"{query}\"")
        search_result = self.api.search(query)
        if search_result == []:
            print("0 search results\n")
            print("\n-----------------#####-----------------\n")
            if self.args.stream == None and self.args.download == None:
                self.run()
            exit()
        print(str(len([search.text for search in search_result])) + " search results found\n")
        time.sleep(0.7)
        
        return search_result

def main(): 
    """ Run the program """

    kickflix = KickFlix()
    kickflix.run()

main()

