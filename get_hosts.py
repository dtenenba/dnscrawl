#!/usr/bin/env python3

"""
crawl DNS records looking for expired ssl certificates
"""

import argparse
import re


TLD = "fhcrc.org"  # could also check fredhutch.org


def main():
    """
    do the work
    """
    parser = argparse.ArgumentParser(description="Get a list of hosts")
    parser.add_argument("intfile", metavar="INTERNALFILE")
    parser.add_argument("extfile", metavar="EXTERNALFILE")
    args = parser.parse_args()
    regex = re.compile("[A-Za-z0-9-_.]{0,}\.%s" % TLD.replace(".", "\."))
    bare_regex = re.compile("^[A-Za-z0-9-_.]{1,}$")
    hostdict = {}
    for filename in [args.intfile, args.extfile]:
        with open(filename) as filehandle:
            lines = filehandle.readlines()
        for line in lines:
            segs = line.split('"')
            name = segs[0].replace('"', "")
            if name != "Name" and name and re.match(bare_regex, name):
                hostdict["{}.{}".format(name, TLD)] = 1
            if TLD in line:
                matches = re.findall(regex, line)
                for match in matches:
                    hostdict[match] = 1

    hosts = sorted(hostdict.keys())
    for host in hosts:
        print(host)


if __name__ == "__main__":
    main()
