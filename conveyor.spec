%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global pypi_name conveyor

Name:           conveyor
Epoch:          1
Version:        XXX
Release:        XXX
Summary:        Conveyor

License:        ASL 2.0
URL:            https://github.com/Hybrid-Cloud/conveyor
Source0:        https://github.com/Hybrid-Cloud/%{name}/%{name}-%{upstream_version}.tar.gz

Source1:        conveyor-dist.conf
Source2:        conveyor.logrotate
Source3:        conveyor.sudoers

Source10:       conveyor-api.service
Source11:       conveyor-clone.service
Source12:       conveyor-resource.service
Source13:       conveyor-plan.service

BuildArch:      noarch
BuildRequires:  intltool
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildRequires:  python-d2to1
BuildRequires:  python-crypto
BuildRequires:  python-cryptography
BuildRequires:  python-conveyor-caaclient
BuildRequires:  python-decorator
BuildRequires:  python-cinderclient
BuildRequires:  python-glanceclient
BuildRequires:  python-greenlet
BuildRequires:  python-heatclient
BuildRequires:  python-iso8601
BuildRequires:  python-keystoneclient
BuildRequires:  python-keystonemiddleware
BuildRequires:  python-lxml
BuildRequires:  python-neutronclient
BuildRequires:  python-novaclient
BuildRequires:  python-oslo-cache
BuildRequires:  python-oslo-concurrency
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-context
BuildRequires:  python-oslo-db
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-messaging
BuildRequires:  python-osprofiler
BuildRequires:  python-oslo-middleware
BuildRequires:  python-oslo-policy
BuildRequires:  python-oslo-reports
BuildRequires:  python-oslo-rootwrap
BuildRequires:  python-oslo-serialization
BuildRequires:  python-oslo-service
BuildRequires:  python-oslo-utils
BuildRequires:  python-oslo-versionedobjects
BuildRequires:  PyYAML

Requires:       python-%{pypi_name} = %{epoch}:%{version}-%{release}

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(pre):    shadow-utils

%description
Conveyor

%package -n python-%{pypi_name}
Summary:        Conveyor Code

Requires:       pyparsing >= 2.0.1
Requires:       python-anyjson
Requires:       python-babel
Requires:       python-conveyor-caaclient
Requires:       python-crypto
Requires:       python-cryptography >= 1.0
Requires:       python-decorator
Requires:       python-eventlet >= 0.17.4
Requires:       python-glanceclient >= 1:2.0.0
Requires:       python-greenlet
Requires:       python-heatclient >= 0.6.0
Requires:       python-httplib2 >= 0.7.5
Requires:       python-iso8601 >= 0.1.9
Requires:       python-keystoneclient >= 1:1.6.0
Requires:       python-keystonemiddleware >= 4.0.0
Requires:       python-lxml >= 2.3
Requires:       python-migrate >= 0.9.6
Requires:       python-netaddr
Requires:       python-oauth2client >= 1.5.0
Requires:       python-os-brick >= 1.0.0
Requires:       python-oslo-cache >= 0.8.0
Requires:       python-oslo-concurrency >= 2.30
Requires:       python-oslo-config >= 3.4.0
Requires:       python-oslo-context >= 2.0.0
Requires:       python-oslo-db >= 4.1.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-log >= 1.14.0
Requires:       python-oslo-messaging >= 2.1.0
Requires:       python-oslo-middleware >= 3.0.0
Requires:       python-oslo-policy >= 0.5.0
Requires:       python-oslo-reports >= 0.6.0
Requires:       python-oslo-rootwrap >= 0.6.0
Requires:       python-oslo-serialization >= 2.1.0
Requires:       python-oslo-service >= 1.0.0
Requires:       python-oslo-utils >= 3.4.0
Requires:       python-oslo-versionedobjects >= 1.4.0
Requires:       python-osprofiler >= 1.1.0
Requires:       python-paramiko
Requires:       python-paste-deploy
Requires:       python-paste
Requires:       python-pbr
Requires:       python-requests
Requires:       python-retrying >= 1.2.3
Requires:       python-routes
Requires:       python-rtslib >= 2.1
Requires:       python-simplejson >= 2.2.0
Requires:       python-six >= 1.9.0
Requires:       python-sqlalchemy >= 1.0.10
Requires:       python-stevedore >= 1.5.0
Requires:       python-suds
Requires:       python-webob >= 1.2.3
Requires:       pytz

%description -n python-%{pypi_name}
Conveyor Code


%package -n python-%{pypi_name}-tests
Summary:        Conveyor tests
Requires:       python-%{pypi_name} = %{epoch}:%{version}-%{release}

