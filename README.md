# HoneyCheck

Versión: ALFA 0.1

HoneyCheck es una utilidad para controlar que no haya servidores DHCP no legítimos dentro de la red en la que nos encontramos y proveer un entorno de actuación modular y totalmente configurable en caso de encontrarlos.


  Wiki:
  https://github.com/CuriosoInformatico/HoneyCheck/wiki


Para empezar a jugar con HoneyCheck primero hay que cumplir con sus dependencias. 

Instalaremos scapy en un entorno virtual para no tocar el entorno de instalación de Python de la máquina real.

    $ git clone https://github.com/CuriosoInformatico/HoneyCheck
    # apt-get install -y python3 python3-virtualenv virtualenv bridge-utils tcpdump
    $ virtualenv -p /usr/bin/python3 venv
    $ source venv/bin/activate
    $ pip install scapy-python3
    
HoneyCheck necesita configurar la interfaz que vayamos a configurar en modo bridge:
Esto se puede configurar en el fichero /etc/network/interfaces siguiendo el siguiente enlace.

https://wiki.debian.org/BridgeNetworkConnections#Configuring_bridging_in_.2Fetc.2Fnetwork.2Finterfaces

En siguiente exto sale de ahí con la adaptación de que en nuestro caso solo queremos hacer un bridge por interfaz para poder controlarlas de forma independiente.

> auto lo br0

> iface lo inet loopback

> iface eth0 inet manual

>iface br0 inet dhcp

>    bridge_ports eth0


