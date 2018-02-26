#!/bin/sh
# convenience wrapper for the rna-seqc jar file
java $JAVA_ARGS $JAVA_OPTS -jar RNA-SeQC_v{}.jar "$@"