%description -n python-%{pypi_name}-tests
Conveyor tests

%prep
%setup -q -n conveyor-%{upstream_version}

find . \( -name .gitignore -o -name .placeholder \) -delete

find conveyor -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

sed -i 's/%{version}.%{milestone}/%{version}/' PKG-INFO

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
PYTHONPATH=. oslo-config-generator --config-file=etc/conveyor/conveyor-config-generator.conf

%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Setup directories
install -d -m 750 %{buildroot}%{_sysconfdir}/conveyor
install -d -m 750 %{buildroot}%{_sysconfdir}/conveyor/rootwrap.d
install -d -m 750 %{buildroot}%{_localstatedir}/log/conveyor
install -d -m 755 %{buildroot}%{_sharedstatedir}/conveyor

# Install config files
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datarootdir}/conveyor/conveyor-dist.conf
install -p -D -m 755 etc/conveyor/conveyor.conf.sample %{buildroot}%{_sysconfdir}/conveyor/conveyor.conf
install -p -D -m 755 etc/conveyor/api-paste.ini %{buildroot}%{_sysconfdir}/conveyor/api-paste.ini
install -p -D -m 755 etc/conveyor/policy.json %{buildroot}%{_sysconfdir}/conveyor/policy.json
install -p -D -m 755 etc/conveyor/rootwrap.conf %{buildroot}%{_sysconfdir}/conveyor/rootwrap.conf
install -p -D -m 755 etc/conveyor/rootwrap.d/*.filters %{buildroot}%{_sysconfdir}/conveyor/rootwrap.d

# Install initscripts for conveyor services
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/conveyor-api.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/conveyor-clone.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/conveyor-resource.service
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/conveyor-plan.service

# Install sudoers
install -p -D -m 440 %{SOURCE3} %{buildroot}%{_sysconfdir}/sudoers.d/conveyor

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/conveyor

# INstall pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/conveyor

# Remove unneeded in production stuff
rm -f %{buildroot}%{_bindir}/conveyor-debug
rm -fr %{buildroot}%{python2_sitelib}/run_tests.*
rm -f %{buildroot}/usr/share/doc/conveyor/README*

%pre -n python-%{pypi_name}
getent group conveyor >/dev/null || groupadd -r conveyor
if ! getent passwd conveyor >/dev/null; then
    useradd -r -g conveyor -G conveyor,nobody -d %{_sharedstatedir}/conveyor -s /sbin/nologin -c "Conveyor Daemons" conveyor
fi
exit 0

%post
%systemd_post conveyor-api
%systemd_post conveyor-clone
%systemd_post conveyor-resource
%systemd_post conveyor-plan

%preun
%systemd_preun conveyor-api
%systemd_preun conveyor-clone
%systemd_preun conveyor-resource
%systemd_preun conveyor-plan

%postun
%systemd_postun_with_restart conveyor-api
%systemd_postun_with_restart conveyor-clone
%systemd_postun_with_restart conveyor-resource
%systemd_postun_with_restart conveyor-plan

%files
%dir %{_sysconfdir}/conveyor
%config(noreplace) %attr(-, root, conveyor) %{_sysconfdir}/conveyor/conveyor.conf
%config(noreplace) %attr(-, root, conveyor) %{_sysconfdir}/conveyor/api-paste.ini
%config(noreplace) %attr(-, root, conveyor) %{_sysconfdir}/conveyor/rootwrap.conf
%config(noreplace) %attr(-, root, conveyor) %{_sysconfdir}/conveyor/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/conveyor
%config(noreplace) %{_sysconfdir}/sudoers.d/conveyor
%{_sysconfdir}/conveyor/rootwrap.d/
%attr(-, root, conveyor) %{_datadir}/conveyor/conveyor-dist.conf

%dir %attr(0750, conveyor, root) %{_localstatedir}/log/conveyor
%dir %attr(0755, conveyor, root) %{_localstatedir}/run/conveyor

%{_bindir}/conveyor-*
%{_unitdir}/*.service
%{_datarootdir}/conveyor

%defattr(-, conveyor, conveyor, -)
%dir %{_sharedstatedir}/conveyor

%files -n python-conveyor
%{?!_licensedir: %global license %%doc}
%license LICENSE
%{python2_sitelib}/conveyor
%{python2_sitelib}/conveyor-*.egg-info
%exclude %{python2_sitelib}/conveyor/tests

%files -n python-conveyor-tests
%license LICENSE
%{python2_sitelib}/conveyor/tests

%changelog
