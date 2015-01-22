PortKnocking
===========

PortKnocking implements port knocking using iptables rules,
however, a complete setup iptables is not generated, only the rules for port knocking are created.
Furthermore, it is able to create a file for port knocking purposes.


Usage
=====

    $ python portknocking.py -h
    Usage: portknocking.py [options] arg1 arg2

    Options:
      -h, --help            show this help message and exit

      Parameters:
        Configuration parameters for iptables rules.

        -p <port ranges>    **REQUIRED** - The ports associated with a process
                            behind a firewall. Ex: -p 1111,2222; -p 4444,2222,7777
        -l <port>, --portConnect=<port>
                            **REQUIRED** - The port to connect.
        -m <tcp|udp|interchange>, --mode=<tcp|udp|interchange>
                            The protocol associated with the port ranges.
        -t <seconds>        Time limit to connect to the daemon.
        -x <tcp|udp>, --protocol=<tcp|udp>
                            The protocol associated with the port to connect.
        -s <server>, --server=<server>
                            Destination server.

      Miscellaneous:
        -o <FILE>, --output=<FILE>
                            Write created rules to FILE.


Examples
========

    $ python portknocking.py -p 1111,2222,3333 -l 22
    $ python portknocking.py -p 1111,2222,3333 -l 22 -m interchange
    $ python portknocking.py -p 1111,2222,3333 -l 22 -t 10
    $ python portknocking.py -p 1111,2222,3333 -l 22 -s 192.168.20.44


Git Repository
==============

    https://github.com/necro369/portknocking
