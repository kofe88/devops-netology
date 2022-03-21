#!/bin/bash
commitRegex='^(\[[[:digit:]]{2}\-[[:alpha:]]+\-[[:digit:]]{2}\-[[:alpha:]]+\]\ [a-zA-Zа-яА-Я0-9\ \.\,\;\:]{1,30}$|merge|hotfix)'
if ! grep -qE "$commitRegex" "$1"; then
    echo "Aborting according commit message policy. Please specify [NN-string-NN-string] string."
    exit 1
fi
