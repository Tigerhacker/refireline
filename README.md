# refireline
Emulates the Fireline service to run Fractured Space

Requires a complete responses.json which will be supplied ~~at a later stage~~

Please excuse the crudity of this model. I didn't have time to build it to scale or paint it.

# Summary
Join the dicussion here: https://discordapp.com/channels/160055190710386688/538510896675422258

## Users
To play single player
- Download the modified executable here: https://cdn.discordapp.com/attachments/538510896675422258/561258485661171722/Fractured_Space.7z
- locate your Fractured Space installation root, by default it is located `C:\Program Files (x86)\Steam\steamapps\common\Space`
- Unpack the downloaded .7z, replace the exe in `<installation root>\spacegame\Binaries\Win64`
- Make a batch file with these two lines 
```
set SteamAppId=310380
"C:\Program Files (x86)\Steam\steamapps\common\Space\spacegame\Binaries\Win64\Fractured Space.exe" -flhost=refireline.returnvector.net
```
   changing `C:\Program Files (x86)\Steam\steamapps\common\Space` to match the last step
to use a server hosted by someone else, change this `refireline.returnvector.net` to their domain
- Double click the batch file to launch


## Hosters
There are many ways to host this, here are a few tips and tricks
- **A valid ssl certificate matching the domain you choose is required, the modified exe does not support plain http** (the flag exists, but is broken)
- I have an official container, https://hub.docker.com/r/tigerhacker/refireline I suggest running it and putting a free tier https://cloudflare.com service in front to handle the SSL connection
- This won't work on Google Cloud's App Engine, if the traffic transits a Google Load Balancer, it will fail (The Fireline client does not send a body size with its POST requests when there is no request payload (Google require a content length of 0 to be set or it will reject the request) https://stackoverflow.com/questions/24219654/content-length-error-in-google-cloud-endpoints-testing
- cPanel works with some minor modification
- I personally recommend Linux+Nginx+uWsgi



# Technical info


## Overview
This python flask app spits out pre-recorded responses from `api.fireteam.net` as requested by Fractured Space (FS).
Currently FS is hardcoded to use the url https://api.fireteam.net and also validates the SSL Connection so a custom intercept/root certificate needs to be installed to impersonate the api.

Currently the flask app doesent handle https so a reveres proxy that offloads SSL is needed, the instructions below use MITM Proxy, which is also useful for capturing the original requests

## Setup
Currently, with these basic instructions, ~~you need to install a _Root Certificate_ on your computer~~(Check out the modified exe linked above), this allows MITM proxy to Imitate *ANY* website, like Fireline, or a bank, you should not do this if you don't know what you are doing as it potentially reduces your computers security!
There will be better _safer_ instructutions eventually

This will also interfere with other games that use Fireline, remove the hosts entry when you are done!

- Decide if you want to run the server on localhost or another box/vm, you will need port 443, 8080 free, and preferably also port 80 free

- Download and install MITM Proxy: https://mitmproxy.org/

- Install the root cert used for intercepting on the machine that will run FS
  - The certificate can be found here %userprofile%\.mitmproxy or ~/.mitmproxy
  - Copy the cert to the machine running FS *if it is a different machine*
  - Run this as admin in that folder to install the cert `certutil.exe -importpfx Root mitmproxy-ca-cert.p12`
  - or manually install it using `certmgr` into the following path `Trusted Root Certification Authorities\Certificates`

- Finally Start up MITM Proxy, we're running it in reverse proxy mode
  - `mitmdump.exe -p 443 --mode reverse:http://127.0.0.1:8080/`
  - and start this to get the launcher to not hang
  - `mitmdump.exe -p 80 --mode reverse:http://127.0.0.1:8080/`

- Edit your `hosts` file to point `api.fireteam.net` at `127.0.0.1` (or the IP of the server running mitm proxy)

- Play fractured space
  - as the Server is serving canned responses which are read only, the store will nolonger work

- Remove the root cert from your computer using `certmgr` when you are done, its called mitmproxy

- Remove the `hosts` entry

## Capture

If you wish to capture your own session (my captures are included for use), here are some basic instructions

- Decide if you want to run the proxy on localhost or another box/vm, you will need port 443 free, and preferably also port 80 free

- Download and install https://mitmproxy.org/

- Install the root cert used for intercepting on the machine that will run FS
  - The certificate can be found here %userprofile%\\.mitmproxy or ~/.mitmproxy
  - Copy the cert to the machine running FS if it is a different machine
  - Run this as admin in that folder to install the cert `certutil.exe -importpfx Root mitmproxy-ca-cert.p12`
  - or manually install it using certmgr into `Trusted Root Certification Authorities\Certificates`

- Finally Start up MITM Proxy, we're running it in reverse proxy mode
  - `mitmdump.exe -p 443 --mode reverse:https://api.fireteam.net:443/ -w dump.out`
  - and start this to get the launcher to not hang
  - `mitmdump.exe -p 80 --mode reverse:http://api.fireteam.net:80/`

- Edit your `hosts` file to point `api.fireteam.net` at `127.0.0.1` (or the IP of the server running mitm proxy)

- Start up FS, optionally launch a conquest solo game (not strictly neccecary), once started and in game, you can quit, quit through the menus, don't force close

- Ctrl+C to exit MITM proxy once FS has shut down

- Remove the root cert from your computer using certmgr, its called _mitmproxy_

- Remove the `hosts` entry

- Finally use the (python 3 only, has dependency issues in python 2.7) script `util/mitm-extractor.py` to build your `responses.json` file
