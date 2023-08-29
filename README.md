RARBG-Flask edition
========

On 31.05.2023 a public torrent tracker RARBG shut down. The reasons why are numerous, but not really relevant to this project. What matters is that that torrent tracker has been in use since 2008 and has amassed a sizable userbase and aggregated a lot of links to various torrents.
When it was shut down, it created a bit of a vacuum for the users that still needed its services. So they started looking for other options. And it just so happened that some user had been running a scraper on the original site for their own usage and decided to make the data they collected public.
Now, it's all fine and dandy, but for most people raw SQLite files are not *terribly* convenient. Sure, there are tools like [DB browser for SQLite](https://sqlitebrowser.org/) to make it easier to browse, but they aren't specialised. So a lot of legwork will have to be done by the user manually.
That gave me an idea to make somewhat simple Flask service to do exactly that - to simplify the process of browsing that database. I'm trying to achieve that with the most minimal required alterations to the original sqlite file.
For obvious legal reasons I'm not sharing the original SQLite file. This project's purpose is mostly because I thought it would be interesting to make. So, if you want to use it yourself, you'll have to find the original SQLite file yourself.

Features
--------

- Make data from RARBG database usable for an average user
- Fetch IMDB data when it's available for an upload

Installation
------------


Contribute
----------


Support
-------

If you are having issues, please let me know.
You can contact me here:

License
-------

The project is licensed under the MIT License.
