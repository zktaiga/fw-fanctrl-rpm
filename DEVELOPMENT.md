# Development Guide

This document explains how to build, test, update, and maintain the RPM packages in this repository.

## Repository Structure

This repository contains three RPM spec files:

- **framework-tool.spec** - Framework Computer's current `framework_tool` utility from `FrameworkComputer/framework-system`.
- **fw-fanctrl.spec** - Fan control service from `TamtamHero/fw-fanctrl`; depends on `framework-tool`.
- **fw-ectool.spec** - Legacy EC utility package kept for users who need `ectool`/`fw-ectool` directly.

Current `fw-fanctrl` releases use `framework_tool`, not `fw-ectool`.

## Prerequisites

### Fedora/RHEL-based Systems

```bash
sudo dnf install rpm-build rpmdevtools rpmlint dnf-plugins-core
```

### Immutable Systems (Bluefin, Silverblue, etc.)

Use a toolbox container:

```bash
toolbox create rpm-build
toolbox enter rpm-build
sudo dnf install rpm-build rpmdevtools rpmlint dnf-plugins-core
```

## Building Locally

### 1. Setup RPM Build Environment

```bash
rpmdev-setuptree
```

### 2. Install Build Dependencies

```bash
sudo dnf builddep framework-tool.spec
sudo dnf builddep fw-fanctrl.spec
sudo dnf builddep fw-ectool.spec
```

### 3. Download Sources

```bash
spectool -g -R framework-tool.spec
spectool -g -R fw-fanctrl.spec
spectool -g -R fw-ectool.spec

# Additional local sources for fw-ectool only
cp fw-ectool.sh framework-ectool.service framework-ectool.sh ~/rpmbuild/SOURCES/
```

### 4. Build Packages

Build dependency order:

```bash
# fw-fanctrl depends on framework-tool
rpmbuild -ba framework-tool.spec
sudo dnf install ~/rpmbuild/RPMS/*/framework-tool-*.rpm
rpmbuild -ba fw-fanctrl.spec

# fw-ectool is independent/legacy
rpmbuild -ba fw-ectool.spec
```

### 5. Built Packages Location

The RPM packages will be in:

- `~/rpmbuild/RPMS/*/framework-tool-*.rpm`
- `~/rpmbuild/RPMS/noarch/fw-fanctrl-*.rpm`
- `~/rpmbuild/RPMS/*/fw-ectool-*.rpm`
- `~/rpmbuild/SRPMS/*.src.rpm`

## Installing Locally Built Packages

### Regular Fedora Systems

```bash
sudo dnf install ~/rpmbuild/RPMS/*/framework-tool-*.rpm ~/rpmbuild/RPMS/noarch/fw-fanctrl-*.rpm
sudo systemctl enable --now fw-fanctrl
```

### Immutable Systems (Bluefin, Silverblue)

```bash
# Copy from toolbox to host if built in toolbox
toolbox run -c rpm-build cp ~/rpmbuild/RPMS/*/*.rpm ~/fw-fanctrl-rpm/

# Install with rpm-ostree
rpm-ostree install ./framework-tool-*.rpm ./fw-fanctrl-*.rpm
systemctl reboot
```

After reboot:

```bash
sudo systemctl enable --now fw-fanctrl
```

## Updating Package Versions

Version updates are Renovate-managed. Specs use tag-based source URLs so Renovate only needs to update `Version:`.

### Updating framework-tool

1. Find the new tag at <https://github.com/FrameworkComputer/framework-system/releases>.
2. Edit `framework-tool.spec`:

   ```spec
   Version:        X.Y.Z
   ```

3. Build and test.

### Updating fw-fanctrl

1. Find the new tag at <https://github.com/TamtamHero/fw-fanctrl/releases>.
2. Edit `fw-fanctrl.spec`:

   ```spec
   Version:        X.Y.Z
   ```

3. Build and test.

No local patch to `install.sh` is carried. The spec installs Python files, configuration, and systemd units directly using RPM-native steps.

### Updating fw-ectool

`fw-ectool` still tracks a specific framework-ec commit because upstream does not publish version tags for this use case.

