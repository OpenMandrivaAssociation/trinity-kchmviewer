#
# Please submit bugfixes or comments via http://www.trinitydesktop.org/
#

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define tde_pkg kchmviewer
%define tde_prefix /opt/trinity
%define tde_appdir %{tde_datadir}/applications
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%if 0%{?mdkversion}
%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1
%endif

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity
%global toolchain %(readlink /usr/bin/cc)


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		3.1.2
Release:		%{?tde_version}_%{?!preversion:1}%{?preversion:0_%{preversion}}%{?dist}
Summary:		CHM viewer for Trinity
Group:			Applications/Utilities
URL:			http://www.trinitydesktop.org/

%if 0%{?suse_version}
License:	GPL-2.0+
%else
License:	GPLv2+
%endif

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/utilities/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildRequires:  cmake make
BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	trinity-tde-cmake >= %{tde_version}
%if "%{?toolchain}" != "clang"
BuildRequires:	gcc-c++
%endif
BuildRequires:	pkgconfig

# SUSE desktop files utility
%if 0%{?suse_version}
BuildRequires:	update-desktop-files
%endif

%if 0%{?opensuse_bs} && 0%{?suse_version}
# for xdg-menu script
BuildRequires:	brp-check-trinity
%endif

# CHMLIB support
%if 0%{?rhel} == 8
%define with_chmlib 0
%else
%define with_chmlib 1
BuildRequires:	chmlib-devel
%endif

# ACL support
BuildRequires:  pkgconfig(libacl)

# IDN support
BuildRequires:	pkgconfig(libidn)

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)

%description
KchmViewer is a chm (MS HTML help file format) viewer, written in C++.
Unlike most existing CHM viewers for Unix, it uses Trolltech Qt widget
library, and does not depend on TDE or GNOME. However, it may be compiled
with full Trinity support, including Trinity widgets and KIO/KHTML. 

The main advantage of KchmViewer is non-English language support. Unlike
others, KchmViewer in most cases correctly detects help file encoding,
correctly shows tables of context of Russian, Korean, Chinese and Japanese
help files, and correctly searches in non-English help files (search for
MBCS languages - ja/ko/ch is still in progress).

Completely safe and harmless. Does not support JavaScript in any way,
optionally warns you before opening an external web page, or switching to
another help file. Shows an appropriate image for every TOC entry. 

KchmViewer Has complete chm index support, including multiple index entries,
cross-links and parent/child entries in index as well as Persistent bookmarks
support. Correctly detects and shows encoding of any valid chm file.


##########

%if 0%{?suse_version} && 0%{?opensuse_bs} == 0
%debug_package
%endif

##########


%prep
%autosetup -n %{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}


%build
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"
export PKG_CONFIG_PATH="%{tde_libdir}/pkgconfig"

if ! rpm -E %%cmake|grep -e 'cd build\|cd ${CMAKE_BUILD_DIR:-build}'; then
  %__mkdir_p build
  cd build
fi

%cmake \
  -DCMAKE_BUILD_TYPE="RelWithDebInfo" \
  -DCMAKE_C_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_CXX_FLAGS="${RPM_OPT_FLAGS}" \
  -DCMAKE_SKIP_RPATH=OFF \
  -DCMAKE_SKIP_INSTALL_RPATH=OFF \
  -DCMAKE_INSTALL_RPATH="%{tde_libdir}" \
  -DCMAKE_VERBOSE_MAKEFILE=ON \
  -DWITH_GCC_VISIBILITY=OFF \
  \
  -DCMAKE_INSTALL_PREFIX="%{tde_prefix}" \
  -DSHARE_INSTALL_PREFIX="%{tde_datadir}" \
  -DLIB_INSTALL_DIR="%{tde_libdir}" \
  -DPLUGIN_INSTALL_DIR="%{tde_tdelibdir}" \
  \
  -DWITH_ALL_OPTIONS=ON \
  -DWITH_GCC_VISIBILITY=ON \
  -DWITH_CHMLIB=%{?with_chmlib} \
  \
  -DBUILD_ALL=ON \
  -DBUILD_DOC=ON \
  -DBUILD_TRANSLATIONS=ON \
  ..

%__make %{?_smp_mflags} || %__make


%install
export PATH="%{tde_bindir}:${PATH}"
%__make install DESTDIR=%{buildroot} -C build

%find_lang %{tde_pkg}

# Removes useless files
%__rm -f %{?buildroot}%{tde_libdir}/*.a

# Fix desktop icon location
if [ -d "%{?buildroot}%{tde_datadir}/applnk" ]; then
  %__mkdir_p "%{?buildroot}%{tde_tdeappdir}"
  %__mv -f "%{?buildroot}%{tde_datadir}/applnk/kchmviewer.desktop" "%{?buildroot}%{tde_tdeappdir}/kchmviewer.desktop"
  %__rm -r "%{buildroot}%{tde_datadir}/applnk"
fi

# Updates applications categories for openSUSE
echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_tdeappdir}/kchmviewer.desktop"
%if 0%{?suse_version}
%suse_update_desktop_file -G "Compressed HTML Viewer" kchmviewer  Office Viewer
%endif


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc ChangeLog COPYING FAQ README.md
%{tde_bindir}/kchmviewer
%{tde_tdelibdir}/tdeio_msits.la
%{tde_tdelibdir}/tdeio_msits.so
%{tde_tdeappdir}/kchmviewer.desktop
%{tde_datadir}/icons/crystalsvg/*/apps/kchmviewer.png
%{tde_datadir}/services/msits.protocol
%{tde_tdedocdir}/HTML/en/kchmviewer/
%{tde_tdedocdir}/HTML/en/tdeioslave/msits/
%{tde_mandir}/man1/kchmviewer.*

