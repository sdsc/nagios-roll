# $Id$
#
# @Copyright@
# 
# 				Rocks(tm)
# 		         www.rocksclusters.org
# 		        version 4.3 (Mars Hill)
# 
# Copyright (c) 2000 - 2007 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(tm)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log$
# Revision 1.2  2009/03/17 06:46:59  jhayes
# Follow conventions from other commands.
#
# Revision 1.1  2009/02/05 18:36:05  bruno
# added
#
#

import os
import sys
import string
import rocks.commands
import rocks.reports.base
import rocks.util

header = """
##
## general settings
##

define timeperiod {
        timeperiod_name 24x7
        alias           24 Hours A Day, 7 Days A Week
        sunday          00:00-24:00
        monday          00:00-24:00
        tuesday         00:00-24:00
        wednesday       00:00-24:00
        thursday        00:00-24:00
        friday          00:00-24:00
        saturday        00:00-24:00
}

define host {
        name                            generic-host
        notifications_enabled           1
        event_handler_enabled           1
        flap_detection_enabled          1
        failure_prediction_enabled      1
        process_perf_data               1
        retain_status_information       1
        retain_nonstatus_information    1
	notification_period		24x7
        register                        0
}

define service {
        name                            generic-service
        active_checks_enabled           1
        passive_checks_enabled          1
        parallelize_check               1
        obsess_over_service             1
        check_freshness                 0
        notifications_enabled           1
        event_handler_enabled           1
        flap_detection_enabled          1
        failure_prediction_enabled      1
        process_perf_data               1
        retain_status_information       1
        retain_nonstatus_information    1
        is_volatile                     0
        register                        0
}

define service {
	name				local-service
	use				generic-service
        check_period                    24x7
        max_check_attempts              4
        normal_check_interval           5
        retry_check_interval            1
        contact_groups                  admins
	notification_options		w,u,c,r
        notification_interval           60
        notification_period             24x7
        register                        0
}
"""

contact_template = """
define contact {
        contact_name                    %s
        alias                           %s admin
        service_notification_period     24x7
        host_notification_period        24x7
        service_notification_options    w,u,c,r
        host_notification_options       d,r
        service_notification_commands   notify-by-email
        host_notification_commands      host-notify-by-email
        email                           %s
}
"""

contactgroup_template = """
define contactgroup {
        contactgroup_name       admins
        alias                   Nagios Administrators
        members                 %s
}
"""

service_template = """
define service {
	use			local-service
	host_name		%s
	service_description	PING
	check_command		check_ping!100.0,20%%!500.0,60%%
}
"""

host_template = """
define host {
	use                   generic-host
	host_name             %s
	alias                 Node %s
	address               %s
	check_command         check-host-alive
	max_check_attempts    10
	notification_interval 120
	notification_period   24x7
	notification_options  d,r
	contact_groups        admins
}
"""

hostgroup_template = """
define hostgroup {
	hostgroup_name	%s
	alias           %s
	members         %s
}
"""

class Command(rocks.commands.Command):
	"""
	Generate nagios object entries.

	<example cmd='list nagios'>
	List nagios objects for all known hosts.
	</example>
	"""

	def hostlines(self, subnet, netmask):
		import rocks.ip

		ip  = rocks.ip.IPGenerator(subnet, netmask)

		self.db.execute('select n.id, n.rack, n.rank,'
			     'a.name, a.shortname '
			     'from nodes n, appliances a, memberships m '
			     'where n.membership=m.id and '
			     'm.appliance=a.id and n.site=0 '
			     'order by n.id')

		nodes = []
		for row in self.db.fetchall():
			node = rocks.util.Struct()

			node.id		= row[0]
			node.rack	= row[1]
			node.rank	= row[2]
			node.appname	= row[3]
			node.appalias	= row[4]
			node.warning    = None

			nodes.append(node)

			self.db.execute('select name,ip from networks where '
				'node=%d and device="eth0"' % (node.id))
			row = self.db.fetchone()

			node.name = [row[0],]
			node.address = row[1]

			if not node.address:
				node.address = ip.dec()

			name  = node.appname
			alias = node.appalias
			if None in (node.rack, node.rank):
				# Alias require a rank otherwise they
				# may not be unique
				alias = None
			else:
				name = name + '-%d-%d' % (node.rack, node.rank)
				if alias:
					alias = alias + '%d-%d' \
						% (node.rack, node.rank)

			# If there is no name in the database, use the
			# generated one.  Otherwise if the generated
			# name does not match the one in the database,
			# don't create an alias, and remark about it.

			if not node.name[0]:
				node.name = [name,]
			
			if node.name[0] != name:
				#node.warning = 'originally %s' % name
				node.name.append (name)
			elif alias:
				node.name.append(alias)

		# Append names from the Aliases table.
		
		for node in nodes:
			self.db.execute('select name from aliases '
				     'where node = %d' % (node.id))
			for alias in self.db.fetchall():
				node.name.append(alias)

		#
		# admin contact info
		#
		contacts = self.command('list.nagios.contact')
		
		for contact in string.split(contacts, ','):
			entry = contact_template % (contact, contact, contact)
			self.addText(entry)

		entry = contactgroup_template % (contacts)
		self.addText(entry)

		#
		# host config
		#
		for node in nodes:
			primary_name = node.name[0]
			if len(node.name) > 1:
				alias_name = node.name[1]
			else:
				alias_name = primary_name

			entry = host_template % \
				(primary_name, alias_name, node.address)
			self.addText(entry)

		#
		# service config
		#
		for node in nodes:
			entry = service_template % (node.name[0])
			self.addText(entry)

		#
		# host group config
		#
		clustername = self.db.getGlobalVar('Info', 'ClusterName')

		n = []
		for node in nodes:
			n.append(node.name[0])
		nodelist = string.join(n, ',')

		entry = hostgroup_template % \
			(clustername, clustername, nodelist)
		self.addText(entry)

		return

      
	def run(self, params, args):
		if len(args) == 0:
			object = 'all'
		elif len(args) == 1:
			object = args[0]
		else:
			self.help()
			sys.exit(-1)

		#
		# print the generic header info
		# 
		self.addText(header)

		#
		# Build the static addresses
		#
		network = self.db.getGlobalVar('Kickstart', 'PrivateNetwork')
		netmask = self.db.getGlobalVar('Kickstart', 'PrivateNetmask')
		self.hostlines(network, netmask)