1. Find the desired commit from <https://github.com/DHowett/framework-ec>.
2. Edit `fw-ectool.spec`:

   ```spec
   %global commit      NEW_COMMIT_HASH_HERE
   Version:            vX.Y.Z
   Release:            1%{gitrel}%{?dist}
   ```

3. Build and test.

## Testing Spec Files

Run the repository check target:

```bash
make check
```

Equivalent manual commands:

```bash
rpmspec -q framework-tool.spec
rpmspec -q fw-fanctrl.spec
rpmspec -q fw-ectool.spec

rpmlint framework-tool.spec fw-fanctrl.spec fw-ectool.spec
```

After building, inspect package contents:

```bash
rpm -qpl ~/rpmbuild/RPMS/*/framework-tool-*.rpm
rpm -qpl ~/rpmbuild/RPMS/noarch/fw-fanctrl-*.rpm
rpm -qpl ~/rpmbuild/RPMS/*/fw-ectool-*.rpm
```

## Publishing to COPR

### Package Setup

Configure these COPR packages as SCM builds from this repository:

1. `framework-tool` using `framework-tool.spec`
2. `fw-fanctrl` using `fw-fanctrl.spec`
3. `fw-ectool` using `fw-ectool.spec` if you still want to publish the legacy helper

For `fw-fanctrl`, add the COPR repository itself as a build dependency so COPR can resolve `framework-tool`.

### Build Order

```text
framework-tool -> fw-fanctrl
fw-ectool can build independently
```

Example with `copr-cli`:

```bash
copr-cli build YOUR_USERNAME/fw-fanctrl --scm --clone-url https://github.com/YOUR_USERNAME/fw-fanctrl-rpm.git --spec framework-tool.spec
copr-cli build YOUR_USERNAME/fw-fanctrl --scm --clone-url https://github.com/YOUR_USERNAME/fw-fanctrl-rpm.git --spec fw-fanctrl.spec
copr-cli build YOUR_USERNAME/fw-fanctrl --scm --clone-url https://github.com/YOUR_USERNAME/fw-fanctrl-rpm.git --spec fw-ectool.spec
```

## Troubleshooting

### fw-fanctrl Build Fails: "framework-tool not found"

Build and publish/install `framework-tool` first, then rebuild `fw-fanctrl`.

### COPR Build Fails

Check:

1. `framework-tool` and `fw-fanctrl` are both configured in COPR.
2. `framework-tool` builds before `fw-fanctrl`.
3. The COPR repo is added as a build dependency for `fw-fanctrl`.
4. Spec files pass `make check` locally.

## Package Information

### framework-tool Files

- `/usr/bin/framework_tool` - Framework Computer utility used by `fw-fanctrl`.
- Shell completions for bash, zsh, and fish.

### fw-fanctrl Files

- `/usr/bin/fw-fanctrl` - Main fan control executable.
- `/usr/lib/python3.X/site-packages/fw_fanctrl/` - Python package.
- `/usr/lib/systemd/system/fw-fanctrl.service` - Main service.
- `/usr/lib/systemd/system/fw-fanctrl-suspend.service` - Sleep hook service.
- `/etc/fw-fanctrl/config.json` - Configuration file.
- `/etc/fw-fanctrl/config.schema.json` - JSON schema.

### fw-ectool Files

- `/usr/bin/ectool` - Legacy EC utility binary.
- `/usr/bin/fw-ectool` - Wrapper script.
- `/usr/lib/systemd/system/framework-ectool.service` - Optional systemd service.
- `/usr/libexec/framework-ectool` - Helper script.

## Version Bumping Checklist

- [ ] Update `Version:` in the relevant spec, or review Renovate's PR.
- [ ] Test with `make check`.
- [ ] Build locally or in COPR.
- [ ] For `fw-fanctrl`, confirm `framework-tool` is available first.
- [ ] Update COPR builds.

## References

- [Fedora RPM Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/)
- [Fedora Rust Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/Rust/)
- [COPR Documentation](https://docs.pagure.org/copr.copr/)
- [fw-fanctrl upstream](https://github.com/TamtamHero/fw-fanctrl)
- [framework-system upstream](https://github.com/FrameworkComputer/framework-system)
- [framework-ec upstream](https://github.com/DHowett/framework-ec)
