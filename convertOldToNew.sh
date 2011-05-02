#!/bin/sh
for i in $(find -name "*.???"); do oldname=${i%.*}; len=$((${#oldname}-3)); newname=${oldname:0:$len}; ext=${i:len};echo mv $i ${newname}_$ext;done
