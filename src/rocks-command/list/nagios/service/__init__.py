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
# Revision 1.4  2009/04/15 16:50:26  jhayes
# Allow specification of per-service monitoring timeperiod.  Remove copying of
# sample configuration to target.
#
# Revision 1.3  2009/04/13 19:10:10  jhayes
# Concentrate nagios config file parsing in parent nagios list command class.
#
# Revision 1.2  2009/04/10 21:36:37  jhayes
# Allow definition of service frequency and retry period.
#
# Revision 1.1  2009/03/31 13:37:36  jhayes
# Add service commands.
#
# Revision 1.1  2009/03/27 18:54:52  jhayes
# Add nagios host commands.
#
# Revision 1.4  2009/03/26 21:26:50  jhayes
# Begin working on using rocks command to manipulate nagios config.
#
# Revision 1.3  2009/03/25 19:55:30  jhayes
# Change default email to cluster contact.
#
# Revision 1.2  2009/03/17 06:46:59  jhayes
# Follow conventions from other commands.
#
# Revision 1.1  2009/02/05 18:36:05  bruno
# added
#

import re
import rocks.commands

class Command(rocks.commands.list.nagios.Command):
  """
  Show nagios services.
  """

  def run(self, params, args):
    objects = self.parse_nagios_file('/opt/nagios/etc/rocks/services.cfg')
    services = []
    commands = {}
    for object in objects:
      if 'command_name' in object:
        found = re.search(r'^(.*/)?([^/]+)$', object['command_line'])
        if found:
          commands[object['command_name']] = found.group(2)
    for object in objects:
      if 'service_description' in object:
        services.append(
          'name="%s" hosts="%s" command="%s" contacts="%s" frequency="%s" retry="%s" timeperiod="%s"' %
          (object['service_description'], object['hostgroup_name'],
           commands[object['check_command']], object['contact_groups'],
           object['check_interval'], object['retry_interval'],
           object['check_period'])
        )
    self.addText("\n".join(services))
