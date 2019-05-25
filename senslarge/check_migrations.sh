#!/bin/bash

EXIT_CODE=0

# Check migrations
for app in evaluations ; do
MIGRATIONS=$(./manage.py makemigrations --dry-run $app)
if [ "$MIGRATIONS" != "No changes detected in app '$app'" ] ; then
    if [ $EXIT_CODE -eq 0 ] ; then
        echo "Migrations should be made : "
    fi
    echo "$MIGRATIONS"
    EXIT_CODE=1
else
    echo "No migration to be done in app $app"
fi
done
exit $EXIT_CODE
