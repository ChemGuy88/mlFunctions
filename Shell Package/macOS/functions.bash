listpath () {
     awk -F\: '{
     for (i = 0; ++i <= NF;)
          print "Path", i,":", $i
     }' <<<"$1"
}
# listpath $PATH
# listpath $PYTHONPATH

getTimestamp() {
    date "+%Y-%m-%d %H-%M-%S"
}

getDirectorySizes () {
    du -csh "$1"/*/
}

getPgrep() {
    pgrep -U "$1" -f "$2" | xargs --no-run-if-empty ps f -o lstart -o "%p %r %y %x %a" --sort +pid p
}
