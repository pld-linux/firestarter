
# todo:
# - init.d file
# - pam file

Summary:	A GNOME firewall tool
Summary(pl):	Narzêdzie do konfiguracji firewalla dzia³aj±ce w ¶rodowisku GNOME
Name:		firestarter
Version:	1.0.3
Release:	0.1	
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://dl.sourceforge.net/firestarter/%{name}-%{version}.tar.gz
# Source0-md5:	f46860a9e16dac4b693bd05f16370b03
Patch0:		%{name}-acfix.patch
Patch1:		%{name}-desktop.patch
Patch2:		%{name}-locale_names.patch
URL:		http://firestarter.sourceforge.net/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gtk+2-devel >= 1:2.0.0
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
FireStarter jest ³atwym w u¿yciu, lecz potê¿nym narzêdziem do
konfiguracji firewalla dzia³aj±cym w ¶rodowisku GNOME. Mo¿esz go u¿yæ,
by szybko stworzyæ bezpieczne ¶rodowisko korzystaj±c z kreatora
tworzenia firewalla, lub skorzystaæ z jego mo¿liwo¶ci monitorowania i
administrowania wraz z istniej±cymi regu³ami firewalla.

%prep
%setup -q
#%patch0 -p0 # really required?
%patch1 -p1
%patch2 -p1

mv -f po/{no,nb}.po

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__sed} -i 's/xml::\/etc\//xml::\$PREFIX\/etc\//' Makefile
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	Applicationsdir=%{_desktopdir}

install -d ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/inbound/
install -d ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/outbound/
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/configuration
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/events-filter-hosts
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/events-filter-ports
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/firestarter.sh
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/firewall
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/sysctl-tuning
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/user-pre
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/user-post
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/inbound/allow-from
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/inbound/allow-service
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/inbound/forward
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/inbound/setup
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/outbound/allow-from
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/outbound/allow-service
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/outbound/allow-to
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/outbound/deny-from
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/outbound/deny-service
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/outbound/deny-to
touch ${RPM_BUILD_ROOT}/%{_sysconfdir}/firestarter/outbound/setup

%find_lang %{name} --with-gnome

%post
%gconf_schema_install firestarter.schemas
%update_desktop_database_post

%preun
if [ $1 = 0 ]; then
    %gconf_schema_uninstall firestarter.schemas
fi

%postun 
%update_desktop_database_postun

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README ChangeLog AUTHORS TODO CREDITS
%attr(755,root,root) %{_bindir}/firestarter
%{_desktopdir}/firestarter.desktop
%{_datadir}/%{name}
%{_pixmapsdir}/*
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_sysconfdir}/gconf/schemas/*
