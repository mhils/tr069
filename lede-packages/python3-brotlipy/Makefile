#
# Copyright (C) 2015-2016 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=brotlipy
PKG_VERSION:=0.6.0
PKG_RELEASE:=1

PKG_LICENSE:=MIT
PKG_MAINTAINER:=Maximilian Hils <lede@maximilianhils.com>

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=https://pypi.python.org/packages/b0/f9/d629de68c3a9f5ce3e1ff2fe70f1cf0396765582bc3194179a2742c47731
PKG_MD5SUM:=477e8c1dd78e00d9b7825f802afb1245

PKG_BUILD_DEPENDS:=python3-cffi/host

include $(INCLUDE_DIR)/package.mk
$(call include_mk, python3-package.mk)

define Package/python3-brotlipy
	SECTION:=lang
	CATEGORY:=Languages
	SUBMENU:=Python
	TITLE:=python3-brotlipy
	URL:=https://github.com/python-hyper/brotlipy
	DEPENDS:=+python3-light +python3-cffi +libstdcpp 
endef

define Package/python3-brotlipy/description
Python bindings to the Brotli compression library
endef

define Build/Compile
	$(call Build/Compile/Py3Mod,,install --prefix="/usr" --root="$(PKG_INSTALL_DIR)")
endef

$(eval $(call Py3Package,python3-brotlipy))
$(eval $(call BuildPackage,python3-brotlipy))
