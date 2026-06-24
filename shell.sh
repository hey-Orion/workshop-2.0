#!/bin/bash

LOG_FILE="/var/log/pipeline/app.log"

if [ ! -f "$LOG_FILE" ]; then
    echo "error"
    exit 1 
fi 

ERROR_COUNT=$(grep -i "critical" "$LOG_FILE" | wc -l)
echo "total: $ERROR_COUNT"


#!/bin/bash

DB_HOST
DB_PORT=5432

echo ""
until nc -z -v -w3 "$DB_HOST" "$DB_PORT"; do 
    echo "db wait"
    sleep 2 
done

echo ""