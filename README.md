# ownCloudMicroSIPBridge
Fetches contact data from ownCloud and creates contacts.xml file for MicroSIP VoIP client

# Intro:
This python script generates a contacts.xml file whic fits as addressbook to
the VoIP client MicroSIP (http://www.microsip.org). It uses the CardDAV CLI
client pyCardDAV (https://github.com/geier/pycarddav) to fetch the contact
data from an CardDAV location like ownCloud.

# Requirements:
- Python 2.7 (tested)
- MicroSIP 3.10.1 (tested)
- Runs on M$ Windows 8.1 (tested)
- Runs with ownCloud 8 (tested)

# Usage:
- Change the settings below in section "My Settings"
- Run "python ownCloudMicroSIPBridge.py"
