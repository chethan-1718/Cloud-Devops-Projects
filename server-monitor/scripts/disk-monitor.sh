#!/bin/bash

# Disk usage threshold 
THRESHOLD=80

# Get root filesystem disk usage as  a number 
DISK_USAGE=$(df -P / | awk 'NR==2 {gsub("%","",$5); print $5}')

# Current Timestamp
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Log file location
LOG_FILE="$HOME/devops-projects/server-monitor/logs/disk-monitor.log"

# Check disk usage
if [ "$DISK_USAGE" -ge "$THRESHOLD" ];then
	echo "$TIMESTAMP WARNING : Disk usage is ${DISK_USAGE}%" | tee -a "$LOG_FILE"
else
	echo "$TIMESTAMP OK : Disk usage is ${DISK_USAGE}%" | tee -a "$LOG_FILE"
fi



# Memory usage threshold
MEMORY_THRESHOLD=80

# Get total and available memory in MB
MEMORY_TOTAL=$(free -m | awk '/^Mem:/ {print $2}')
MEMORY_AVAILABLE=$(free -m | awk '/^Mem:/ {print $7}')

# Calculate memory usage percentage
MEMORY_USAGE=$(( (MEMORY_TOTAL - MEMORY_AVAILABLE) * 100 / MEMORY_TOTAL ))

# Check memory usage
if [ "$MEMORY_USAGE" -ge "$MEMORY_THRESHOLD" ]; then
    echo "$TIMESTAMP WARNING: Memory usage is ${MEMORY_USAGE}%" | tee -a "$LOG_FILE"
else
    echo "$TIMESTAMP OK: Memory usage is ${MEMORY_USAGE}%" | tee -a "$LOG_FILE"
fi



# CPU load monitoring
CPU_THRESHOLD=$(nproc)

# Get the 1-minute load average
CPU_LOAD=$(awk '{print $1}' /proc/loadavg)

# Compare load average with the threshold
if awk -v cpu_value="$CPU_LOAD" -v threshold="$CPU_THRESHOLD" \
    'BEGIN {exit !(cpu_value >= threshold)}'; then
    echo "$TIMESTAMP WARNING: CPU load average is ${CPU_LOAD}" | tee -a "$LOG_FILE"
else
    echo "$TIMESTAMP OK: CPU load average is ${CPU_LOAD}" | tee -a "$LOG_FILE"
fi

