Summary:	A GNOME firewall tool
Summary(pl):	Narz�dzie do konfiguracji firewalla dzia�aj�ce w �rodowisku GNOME
Name:		firestarter
Version:	0.9.3
Release:	1	
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://dl.sourceforge.net/firestarter/%{name}-%{version}.tar.gz
# Source0-md5:	68b7b18663581fd20bb434cee4bbcc1a
Patch0:		%{name}-acfix.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-locale_names.patch
Patch3:		%{name}-kdesu.patch
URL:		http://firestarter.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel >= 2.0.0
BuildRequires:	libgnome-devel >= 2.0.0
BuildRequires:	libgnomeui-devel >= 2.0.0
BuildRequires:	libtool
BuildRequires:	sed >= 4.0
Requires:	iptables
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FireStarter is an easy-to-use, yet powerful, Linux firewall tool for
GNOME. Use it to quickly set up a secure environment using the
firewall creation wizard, or use it's monitoring and administrating
features with your old firewall scripts.

%description -l pl
FireStarter jest �atwym w u�yciu, lecz pot�nym narz�dziem do
konfiguracji firewalla dzia�aj�cym w �rodowisku GNOME. Mo�esz go u�y�,
by szybko stworzy� bezpieczne �rodowisko korzystaj�c z kreatora
tworzenia firewalla, lub skorzysta� z jego mo�liwo�ci monitorowania i
administrowania wraz z istniej�cymi regu�ami firewalla.

%prep
%setup -q
%patch0 -p0
%patch1 -p1
%patch2 -p1
%patch3 -p0

mv -f po/{no,nb}.po

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__sed} -i 's/xml::\/etc\//xml::\$PREFIX\/etc\//' Makefile
#sed -e s/xml::/xml::\$PREFIX/ Makefile > Makefile.new ; mv Makefile.new Makefile
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	Applicationsdir=%{_desktopdir}

%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README ChangeLog AUTHORS TODO CREDITS
%attr(755,root,root) %{_bindir}/firestarter
%{_desktopdir}/firestarter.desktop
%{_pixmapsdir}/*
%config(noreplace) %{_sysconfdir}/firestarter/*
%{_sysconfdir}/gconf/schemas/*
