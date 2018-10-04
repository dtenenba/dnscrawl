# SSL Certificate Crawler

## Prerequisites

* Python 3
* [Pipenv](https://pipenv.readthedocs.io/en/latest/)
* The `openssl` command

## Setup


```
git clone https://github.com/dtenenba/dnscrawl.git
cd dnscrawl
pipenv install # install dependencies
pipenv shell # run this each time you want to run the program(s)
```

### Get CSV files from InfoBlox

InfoBlox has an API but it ended up being easier to export information from the web UI than to learn how to use the API to get the same information. ;-)

1. Log into InfoBlox: https://ibx0.fhcrc.org/ui/
2. Go to [DNS View](https://ibx0.fhcrc.org/ui/nBJ-Hf7PKRawZ-jMk12q6w/nBJc5/Mk172#-1967799319)
3. Click on `External`, then, `fhcrc.org` ([direct link](https://ibx0.fhcrc.org/ui/0_MKtoqgCQPbXOhF67jWpg/0_M1d/XOh70#-728562417))
4. Click the Export button (an arrow pointing towards the upper right)
5. Click `Start`
6. When export is done, click Download and save the file. 
7. Name it `InfoBloxExternalFhcrc.csv` (or `InfoBloxInternalFhcrc.csv` if
  downloading the internal data).
8. Repeat steps `3` onward, but clicking on `Internal` instead of `External`. ([direct link](https://ibx0.fhcrc.org/ui/0_MKtoqgCQPbXOhF67jWpg/0_M1d/XOh70#1981605629))  









## Scripts

There are two scripts, the first one (`get_hosts.py`)  processes the data from InfoBlox 
and the second one (`cert_crawl.py`) looks up the certificate of each host and writes out
information about the certificate.

### Get list of hosts

Run as follows:

```
python3 get_hosts.py InfoBloxInternalFhcrc.csv InfoBloxExternalFhcrc.csv > hosts.txt
```

### Query certificates:

Run as follows. You may see output that looks like errors, but you can safely ignore it. It just means that many hosts are not listening on port 443 or do not have certificates set up.


```
python3 cert_crawl.py hosts.txt | tee certinfo.tsv
```

When done, the output file (`certinfo.tsv`) will contain 3 tab-delimited columns, the first is the host name, the second is the serial number of the certificate, and the third is the certificate expiration date.

You can filter this list to show only the ones that expire in November 2018:

```
grep "Nov 23" certinfo.tsv | grep 2018 > expiring.txt
```

Now `expiring.txt` contains the names of hosts whose certificates expire in November 2018. These **should** have the same certificate serial number  (indicating the `fhcrc.org` wildcard certificate and expiration date).


## Notes

* This only scans port 443. We can modify it to scan other ports.
* This program **may** set off alarm bells in ISO, but I have not gotten in trouble yet.