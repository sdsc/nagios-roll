NAME           = nagios-plugins
VERSION        = 2.0.3
RELEASE        = 0
PKGROOT        = /opt/nagios

SRC_SUBDIR     = nagios-plugins

SOURCE_NAME    = $(NAME)
SOURCE_SUFFIX  = tar.gz
SOURCE_VERSION = $(VERSION)
SOURCE_PKG     = $(SOURCE_NAME)-$(SOURCE_VERSION).$(SOURCE_SUFFIX)
SOURCE_DIR     = $(SOURCE_PKG:%.$(SOURCE_SUFFIX)=%)

TAR_GZ_PKGS    = $(SOURCE_PKG)

RPM.EXTRAS     = AutoReq:No
