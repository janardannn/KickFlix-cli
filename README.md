# ABOUT

A command-line based, minimal torrent streaming client made using Python and Webtorrent-cli.

## Installation

```bash
pip install -r requirements.txt
```

It uses webtorrent-cli to stream/download torrents (necessary)

Download Nodejs from [here](https://nodejs.org/en/download/), install the package and then run this command in terminal
```bash
npm install webtorrent-cli -g
```

ALso, if you want to stream torrents you'll need VLC Media Player (maybe the reason why you're using this script) (optional, downloaing will work without VLC)

Download VLC from [here](https://www.videolan.org/)

## Usage

To stream a torrent directly from command line (streams the torrent at top in search results)
```python
python3 KickFlix.py -s "torrent" 
```
Downloading a torrent from command line (downloads the torrent at top in search results)
```python
python3 KickFlix.py -d "torrent"
```
Using the script to search torrents and then to stream/download selected torrent
```python
python3 KickFlix.py
```
