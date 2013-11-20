# $Id$
#
# @Copyright@
# 
#         Rocks(tm)
#              www.rocksclusters.org
#             version 4.3 (Mars Hill)
# 
# Copyright (c) 2000 - 2011 The Regents of the University of California.
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

import os
import re
import rocks.commands

# Mappings from Nagios attribute names to "rocks add nagios" param names for
# each recognized type of object
attributeMaps = {
  'contact': {
    'email':'email', 'contactgroups':'groups'
  },
  'host': {
    'contact_groups':'contacts', 'hostgroups':'groups', 'address':'ip',
    'host_name':'name'
  },
  'service': {
    'check_command':'command', 'contact_groups':'contacts',
    'check_interval':'frequency', 'hostgroup_name':'hosts',
    'service_description':'name', 'retry_interval':'retry',
    'check_period':'timeperiod'
  },
  'timeperiod': {
    'timeperiod_name':'name', 'sunday':'sunday', 'monday':'monday',
    'tuesday':'tuesday', 'wednesday':'wednesday', 'thursday':'thursday',
    'friday':'friday', 'saturday':'saturday'
  }
}

class Command(rocks.commands.Command):
  """
  Print rocks commands to add objects defined in a Nagios file or directory.

  <arg type='string' name='path'>
  Path to Nagios config file or directory containing Nagios config files.
  Defaults to /opt/nagios/etc/rocks.
  </arg>
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

    if len(args) == 0:
      args.append('/opt/nagios/etc/rocks')

    if os.path.isdir(args[0]):
      objects = []
      for file in os.listdir(args[0]):
        objects.extend(self.parse_nagios_file(args[0] + '/' + file))
    else:
      objects = self.parse_nagios_file(args[0])

    commands = {}
    result = []
    for object in objects:
      type = object['type']
      if object.has_key('register'):
        continue
      elif type == 'command':
        if object.has_key('command_name') and object.has_key('command_line'):
          commands[object['command_name']] = object['command_line']
      elif attributeMaps.has_key(type):
        map = attributeMaps[type]
        text = '/opt/rocks/bin/rocks add nagios ' + type
        for attribute in map:
          if not object.has_key(attribute):
            continue
          if map[attribute] == 'command' and \
             commands.has_key(object[attribute]):
            object[attribute] = commands[object[attribute]]
          text += " %s='%s'" % (map[attribute], object[attribute])
        result.append(text)
    self.addText("\n".join(sorted(result)))
