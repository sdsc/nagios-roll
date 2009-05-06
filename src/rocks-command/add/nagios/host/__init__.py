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
# Revision 1.14  2009/05/06 18:50:09  jhayes
# Clean up implementation using new dump command.
#
# Revision 1.13  2009/04/15 18:26:29  jhayes
# Add shorthand for specifying timeperiods.
#
# Revision 1.12  2009/04/15 16:50:26  jhayes
# Allow specification of per-service monitoring timeperiod.  Remove copying of
# sample configuration to target.
#
# Revision 1.11  2009/04/15 01:39:40  jhayes
# Add separate commands for manipulating timeperiod definitions.
#
# Revision 1.10  2009/04/14 20:50:07  jhayes
# More code cleaning.
#
# Revision 1.9  2009/04/13 23:19:10  jhayes
# Code cleaning.
#
# Revision 1.8  2009/04/01 19:09:02  jhayes
# Allow batch add in prep for sync command.
#
# Revision 1.7  2009/03/31 21:52:31  jhayes
# Restart nagios after adding/removing objects.
#
# Revision 1.6  2009/03/30 23:14:49  jhayes
# Debugging.
#
# Revision 1.5  2009/03/30 21:16:58  jhayes
# Debugging.
#
# Revision 1.4  2009/03/30 19:29:42  jhayes
# Split nagios service manipluation into separate commands.  Remove all add
# arguments in favor of named params.  Lotsa code improvements.
#
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

import os
import rocks.commands

hostHeader = """\
##
## Generated by rocks; do not edit!
##

define command {
  command_name ping-host
  command_line /opt/nagios/libexec/check_ping -H $HOSTADDRESS$ -w 3000.0,80% -c 5000.0,100% -p 5
}

define host {
  name                          host-defaults
  alias                         Host Defaults
  check_command                 ping-host
  max_check_attempts            10            ; 10 failed pings == "down"
  check_interval                5             ; check every 5 min
  retry_interval                1             ; wait 1 min between retries
  check_period                  always        ; check all day, every day
  event_handler_enabled         1
  flap_detection_enabled        1
  process_perf_data             1
  retain_status_information     1
  retain_nonstatus_information  1
  notification_interval         240           ; renotify after 4 hours
  notification_period           always        ; send notification whenever
  notification_options          d,u,r         ; down, up, recover
  notifications_enabled         1
  register                      0
}
"""

hostFormat = """\
define host {
  use            host-defaults
  host_name      %s
  alias          %s
  address        %s
  hostgroups     %s
  contact_groups %s
}
"""

hostgroupFormat = """\
define hostgroup {
  hostgroup_name  %s
  alias           %s
  members         %s
}
"""

hostsPath = '/opt/nagios/etc/rocks/hosts.cfg'

class Command(rocks.commands.add.nagios.Command):
  """
  Add a new nagios host.

  <param type='string' name='file'>
  Read host definitions from a file.
  </param>

  <param type='string' name='name'>
  The host name.
  </param>

  <param type='string' name='ip'>
  The host address.
  </param>

  <param type='string' name='groups'>
  Host groups that should include this host.
  </param>

  <param type='string' name='contacts'>
  Contact group to be notified of host status.
  </param>

  <example cmd='add nagios host name=nas-0-0 ip=10.1.1.100'>
  </example>

  <example cmd='add nagios host name=compute-0-1 ip=10.1.1.101 groups="compute nodes"'>
  </example>
  """

  def run(self, params, args):

    # Get list of existing hosts
    objects = self.parse_dump_nagios_output([hostsPath])
    # Allow batch input from file
    if 'file' in params:
      extension = self.parse_file(params['file'])
    else:
      extension = [params]
    for object in extension:
      if not 'name' in object:
        self.abort('name required')
      if not 'ip' in object:
        self.abort('ip required')
      if not 'contacts' in object:
        self.abort('contacts required')
      if not 'groups' in object:
        object['groups'] = object['name'] + ' group'
    objects.extend(extension)

    # Dictionaries ensure that user's values override any previous definition
    addressesByName = {}
    contactGroupsByName = {}
    hostGroupsByName = {}
    membersByGroup = {}
    for object in objects:
      if not ('name' in object and 'ip' in object and
              'contacts' in object and 'groups' in object):
        continue
      name = object['name']
      addressesByName[name] = object['ip']
      contactGroupsByName[name] = object['contacts']
      hostGroupsByName[name] = object['groups']
      for group in object['groups'].split(','):
        if not group in membersByGroup:
          membersByGroup[group] = name
        else:
          membersByGroup[group] += ',' + name

    self.command(
      'add.nagios.timeperiod',
      ['name=always', 'sunday=*', 'monday=*', 'tuesday=*', 'wednesday=*',
       'thursday=*', 'friday=*', 'saturday=*']
    )
    f = open(hostsPath, 'w')
    f.write(hostHeader)
    for name in addressesByName:
      f.write("\n")
      f.write(
        hostFormat %
        (name, name, addressesByName[name], hostGroupsByName[name],
         contactGroupsByName[name])
      )

    for group in membersByGroup:
      f.write("\n")
      f.write(hostgroupFormat % (group, group, membersByGroup[group]))
    f.close()

    os.system('service nagios restart > /dev/null 2>&1')
