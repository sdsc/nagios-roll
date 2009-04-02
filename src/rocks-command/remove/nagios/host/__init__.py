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
# Revision 1.6  2009/04/02 17:14:44  jhayes
# Remove redundant restarts.
#
# Revision 1.5  2009/04/01 19:09:02  jhayes
# Allow batch add in prep for sync command.
#
# Revision 1.4  2009/03/31 21:52:31  jhayes
# Restart nagios after adding/removing objects.
#
# Revision 1.3  2009/03/30 21:16:58  jhayes
# Debugging.
#
# Revision 1.2  2009/03/30 19:29:43  jhayes
# Split nagios service manipluation into separate commands.  Remove all add
# arguments in favor of named params.  Lotsa code improvements.
#
# Revision 1.1  2009/03/27 18:54:52  jhayes
# Add nagios host commands.
#
# Revision 1.3  2009/03/26 21:26:50  jhayes
# Begin working on using rocks command to manipulate nagios config.
#
# Revision 1.2  2009/03/17 06:47:00  jhayes
# Follow conventions from other commands.
#
# Revision 1.1  2009/02/05 18:36:05  bruno
# added
#

import os
import re
import tempfile
import rocks.commands

class Command(rocks.commands.Command):
  """
  Remove an existing nagios host.

  <arg type='string' name='name'>
  The host name.
  </arg>
  """

  def run(self, params, args):

    if len(args) != 1:
      self.abort('host name required')

    lines = self.command('list.nagios.host').split("\n")
    if len(lines) == 1 and lines[0] == '':
      lines = []

    tempname = tempfile.mktemp('.txt')
    f = open(tempname, 'w')
    for line in lines:
      if not re.search('name=[\'"]?' + args[0] + r'[\'"]?(\s|$)', line):
        f.write(line + "\n")
    f.close()

    if os.path.exists('/opt/nagios/etc/rocks/hosts.cfg'):
      os.remove('/opt/nagios/etc/rocks/hosts.cfg')
    self.command('add.nagios.host', ['file=' + tempname])

    os.remove(tempname)
    return
