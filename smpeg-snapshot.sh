#!/bin/bash

set -e

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
svn=$(date +%Y%m%d)

pushd "$tmp"
svn export svn://svn.icculus.org/smpeg/trunk smpeg
pushd smpeg
aclocal-1.7 $ACLOCAL_FLAGS
automake-1.7 --foreign
autoconf
./configure
make dist
mv *.tar.gz "$pwd"/smpeg-$svn.tar.gz
popd >/dev/null

