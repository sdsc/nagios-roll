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
# Revision 1.2  2009/04/15 18:26:29  jhayes
# Add shorthand for specifying timeperiods.
#
# Revision 1.1  2009/04/15 01:39:41  jhayes
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

timeperiodsHeader = """\
##
## Generated by rocks; do not edit!
##
"""

timeperiodFormat = """\
define timeperiod {
  timeperiod_name %s
  alias           %s
%s}
"""
dayperiodFormat = "  %-16s%s\n"

timeperiodsPath = '/opt/nagios/etc/rocks/timeperiods.cfg'

class Command(rocks.commands.add.nagios.Command):
  """
  Add a new nagios timeperiod.

  <param type='string' name='name'>
  The timeperiod name.
  </param>

  <param type='string' name='sunday'>
  The time range for Sunday
  </param>

  <param type='string' name='monday'>
  The time range for Sunday
  </param>

  <param type='string' name='tuesday'>
  The time range for Sunday
  </param>

  <param type='string' name='wednesday'>
  The time range for Sunday
  </param>

  <param type='string' name='thursday'>
  The time range for Sunday
  </param>

  <param type='string' name='friday'>
  The time range for Sunday
  </param>

  <param type='string' name='saturday'>
  The time range for Sunday
  </param>
  """

  def run(self, params, args):

    days = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday',
            'friday', 'saturday')

    # Get list of existing timeperiods
    objects = self.parse_list_nagios_output(['file=' + timeperiodsPath])
    # Allow batch input from file
    if 'file' in params:
      extension = self.parse_file(params['file'])
    else:
      extension = [params]
    # Allow Nagios names as alternative to param names--makes implementation of
    # remove cleaner
    for object in extension:
      if 'name' in object:
        object['timeperiod_name'] = object['name']
      elif not 'timeperiod_name' in object:
        self.abort('name required')
    objects.extend(extension)

    # Dictionaries ensure that user's values override any previous definition
    dayperiodsByName = {}
    for object in objects:
      if 'timeperiod_name' in object:
        dayperiodsByName[object['timeperiod_name']] = object

    f = open(timeperiodsPath, 'w')
    f.write(timeperiodsHeader)
    for name in dayperiodsByName:
      dayperiods = ''
      for day in days:
        if day in dayperiodsByName[name]:
          period = dayperiodsByName[name][day]
          if period == '*':
            period = '00:00-24:00'
          dayperiods += dayperiodFormat % (day, period)
      f.write("\n")
      f.write(timeperiodFormat % (name, name, dayperiods))
    f.close()

    os.system('service nagios restart > /dev/null 2>&1')