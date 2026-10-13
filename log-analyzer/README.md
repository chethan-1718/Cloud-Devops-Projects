# Linux Log Analyzer and Alerting System

## Overview

A Bash-based Linux log analyzer that scans system logs, summarizes errors and warnings, identifies failed SSH login attempts, groups failed logins by source IP address, and generates timestamped reports with threshold-based alerts.

This project uses synthetic log entries for testing and learning.

## Features

- Counts `ERROR`, `WARNING`, and `INFO` log entries.
- Detects failed SSH login attempts.
- Groups failed login attempts by source IP address.
- Supports a configurable alert threshold.
- Validates threshold input.
- Handles a missing log file gracefully.
- Generates timestamped reports and displays results in the terminal.

## Technologies

- Linux / Ubuntu
- Bash scripting
- `grep`, `awk`, `sort`, `uniq`, `wc`, and `tee`
- Git and GitHub

## Project Structure

```text
log-analyzer/
├── scripts/
│   └── analyze-logs.sh
├── logs/
│   └── system.log
├── reports/
└── README.md
```

## How to Run

Run these commands from the `log-analyzer` directory.

Analyze logs using the default threshold of 3:

```bash
bash scripts/analyze-logs.sh
```

Set a custom threshold:

```bash
bash scripts/analyze-logs.sh 5
```

View generated reports:

```bash
ls -lt reports/
```

## Example Use Cases

- Investigating repeated failed SSH login attempts.
- Summarizing error and warning messages.
- Identifying source IPs associated with failed logins.
- Practicing basic Linux log analysis and Bash automation.

## Limitations

- The included log file contains synthetic sample data, not actual security incidents.
- The script analyzes the specified log file; it does not continuously monitor logs.
- Alerts are written to the report and terminal; email or external notification integration is not included.

## Future Improvements

- Support common Linux authentication log formats.
- Add automated tests and optional email notifications.
- Schedule analysis with cron.

## Learning Outcomes

Practiced Bash scripting, command-line arguments, input validation, text processing, pipelines, file handling, exit codes, and report generation.
