#!/bin/sh
# convenience wrapper for the trimmomatic.jar file
java $JAVA_ARGS $JAVA_OPTS -jar trimmomatic.jar "$@"
