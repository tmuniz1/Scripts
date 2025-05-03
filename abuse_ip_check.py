####################################################################################
#
# Name: abuse_ip_check.py
# Author: Tim Muniz
# Date: 10-17-2024
#
# Description: Checks AbuseIP DB website if an IP/IPs have been reported. 
# Syntax: python abuse_ip_check.py [-h] [-i IP] [-f FILE]
#
####################################################################################
import requests
import json
import argparse
import sys
import pycountry

# Defining the api-endpoint
url = 'https://api.abuseipdb.com/api/v2/check'


def lookupFile(susFile):
    headers = {'Accept': 'application/json','Key': '<API_KEY>'}
    
    with open(susFile) as file:
        for susIP in file:
            susIP = susIP.strip()
            querystring = {'ipAddress': susIP,'maxAgeInDays': '90'}
            #print("IP Address:" + susIP + "\r\n")
            response = requests.request(method='GET', url=url, headers=headers, params=querystring)
            # Formatted output
            decodedResponse = json.loads(response.text)
            print("******Abuse Report******")
            print (json.dumps(decodedResponse, sort_keys=True, indent=4))
            print("IP Address: "+ decodedResponse["data"]["ipAddress"])
            print("Abuse Score: "+ str(decodedResponse["data"]["abuseConfidenceScore"]))
            countryName = str(decodedResponse["data"]["countryCode"])
            country = pycountry.countries.get(alpha_2=countryName)
            if country != None:
                print("Country: ", country.name)
            else:
                print("Country not found.")
            print("ISP: " + str(decodedResponse["data"]["isp"]) + "\n")
            #print (json.dumps(decodedResponse, sort_keys=True, indent=4))

def lookupIP(susIP):
    headers = {'Accept': 'application/json','Key': '<API_KEY>'}
    querystring = {'ipAddress': susIP,'maxAgeInDays': '90'}
    response = requests.request(method='GET', url=url, headers=headers, params=querystring)
    # Formatted output
    decodedResponse = json.loads(response.text)
    #print (json.dumps(decodedResponse, sort_keys=True, indent=4))
    print("******Abuse Report******")
    print("IP Address: "+ decodedResponse["data"]["ipAddress"])
    print("Abuse Score: "+ str(decodedResponse["data"]["abuseConfidenceScore"]))
    countryName = pycountry.countries.get(alpha_2=str(decodedResponse["data"]["countryCode"]))
    print("Country: ", countryName.name)
    print("ISP: " + str(decodedResponse["data"]["isp"]) + "\n")


def main(argv):
    parser = argparse.ArgumentParser(description="Pulls the AbuseIP information for a given IP.")
    parser.add_argument('-i', '--ip', help="Suspicious IP Address")
    parser.add_argument('-f', '--file', help="File with Suspicious IPS")
    args = parser.parse_args()

    if args.ip:
        lookupIP(args.ip)
    elif args.file:
        lookupFile(args.file)
    else:
        sys.exit("Syntax: python abuse_ip_check.py [-h] [-i IP] [-f FILE]")


if __name__ == "__main__":
    main(sys.argv[1:])
