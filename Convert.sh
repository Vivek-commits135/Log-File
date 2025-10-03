#!/bin/bash
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
awk -f "${script_dir}/Validate.awk" "$1"
if [[ $? -ne 0 ]]; then
    exit 1
else
    sed -e 's/\[//1' -e 's/\[//1' -e 's/] /,/1' -e 's/] /,/1' "$1" | awk -f "${script_dir}/Convert.awk" > "${script_dir}/Summary.csv"
fi