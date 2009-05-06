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
# Revision 1.10  2009/05/06 18:50:09  jhayes
# Clean up implementation using new dump command.
#
# Revision 1.9  2009/04/15 18:26:29  jhayes
# Add shorthand for specifying timeperiods.
#
# Revision 1.8  2009/04/15 16:50:26  jhayes
# Allow specification of per-service monitoring timeperiod.  Remove copying of
# sample configuration to target.
#
# Revision 1.7  2009/04/15 16:18:03  jhayes
# Fix bug in service remove.
#
# Revision 1.6  2009/04/14 20:50:07  jhayes
# More code cleaning.
#
# Revision 1.5  2009/04/13 23:19:10  jhayes
# Code cleaning.
#
# Revision 1.4  2009/04/10 21:36:37  jhayes
# Allow definition of service frequency and retry period.
#
# Revision 1.3  2009/04/01 19:12:50  jhayes
# Add warning header to configuration files.
#
# Revision 1.2  2009/03/31 21:52:31  jhayes
# Restart nagios after adding/removing objects.
#
# Revision 1.1  2009/03/31 13:37:36  jhayes
# Add service commands.
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

serviceHeader = """\
##
## Generated by rocks; do not edit!
##

define service {
  name                         service-defaults
  is_volatile                  0
  max_check_attempts           4
  active_checks_enabled        1
  passive_checks_enabled       1
  obsess_over_service          1
  check_freshness              0
  event_handler_enabled        1
  flap_detection_enabled       1
  process_perf_data            1
  retain_status_information    1
  retain_nonstatus_information 1
  notification_interval        240
  notification_period          always
  notification_options         w,u,c,r
  notifications_enabled        1
  register                     0
}
"""

commandFormat = """\
define command {
  command_name %s
  command_line %s
}
"""

serviceFormat = """\
define service {
  use                 service-defaults
  hostgroup_name      %s
  service_description %s
  check_command       %s
  check_interval      %s
  retry_interval      %s
  check_period        %s
  contact_groups      %s
}
"""

servicesPath = '/opt/nagios/etc/rocks/services.cfg'

class Command(rocks.commands.add.nagios.Command):
  """
  Add a new nagios service.

  <param type='string' name='name'>
  The name of the service.
  </param>

  <param type='string' name='hosts'>
  The host group that provides the service.
  </param>

  <param type='string' name='command'>
  The command to execute to test this service.
  </param>

  <param type='string' name='contacts'>
  The contract group to notify about service state.
  </param>

  <param type='integer' name='frequency'>
  How often to check the service.
  </param>

  <param type='integer' name='retry'>
  How often to retry the service when it fails initially.
  </param>

  <param type='string' name='timeperiod'>
  The times to monitor the service; defaults to always.
  </param>
  """

  def run(self, params, args):

    # Get list of existing services
    objects = self.parse_dump_nagios_output([servicesPath])
    # Allow batch input from file
    if 'file' in params:
      extension = self.parse_file(params['file'])
    else:
      extension = [params]
    for object in extension:
      if not 'name' in object:
        self.abort('name required')
      if not 'hosts' in object:
        self.abort('hosts required')
      if not 'command' in object:
        self.abort('command required')
      if not 'contacts' in object:
        self.abort('contacts required')
      if not 'frequency' in object:
        object['frequency'] = 5
      if not 'retry' in object:
        object['retry'] = 1
      if not 'timeperiod' in object:
        object['timeperiod'] = 'always'
    objects.extend(extension)

    # Dictionaries ensure that user's values override any previous definition
    checkCommandsByName = {}
    checkIntervalsByName = {}
    checkPeriodsByName = {}
    contactGroupsByName = {}
    hostGroupsByName = {}
    retryIntervalsByName = {}
    for object in objects:
      if not ('name' in object and 'hosts' in object and
              'command' in object and 'contacts' in object and
              'frequency' in object and 'retry' in object and
              'timeperiod' in object):
        continue
      name = object['name']
      checkCommandsByName[name] = object['command']
      checkIntervalsByName[name] = object['frequency']
      checkPeriodsByName[name] = object['timeperiod']
      contactGroupsByName[name] = object['contacts']
      hostGroupsByName[name] = object['hosts']
      retryIntervalsByName[name] = object['retry']

    self.command(
      'add.nagios.timeperiod',
      ['name=always', 'sunday=*', 'monday=*', 'tuesday=*', 'wednesday=*',
       'thursday=*', 'friday=*', 'saturday=*']
    )
    f = open(servicesPath, 'w')
    f.write(serviceHeader)
    for name in checkCommandsByName:
      f.write("\n")
      commandName = name + '-command'
      command = checkCommandsByName[name]
      if not command.startswith('/'):
        command = '/opt/nagios/libexec/' + command
      f.write(commandFormat % (commandName, command))
      f.write("\n")
      f.write(
        serviceFormat %
        (hostGroupsByName[name], name, commandName, checkIntervalsByName[name],
         retryIntervalsByName[name], checkPeriodsByName[name],
         contactGroupsByName[name])
      )
    f.close()

    os.system('service nagios restart > /dev/null 2>&1')
