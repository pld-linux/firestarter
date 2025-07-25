Summary:	A GNOME firewall tool
Summary(pl.UTF-8):	Narzędzie do konfiguracji firewalla działające w środowisku GNOME
Name:		firestarter
Version:	1.0.3
Release:	7
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://downloads.sourceforge.net/firestarter/%{name}-%{version}.tar.gz
# Source0-md5:	f46860a9e16dac4b693bd05f16370b03
Source1:	%{name}.init
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-locale_names.patch
Patch2:		%{name}-script.patch
URL:		http://www.fs-security.com/
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	gnome-common
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	intltool
BuildRequires:	libgnome-devel >= 2.0.0
BuildRequires:	libgnomeui-devel >= 2.0.0
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	iptables
Requires:	rc-scripts
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
FireStarter is an easy-to-use, yet powerful, Linux firewall tool for
GNOME. Use it to quickly set up a secure environment using the
firewall creation wizard, or use it's monitoring and administrating
features with your old firewall scripts.

%description -l pl.UTF-8
FireStarter jest łatwym w użyciu, lecz potężnym narzędziem do
konfiguracji firewalla działającym w środowisku GNOME. Możesz go użyć,
by szybko stworzyć bezpieczne środowisko korzystając z kreatora
tworzenia firewalla, lub skorzystać z jego możliwości monitorowania i
administrowania wraz z istniejącymi regułami firewalla.

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
%patch -P2 -p1

mv -f po/{no,nb}.po

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__sed} -i 's/xml::\/etc\//xml::\$PREFIX\/etc\//' Makefile
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,pam.d}
install -d $RPM_BUILD_ROOT%{_sbindir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	Applicationsdir=%{_desktopdir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/firestarter
cp -a firestarter.pam $RPM_BUILD_ROOT/etc/pam.d/firestarter

install -d $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/inbound
install -d $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/outbound
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/configuration
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/events-filter-hosts
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/events-filter-ports
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/firestarter.sh
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/firewall
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/sysctl-tuning
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/user-pre
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/user-post
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/inbound/allow-from
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/inbound/allow-service
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/inbound/forward
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/inbound/setup
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/outbound/allow-from
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/outbound/allow-service
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/outbound/allow-to
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/outbound/deny-from
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/outbound/deny-service
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/outbound/deny-to
touch $RPM_BUILD_ROOT%{_sysconfdir}/firestarter/outbound/setup

mv $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/firestarter

# TODO: use .desktop magic for this
cat <<'EOF' > $RPM_BUILD_ROOT%{_bindir}/firestarter
#!/bin/sh
if [ -x %{_bindir}/gksudo ] ; then
	exec gksudo -g %{_sbindir}/firestarter
elif [ -x %{_bindir}/kdesu ] ; then
	exec kdesu %{_sbindir}/firestarter
else
	exec %{_sbindir}/firestarter
fi
EOF

[ -d $RPM_BUILD_ROOT%{_datadir}/locale/sr@latin ] || \
	mv -f $RPM_BUILD_ROOT%{_datadir}/locale/sr@{Latn,latin}
%find_lang %{name} --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install firestarter.schemas
%update_desktop_database_post
/sbin/chkconfig --add firestarter
%service firestarter restart

%preun
if [ "$1" = 0 ]; then
	%gconf_schema_uninstall firestarter.schemas
	%service firestarter stop
	/sbin/chkconfig --del firestarter
fi

%postun
%update_desktop_database_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README ChangeLog AUTHORS TODO CREDITS
%attr(755,root,root) %{_bindir}/firestarter
%attr(755,root,root) %{_sbindir}/firestarter
%attr(754,root,root) /etc/rc.d/init.d/firestarter
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/firestarter
%{_sysconfdir}/gconf/schemas/firestarter.schemas
%{_desktopdir}/firestarter.desktop
%{_pixmapsdir}/firestarter.png
%{_datadir}/%{name}
%dir %attr(700,root,root) %{_sysconfdir}/%{name}
%dir %attr(700,root,root) %{_sysconfdir}/%{name}/inbound
%dir %attr(700,root,root) %{_sysconfdir}/%{name}/outbound
%config(noreplace) %attr(700,root,root) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/firestarter.sh
%config(noreplace) %attr(440,root,root) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/inbound/*
%config(noreplace) %attr(440,root,root) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/outbound/*
%config(noreplace) %attr(440,root,root) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/configuration
%config(noreplace) %attr(440,root,root) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/events-filter-*
%config(noreplace) %attr(440,root,root) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/firewall
%config(noreplace) %attr(440,root,root) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/non-routables
%config(noreplace) %attr(440,root,root) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/sysctl-tuning
%config(noreplace) %attr(440,root,root) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/user-*
