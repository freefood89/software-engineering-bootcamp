#!/usr/bin/env bash

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
FRONTEND_LOCATION="${SCRIPTPATH}/../frontend/build"

aws s3 cp $FRONTEND_LOCATION s3://imagely-frontend --recursive