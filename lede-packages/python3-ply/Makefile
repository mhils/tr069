#
# Copyright (C) 2015-2016 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=ply
PKG_VERSION:=3.9
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=http://www.dabeaz.com/ply
PKG_MD5SUM:=c5c5767376eff902617fd9874f0c76b7

PKG_BUILD_DEPENDS:=python3 python3-setuptools
HOST_BUILD_DEPENDS:=python3/host python3-setuptools/host

PKG_LICENSE:=BSD-3-Clause
PKG_LICENSE_FILES:=README.md
PKG_MAINTAINER:=Maximilian Hils <lede@maximilianhils.com>

include $(INCLUDE_DIR)/host-build.mk
include $(INCLUDE_DIR)/package.mk
$(call include_mk, python3-package.mk)
$(call include_mk, python3-host.mk)

define Package/python3-ply
	SECTION:=lang
	CATEGORY:=Languages
	SUBMENU:=Python
	TITLE:=python3-ply
	URL:=http://www.dabeaz.com/ply/
	DEPENDS:=+python3-light
endef

define Package/python3-ply/description
PLY is a 100% Python implementation of the common parsing tools lex
and yacc.
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

$(eval $(call Py3Package,python3-ply))
$(eval $(call BuildPackage,python3-ply))
