#!/bin/sh

WEB_EXT=../node_modules/web-ext/bin/web-ext

$WEB_EXT lint -s chrome;

echo "API key issuer:";
read issuer;

echo "API key secret:";
read secret;

$WEB_EXT sign --api-key $issuer --api-secret $secret -s chrome -a .;

mv bmat*.xpi ../bmat/static;
