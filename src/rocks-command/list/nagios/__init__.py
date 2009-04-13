# $Id$
#
# @Copyright@
# 
#         Rocks(tm)
#              www.rocksclusters.org
#             version 4.3 (Mars Hill)
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
#   "This product includes software developed by the Rocks(tm)
#   Cluster Group at the San Diego Supercomputer Center at the
#   University of California, San Diego and its contributors."
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
# Revision 1.4  2009/04/13 23:19:10  jhayes
# Code cleaning.
#
# Revision 1.3  2009/04/13 19:10:10  jhayes
# Concentrate nagios config file parsing in parent nagios list command class.
#
# Revision 1.2  2009/03/17 06:46:59  jhayes
# Follow conventions from other commands.
#
# Revision 1.1  2009/02/05 18:36:05  bruno
# added
#
#

import os
import re
import rocks.commands

class Command(rocks.commands.Command):
  """
  A class that defines common behavior for Nagios list commands.
  """

  def parse_nagios_file(self, path):
    """
    Returns a list of dictionaries that corresponds to the Nagios object
    definitions contained in the given file.
    """
    if not os.path.exists(path):
      return []
    f = open(path, 'r')
    result = self.parse_nagios_definitions(f.readlines())
    f.close()
    return result

  def parse_nagios_definitions(self, lines):
    """
    Returns a list of dictionaries that corresponds to the Nagios object
    definitions contained in the given list of definition lines.
    """
    result = []
    object = {}
    for line in lines:
      parse = re.match(r'^\s*define\s+(\S+)\s*{(.*)$', line)
      if parse:
        object = {'type': parse.group(1)}
        line = parse.group(2)
      parse = re.match(r'^\s*(\w+)\s*([^;}]+)(.*)$', line)
      if parse:
        object[parse.group(1)] = parse.group(2).strip()
        line = parse.group(3)
      parse = re.match(r'^\s*}', line)
      if parse:
        result.append(object)
    return result

  def run(self, params, args):
    """
    List objects defined in a Nagios file--mostly for debugging.
    """
    if not 'file' in params:
      self.abort('"file" parameter required')
    objects = self.parse_nagios_file(params['file'])
    result = []
    for object in objects:
      if 'type' in params and params['type'] != object['type']:
        continue
      text = ''
      for attribute in object:
        text += ' %s="%s"' % (attribute, object[attribute])
      result.append(text)
    self.addText("\n".join(result))
