#
# Copyright (C) 2015-2016 OpenWrt.org
#
# This is free software, licensed under the GNU General Public License v2.
# See /LICENSE for more information.
#

include $(TOPDIR)/rules.mk

PKG_NAME:=ruamel.yaml
PKG_VERSION:=0.13.7
PKG_RELEASE:=1

PKG_SOURCE:=$(PKG_NAME)-$(PKG_VERSION).tar.gz
PKG_SOURCE_URL:=https://pypi.python.org/packages/e0/f0/4eeb3183f50df3dfa9b1d931c09c98cd0ad48684407a7ee7bdc5b54360f2
PKG_MD5SUM:=763769a2952ba52983a65e726089334b

PKG_BUILD_DEPENDS:=python3/host

PKG_LICENSE:=MIT License
PKG_LICENSE_FILES:=LICENSE.MIT
PKG_MAINTAINER:=Maximilian Hils <lede@maximilianhils.com>

include $(INCLUDE_DIR)/package.mk
$(call include_mk, python3-package.mk)

define Package/python3-ruamel.yaml
	SECTION:=lang
	CATEGORY:=Languages
	SUBMENU:=Python
	TITLE:=python3-ruamel.yaml
	URL:=https://bitbucket.org/ruamel/yaml
	DEPENDS:=+python3-light
endef

define Package/python3-ruamel.yaml/description
ruamel.yaml is a YAML 1.2 loader/dumper package for Python.
endef

define Build/Compile
	$(call Build/Compile/Py3Mod,,install --prefix="/usr" --root="$(PKG_INSTALL_DIR)")
endef

$(eval $(call Py3Package,python3-ruamel.yaml))
$(eval $(call BuildPackage,python3-ruamel.yaml))
