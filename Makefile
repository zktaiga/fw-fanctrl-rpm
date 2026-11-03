SPECFILES := framework-tool.spec fw-fanctrl.spec fw-ectool.spec
RPM_TOPDIR ?= $(CURDIR)/.build/framework-tool

.PHONY: check spec lint build-framework-tool

check: spec lint

spec:
	@command -v rpmspec >/dev/null || { echo "rpmspec is required" >&2; exit 1; }
	rpmspec -q $(SPECFILES)

lint:
	@command -v rpmlint >/dev/null || { echo "rpmlint is required" >&2; exit 1; }
	rpmlint $(SPECFILES)

build-framework-tool:
	@command -v spectool >/dev/null || { echo "spectool (rpmdevtools) is required" >&2; exit 1; }
	@command -v rpmbuild >/dev/null || { echo "rpmbuild is required" >&2; exit 1; }
	mkdir -p "$(RPM_TOPDIR)/SOURCES"
	spectool -g -R --force --define "_topdir $(RPM_TOPDIR)" framework-tool.spec
	rpmbuild -ba --define "_topdir $(RPM_TOPDIR)" framework-tool.spec
