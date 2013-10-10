#!/usr/bin/env bash

domain="nive"
py=../nivetest/bin/python
if [[ -f $INS/bin/pyramidpy ]];then
    py="$INS/bin/pyramidpy"
fi
$py setup.py  extract_messages
$py setup.py  update_catalog -D $domain
$py setup.py  compile_catalog -D $domain

