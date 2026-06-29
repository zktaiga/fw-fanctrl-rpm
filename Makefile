SPECFILES := framework-tool.spec fw-fanctrl.spec fw-ectool.spec

.PHONY: check spec lint

check: spec lint

spec:
	@command -v rpmspec >/dev/null || { echo "rpmspec is required" >&2; exit 1; }
	rpmspec -q $(SPECFILES)

lint:
	@command -v rpmlint >/dev/null || { echo "rpmlint is required" >&2; exit 1; }
	rpmlint $(SPECFILES)
