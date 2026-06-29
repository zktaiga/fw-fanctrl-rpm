# fw-fanctrl rpm

COPR for Framework Fan Control utilities.

| Packages       | COPR                                                                                                                                                                                                                                             |
|----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| framework-tool | [![Copr build status for framework-tool](https://copr.fedorainfracloud.org/coprs/zktaiga/fw-fanctrl/package/framework-tool/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/zktaiga/fw-fanctrl/package/framework-tool/) |
| fw-fanctrl     | [![Copr build status for fw-fanctrl](https://copr.fedorainfracloud.org/coprs/zktaiga/fw-fanctrl/package/fw-fanctrl/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/zktaiga/fw-fanctrl/package/fw-fanctrl/)             |
| fw-ectool      | [![Copr build status for fw-ectool](https://copr.fedorainfracloud.org/coprs/zktaiga/fw-fanctrl/package/fw-ectool/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/zktaiga/fw-fanctrl/package/fw-ectool/)                |

## Installation

### Traditional Fedora/CentOS/RHEL

```bash
sudo dnf copr enable zktaiga/fw-fanctrl
sudo dnf install fw-fanctrl
sudo systemctl enable --now fw-fanctrl
```

To verify it's running:

```bash
systemctl status fw-fanctrl
```

### Immutable Fedora (Silverblue, Kinoite, Bluefin, etc.)

If `dnf copr` is available:

```bash
sudo dnf copr enable zktaiga/fw-fanctrl
sudo rpm-ostree install fw-fanctrl
sudo systemctl reboot
```

If `dnf copr` is not available, add the COPR repo file manually instead:

```bash
FEDORA_VERSION="$(rpm -E %fedora)"

sudo curl -L \
  -o /etc/yum.repos.d/zktaiga-fw-fanctrl.repo \
  "https://copr.fedorainfracloud.org/coprs/zktaiga/fw-fanctrl/repo/fedora-${FEDORA_VERSION}/zktaiga-fw-fanctrl-fedora-${FEDORA_VERSION}.repo"

sudo rpm-ostree refresh-md --force
sudo rpm-ostree install fw-fanctrl
sudo systemctl reboot
```

After rebooting into the new deployment, enable and start the service:

```bash
sudo systemctl enable --now fw-fanctrl
systemctl status fw-fanctrl
```

To apply the package without rebooting first, use `--apply-live`:

```bash
sudo rpm-ostree install --apply-live fw-fanctrl
sudo systemctl enable --now fw-fanctrl
```

This will install `fw-fanctrl` along with its dependency `framework-tool`. `fw-ectool` is still packaged for users who need the legacy EC utility directly, but current `fw-fanctrl` releases use Framework's `framework_tool`.

Commands such as `fw-fanctrl reload` require the `fw-fanctrl` service to be running first. If `reload` fails with `No such file or directory`, check the service status and logs:

```bash
systemctl status fw-fanctrl
journalctl -u fw-fanctrl -b --no-pager
```

The downloaded COPR repo file uses `$releasever`, so it should continue to point at the matching Fedora release after upgrades. However, rpm-ostree upgrades require this COPR to have builds for the target Fedora release. If an upgrade fails because `fw-fanctrl` cannot be resolved, temporarily remove it and reinstall once builds are available for your Fedora version.
