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
# Revision 1.2  2009/04/13 23:19:10  jhayes
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

import re
import rocks.commands

class Command(rocks.commands.Command):
  """
  Add a new nagios notification email.
  """

  def parse_attributes(self, lines):
    """
    Converts a list of lines with the format attr=value [attr=value ...] to a
    list of dictionaries.
    """
    result = []
    for line in lines:
      object = {}
      s = line
      parse = re.match(r'\s*(\w+)=(\'[^\']*\'|"[^"]*"|[^\'"\s]+)', s)
      while parse:
        object[parse.group(1)] = parse.group(2).strip('\'"')
        s = s[len(parse.group(0)):]
        parse = re.match(r'\s*(\w+)=(\'[^\']*\'|"[^"]*"|[^\'\s"]+)', s)
      result.append(object)
    return result

  def parse_file(self, path):
    """
    Converts a file containing lines of the format attr=value [attr=value ...]
    to a list of dictionaries.
    """
    f = open(path)
    lines = []
    for line in f:
      line = line.strip()
      if line != '' and not line.startswith('#'):
        lines.append(line)
    f.close()
    return self.parse_attributes(lines)

  def parse_list_nagios_output(self, args):
    """
    Converts the output of the "rocks list nagios" command to a list of
    dictionaries.
    """
    lines = self.command('list.nagios', args).split("\n")
    if len(lines) == 1 and lines[0] == '':
      return []
    return self.parse_attributes(lines)
