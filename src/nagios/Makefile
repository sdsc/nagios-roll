#
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
# Revision 1.1  2009/02/05 18:36:05  bruno
# added
#
#

PKGROOT		= /opt/nagios
REDHAT.ROOT     = $(PWD)/../../

-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

#CONFIG_FILES	= cgi.cfg commands.cfg localhost.cfg nagios.cfg resource.cfg
CONFIG_FILES	=


build:
	tar zxvf $(NAME)-$(VERSION).tar.gz
	(								\
		cd $(NAME)-$(VERSION);					\
		./configure --prefix=$(PKGROOT) 			\
			--with-nagios-user=nagios 			\
			--with-nagios-group=apache;			\
		make all;						\
	)


install::
	mkdir -p $(ROOT)/$(PKGROOT)
	(								\
		cd $(NAME)-$(VERSION);					\
		make prefix=$(ROOT)/$(PKGROOT) install;			\
		make prefix=$(ROOT)/$(PKGROOT) install-config;		\
		mkdir -p $(ROOT)/etc/rc.d/init.d;			\
		install -m755 daemon-init 				\
			$(ROOT)/etc/rc.d/init.d/nagios;			\
	)

	# grep -v "cfg_file=/opt/nagios/etc/localhost.cfg"		\
		# $(ROOT)/$(PKGROOT)/etc/nagios.cfg-sample 		\
		# > $(ROOT)/$(PKGROOT)/etc/nagios.cfg-sample.rocks
	# mv $(ROOT)/$(PKGROOT)/etc/nagios.cfg-sample.rocks 		\
		# $(ROOT)/$(PKGROOT)/etc/nagios.cfg-sample		

	for i in $(CONFIG_FILES) ; do 					\
		install -m744 $(ROOT)/$(PKGROOT)/etc/$$i-sample		\
			$(ROOT)/$(PKGROOT)/etc/$$i;			\
	done


clean::
	rm -rf $(NAME)-$(VERSION)

