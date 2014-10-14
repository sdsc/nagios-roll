NAME    = nagios
VERSION = 4.0.8
RELEASE = 0
PKGROOT = /opt/nagios
RPM.EXTRAS         = AutoReq:No

SRC_SUBDIR         = nagios

SOURCE_NAME        = $(NAME)
SOURCE_VERSION     = $(VERSION)
SOURCE_SUFFIX      = tar.gz
SOURCE_PKG         = $(SOURCE_NAME)-$(SOURCE_VERSION).$(SOURCE_SUFFIX)
SOURCE_DIR         = $(SOURCE_PKG:%.$(SOURCE_SUFFIX)=%)

TAR_GZ_PKGS           = $(SOURCE_PKG)

