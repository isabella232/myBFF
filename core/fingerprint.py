#! /usr/bin/python
# Fingerprint Web Applications to determine which brute force module should be run.
from requests import session
import requests
import re
from modules.citrixBrute import citrixbrute
from modules.MobileIronBrute import MobileIron
from modules.JuniperBrute import JuniperBrute
from modules.SiteScopeBrute import SiteScopeBrute
from modules.Office365Brute import office365Brute
from modules.owaBrute import OWAlogin
from modules.citrixBrute2010 import citrixbrute2010
from modules.citAPI import citapiBrute
#from modules.SMBbrute import SMB

class Fingerprint():
    def connect(self, config):
        if 'http' in config["HOST"]:
            with session() as c:
                requests.packages.urllib3.disable_warnings()
                if config["vhost"]:
                    initialConnect = c.get(config["HOST"] + "/" + config["vhost"], verify=False)
                else:
                    initialConnect = c.get(config["HOST"], verify=False)
                #print initialConnect.text
                citAPI = re.search('Citrix', initialConnect.text)
                if citAPI:
                    try:
                        citConnect = c.get(config["HOST"] + '/nitro/v1/config', allow_redirects=False, verify=False)
                        if str(citConnect.status_code) == '200':
                            print "[+]  Citrix API found. Running Citrix API Brute Force Module..."
                            citapibrute = citapiBrute()
                            citapibrute.payload(config)
                    except:
                        print "oops"
                cit = re.search('Citrix Access Gateway', initialConnect.text)
                mi = re.search('MobileIron', initialConnect.text)
                jun = re.search('dana-na', initialConnect.text)
                hpss = re.search('SiteScope', initialConnect.text)
                o365 = re.search('outlook', initialConnect.text)
                owa = re.search('Outlook', initialConnect.text)
                cit2 = re.search("Citrix/XenApp", initialConnect.text)
                cit3 = re.search("20[1,0][4,8,0,9] Citrix", initialConnect.text)
                cit4 = re.search("2005 Citrix", initialConnect.text)
                if cit or cit4:
                    print "[+]  Citrix Access Gateway found. Running Citrix Brute Force Module..."
                    citrixBrute = citrixbrute()
                    citrixBrute.payload(config)
                elif cit2 or cit3:
                    print "[+]  Citrix Access Gateway 2010 found. Running Citrix Brute Force Module..."
                    citrixBrute2010 = citrixbrute2010()
                    citrixBrute2010.payload(config)
                elif mi:
                    print "[+]  MobileIron found. Running MobileIron Brute Force Module..."
                    mobileiron = MobileIron()
                    mobileiron.payload(config)
                elif jun:
                    print "[+]  Juniper device found. Running Juniper Brute Force Module..."
                    juniper = JuniperBrute()
                    juniper.payload(config)
                elif hpss:
                    print "[+]  HP SiteScope found. Running SiteScope Brute Force Module..."
                    sitescope = SiteScopeBrute()
                    sitescope.payload(config)
                elif o365:
                    print "[+]  Office365 found. Running Office365 Brute Force Module..."
                    office365 = office365Brute()
                    office365.payload(config)
                elif owa:
                    print "[+]  Outlook Web App found. Running OWA Brute Force Module..."
                    #owalogin = OWAlogin()
                    #owalogin.payload(config)
                    office365 = office365Brute()
                    office365.payload(config)
                else:
                    #print initialConnect.text
                    print "[-]  Fingerprinting Failed."
                    #citapibrute = citapiBrute()
                    #citapibrute.payload(config)
        #elif 'smb' in config["HOST"]:
#            print "[+]  You selected SMB brute forcing. Running SMB Brute Force Module..."
#            smbbrute = SMB()
#            smbbrute.payload(config)
        else:
            print("Other protocols have not yet been implemented, but I'm working on it! :-)")
