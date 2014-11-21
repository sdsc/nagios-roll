NAME           = sdsc-nsca
VERSION        = 2.9.1
RELEASE        = 1
PKGROOT        = /opt/nagios

SRC_SUBDIR     = nsca

SOURCE_NAME    = nsca
SOURCE_SUFFIX  = tar.gz
SOURCE_VERSION = $(VERSION)
SOURCE_PKG     = $(SOURCE_NAME)-$(SOURCE_VERSION).$(SOURCE_SUFFIX)
SOURCE_DIR     = $(SOURCE_PKG:%.$(SOURCE_SUFFIX)=%)

TAR_GZ_PKGS    = $(SOURCE_PKG)

RPM.EXTRAS     = AutoReq:No
