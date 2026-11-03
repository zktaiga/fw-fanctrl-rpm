%global debug_package %{nil}
# Renovate updates this release tag and binary checksum together.
%global tool_tag v0.6.6
%global tool_sha256 ebc2f3ca300dac6f484c02d058833372ff8dd3c23f2a74b63c774f8dc2f86171

Name:           framework-tool
Version:        %{sub %{tool_tag} 2}
Release:        1%{?dist}
Summary:        Tool to control Framework Computer systems

License:        BSD-3-Clause
URL:            https://github.com/FrameworkComputer/framework-system
Source0:        %{url}/archive/refs/tags/v%{version}/framework-system-%{version}.tar.gz
Source1:        %{url}/releases/download/v%{version}/framework_tool

ExclusiveArch:  x86_64
BuildRequires:  coreutils

Provides:       framework_tool = %{version}-%{release}

%description
framework_tool is Framework Computer's command-line utility for inspecting and
controlling Framework systems, including embedded-controller fan behavior used
by fw-fanctrl.

%prep
echo "%{tool_sha256}  %{SOURCE1}" | sha256sum --check
%autosetup -n framework-system-%{version}

%build
# Upstream publishes the Linux framework_tool release binary. Building from
# source in Fedora/COPR currently requires several Rust crates that are not
# packaged for Fedora, so this RPM repackages the checksum-pinned release asset.

%install
install -Dm755 %{SOURCE1} %{buildroot}%{_bindir}/framework_tool
install -Dm644 framework_tool/framework_tool.1 \
    %{buildroot}%{_mandir}/man1/framework_tool.1
install -Dm644 framework_tool/completions/bash/framework_tool \
    %{buildroot}%{_datadir}/bash-completion/completions/framework_tool
install -Dm644 framework_tool/completions/zsh/_framework_tool \
    %{buildroot}%{_datadir}/zsh/site-functions/_framework_tool
install -Dm644 framework_tool/completions/fish/framework_tool.fish \
    %{buildroot}%{_datadir}/fish/vendor_completions.d/framework_tool.fish

%files
%license LICENSE.md
%doc README.md EXAMPLES.md EXAMPLES_ADVANCED.md
%{_bindir}/framework_tool
%{_mandir}/man1/framework_tool.1*
%{_datadir}/bash-completion/completions/framework_tool
%{_datadir}/zsh/site-functions/_framework_tool
%{_datadir}/fish/vendor_completions.d/framework_tool.fish

%changelog
%autochangelog
