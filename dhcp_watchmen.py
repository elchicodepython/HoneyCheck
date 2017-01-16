import logging.config
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)


from threading import Thread
from scapy.all import *
import time


logger = logging.getLogger(name='elchicodepython.honeycheck')


def exec_array( array, **kwargs):
    for object, method in array:
       method(object, **kwargs) # == object.method()



class DHCPServer:

    def __init__(self, ip, hw):
        self.ip = ip
        self.hw = hw

    def __repr__(self):
        return '<DHCPServer Object (ip = %s, hw = %s)>' % (self.ip, self.hw)

    def __str__(self):
        return '<DHCPServer Object (ip = %s, hw = %s)>' % (self.ip, self.hw)


class Status:
    OK = 1
    ROGUE_DETECTED = 2


class DHCPWatchmen:

    def __init__(self, iface, fail_test, pass_test, final_exec, whitelist):

        '''
        :param iface: interface to watch
        :param fail_test: action to trigger if a rogue dhcp server is detected
        :param pass_test: action to trigger if there are no rogue dhcp servers detected
        :param final_exec: action to trigger always after fail_test or pass_test
        :param whitelist: list of IPs of verified DHCP servers to ignore.
        '''

        self.iface = iface
        self.hw = get_if_hwaddr(iface)
        self.fail_test = fail_test
        self.pass_test = pass_test
        self.final_exec = final_exec
        self.whitelist = whitelist

        self.dhcp_servers = {}
        self.last_status = Status.OK




    def check_dhcp_servers(self, number_allowed):

        '''
        Check if the number of DHCP Servers detected is allowed
        and trigger the corresponding action to each situation
        :param number_allowed: number of dhcp_servers allowed
        '''

        if len(self.dhcp_servers) > number_allowed:
            if self.last_status != Status.ROGUE_DETECTED:
                logger.warning('MORE DHCP SERVERS THAN ALLOWED: ')
                self.last_status = Status.ROGUE_DETECTED
                exec_array(self.fail_test, watchmen = self)
            self.dhcp_servers = {}


        else:
            if self.last_status != Status.OK:
                logger.info('All seems right')
                self.last_status = Status.OK
                exec_array(self.pass_test, watchmen = self)

        exec_array(self.final_exec, watchmen=self)

    def check_packet(self, packet):


        if packet.payload.op == 2:

            if self.whitelist:
                if (packet.payload.src not in self.whitelist):
                    self.dhcp_servers[packet.payload.src] = DHCPServer(packet.payload.src, packet.src)
            else:
                self.dhcp_servers[packet.payload.src] =  DHCPServer(packet.payload.src, packet.src)

    def send_dhcp_discovery(self):
        dhcp_discover = Ether(dst="ff:ff:ff:ff:ff:ff") / IP(src="0.0.0.0", dst="255.255.255.255") / UDP(sport=68, dport=67) / BOOTP(chaddr=self.hw, flags = 0x8000) / DHCP(options=[("message-type", "discover"), "end"])
        sendp(dhcp_discover, verbose = 0)
        logger.debug('DHCP DISCOVER SEND')

    def dhcp_discovery_daemon(self, timeout):

        if self.whitelist:
            # There are no supposed to be DHCP servers that dont exists in the whitelist
            logger.info('Whitelist enabled for ' + self.iface)
            max_servers_allowed = 0
        else:
            # It is suppose to be at least one DHCP Server in the network
            logger.info('Executing HoneyCheck in %s without Whitelist' % self.iface)
            max_servers_allowed = 1

        while True:
            self.send_dhcp_discovery()
            time.sleep(timeout)
            self.check_dhcp_servers(max_servers_allowed)

    def sniff_dhcp(self):
        sniff(iface = self.iface, filter='udp port 68', prn = self.check_packet)


    def __repr__(self):
        return '<DHCPSWatchmen Object (iface = %s)>' % (self.iface)

    def __str__(self):
        return '<DHCPSWatchmen Object (iface = %s)>' % (self.iface)




