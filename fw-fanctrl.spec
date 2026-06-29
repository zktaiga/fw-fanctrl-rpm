Name:           fw-fanctrl
# renovate: datasource=github-tags depName=TamtamHero/fw-fanctrl extractVersion=^v(?<version>.*)$
Version:        1.1.0
Release:        1%{?dist}
Summary:        Framework FanControl Software

License:        BSD-3-Clause
URL:            https://github.com/TamtamHero/%{name}
Source0:        %{url}/archive/refs/tags/v%{version}/%{name}-%{version}.tar.gz

ExclusiveArch:  x86_64
BuildRequires:  pyproject-rpm-macros
BuildRequires:  systemd-rpm-macros
BuildRequires:  sed

Requires:       framework-tool

%description
Framework fan control service using Framework Computer's framework_tool.

%prep
%autosetup -n %{name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

install -Dm644 src/fw_fanctrl/_resources/config.json \
    %{buildroot}%{_sysconfdir}/%{name}/config.json
install -Dm644 src/fw_fanctrl/_resources/config.schema.json \
    %{buildroot}%{_sysconfdir}/%{name}/config.schema.json

install -d %{buildroot}%{_unitdir}
for service in services/*.service; do
    service_name="$(basename "${service}")"
    sed \
        -e 's|"%PYTHON_SCRIPT_INSTALLATION_PATH%"|%{_bindir}/fw-fanctrl|g' \
        -e 's|%SYSCONF_DIRECTORY%|%{_sysconfdir}|g' \
        "${service}" > "%{buildroot}%{_unitdir}/${service_name}"
done

%post
%systemd_post %{name}.service %{name}-suspend.service

%preun
%systemd_preun %{name}.service %{name}-suspend.service

%postun
%systemd_postun %{name}.service %{name}-suspend.service

%files
%license LICENSE
%{_bindir}/%{name}
%{python3_sitelib}/fw_fanctrl*
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}-suspend.service
%config(noreplace) %{_sysconfdir}/%{name}/config.json
%{_sysconfdir}/%{name}/config.schema.json

%changelog
%autochangelog
