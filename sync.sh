#!/bin/bash

: ${ROOT:=$(pwd)}
: ${REMOTE_KEY:=${ROOT}"/baysingers_production_20160627.pem"}
: ${SYNC_FOLDER:=${ROOT}"/sync/"}
: ${SQL_FOLDER:=${ROOT}"/syncPushSQL/"}
: ${CSV_FOLDER:=${ROOT}"/csv/"}
: ${REMOTE_ROOT_FOLDER:="/home/ubuntu/.virtualenvs/baysingers-v3/"}
: ${REMOTE_CURRENT_FOLDER:=${REMOTE_ROOT_FOLDER}"current/"}
: ${REMOTE_JSON_FOLDER:=${REMOTE_CURRENT_FOLDER}"sync/"}
: ${REMOTE_SQL_FOLDER:=${REMOTE_CURRENT_FOLDER}"syncPushSQL/"}
: ${REMOTE_CSV_FOLDER:=${REMOTE_CURRENT_FOLDER}"csv/"}

cd ${SYNC_FOLDER}
rm *.json
cd ${SQL_FOLDER}
rm *.sql
cd ${CSV_FOLDER}
rm *.csv
cd ${ROOT}
python < obAPI.py
ssh -i ${REMOTE_KEY} ubuntu@baysingers.com "cd ${REMOTE_ROOT_FOLDER} ; ./cleanSync.sh"
rsync -e "ssh -i ${REMOTE_KEY}" --verbose --progress --recursive --archive ${SYNC_FOLDER} ubuntu@baysingers.com:${REMOTE_JSON_FOLDER}
rsync -e "ssh -i ${REMOTE_KEY}" --verbose --progress --recursive --archive ${SQL_FOLDER} ubuntu@baysingers.com:${REMOTE_SQL_FOLDER}
rsync -e "ssh -i ${REMOTE_KEY}" --verbose --progress --recursive --archive ${CSV_FOLDER} ubuntu@baysingers.com:${REMOTE_CSV_FOLDER}
#ssh -i ${REMOTE_KEY} ubuntu@baysingers.com "cd ~ ; ./runSync.sh"