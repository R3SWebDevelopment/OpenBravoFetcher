#!/bin/bash

: ${ROOT:=$(pwd)}
: ${REMOTE_KEY:=${ROOT}"/keys/baysingers_production_20160627.pem"}
: ${SYNC_FOLDER:=${ROOT}"/sync/"}
: ${SQL_FOLDER:=${ROOT}"/syncPushSQL/"}
: ${REMOTE_ROOT_FOLDER:="/home/ubuntu/.virtualenvs/baysingers-v3/"}
: ${REMOTE_CURRENT_FOLDER:=${REMOTE_ROOT_FOLDER}"current/"}
: ${REMOTE_JSON_FOLDER:=${REMOTE_CURRENT_FOLDER}"sync/"}
: ${REMOTE_SQL_FOLDER:=${REMOTE_CURRENT_FOLDER}"syncPushSQL/"}

cd ${SYNC_FOLDER}
rm *.json
cd ${SQL_FOLDER}
rm *.sql
cd ${ROOT}
python < obAPI.py
ssh -i ${REMOTE_KEY} ubuntu@baysingers.com "cd ${REMOTE_ROOT_FOLDER} ; ./cleanSync.sh"
rsync -e "${REMOTE_KEY}" --verbose --progress --recursive --archive ${SYNC_FOLDER} ubuntu@baysingers.com:${REMOTE_JSON_FOLDER}
rsync -e "${REMOTE_KEY}" --verbose --progress --recursive --archive ${SQL_FOLDER} ubuntu@baysingers.com:${REMOTE_SQL_FOLDER}
ssh -i ${REMOTE_KEY} ubuntu@baysingers.com "cd ~ ; ./runSync.sh"