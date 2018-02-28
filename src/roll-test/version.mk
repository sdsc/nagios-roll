NAME       = sdsc-nagios-roll-test
VERSION    = 1
RELEASE    = 4
PKGROOT    = /root/rolltests

RPM.EXTRAS = AutoReq:No\nAutoProv:No
RPM.FILES  = $(PKGROOT)/nagios.t
