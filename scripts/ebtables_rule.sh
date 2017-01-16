#!/usr/bin/env bash

# REQUIRE whitelist param in configuration

trusty_dhcp_server=$(echo $@ | cut -f 2 -d "-");

echo $trusty_dhcp_server;
echo '--';
echo $@;

ebtables -A INPUT -p 0x0800 --ip-proto udp --ip-source ! $trusty_dhcp_server --ip-source-port 67:68 -j DROP;
/etc/init.d/networking restart