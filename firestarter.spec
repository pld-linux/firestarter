Summary:	A GNOME firewall tool
Summary(pl):	Narzêdzie do konfiguracji firewalla dzia³aj±ce w ¶rodowisku GNOME
Name:		firestarter
Version:	0.8.2
Release:	1
License:	GPL
Group:		X11/Applications/Networking
Source0:	ftp://download.sourceforge.net/pub/sourceforge/firestarter/%{name}-%{version}.tar.gz
URL:		http://firestarter.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+-devel >= 1.2.5
BuildRequires:	gnome-core-devel
BuildRequires:	gnome-libs-devel >= 1.0.55
BuildRequires:	libtool
Requires:	ipchains >= 1.3.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6

%description
FireStarter is an easy-to-use, yet powerful, Linux firewall tool for
GNOME. Use it to quickly set up a secure environment using the
firewall creation wizard, or use it's monitoring and administrating
features with your old firewall scripts.

%description -l pl
FireStarter jest ³atwym w u¿yciu, lecz potê¿nym narzêdziem do
konfiguracji firewalla dzia³aj±cym w ¶rodowisku GNOME. Mo¿esz go u¿yæ,
by szybko stworzyæ bezpieczne ¶rodowisko korzystaj±c z kreatora
tworzenia firewalla, lub skorzystaæ z jego mo¿liwo¶ci monitorowania i
administrowania wraz z istniej±cymi regu³ami firewalla.

%prep
%setup -q

%build
rm -f missing
%{__libtoolize}
%{__aclocal} -I macros
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	Applicationsdir=%{_applnkdir}/System/Administration


%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README ChangeLog AUTHORS TODO CREDITS
%attr(755,root,root) %{_bindir}/firestarter
%{_applnkdir}/System/Administration/firestarter.desktop
%{_pixmapsdir}/*
