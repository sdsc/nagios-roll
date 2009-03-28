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
# Revision 1.3  2009/03/28 00:40:39  jhayes
# More debugging.
#
# Revision 1.2  2009/03/27 22:58:29  jhayes
# Debugging.
#
# Revision 1.1  2009/03/27 18:54:51  jhayes
# Add nagios host commands.
#
# Revision 1.4  2009/03/27 17:48:42  jhayes
# Tidier implementation.
#
# Revision 1.3  2009/03/26 21:26:50  jhayes
# Begin working on using rocks command to manipulate nagios config.
#
# Revision 1.2  2009/03/17 06:46:59  jhayes
# Follow conventions from other commands.
#
# Revision 1.1  2009/02/05 18:36:05  bruno
# added
#

import string
import rocks.commands

timeperiodDefs = """\
define timeperiod {
  timeperiod_name 24x7    
  alias           All day, every day
  sunday          00:00-24:00
  monday          00:00-24:00
  tuesday         00:00-24:00
  wednesday       00:00-24:00
  thursday        00:00-24:00
  friday          00:00-24:00
  saturday        00:00-24:00
}
"""

hostHeader = """\
define command {
  command_name host-ping
  command_line $USER1$/check_ping -H $HOSTADDRESS$ -w 3000.0,80% -c 5000.0,100% -p 5
}

define host {
  name                          host-defaults
  alias                         Host Defaults
  check_command                 host-ping
  max_check_attempts            10            ; 10 failed pings == "down"
  check_interval                5             ; check every 5 min
  retry_interval                1             ; wait 1 min between retries
  check_period                  24x7          ; check all day, every day
  event_handler_enabled         1
  flap_detection_enabled        1
  process_perf_data             1
  retain_status_information     1
  retain_nonstatus_information  1
  contact_groups                nagios-administrators
  notification_interval         240           ; renotify after 4 hours
  notification_period           24x7          ; send notification whenever
  notification_options          d,u,r         ; down, up, recover
  notifications_enabled         1
  register                      0
}
"""

hostFormat = """\
define host {
  use       host-defaults
  host_name %s
  alias     %s
  address   %s
}
"""

hostgroupFormat = """\
define hostgroup {
  hostgroup_name  All Hosts
  alias           All Hosts
  members         %s
}
"""

# TODO: Here for now, maybe separated later
serviceHeader = """\
define service {
  name                         service-defaults
  is_volatile                  0
  max_check_attempts           4
  check_interval               5
  retry_interval               1
  active_checks_enabled        1
  passive_checks_enabled       1
  check_period                 24x7
  obsess_over_service          1
  check_freshness              0
  event_handler_enabled        1
  flap_detection_enabled       1
  process_perf_data            1
  retain_status_information    1
  retain_nonstatus_information 1
  notification_interval        240
  notification_period          24x7
  notification_options         w,u,c,r
  notifications_enabled        1
  contact_groups               nagios-administrators
  register                     0
}
"""

serviceFormat = """\
define service {
  use                 service-defaults
  hostgroup_name      %s
  service_description %s
  check_command       %s
}
"""

class Command(rocks.commands.Command):
  """
  Add a new nagios host.

  <arg type='string' name='name'>
  The host name.
  </arg>

  <arg type='string' name='ip'>
  The host address.
  </arg>
  """

  def run(self, params, args):

    if len(args) != 2:
      self.abort('name, ip required')

    hosts = string.split(self.command('list.nagios.host'), "\n")
    if len(hosts) == 1 and hosts[0] == '':
      hosts = []
    newHost = args[0] + " " + args[1]
    for host in hosts:
      if host == newHost:
        return
    hosts.append(newHost)

    f = open('/opt/nagios/etc/rocks/timeperiods.cfg', 'w')
    f.write(timeperiodDefs)
    f.close()

    names = []
    f = open('/opt/nagios/etc/rocks/hosts.cfg', 'w')
    f.write(hostHeader)
    for host in hosts:
      (name, ip) = string.split(host)
      f.write("\n")
      f.write(hostFormat % (name, name, ip))
      names.append(name)
    f.write("\n")
    f.write(hostgroupFormat % string.join(names, ','))
    f.write("\n")
    f.write(serviceHeader)
    f.write("\n")
    f.write(serviceFormat % ('All Hosts', 'PING', 'host-ping'))
    f.close()

    return
