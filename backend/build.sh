#!/bin/sh
mkdir -p build/parsers
mkdir -p build/stores
cp -R parsers/*.py build/parsers
cp -R stores/*.py build/stores
cp aggregator.py utils.py build
cp prod.env build/.env
cp -R $VIRTUAL_ENV/lib/python2.7/site-packages/ build

cd build
zip -r9 ../latitude-backend.zip *
zip -g ../latitude-backend.zip .env
