#!/usr/bin/env python
"""Demo script showing how to merge logs with namespaces."""

from pynico import pynico as me

# Create the main log
main_log = me.Log("Main application started")

# Create a log for database operations
db_log = me.Log("Database connection established")
db_log.append("Query executed: SELECT * FROM users")
db_log.append("Query executed: INSERT INTO logs")
db_log.append("Database connection closed")

# Create a log for API operations
api_log = me.Log("API server started")
api_log.append("Received GET /users request")
api_log.append("Received POST /data request")
api_log.appendError("Failed to process request - timeout")

# Merge both logs into the main log with namespaces
main_log.append("Starting database operations")
main_log.mergeLog(db_log, log_name="database")

main_log.append("Starting API operations")
main_log.mergeLog(api_log, log_name="api")

main_log.append("All operations completed")

print("=" * 70)
print("ALL LOG ENTRIES:")
print("=" * 70)
main_log.printWhatHappened()

print("\n" + "=" * 70)
print("ONLY DATABASE LOG ENTRIES:")
print("=" * 70)
main_log.printWhatHappened(log_name="database")

print("\n" + "=" * 70)
print("ONLY API LOG ENTRIES:")
print("=" * 70)
main_log.printWhatHappened(log_name="api")

print("\n" + "=" * 70)
print("AVAILABLE LOG NAMES:")
print("=" * 70)
print(main_log.getLogNames())

print("\n" + "=" * 70)
print("GET DATABASE LOG AS LIST:")
print("=" * 70)
db_entries = main_log.getLog(log_name="database")
for entry in db_entries:
    print(f"  [{entry.get('when')}] {entry.get('what')}")
