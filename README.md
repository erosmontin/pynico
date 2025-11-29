# pynico

A Python utility package designed to simplify common file operations, logging, path manipulation, and system tasks.

## Overview

`pynico` provides a collection of practical utilities that streamline everyday Python development tasks. Whether you're managing file paths, tracking operations with logs, executing shell commands, or handling temporary files, pynico offers clean, robust abstractions to make your code more maintainable.

## Key Features

### 🗂️ Path Management (`Pathable`)
- **Intelligent path handling** with automatic file/directory detection
- **Multi-extension support** (e.g., `file.tar.gz` handled correctly)
- **Undo/reset capabilities** for path transformations
- **Safe filename generation** with UUID-based randomization
- **Extension manipulation** (add prefix/suffix, change extensions)
- **Glob pattern matching** with built-in sorting
- **MIME type detection**

### 📝 Logging (`Log`)
- **Timestamped log entries** with customizable formats
- **Log merging with namespaces** - combine multiple logs and filter by source
- **JSON export/import** for log persistence
- **Error tracking** with dedicated error append methods
- **Retrieve logs by namespace** for multi-component applications

### 🗑️ Garbage Collection (`GarbageCollector`)
- **Automatic cleanup** on object destruction
- **Stack-based deletion queue**
- **Force deletion** for permission-restricted files
- **Safe file/directory removal** with error handling

### ⏱️ Timing (`Timer`)
- **Multi-stop timer** for performance tracking
- **Automatic statistics** (avg, sum)
- **JSON export** with custom headers
- **Message tagging** for each stop

### 🛠️ Utility Functions
- **Secure file copying** with MD5 verification and automatic retries
- **JSON/CSV/Pickle** read/write helpers with sanitization
- **Package version detection** for dependency tracking
- **Shell command execution** (`BashIt` class)
- **Tar/TarGz extraction** helpers
- **Platform information** gathering

## Installation

```bash
pip install pynico
```

## Quick Start

```python
from pynico import pynico as me

# Path manipulation
path = me.Pathable("/data/project/file.tar.gz")
print(path.getFileName())      # "file"
print(path.getExtension())     # "tar.gz"
path.addSuffix("_backup")      # "/data/project/file_backup.tar.gz"

# Logging with namespaces
main_log = me.Log("Application started")
db_log = me.Log("Database connected")
db_log.append("Query executed")

main_log.mergeLog(db_log, log_name="database")
main_log.printWhatHappened(log_name="database")  # Filter by namespace

# Automatic cleanup
gc = me.GarbageCollector()
temp_file = me.createRandomTemporaryPathableFromFileName("data.json")
gc.throw(temp_file.getPosition())
# File automatically deleted when gc is destroyed

# Secure file operations
result = me.securecopy("source.dat", "dest.dat", max_attempts=3, 
                       delete_after_copy=True)
print(result)  # {"status": "ok", "message": "file copied", "md5": "..."}

# Timing operations
timer = me.Timer()
# ... do work ...
timer.stop("Phase 1 complete")
# ... more work ...
timer.stop("Phase 2 complete")
timer.show()  # Print all stops
```

## Documentation

For detailed API documentation and examples, see [LLMREADME.md](LLMREADME.md) - optimized for AI assistants and developers.

## Use Cases

- **Data processing pipelines** - Track operations, manage temporary files
- **Scientific computing** - Organize results, log experiments
- **File conversion tools** - Handle multi-extension formats safely
- **Automation scripts** - Execute commands, verify file integrity
- **Multi-component applications** - Merge logs from different subsystems

## Requirements

- Python 3.7+
- Standard library only (no external dependencies)

## Author

[*Dr. Eros Montin, PhD*](http://me.biodimensional.com)

**46&2 just ahead of me!**
