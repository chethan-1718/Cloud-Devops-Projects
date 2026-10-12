# Linux Server Monitoring and Automated Backup System

A Bash-based Linux project that monitors system resource usage, creates compressed backups, manages backup retention, and records activity in log files.

## Features

- **Disk monitoring:** Checks root filesystem usage against an 80% threshold.
- **Memory monitoring:** Checks memory usage against an 80% threshold.
- **CPU monitoring:** Checks system load average against the number of available CPU cores.
- **Automated backups:** Creates timestamped, compressed `.tar.gz` archives.
- **Backup verification:** Checks whether generated archives can be listed successfully.
- **Retention policy:** Removes backup archives older than the configured retention period.
- **Logging:** Records monitoring results, backup successes, failures, and cleanup activity.
- **Cron scheduling:** Automates periodic monitoring and daily backups.

## Technologies Used

- Linux (Ubuntu on WSL)
- Bash scripting
- Cron
- `tar`, `find`, `df`, `free`, `date`, and `du`
- Vim

## Project Structure

```text
server-monitor/
├── scripts/
│   ├── disk-monitor.sh
│   └── backup.sh
├── logs/
│   ├── disk-monitor.log
│   └── backup.log
├── backups/
├── backup_source/
├── retention-test/
└── README.md
```

## Setup

Clone the repository and enter the project directory:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd server-monitor
```

Make the scripts executable:

```bash
chmod +x scripts/disk-monitor.sh scripts/backup.sh
```

Create the required directories:

```bash
mkdir -p logs backups backup_source
```

Add files you want to back up to `backup_source/`.

## Run the Scripts

Run the monitoring script:

```bash
./scripts/disk-monitor.sh
```

Run the backup script:

```bash
./scripts/backup.sh
```

View the logs:

```bash
tail -n 20 logs/disk-monitor.log
tail -n 20 logs/backup.log
```

List generated backup archives:

```bash
ls -lh backups/
```

## Cron Scheduling

Example crontab entries:

```cron
*/5 * * * * /home/username/devops-projects/server-monitor/scripts/disk-monitor.sh
0 20 * * * /home/username/devops-projects/server-monitor/scripts/backup.sh
```

These entries run monitoring every five minutes and schedule backups daily at 8 PM, using the system's local time.

Edit scheduled jobs with:

```bash
crontab -e
```

**Note:** When running under WSL, scheduled jobs require the WSL environment to be running and the cron service to be active.

## Backup Retention

The backup script uses `find` to identify and delete matching archives beyond the configured retention threshold.

Example cleanup command:

```bash
find "$BACKUP_DIR" \
  -type f \
  -name 'backup-*.tar.gz' \
  -mtime +7 \
  -print \
  -delete
```

Test cleanup behavior in a separate test directory before applying deletion commands to real backups.

## Testing

- Executed the disk monitoring script and checked its logs.
- Ran the backup script and verified that timestamped archives were created.
- Tested error handling for a missing source directory.
- Created an old test archive and verified that the retention command deleted it.

## Learning Outcomes

This project provides hands-on practice with Bash scripting, Linux system administration, cron scheduling, file permissions, log management, compressed archives, error handling, and automated cleanup.

## Future Improvements

- Send alerts when disk or memory usage exceeds configured thresholds.
- Add configurable retention settings.
- Add automated tests and CI checks.
- Improve backup integrity checks and failure handling.
- Add a dry-run mode for retention cleanup.
