#!/usr/bin/env python
"""
portknocking.py

"""

from optparse import OptionParser, OptionGroup
from random import randint
import os.path

def main():
	usage = "usage: %prog [options] arg1 arg2"
	parser = OptionParser(usage)

	group1 = OptionGroup(
        	parser, "Parameters",
        	"Configuration parameters for iptables rules."
	)
	group1.add_option(
		"-p", dest="portranges", metavar="<port ranges>",
		help="**REQUIRED** - The ports associated with a process behind a firewall. Ex: -p 1111,2222; -p 4444,2222,7777"
	)
	group1.add_option(
		"-l", "--portConnect", dest="connect", metavar="<port>",
		help="**REQUIRED** - The port to connect."
	)
	group1.add_option(
		"-m", "--mode", dest="mode", metavar="<tcp|udp|interchange>", default="tcp",
		help="The protocol associated with the port ranges."
	)
	group1.add_option(
		"-t", dest="time", metavar="<seconds>", type="int", default=30,
		help="Time limit to connect to the daemon."
	)
	group1.add_option(
		"-x", "--protocol", dest="connectprotocol", metavar="<tcp|udp>", default="tcp",
		help="The protocol associated with the port to connect."
	)
	group1.add_option(
		"-s", "--server", dest="server", metavar="<server>", default="your_server",
		help="Destination server."
	)
	parser.add_option_group(group1)

	group2 = OptionGroup(
        parser, "Miscellaneous",
	)
	group2.add_option(
		"-o", "--output", dest="output", metavar="<FILE>",
		help="Write created rules to FILE."
	)
	parser.add_option_group(group2)

	(options, args) = parser.parse_args()

	if options.portranges is None or options.connect is None:
		print "Missing parameters. Use the Help for more information. (-h)"
	else:
		iptables = ""
		ports = options.portranges.split(",")
		if options.mode.lower() == "interchange":
			prot = [("tcp" if randint(0,100)%2 == 0 else "udp") for x in range(len(ports))]
		else:
			prot = [options.mode for x in range(len(ports))]

		for idx, item in enumerate(ports):
			iptables += "iptables -N CHECK" + str(idx+1) + "\n"
			if idx != 0:
				iptables += "iptables -A CHECK" + str(idx+1) + " -m recent --name KNOCK" + str(idx) + " --remove" + "\n"
			iptables += "iptables -A CHECK" + str(idx+1) + " -p " + prot[idx] + " --dport " + str(item) + " -m recent --name KNOCK" + str(idx+1) + " --set -j DROP" + "\n"
			if idx != 0:
				iptables += "iptables -A CHECK" + str(idx+1) + " -j CHECK1" + "\n\n"
			else:
				iptables += "iptables -A CHECK1 -j DROP" + "\n\n"

		iptables += "iptables -N GRANTED" + "\n"
		iptables += "iptables -A GRANTED -m recent --name KNOCK" + str(len(ports)) + " --remove" + "\n"
		iptables += "iptables -A GRANTED -p " + options.connectprotocol + " --dport " + str(options.connect) + " -j ACCEPT" + "\n"
		iptables += "iptables -A GRANTED -j CHECK1" + "\n\n"

		iptables += "iptables -A INPUT -m recent --rcheck --seconds " + str(options.time) + " --name KNOCK" + str(len(ports)) + " -j GRANTED" + "\n"
		for counter in range(len(ports)-1, 0, -1):
			iptables += "iptables -A INPUT -m recent --rcheck --seconds 5 --name KNOCK" + str(counter) + " -j CHECK" + str(counter+1) + "\n"
		iptables += "iptables -A INPUT -j CHECK1" + "\n\n"

		print iptables

		if options.output is not None:
			if os.path.exists("./" + options.output):
				while True:
					name = options.output + "_" + str(randint(0,100))
					if os.path.exists("./" + name) is False:
						break
				print "The '{0}' file exists. Renamed to '{1}'.".format(options.output, name)
			else:
				name = options.output

			f = open(name, "w")
			f.write(iptables)
			f.close()
			
			print "File saved.\n"

		connectionfile = "portknocking_connection_" + str(options.connect) + "_" + str(options.connectprotocol)
		if os.path.exists("./" + connectionfile):
			while True:
				n = connectionfile + "-" + str(randint(0,100))
				if os.path.exists("./" + n) is False:
					connectionfile = n
					break

		f = open(connectionfile, "w")
		f.write('#!/bin/bash\n\n')
		f.write('ports=( ')
		for item in ports:
			f.write('"%s" ' % item)
		f.write(')\n')
		f.write('protocol=( ')
		for item in prot:
			f.write('"%s" ' % item)
		f.write(')\n')
		f.write('host="' + options.server + '"\n\n')
		f.write('for x in  ${!ports[*]}; do\n')
		f.write('    if [ "${protocol[$x]}" == "udp" ]; then\n')
		f.write('        hping3 --udp -c 1 $host -p ${ports[$x]}\n')
		f.write('    else\n')
		f.write('        hping3 -c 1 $host -p ${ports[$x]}\n')
		f.write('    fi\n')
		f.write('    sleep 1\n')
		f.write('done\n\n')
		f.write('echo "You have ' + str(options.time) + ' seconds to connect on port ' + str(options.connect) + '"\n')
		f.close()

		print "Port Knocking file saved. (name: {0})".format(connectionfile)

if __name__ == "__main__":
	main()
