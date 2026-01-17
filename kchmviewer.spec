%bcond clang 1
%bcond chmlib 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg kchmviewer
%define tde_prefix /opt/trinity


%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:			trinity-%{tde_pkg}
Epoch:			%{tde_epoch}
Version:		3.1.2
Release:		%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:		CHM viewer for Trinity
Group:			Applications/Utilities
URL:			http://www.trinitydesktop.org/

License:	GPLv2+


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/utilities/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DPLUGIN_INSTALL_DIR=%{tde_prefix}/%{_lib}/trinity
BuildOption:    -DWITH_CHMLIB=%{!?with_chmlib:OFF}%{?with_chmlib:ON}
BuildOption:    -DBUILD_ALL=ON
BuildOption:    -DBUILD_DOC=ON
BuildOption:    -DBUILD_TRANSLATIONS=ON
BuildOption:    -DWITH_ALL_OPTIONS=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}

BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig


# CHMLIB support
%{?with_chmlib:BuildRequires:	chmlib-devel}

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


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_prefix}/bin:${PATH}"
export PKG_CONFIG_PATH="%{tde_prefix}/%{_lib}/pkgconfig"


%install -a
%find_lang %{tde_pkg}

# Removes useless files
%__rm -f %{?buildroot}%{tde_prefix}/%{_lib}/*.a

# Fix desktop icon location
if [ -d "%{?buildroot}%{tde_prefix}/share/applnk" ]; then
  %__mkdir_p "%{?buildroot}%{tde_prefix}/share/applications/tde"
  %__mv -f "%{?buildroot}%{tde_prefix}/share/applnk/kchmviewer.desktop" "%{?buildroot}%{tde_prefix}/share/applications/tde/kchmviewer.desktop"
  %__rm -r "%{buildroot}%{tde_prefix}/share/applnk"
fi

# Updates applications categories for openSUSE
echo "OnlyShowIn=TDE;" >>"%{?buildroot}%{tde_prefix}/share/applications/tde/kchmviewer.desktop"


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc ChangeLog COPYING FAQ README.md
%{tde_prefix}/bin/kchmviewer
%{tde_prefix}/%{_lib}/trinity/tdeio_msits.la
%{tde_prefix}/%{_lib}/trinity/tdeio_msits.so
%{tde_prefix}/share/applications/tde/kchmviewer.desktop
%{tde_prefix}/share/icons/crystalsvg/*/apps/kchmviewer.png
%{tde_prefix}/share/services/msits.protocol
%{tde_prefix}/share/doc/tde/HTML/en/kchmviewer/
%{tde_prefix}/share/doc/tde/HTML/en/tdeioslave/msits/
%{tde_prefix}/share/man/man1/kchmviewer.*

