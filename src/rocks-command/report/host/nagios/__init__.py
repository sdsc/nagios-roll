# $Id$
#
# @Copyright@
# 
# 				Rocks(tm)
# 		         www.rocksclusters.org
# 		        version 4.3 (Mars Hill)
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

import re
import rocks.commands
import socket

hostsPath = '/opt/nagios/etc/rocks/hosts.cfg'
servicesPath = '/opt/nagios/etc/rocks/services.cfg'

class Command(rocks.commands.Command):
  """
  Output XML for configuring NSCA for a host.

  <arg type='string' name='host'>
  Name/ip of the host for which configuration is desired.
  </arg>
  """

  def run(self, params, args):

    if len(args) != 1:
      self.abort('host required')
    ip = socket.gethostbyname(args[0])

    # Get list of existing services
    objects = self.parse_dump_nagios_output([servicesPath])

    checkCommandsByName = {}
    checkIntervalsByName = {}
    passiveServicesByHostGroup = {}
    hostGroupsByName = {}

    for object in objects:
      if not ('name' in object and 'hosts' in object and
              'command' in object and 'frequency' in object and
              'timeperiod' in object):
        continue
      elif object['timeperiod'] != 'passive':
        continue
      name = object['name']
      if not object['command'].startswith('/'):
        object['command'] = '/opt/nagios/libexec/' + object['command']
      checkCommandsByName[name] = object['command']
      checkIntervalsByName[name] = object['frequency']
      hostGroupsByName[name] = object['hosts']
      if not hostGroupsByName[name] in passiveServicesByHostGroup:
        passiveServicesByHostGroup[hostGroupsByName[name]] = []
      passiveServicesByHostGroup[hostGroupsByName[name]].append(name)

    result = []

    # Get the list of IPs in each host group
    objects = self.parse_dump_nagios_output([hostsPath])
    ipsByHostGroup = {}
    for object in objects:
      if not ('groups' in object and 'ip' in object):
        continue
      for group in object['groups'].split(','):
        if not group in ipsByHostGroup:
          ipsByHostGroup[group] = []
        ipsByHostGroup[group].append(object['ip'])

    result = "<![CDATA[\n"
    for group in passiveServicesByHostGroup:
      for name in passiveServicesByHostGroup[group]:
        if ip in ipsByHostGroup[group]:
          result += "/opt/nagios/bin/nsca_schedule %s %s %s\n" % \
            (name, checkIntervalsByName[name], checkCommandsByName[name])
    result += ']]>'

    self.addText(result)

  def parse_attributes(self, lines):
    """
    Converts a list of lines with the format attr=value [attr=value ...] to a
    list of dictionaries.
    """
    result = []
    for line in lines:
      object = {}
      s = line
      parse = re.search(r'\s*add\s*nagios\s*\w+(.*)', s)
      if parse:
        s = parse.group(1)
      parse = re.match(r'\s*(\w+)=(\'[^\']*\'|"[^"]*"|[^\'"\s]+)', s)
      while parse:
        object[parse.group(1)] = parse.group(2).strip('\'"')
        s = s[len(parse.group(0)):]
        parse = re.match(r'\s*(\w+)=(\'[^\']*\'|"[^"]*"|[^\'\s"]+)', s)
      result.append(object)
    return result

  def parse_dump_nagios_output(self, args):
    """
    Converts the output of the "rocks dump nagios" command to a list of
    dictionaries.
    """
    lines = self.command('dump.nagios', args).split("\n")
    if len(lines) == 1 and lines[0] == '':
      return []
    return self.parse_attributes(lines)
