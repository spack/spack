#!/usr/bin/env bash

if [[ "$1" == "intel64" ]] ; then
    export FOO='intel64'
else
    export FOO='default'
fi