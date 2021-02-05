#! /bin/bash
OS="`uname -s`"

if test "${OS}" = "Darwin" ; then
	BASE64DEC="-D"
else
	BASE64DEC="-d"
fi
