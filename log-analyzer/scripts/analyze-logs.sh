#!/bin/bash

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

LOG_FILE="$PROJECT_DIR/logs/system.log"
REPORT_DIR="$PROJECT_DIR/reports"

if [[ ! -f "$LOG_FILE" ]]; then
    echo "ERROR: Log file not found: $LOG_FILE"
    exit 1
fi

mkdir -p "$REPORT_DIR"

TIMESTAMP=$(date '+%Y-%m-%d_%H-%M-%S')
REPORT_FILE="$REPORT_DIR/report-$TIMESTAMP.txt"

FAILED_LOGINS=$(grep -c 'Failed password' "$LOG_FILE")
ALERT_THRESHOLD=${1:-3}


if ! [[ "$ALERT_THRESHOLD" =~ ^[0-9]+$ ]] || (( ALERT_THRESHOLD < 1 )) ; then
        echo "ERROR : Alert threshold must be a positive integer."
	exit 1
fi 

{
    echo "===== Linux Log Analyzer ====="
    echo "Analysis time: $(date)"
    echo "Log file: $LOG_FILE"
    echo

    echo "ERROR count: $(grep -c 'ERROR' "$LOG_FILE")"
    echo "WARNING count: $(grep -c 'WARNING' "$LOG_FILE")"
    echo "INFO count: $(grep -c 'INFO' "$LOG_FILE")"
    echo "Failed Login attempts: $FAILED_LOGINS"
    echo 
    echo "==== Failed Login Details ===="
    grep -i "Failed Password" "$LOG_FILE"

    echo "===== Failed Attempts by IP ====="
    grep "Failed password" "$LOG_FILE" | awk '{
	    for (i = 1; i <= NF; i++) {
		    if ($i == "from") {
			    print $(i+1)
			}
   		}
	}' | sort | uniq -c

    if [[ "$FAILED_LOGINS" -ge "$ALERT_THRESHOLD" ]];
    then
	    echo "Alert: High number of failed login attempts detected!"
    else
	    echo "OK: Failed login attempts are below the threshold."
    fi

} | tee "$REPORT_FILE"

echo
echo "Report saved to: $REPORT_FILE"

