#!/usr/bin/env bash
set -euo pipefail

if [[ "$EUID" != 0 ]]; then
    exec sudo bash "$0" "$@"
fi

if [[ -d /etc/framework-ectool ]]; then
    shopt -s nullglob
    for script in /etc/framework-ectool/*; do
        [[ -f "$script" && -x "$script" ]] || continue
        bash "$script"
    done
fi
