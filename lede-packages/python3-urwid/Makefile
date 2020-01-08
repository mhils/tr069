#
# Copyright (C) 2015-2016 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=urwid
PKG_VERSION:=1.3.1
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=https://pypi.python.org/packages/85/5d/9317d75b7488c335b86bd9559ca03a2a023ed3413d0e8bfe18bea76f24be
PKG_MD5SUM:=2e1a005cb31368fe21bfeba2d6ad5a5c

PKG_BUILD_DEPENDS:=python3/host

PKG_LICENSE:=LGPL
PKG_LICENSE_FILES:=LICENSE.LGPL
PKG_MAINTAINER:=Maximilian Hils <lede@maximilianhils.com>

include $(INCLUDE_DIR)/package.mk
$(call include_mk, python3-package.mk)

define Package/python3-urwid
	SECTION:=lang
	CATEGORY:=Languages
	SUBMENU:=Python
	TITLE:=python3-urwid
	URL:=http://urwid.org/
	DEPENDS:=+python3-light
endef

define Package/python3-urwid/description
Python bindings to the Brotli compression library
endef

define Build/Compile
	$(call Build/Compile/Py3Mod,,install --prefix="/usr" --root="$(PKG_INSTALL_DIR)")
endef

$(eval $(call Py3Package,python3-urwid))
$(eval $(call BuildPackage,python3-urwid))
