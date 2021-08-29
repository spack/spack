#!/bin/bash
# There are several older branches are that are still being maintained,
# e.g., 5.13.x, 5.10.x, 5.4.x, 4.19.x, 4.14.x, 4.4.x, etc.  It's certainly
# possible to automate the update process within package.py, but for now
# let's do this manually and see how often it gets used.

# To run:
# 1. Delete all of the existing "version()" lines in package.py.
# 2. bash ./generate_versions.sh >> package.py
# 3. Edit package.py to comment out versions that are not interesting.
#    That's probably everything before 2.6.29 or so.

# Subdirectories v3.0 and v3.x are duplicates.  We'll use the latter.
# The 6.x directory exists but has not yet (29 Aug 2021) been populated.
for d in 1.0 1.1 1.2 1.3 2.0 2.1 2.2 2.3 2.4 2.5 2.6 3.x 4.x 5.x
do
    wget https://mirrors.edge.kernel.org/pub/linux/kernel/v${d}/sha256sums.asc
    mv sha256sums.asc v${d}_sha256sums.asc
done

grep -rh xz v*_sha256sums.asc  	| \
	grep linux 		            | \
	tr -s [:blank:] 	        | \
	sed -e "s/linux-//" 	    | \
	sed -e "s/.tar.xz//"	    | \
	sort -k2 -Vr		        | \
	sed -e "s/\(.*\) \(.*\)/    version(\'\2\', sha256=\'\1\')/"

