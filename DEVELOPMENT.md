# Development Guide

This document explains how to build, test, update, and maintain the fw-fanctrl RPM packages.

## Repository Structure

This repository contains two separate RPM spec files:

- **fw-ectool.spec** - EC tool for Framework laptops (dependency)
- **fw-fanctrl.spec** - Fan control software (main package)

Both packages are built separately but `fw-fanctrl` requires `fw-ectool` to be installed.

## Prerequisites

### For Building on Fedora/RHEL-based Systems

```bash
sudo dnf install rpm-build rpmdevtools
```

### For Building on Immutable Systems (Bluefin, Silverblue, etc.)

Use a toolbox container:

```bash
toolbox create rpm-build
toolbox enter rpm-build
sudo dnf install rpm-build rpmdevtools
```

## Building Locally

### 1. Setup RPM Build Environment

```bash
rpmdev-setuptree
```

### 2. Install Build Dependencies

```bash
sudo dnf builddep fw-ectool.spec
sudo dnf builddep fw-fanctrl.spec
```

### 3. Download Sources

```bash
spectool -g -R fw-ectool.spec
spectool -g -R fw-fanctrl.spec

# Copy additional source files
cp fw-ectool.sh framework-ectool.service framework-ectool.sh ~/rpmbuild/SOURCES/
cp 138-no-build.patch ~/rpmbuild/SOURCES/
```

### 4. Build Packages (in order)

**Important:** Build fw-ectool first, as fw-fanctrl depends on it.

```bash
# Build fw-ectool
rpmbuild -ba fw-ectool.spec

# Install fw-ectool (needed for fw-fanctrl build)
sudo dnf install ~/rpmbuild/RPMS/x86_64/fw-ectool-*.rpm

# Build fw-fanctrl
rpmbuild -ba fw-fanctrl.spec
```

### 5. Built Packages Location

The RPM packages will be in:
- `~/rpmbuild/RPMS/x86_64/fw-ectool-*.rpm`
- `~/rpmbuild/RPMS/x86_64/fw-fanctrl-*.rpm`
- `~/rpmbuild/SRPMS/*.src.rpm` (source RPMs)

## Installing Locally Built Packages

### On Regular Fedora Systems

```bash
sudo dnf install ~/rpmbuild/RPMS/x86_64/fw-ectool-*.rpm ~/rpmbuild/RPMS/x86_64/fw-fanctrl-*.rpm
```

### On Immutable Systems (Bluefin, Silverblue)

```bash
# Copy from toolbox to host (if built in toolbox)
toolbox run -c rpm-build cp ~/rpmbuild/RPMS/x86_64/*.rpm ~/fw-fanctrl-rpm/

# Install with rpm-ostree
rpm-ostree install ./fw-ectool-*.rpm ./fw-fanctrl-*.rpm

# Reboot to apply
systemctl reboot
```

## Updating Package Versions

### Updating fw-ectool

1. Find the new commit hash from https://github.com/DHowett/framework-ec

2. Edit `fw-ectool.spec`:
   ```spec
   %global commit      NEW_COMMIT_HASH_HERE
   %global commit_date YYYYMMDD
   ```

3. Update version/release if needed:
   ```spec
   Version:        vX.Y.Z
   Release:        1%{gitrel}%{?dist}
   ```

4. Build and test

### Updating fw-fanctrl

1. Find the new commit hash from https://github.com/TamtamHero/fw-fanctrl

2. Edit `fw-fanctrl.spec`:
   ```spec
   %global commit      NEW_COMMIT_HASH_HERE
   %global commit_date YYYYMMDD
   ```

3. Update version/release if needed:
   ```spec
   Version:        X.Y.Z
   Release:        1%{gitrel}%{?dist}
   ```

4. If fw-ectool version changed, update the dependency:
   ```spec
   Requires:       fw-ectool
   ```

5. Build and test

## Testing Spec Files

### Validate Spec Syntax

```bash
rpmspec -q fw-ectool.spec
rpmspec -q fw-fanctrl.spec
```

This will show what packages will be produced.

### Check for Build Issues

```bash
rpmlint fw-ectool.spec
rpmlint fw-fanctrl.spec
```

### Test Installation

After building, test the RPMs:

