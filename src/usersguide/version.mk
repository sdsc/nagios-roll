NAME       = sdsc-roll-$(ROLL)-usersguide
VERSION    = 1
RELEASE    = 1

RPM.EXTRAS = AutoReq:No

SUMMARY_COMPATIBLE   = $(VERSION)
SUMMARY_MAINTAINER   = Rocks Group
SUMMARY_ARCHITECTURE = i386, x86_64

ROLL_REQUIRES  = base kernel os web-server
ROLL_CONFLICTS = 
