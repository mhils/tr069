#
# Copyright (C) 2015-2016 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=cffi
PKG_VERSION:=1.9.1
PKG_RELEASE:=1

PKG_LICENSE:=MIT
PKG_MAINTAINER:=Maximilian Hils <lede@maximilianhils.com>

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=https://pypi.python.org/packages/a1/32/e3d6c3a8b5461b903651dd6ce958ed03c093d2e00128e3f33ea69f1d7965
PKG_MD5SUM:=b8fa7ccb87790531db3316ab17aa8244

PKG_BUILD_DEPENDS:=python3 python3-setuptools
HOST_BUILD_DEPENDS:=libffi/host python3/host python3-setuptools/host python3-pycparser/host

include $(INCLUDE_DIR)/host-build.mk
include $(INCLUDE_DIR)/package.mk
$(call include_mk, python3-package.mk)
$(call include_mk, python3-host.mk)

define Package/python3-cffi
	SECTION:=lang
	CATEGORY:=Languages
	SUBMENU:=Python
	TITLE:=python3-cffi
	URL:=http://cffi.readthedocs.org/
	DEPENDS:=+libffi +python3-light +python3-pycparser
endef

define Package/python3-cffi/description
Foreign Function Interface for Python calling C code.
endef

define Build/Compile
	$(call Build/Compile/Py3Mod,,install --prefix="/usr" --root="$(PKG_INSTALL_DIR)")
endef

define Host/Compile
	$(call Build/Compile/HostPy3Mod,,install --prefix="" --root="$(STAGING_DIR_HOSTPKG)")
endef

define Host/Install
endef

$(eval $(call HostBuild))

$(eval $(call Py3Package,python3-cffi))
$(eval $(call BuildPackage,python3-cffi))
