ROLL			= nagios
NAME    		= roll-$(ROLL)-usersguide
RELEASE 		= 0

PKGROOT			= /var/www/html/roll-documentation/$(ROLL)/$(VERSION)

SUMMARY_COMPATIBLE      = $(VERSION)
SUMMARY_MAINTAINER      = Rocks Group
SUMMARY_ARCHITECTURE    = i386, x86_64

ROLL_REQUIRES           = base kernel os1 os2 web-server
ROLL_CONFLICTS          = 

