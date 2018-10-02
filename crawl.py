#!/usr/bin/env python3

"""
crawl DNS records looking for expired ssl certificates
"""

import argparse
import re

from io import StringIO
import requests
import sh


TLD = "fhcrc.org" # could also check fredhutch.org

def main():
    """
    do the work
    """
    parser = argparse.ArgumentParser(description='Check for expired certs')
    parser.add_argument("infile", metavar="INPUTFILE")
    args = parser.parse_args()
    regex = re.compile("[A-Za-z0-9-_.]{0,}\.%s" % TLD.replace(".", "\."))
    with open(args.infile) as infile:
        lines = infile.readlines()
    print(len(lines))
    hostdict = {}
    for line in lines:
        if TLD in line:
            matches = re.findall(regex, line)
            for match in matches:
                hostdict[match] = 1
    hosts = sorted(hostdict.keys())
    for host in hosts:
        print(host)
        buf = StringIO()   
        sh.openssl(sh.openssl(sh.echo(_piped=True), "s_client", "-showcerts", "-servername", host, "-connect", "{}:443".format(host), _piped=True), "x509", "-inform", "pem", "-noout", "-text", _out=buf)
        # echo | openssl s_client -showcerts -servername gnupg.org -connect gnupg.org:443 2>/dev/null | openssl x509 -inform pem -noout -text
        


if __name__ == "__main__":
    main()
