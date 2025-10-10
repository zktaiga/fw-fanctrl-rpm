%global jobid 899
%global debug_package %{nil}

%global reponame    fw-fanctrl
%global commit      776f619cea2b07bf7c21cdd41e9e50297377ec3b
%global commit_date 20250929
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitrel      .%{commit_date}.git%{shortcommit}

Name:           fw-fanctrl
Version:        0.0.0
Release:        1%{gitrel}%{?dist}
Summary:        Framework FanControl Software

License:        BSD-3-Clause
URL:            https://github.com/TamtamHero/%{name}
Source0:        https://github.com/TamtamHero/%{name}/archive/%{commit}.tar.gz

BuildRequires:  systemd-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(wheel)
BuildRequires:  python3dist(build)
Requires:       python3
Requires:       fw-ectool

Patch0:         138-no-build.patch

%description
Framework Fan control script

%prep
%autosetup -n %{name}-%{commit}

%build
%pyproject_wheel

%install
./install.sh --no-sudo \
    --no-ectool \
    --no-pip-install \
    --no-pip-build \
    --no-post-install \
    --effective-installation-dir %{_bindir} \
    --dest-dir %{buildroot} \
    --prefix-dir /usr \
    --sysconf-dir /etc
%pyproject_install

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%license LICENSE
%{_bindir}/%{name}
%{python3_sitelib}/fw_fanctrl*
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/%{name}/config.json
%{_sysconfdir}/%{name}/config.schema.json
%{_prefix}/lib/systemd/system-sleep/%{name}-suspend

%changelog
%autochangelog
