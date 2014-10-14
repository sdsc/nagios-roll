NAME           = libmcrypt
VERSION        = 2.5.8
RELEASE        = 1
PKGROOT        = /opt/rocks

SRC_SUBDIR     = libmcrypt

SOURCE_NAME    = $(NAME)
SOURCE_SUFFIX  = tar.gz
SOURCE_VERSION = $(VERSION)
SOURCE_PKG     = $(SOURCE_NAME)-$(SOURCE_VERSION).$(SOURCE_SUFFIX)
SOURCE_DIR     = $(SOURCE_PKG:%.$(SOURCE_SUFFIX)=%)

TAR_GZ_PKGS    = $(SOURCE_PKG)

RPM.EXTRAS     = AutoReq:No
