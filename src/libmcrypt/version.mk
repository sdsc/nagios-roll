NAME           = sdsc-libmcrypt
VERSION        = 2.5.8
RELEASE        = 2
PKGROOT        = /opt/rocks

SRC_SUBDIR     = libmcrypt

SOURCE_NAME    = libmcrypt
SOURCE_SUFFIX  = tar.gz
SOURCE_VERSION = $(VERSION)
SOURCE_PKG     = $(SOURCE_NAME)-$(SOURCE_VERSION).$(SOURCE_SUFFIX)
SOURCE_DIR     = $(SOURCE_PKG:%.$(SOURCE_SUFFIX)=%)

TAR_GZ_PKGS    = $(SOURCE_PKG)

RPM.EXTRAS     = AutoReq:No