```bash
rpm -qpl ~/rpmbuild/RPMS/x86_64/fw-ectool-*.rpm  # List files
rpm -qpl ~/rpmbuild/RPMS/x86_64/fw-fanctrl-*.rpm
```

## Publishing to COPR

### Setting Up a New COPR Repository

1. Go to https://copr.fedorainfracloud.org/
2. Click "New Project"
3. Fill in:
   - **Name:** `fw-fanctrl`
   - **Chroots:** Select Fedora versions (e.g., Fedora 42, Fedora 41)
4. Create project

### Adding Packages to COPR

#### Add fw-ectool Package

1. In your COPR project, click "Packages" → "Add Package"
2. Select "SCM" type
3. Fill in:
   - **Package name:** `fw-ectool`
   - **Clone URL:** `https://github.com/YOUR_USERNAME/fw-fanctrl-rpm.git`
   - **Spec file:** `fw-ectool.spec`
4. Save

#### Add fw-fanctrl Package

1. Click "Add Package" again
2. Select "SCM" type
3. Fill in:
   - **Package name:** `fw-fanctrl`
   - **Clone URL:** `https://github.com/YOUR_USERNAME/fw-fanctrl-rpm.git`
   - **Spec file:** `fw-fanctrl.spec`
4. **Important:** In "Edit" → "Build Dependencies" → Add your COPR repo (so it can find fw-ectool)
5. Save

### Building in COPR

**Build order matters:**

1. Build `fw-ectool` first
2. Wait for it to complete successfully
3. Then build `fw-fanctrl`

To rebuild after updates:
```bash
# Using copr-cli (if installed)
copr-cli build YOUR_USERNAME/fw-fanctrl --scm --clone-url https://github.com/YOUR_USERNAME/fw-fanctrl-rpm.git --spec fw-ectool.spec
copr-cli build YOUR_USERNAME/fw-fanctrl --scm --clone-url https://github.com/YOUR_USERNAME/fw-fanctrl-rpm.git --spec fw-fanctrl.spec
```

Or use the web interface to trigger builds.

## Troubleshooting

### Build Fails: "Cannot read patch file"

Make sure all source files are copied to `~/rpmbuild/SOURCES/`:
```bash
cp 138-no-build.patch fw-ectool.sh framework-ectool.service framework-ectool.sh ~/rpmbuild/SOURCES/
```

### fw-fanctrl Build Fails: "fw-ectool not found"

Build and install fw-ectool first:
```bash
rpmbuild -ba fw-ectool.spec
sudo dnf install ~/rpmbuild/RPMS/x86_64/fw-ectool-*.rpm
```

### COPR Build Fails

Check:
1. Both packages are configured in COPR
2. Build order (fw-ectool before fw-fanctrl)
3. COPR repo is added as build dependency for fw-fanctrl
4. Spec files are valid (`rpmspec -q` test)

## Package Information

### fw-ectool Files

- `/usr/bin/ectool` - EC tool binary
- `/usr/bin/fw-ectool` - Wrapper script
- `/usr/lib/systemd/system/framework-ectool.service` - Systemd service
- `/usr/libexec/framework-ectool` - Helper script

### fw-fanctrl Files

- `/usr/bin/fw-fanctrl` - Main fan control executable
- `/usr/lib/python3.13/site-packages/fw_fanctrl/` - Python package
- `/usr/lib/systemd/system/fw-fanctrl.service` - Systemd service
- `/etc/fw-fanctrl/config.json` - Configuration file
- `/etc/fw-fanctrl/config.schema.json` - JSON schema
- `/usr/lib/systemd/system-sleep/fw-fanctrl-suspend` - Suspend hook

## Version Bumping Checklist

When updating versions:

- [ ] Update `%global commit` hash
- [ ] Update `%global commit_date`
- [ ] Update `Version:` if upstream version changed
- [ ] Update `Release:` (reset to 1 on version bump, increment on packaging changes)
- [ ] Test build locally
- [ ] Verify spec with `rpmspec -q`
- [ ] Test installation
- [ ] Update COPR builds
- [ ] Tag release in git (optional): `git tag vX.Y.Z && git push --tags`

## References

- [Fedora RPM Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/)
- [COPR Documentation](https://docs.pagure.org/copr.copr/)
- [fw-fanctrl upstream](https://github.com/TamtamHero/fw-fanctrl)
- [framework-ec upstream](https://github.com/DHowett/framework-ec)
