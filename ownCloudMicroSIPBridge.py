# The MIT License (MIT)
# 
# Copyright (c) 2015 Roland Rickborn
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Intro:
# This python script generates a contacts.xml file whic fits as addressbook to
# the VoIP client MicroSIP (http://www.microsip.org). It uses the CardDAV CLI
# client pyCardDAV (https://github.com/geier/pycarddav) to fetch the contact
# data from an CardDAV location like ownCloud.
#
# Requirements:
# - Python 2.7 (tested)
# - MicroSIP 3.10.1 (tested)
# - Runs on M$ Windows 8.1 (tested)
# - Runs with ownCloud 8 (tested)
#
# Usage:
# 1) Change the settings below in section "My Settings"
# 2) Runt "python ownCloudMicroSIPBridge.py"

try:
    import subprocess
    import shutil
    import string
    import os
    import time
    import sys
except ImportError as error:
    sys.stderr.write(str(error))
    sys.exit(1)

__author__ = 'Roland Rickborn'

# My Settings
pathToPython = 'c:\Python27\python.exe'
pathToPyCardSync = 'c:\Python27\Scripts\pycardsyncer'
pathToPyCardQuery = 'c:\Python27\Scripts\pc_query'
pathToConfFile = '%LOCALAPPDATA%\PyCardDAV\pycard.conf'
pathToMicroSipContactFile = '%APPDATA%\MicroSIP\Contacts.xml'

# Sync data
subprocess.call([pathToPython,pathToPyCardSync,'-c',pathToConfFile])

# Read data
retval = subprocess.check_output([pathToPython,pathToPyCardQuery,'-c',pathToConfFile,'-A'])

# Split initial welcome text
tmp = string.split(retval,"searching for ...\r\n")
tmp = string.replace(tmp[1],"\r","")

# Get raw contact data
contact_raw = string.split(tmp,"Name: ")

# Destill required contact data
contacts = []
for item1 in contact_raw:
    try:
        has_phone_work = 0
        has_phone_mobil = 0
        has_phone_home = 0
        telhome = 0
        telmobil = 0
        telwork = 0
        tmp_item = string.split(item1,"\n")
        name_raw = tmp_item[0]
        if name_raw.find(",") >= 0:
            tmp = string.split(name_raw,",")
            firstname = tmp[1].strip()
            lastname = tmp[0].strip()
        else:
            tmp = string.split(name_raw," ")
            firstname = tmp[0].strip()
            name_raw = string.join(tmp[1:]," ")
            lastname = name_raw.strip()
        for item2 in tmp_item:
            if item2.startswith("TEL"):
                if item2.find("WORK") >= 0 and item2.find("VOICE") >= 0:
                    #TEL (PREF, WORK, VOICE): +49715116192311
                    tmp = string.split(item2,":")
                    telwork_raw = string.replace(tmp[1]," ","")
                    telwork_raw = string.replace(telwork_raw,"-","")
                    telwork = "%s %s" % (telwork_raw[0:3],telwork_raw[3:])
                    if len(telwork) > 3:
                        has_phone_work = 1
                elif item2.find("CELL") >= 0 and item2.find("VOICE") >= 0:
                    #TEL (CELL, VOICE): +491716726811
                    tmp = string.split(item2,":")
                    telmobil_raw = string.replace(tmp[1]," ","")
                    telmobil_raw = string.replace(telmobil_raw,"-","")
                    telmobil = "%s %s" % (telmobil_raw[0:3],telmobil_raw[3:])
                    if len(telmobil) > 3:
                        has_phone_mobil = 1
                elif item2.find("HOME") >= 0 and item2.find("VOICE") >= 0:
                    #TEL (PREF, HOME, VOICE): +49 7243531304
                    tmp = string.split(item2,":")
                    telhome_raw = string.replace(tmp[1]," ","")
                    telhome_raw = string.replace(telhome_raw,"-","")
                    telhome = "%s %s" % (telhome_raw[0:3],telhome_raw[3:])
                    if len(telhome) > 3:
                        has_phone_home = 1
            elif item2.startswith("ORG"):
                #ORG: exensio GmbH;
                tmp = string.split(item2,":")
                org_raw = string.replace(tmp[1],";","")
                org = org_raw.strip()
        if has_phone_home == 1:
            contacts.append([firstname,lastname,org,telhome,'Home'])
        if has_phone_mobil == 1:
            contacts.append([firstname,lastname,org,telmobil,'Mobil'])
        if has_phone_work == 1:
            contacts.append([firstname,lastname,org,telwork,'Work'])
    except:
        continue

# Create output file
f = open(r'%TMP%\_Contacts.xml', 'w')
f.write('<?xml version="1.0"?>\n')
f.write('<contacts>\n')
for item in contacts:
    f.write('<contact number="%s"  name="%s %s (%s, %s)"  presence="0"  directory="0" ></contact>\n'
            % (item[3],item[0],item[1],item[2],item[4]))
f.write('</contacts>\n')
f.close()

# Copy output file
shutil.copyfile('%TMP%\_Contacts.xml',pathToMicroSipContactFile)
os.remove('%TMP%\_Contacts.xml')
sys.exit(0)