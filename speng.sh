#!/usr/bin/env bash

PROJECT_FOLDER="/Users/jannie/Workshop/speng"
SAMPLE_FOLDER="/Applications/LibreOffice.app/Contents/Resources/Scripts/python"
TEMPLATE_FOLDER="~/Library/Application\ Support/LibreOffice/4/user/template"
SCRIPT="scriptlight.py"
HOSTING_DOCUMENT="se.ott"

usage () {
   	echo "Usage: speng (start|run <function>|deploy|open)"
}

case "$1" in
start)
  /Applications/LibreOffice.app/Contents/MacOS/soffice --writer --accept="socket,host=localhost,port=2002;urp;StarOffice.ServiceManager"
;;
run)
  /Applications/LibreOffice.app/Contents/Resources/python -c "import scriptlight; scriptlight.$2()"
;;
deploy)
  cd $PROJECT_FOLDER
  python push_macro.py $SCRIPT $HOSTING_DOCUMENT
;;
open)
   edit . $SAMPLE_FOLDER
;;
*)
    # test if script is sourced
    if [[ $0 = ${BASH_SOURCE} ]] ; then
        usage
    else
        cd $PROJECT_FOLDER
    fi
;;
esac