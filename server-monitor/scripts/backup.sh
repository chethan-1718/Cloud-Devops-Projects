
#!/bin/bash

# Source directory to back up
SOURCE_DIR="$HOME/devops-projects/server-monitor/backup_source"

# Directory to store backups
BACKUP_DIR="$HOME/devops-projects/server-monitor/backups"

# Log file
LOG_FILE="$HOME/devops-projects/server-monitor/logs/backup.log"

# Current timestamp
TIMESTAMP=$(date "+%Y-%m-%d_%H-%M-%S")

# Check whether the source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') ERROR: Source directory not found: $SOURCE_DIR" | tee -a "$LOG_FILE"
    exit 1
fi

#Create backup Dir if its not there 
if ! mkdir -p "$BACKUP_DIR"; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') ERROR: Could not create backup directory: $BACKUP_DIR" | tee -a "$LOG_FILE"
    exit 1
fi

# Create a compressed backup archive
if tar -czf "$BACKUP_DIR/backup-$TIMESTAMP.tar.gz" -C "$SOURCE_DIR" . &&
   tar -tzf "$BACKUP_DIR/backup-$TIMESTAMP.tar.gz" > /dev/null; then   

    echo "$(date '+%Y-%m-%d %H:%M:%S') SUCCESS: Backup created: $BACKUP_DIR/backup-$TIMESTAMP.tar.gz ($(du -h "$BACKUP_DIR/backup-$TIMESTAMP.tar.gz" | cut -f1))" | tee -a "$LOG_FILE"

else   
    echo "$(date '+%Y-%m-%d %H:%M:%S') ERROR: Backup failed" | tee -a "$LOG_FILE"
    exit 1
fi


# Remove backups older than 7 days
echo "$(date '+%Y-%m-%d %H:%M:%S') INFO: Cleaning up backups older than 7 days" | tee -a "$LOG_FILE"

find "$BACKUP_DIR" \
	-type f \
	-name 'backup-*.tar.gz' \
	-mtime +7 \
	-print \
	-delete >> "$LOG_FILE" 2>&1

echo "$(date '+%Y-%m-%d %H:%M:%S') INFO: Backup clean completed" | tee -a "$LOG_FILE"
