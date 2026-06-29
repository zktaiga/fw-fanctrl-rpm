%bcond check 0

Name:           framework-tool
# renovate: datasource=github-tags depName=FrameworkComputer/framework-system extractVersion=^v(?<version>.*)$
Version:        0.6.4
Release:        1%{?dist}
Summary:        Tool to control Framework Computer systems

License:        BSD-3-Clause
URL:            https://github.com/FrameworkComputer/framework-system
Source0:        %{url}/archive/refs/tags/v%{version}/framework-system-%{version}.tar.gz
# Move Windows-only build dependencies behind cfg(windows) so Linux RPM builds
# do not need crates that are unused on Fedora.
Patch0:         framework-system-linux-build-deps.patch

ExclusiveArch:  %{rust_arches}

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  pkgconfig(libusb-1.0)
BuildRequires:  hidapi-devel

Provides:       framework_tool = %{version}-%{release}

%description
framework_tool is Framework Computer's command-line utility for inspecting and
controlling Framework systems, including embedded-controller fan behavior used
by fw-fanctrl.

%prep
%autosetup -n framework-system-%{version} -p0
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires

%build
%cargo_build

%install
install -Dm755 target/release/framework_tool %{buildroot}%{_bindir}/framework_tool
install -Dm644 framework_tool/completions/bash/framework_tool \
    %{buildroot}%{_datadir}/bash-completion/completions/framework_tool
install -Dm644 framework_tool/completions/zsh/_framework_tool \
    %{buildroot}%{_datadir}/zsh/site-functions/_framework_tool
install -Dm644 framework_tool/completions/fish/framework_tool.fish \
    %{buildroot}%{_datadir}/fish/vendor_completions.d/framework_tool.fish

%if %{with check}
%check
%cargo_test
%endif

%files
%license LICENSE.md
%doc README.md EXAMPLES.md EXAMPLES_ADVANCED.md
%{_bindir}/framework_tool
%{_datadir}/bash-completion/completions/framework_tool
%{_datadir}/zsh/site-functions/_framework_tool
%{_datadir}/fish/vendor_completions.d/framework_tool.fish

%changelog
%autochangelog
