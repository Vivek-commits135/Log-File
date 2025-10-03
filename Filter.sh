#!/bin/bash
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# if no filter is set
if [[ $# -eq 1 ]]; then
    cat "${script_dir}/Summary.csv" > "$1"
    exit 0
fi

# load all selected filters into arrays
levels=()
events=()
if [[ $4 -eq 1 ]]; then
    levels+=("notice")
fi
if [[ $5 -eq 1 ]]; then
    levels+=("error")
fi
if [[ $6 -eq 1 ]]; then
    events+=("E1")
fi
if [[ $7 -eq 1 ]]; then
    events+=("E2")
fi
if [[ $8 -eq 1 ]]; then
    events+=("E3")
fi
if [[ $9 -eq 1 ]]; then
    events+=("E4")
fi
if [[ ${10} -eq 1 ]]; then
    events+=("E5")
fi
if [[ ${11} -eq 1 ]]; then
    events+=("E6")
fi
levelstr=$(IFS=","; echo "${levels[*]}")
eventstr=$(IFS=","; echo "${events[*]}")
awk -v from="$2" -v to="$3" -v levelstr="$levelstr" -v eventstr="$eventstr" -f "${script_dir}/Filter.awk" "${script_dir}/Summary.csv" > "$1"