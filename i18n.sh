#!/usr/bin/env bash
domain="nive_cms"
scrp=../nivetest/bin/pot-create 

$scrp -o $domain/locale/$domain.pot $domain

