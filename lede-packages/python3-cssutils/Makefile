#
# Copyright (C) 2015-2016 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=cssutils
PKG_VERSION:=1.0.1
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=https://pypi.python.org/packages/22/de/6b03e0088baf0299ab7d2e95a9e26c2092e9cb3855876b958b6a62175ca2
PKG_MD5SUM:=7fcdf2c3e9f053136af1990146eb361d

PKG_BUILD_DEPENDS:=python3/host

PKG_LICENSE:=LGPL
PKG_LICENSE_FILES:=LICENSE.LGPL
PKG_MAINTAINER:=Maximilian Hils <lede@maximilianhils.com>

include $(INCLUDE_DIR)/package.mk
$(call include_mk, python3-package.mk)

define Package/python3-cssutils
	SECTION:=lang
	CATEGORY:=Languages
	SUBMENU:=Python
	TITLE:=python3-cssutils
	URL:=http://cthedot.de/cssutils/
	DEPENDS:=+python3-light
endef

define Package/python3-cssutils/description
A Python package to parse and build CSS Cascading Style Sheets. Currently a DOM only, no rendering options.
endef

define Build/Compile
	$(call Build/Compile/Py3Mod,,install --prefix="/usr" --root="$(PKG_INSTALL_DIR)")
endef

$(eval $(call Py3Package,python3-cssutils))
$(eval $(call BuildPackage,python3-cssutils))
