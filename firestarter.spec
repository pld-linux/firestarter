%define name	firestarter
%define version 0.2.2
%define release 1
%define prefix  /usr

Summary: A firewall tool GNOME
Name: %{name}
Version: %{version}
Release: %{release}
Copyright: GPL
Group: Applications/Internet
URL: http://firestarter.sourceforge.net

Source: http://download.sourceforge.com/firestarter/firestarter-%{version}.tar.gz
BuildRoot: /var/tmp/%{name}-%{version}-%{release}-root

Docdir: %{prefix}/doc

Requires: gtk+ >= 1.2.5
Requires: gnome-libs >= 1.0.55
Requires: ipchains >= 1.3.9

%description
FireStarter is an easy-to-use, yet powerful, Linux firewall tool for GNOME.
Use it to quickly set up a secure environment using the firewall creation
wizard, or use it's monitoring and administrating features with your old
firewall scripts.

%prep

%setup

%build
CFLAGS="-O2" 
%ifarch i586
CFLAGS="-O2 -mpentium -march=pentium" 
%endif
%ifarch i686
CFLAGS="-O2 -mpentiumpro -march=pentiumpro" 
%endif
./configure --prefix=%{prefix}
make

%install
rm -rf $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT%{prefix} install

%files
%defattr(-,root,root)
%doc README ChangeLog AUTHORS TODO COPYING CREDITS
%attr(755,root,root) %{prefix}/bin/firestarter
%{prefix}/share/gnome/apps/Internet/firestarter.desktop
%{prefix}/share/pixmaps/*

%clean
rm -r $RPM_BUILD_ROOT

%changelog
* Mon May 29 2000 Tomas Junnonen
- First spec file
