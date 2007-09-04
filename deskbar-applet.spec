%define name deskbar-applet
%define version 2.19.92
%define release %mkrel 3

%define _requires_exceptions pkgconfig\(.*\)

Summary: All-in-one search bar for the GNOME panel
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://ftp.gnome.org/pub/GNOME/sources/deskbar-applet/%{name}-%{version}.tar.bz2
Patch1: deskbar-applet-2.19.90.1-seamonkey.patch
#gw svn patches
Patch2: deskbar-applet-1634-fix-evolution-addressbook-search.patch
Patch3: deskbar-applet-1635-fix-gdm-logout-action.patch
License: GPL
Group: Graphical desktop/GNOME
Url: http://live.gnome.org/DeskbarApplet
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: gtk+2-devel
BuildRequires: pygtk2.0-devel
BuildRequires: gnome-python-extras
BuildRequires: gnome-python-applet
BuildRequires: evolution-data-server-devel
BuildRequires: gnome-desktop-devel
BuildRequires: automake1.9
BuildRequires: gnome-common
BuildRequires: intltool
BuildRequires: gnome-doc-utils
BuildRequires: mozilla-firefox
BuildRequires: python-beagle
BuildRequires: scrollkeeper
Requires: gnome-python-extras
Requires: gnome-python-gnomevfs
Requires: gnome-python-gconf
Requires: gnome-python-applet
Requires: python-elementtree
Requires: dbus-python
Requires(post): scrollkeeper
Requires(postun): scrollkeeper
Suggests: python-beagle beagle-gui
Suggests: libmozilla-firefox

%description
The Deskbar is an all-in-one search bar. It is a Linux/Gnome panel
applet that is similar to Google's (Windows only) Deskbar
It supports the search in Beagle, Mozilla Firefox and Epiphany.

%prep
%setup -q
%patch1 -p1 -b .seamonkey
%patch2 -p1
%patch3 -p1

%build
%configure2_5x --disable-scrollkeeper
%make

%install
rm -rf $RPM_BUILD_ROOT %name.lang
%makeinstall_std
%find_lang %name
%find_lang deskbar --with-gnome
for omf in %buildroot%_datadir/omf/*/*-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/.*-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %name.lang
done
cat deskbar.lang >> %name.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
%post_install_gconf_schemas %name
%update_icon_cache hicolor
%update_scrollkeeper

%preun
%preun_uninstall_gconf_schemas %name

%postun
%clean_icon_cache hicolor
%clean_scrollkeeper

%files -f %name.lang
%defattr(-,root,root)
%doc README NEWS TODO ChangeLog AUTHORS
%_sysconfdir/gconf/schemas/deskbar-applet.schemas
%_libdir/bonobo/servers/*
%_libdir/%name/
%py_puresitedir/*deskbar*
%_libdir/pkgconfig/%name.pc
%_datadir/%name
%_datadir/icons/hicolor/*/apps/*
%dir %_datadir/omf/*/
%_datadir/omf/*/*-C.omf
