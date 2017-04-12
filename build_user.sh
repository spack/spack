#!/bin/sh

function s {
	spack find $@ | grep 'No package'
	if [ $? -eq 0 ]
	then
		spack install -y $@
	else
		echo "$@ has been installed."
	fi
}  

compilers=(
    %gcc@6.3.0
    %intel@17
)

s zlib 	%gcc@6.3.0
