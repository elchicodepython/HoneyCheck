#!/usr/bin/env bash

dhcp_servers=$(echo $@ | cut -f 1 -d "-");

zenity --warning --text "HoneyCheck: SOMETHING SUSPICIUS WITH DHCP SERVERS\n$dhcp_servers";