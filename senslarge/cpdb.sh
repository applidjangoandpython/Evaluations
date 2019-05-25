#!/bin/sh

DB='senslarge'
SSH_HOST='hbprod1'

if [ ! -z "$1" ] ; then SSH_HOST=$1 ; fi

dropdb $DB
createdb $DB

ssh $SSH_HOST "pg_dump --no-owner --no-privileges $DB | gzip" > $DB.sql.gz 
gunzip --stdout $DB.sql.gz | psql $DB
