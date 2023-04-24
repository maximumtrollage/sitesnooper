# SiteSnooper

basically a simple version of dirbuster.

`./google` is provided as an example output.
As well as `./test_wordlist.txt` for google.

# Usage

```             
usage: sitesnooper.py [-h] -s SITE -t TIMEOUT -w WORDLIST [--threads THREADS]

options:
  -h, --help            show this help message and exit
  -s SITE, --site SITE  pass in the site URL
  -t TIMEOUT, --timeout TIMEOUT
                        connection timeout in seconds
  -w WORDLIST, --wordlist WORDLIST
                        pass in the path to a wordlist
  --threads THREADS     define the number of threads to use. Default is 5
```

Example:
```sh
$ pip3 install -r requirements.txt
# or
$ python3 -m pip install -r requirements.txt
# then
$ python3 .\sitesnooper.py -s google.com -t 1 -w test_wordlist.txt --threads 5
```

Example output:
```
   _____ _ _        _____                                   
  / ____(_) |      / ____|                                  
 | (___  _| |_ ___| (___  _ __   ___   ___  _ __   ___ _ __ 
  \___ \| | __/ _ \\___ \| '_ \ / _ \ / _ \| '_ \ / _ \ '__|
  ____) | | ||  __/____) | | | | (_) | (_) | |_) |  __/ |   
 |_____/|_|\__\___|_____/|_| |_|\___/ \___/| .__/ \___|_|   
    made by: maximumtrollage               | |              
       "h" (79735) on VACBAN               |_|               

    Site....: http://google.com
    Timeout.: .5
    Wordlist: test_wordlist.txt
    Threads.: 10

./exists.txt contains paths that, well, exist.
The opposite for ./doesnt_exist.txt


What was/wasn't found?
     was: /robots.txt
     was: /sitemap.txt

```

# Uhhhhhh

Everything is outputted to: ./SITENAME \
Here is a tree view:
```
📂 - SITENAME
├── 📄 - README.txt
├── 📄 - exists.txt
├── 📄 - doesnt_exist.txt
├── 📄 - robots.txt (if found)
└── 📄 - sitemap.txt (if found)
```

If you want a shit load of wordlists, check out the VACBAN thread you most likely found this on.

# License

SiteSnooper is licensed under the MIT license. See more at [LICENSE](./LICENSE)
