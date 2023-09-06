RARBG-Flask edition
========

On 31.05.2023 a public torrent tracker RARBG shut down. The reasons why are numerous, but not really relevant to this project. What matters is that that torrent tracker has been in use since 2008 and has amassed a sizable userbase and aggregated a lot of links to various torrents.

When it was shut down, it created a bit of a vacuum for the users that still needed its services. So they started looking for other options. One such option was RARBG itself. As it happenes, some user had been running a web scraper on the original site for their own usage and decided to make the data they collected public.

Now, it's all fine and dandy, but for most people raw SQLite files are not *terribly* convenient. Sure, there are tools like [DB browser for SQLite](https://sqlitebrowser.org/) to make it possible to browse it, but they aren't specialised. So a lot of legwork will have to be done by the user manually.
That gave me an idea to make somewhat simple Flask service to do exactly that - to simplify the process of browsing that database. I'm trying to achieve that with the most minimal required alterations to the original sqlite file.

For obvious legal reasons I'm not sharing the original SQLite file. This project's was made mostly for my own amusement. So, if you want to use it yourself, you'll have to find the original SQLite file yourself. This git repo does include an sqlite file for demonstration purposes, but it's a relatively small selection and the hashes were intentionally deleted and replaced by the word "PLACEHOLDER". Everything functions as intended, but you won't be able to download anything.

Features
--------

This project provides a flask-based web interface for viewer to navigate torrent file database.
The app allows user:

* to browse through files by categories
* to search for files by name
* to look through information from IMDB if any is available.

Installation
------------
Install dependencies 


```console
$ pip install -r requirements.txt
```
Run


```python
$ python main.py
```

