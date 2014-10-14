NAME               = nagios-plugins
VERSION            = 2.0.3
RELEASE            = 0
PKGROOT            = /opt/nagios
RPM.EXTRAS         = AutoReq:No

SRC_SUBDIR         = nagios-plugins

SOURCE_NAME        = $(NAME)
SOURCE_VERSION     = $(VERSION)
SOURCE_SUFFIX      = tar.gz
SOURCE_PKG         = $(SOURCE_NAME)-$(SOURCE_VERSION).$(SOURCE_SUFFIX)
SOURCE_DIR         = $(SOURCE_PKG:%.$(SOURCE_SUFFIX)=%)

TAR_GZ_PKGS        = $(SOURCE_PKG)

