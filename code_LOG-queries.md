# ERROR issues of specific host

fetch logs
| filter host.name == "hostname"
| filter timeframe between("2025-03-15T00:00:00", "2025-03-18T00:00:00")
| filter severity == "ERROR"
| sort timestamp desc


or 
| filter contains(content, "exception")

# Known Error patterns
fetch logs
| filter host.name == "hostname"
| filter timeframe between("2025-03-03T00:00:00", "2025-03-18T00:00:00")
| filter severity == "ERROR" or severity == "CRITICAL"
| sort timestamp desc


# Anomalies
fetch logs
| filter host.name == "hostname" 
| filter timeframe between("2025-03-03T00:00:00", "2025-03-18T00:00:00")
| filter contains(content, "exception") or contains(content, "timeout") or contains(content, "failure") or contains(content, "refused")


# HEAVY LOAD
fetch logs
| filter host.name == "hostname" 
| filter timeframe between("2025-03-03T00:00:00", "2025-03-18T00:00:00")
| join dt.entity.process on host.id
| filter dt.entity.process.cpu > 80 or dt.entity.process.memory.used > 90