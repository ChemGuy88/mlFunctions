#!/bin/bash

# An example of how to read text to a while-loop.

# Formatting
bld=$(tput bold)
nrl=$(tput sgr0)
GRN=$'\e[0;32m'
RED=$'\e[0;31m'
NC=$'\e[0m'

TEXT=$'a\nx\nc'
echo " ${bld}${GRN}>>>${nrl}${NC} This is the text being fed to the for-loop ${bld}${GRN}>>>${nrl}${NC}"
echo "$TEXT"
echo " ${bld}${GRN}<<<${nrl}${NC} This is the text being fed to the for-loop ${bld}${GRN}<<<${nrl}${NC}"


echo " ${bld}${RED}>>>${nrl}${NC} This is the for-loop segmentation of the text ${bld}${RED}>>>${nrl}${NC}"
it=0
while read -r line;
do
    it=$((it+1))
    echo "Line $it: $line"
done < <(echo "$TEXT")
echo " ${bld}${RED}<<<${nrl}${NC} This is the for-loop segmentation of the text ${bld}${RED}<<<${nrl}${NC}"
