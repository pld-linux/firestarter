Summary:	A GNOME firewall tool
Name:		firestarter
Version:	0.5.0
Release:	1
License:	GPL
Group:		X11/Applications/Networking
Group(de):	X11/Applikationen/Netzwerkwesen
Group(pl):	X11/Aplikacje/Sieciowe
Source0:	ftp://download.sourceforge.net/pub/sourceforge/firestarter/%{name}-%{version}.tar.gz
URL:		http://firestarter.sourceforge.net/
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel >= 1.2.5
BuildRequires:	gnome-core-devel
BuildRequires:	gnome-libs-devel >= 1.0.55
Requires:	ipchains >= 1.3.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6

%description
FireStarter is an easy-to-use, yet powerful, Linux firewall tool for
GNOME. Use it to quickly set up a secure environment using the
firewall creation wizard, or use it's monitoring and administrating
features with your old firewall scripts.

%prep
%setup -q

%build
gettextize --copy --force
%configure

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	Productivitydir=%{_applnkdir}/System

gzip -9nf README ChangeLog AUTHORS TODO CREDITS

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *gz
%attr(755,root,root) %{_bindir}/firestarter
%{_applnkdir}/System/firestarter.desktop
%{_pixmapsdir}/*
