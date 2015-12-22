#!/bin/sh

which cacheBust >/dev/null 2>&1
if [ $? -ne 0 ];
then
    echo "cacheBust is not installed. Install it first." >&2
    exit 1
fi

cacheBust test/test.html -r test/root
