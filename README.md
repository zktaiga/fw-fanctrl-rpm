# fw-fanctrl rpm

COPR for Framework Fan Control utilities.

| Packages   | COPR                                                                                                                                                                                                                                     |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| fw-ectool  | [![Copr build status for fw-ectool](https://copr.fedorainfracloud.org/coprs/zktaiga/fw-fanctrl/package/fw-ectool/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/zktaiga/fw-fanctrl/package/fw-ectool/)    |
| fw-fanctrl | [![Copr build status for fw-fanctrl](https://copr.fedorainfracloud.org/coprs/zktaiga/fw-fanctrl/package/fw-fanctrl/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/zktaiga/fw-fanctrl/package/fw-fanctrl/) |

## Installation

### Traditional Fedora/CentOS/RHEL

```bash
sudo dnf copr enable zktaiga/fw-fanctrl
sudo dnf install fw-fanctrl
```

### Immutable Fedora (Silverblue, Kinoite, Bluefin, etc.)

```bash
sudo dnf copr enable zktaiga/fw-fanctrl
sudo rpm-ostree install fw-fanctrl
# Reboot to apply, or use --apply-live to avoid reboot:
# sudo rpm-ostree install --apply-live fw-fanctrl
```

This will install `fw-fanctrl` along with its dependency `fw-ectool`.

**After installation, you must manually enable and start the service:**

```bash
sudo systemctl enable --now fw-fanctrl
```

To verify it's running:

```bash
sudo systemctl status fw-fanctrl
```
