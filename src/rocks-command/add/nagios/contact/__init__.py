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
# Revision 1.16  2009/04/15 18:26:29  jhayes
# Add shorthand for specifying timeperiods.
#
# Revision 1.15  2009/04/15 16:50:26  jhayes
# Allow specification of per-service monitoring timeperiod.  Remove copying of
# sample configuration to target.
#
# Revision 1.14  2009/04/15 01:39:40  jhayes
# Add separate commands for manipulating timeperiod definitions.
#
# Revision 1.13  2009/04/14 20:50:07  jhayes
# More code cleaning.
#
# Revision 1.12  2009/04/13 23:19:10  jhayes
# Code cleaning.
#
# Revision 1.11  2009/04/01 19:12:50  jhayes
# Add warning header to configuration files.
#
# Revision 1.10  2009/03/31 21:52:30  jhayes
# Restart nagios after adding/removing objects.
#
# Revision 1.9  2009/03/30 19:29:42  jhayes
# Split nagios service manipluation into separate commands.  Remove all add
# arguments in favor of named params.  Lotsa code improvements.
#
# Revision 1.8  2009/03/28 06:15:02  jhayes
# Add ability to specify contact groups when adding contact.
#
# Revision 1.7  2009/03/28 00:40:39  jhayes
# More debugging.
#
# Revision 1.6  2009/03/27 22:58:29  jhayes
# Debugging.
#
# Revision 1.5  2009/03/27 18:54:51  jhayes
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

contactHeader = """\
##
## Generated by rocks; do not edit!
##

define command {
  command_name email-re-host
  command_line /usr/bin/printf "%b" "***** Nagios *****\\n\\nNotification Type: $NOTIFICATIONTYPE$\\nHost: $HOSTNAME$\\nState: $HOSTSTATE$\\nAddress: $HOSTADDRESS$\\nInfo: $HOSTOUTPUT$\\n\\nDate/Time: $LONGDATETIME$\\n" | @MAIL_PROG@ -s "** $NOTIFICATIONTYPE$ Host Alert: $HOSTNAME$ is $HOSTSTATE$ **" $CONTACTEMAIL$
}

define command {
  command_name email-re-service
  command_line /usr/bin/printf "%b" "***** Nagios *****\\n\\nNotification Type: $NOTIFICATIONTYPE$\\n\\nService: $SERVICEDESC$\\nHost: $HOSTALIAS$\\nAddress: $HOSTADDRESS$\\nState: $SERVICESTATE$\\n\\nDate/Time: $LONGDATETIME$\\n\\nAdditional Info:\\n\\n$SERVICEOUTPUT$" | @MAIL_PROG@ -s "** $NOTIFICATIONTYPE$ Service Alert: $HOSTALIAS$/$SERVICEDESC$ is $SERVICESTATE$ **" $CONTACTEMAIL$
}

define contact {
  name                          contact-defaults
  host_notifications_enabled    1
  service_notifications_enabled 1
  host_notification_period      always
  service_notification_period   always
  host_notification_options     d,u,r,f,s
  service_notification_options  w,u,c,r,f,s
  host_notification_commands    email-re-host
  service_notification_commands email-re-service
  register                      0
}
"""

contactFormat = """\
define contact {
  use           contact-defaults
  contact_name  %s
  contactgroups %s
  email         %s
}
"""

contactgroupFormat = """\
define contactgroup {
  contactgroup_name %s
  alias             %s
  members           %s
}
"""

contactsPath = '/opt/nagios/etc/rocks/contacts.cfg'

class Command(rocks.commands.add.nagios.Command):
  """
  Add a new nagios notification email.

  <param type='string' name='email'>
  The notification email address.
  </param>

  <param type='string' name='groups'>
  Contact groups that should include this contact.
  </param>

  <example cmd='add nagios contact email=me@myhost.org'>
  </example>

  <example cmd='add nagios contact email=me@myhost.org groups=administrators'>
  </example>
  """

  def run(self, params, args):

    # Get list of existing contacts
    objects = self.parse_list_nagios_output(['file=' + contactsPath])
    # Allow batch input from file
    if 'file' in params:
      extension = self.parse_file(params['file'])
    else:
      extension = [params]
    # Allow Nagios names as alternative to param names--makes implementation of
    # remove cleaner
    for object in extension:
      if not 'email' in object:
        self.abort('email required')
      if 'groups' in object:
        object['contactgroups'] = object['groups']
      elif not 'contactgroups' in object:
        object['contactgroups'] = object['email'] + ' group'
    objects.extend(extension)

    # Dictionaries ensure that user's values override any previous definition
    contactGroupsByEmail = {}
    membersByGroup = {}
    for object in objects:
      if not ('email' in object and 'contactgroups' in object):
        continue
      email = object['email']
      contactGroupsByEmail[email] = object['contactgroups']
      for group in object['contactgroups'].split(','):
        if not group in membersByGroup:
          membersByGroup[group] = email
        else:
          membersByGroup[group] += ',' + email

    self.command(
      'add.nagios.timeperiod',
      ['name=always', 'sunday=*', 'monday=*', 'tuesday=*', 'wednesday=*',
       'thursday=*', 'friday=*', 'saturday=*']
    )
    f = open(contactsPath, 'w')
    f.write(contactHeader)
    for email in contactGroupsByEmail:
      f.write("\n")
      f.write(contactFormat % (email, contactGroupsByEmail[email], email))

    for group in membersByGroup:
      f.write("\n")
      f.write(contactgroupFormat % (group, group, membersByGroup[group]))
    f.close()

    os.system('service nagios restart > /dev/null 2>&1')
