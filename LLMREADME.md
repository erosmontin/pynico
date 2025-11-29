# pynico - LLM Developer Reference

**AI Assistant Guide**: This document provides structured information about the `pynico` package optimized for code generation and assistance.

## Package Import

```python
from pynico import pynico as me
```

**Convention**: The package is typically imported as `me` by the author.

---

## Core Classes and Methods

### 1. `Pathable` - Path Manipulation

**Purpose**: Object-oriented path handling with intelligent file/directory detection and transformation tracking.

**Creation**:
```python
path = me.Pathable("/path/to/file.tar.gz")
```

**Key Characteristics**:
- Uses internal stack to track path changes (supports undo/reset)
- Automatically detects file vs directory based on extension
- Handles multi-part extensions correctly (e.g., `.tar.gz`)

#### Essential Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `getPosition()` | str | Current full path |
| `getPath()` | str | Directory portion only |
| `getBaseName()` | str | Filename with extension |
| `getFileName()` | str | Filename without extension |
| `getExtension()` | str | Extension (e.g., "tar.gz") |
| `isFile()` | bool | True if path has extension or file exists |
| `isDir()` | bool | True if no extension or directory exists |
| `exists()` | bool | True if path exists on filesystem |

#### Path Transformation Methods

```python
# Change components
path.changePath("/new/directory")          # Move to new directory
path.changeBaseName("newfile.txt")         # Set new basename
path.changeFileName("newname")             # Change name, keep extension
path.changeExtension("json")               # Change extension

# Add modifications
path.addPrefix("backup_")                  # Prepend to filename
path.addSuffix("_v2")                      # Append to filename
path.appendPath("subdir")                  # Add subdirectory to path
path.appendPathRandom()                    # Add random UUID subdirectory

# Special operations
path.changeBaseNameSafe()                  # Generate random UUID filename
path.ensureDirectoryExistence()            # Create parent directories (mkdir -p)
path.touch()                               # Create empty file

# Undo/Reset
path.undo()                                # Revert last change
path.reset()                               # Revert to original path
```

#### File Discovery Methods

```python
# Find files
path.getFilesInPathByExtension("json")                    # All .json in directory
path.getFilesInPathByExtensionAndPattern("log_*", "txt")  # Filtered by pattern
path.getFilesInPathByPattern("*.csv")                     # Glob pattern
path.getDirectoriesInPath(recursive=False)                # List subdirectories

# All return sorted lists by default (sort=True parameter)
```

#### File Operations

```python
path.readJson()           # Load JSON from file
path.writeJson(data)      # Save data as JSON
path.readPkl()            # Load pickle file
path.writePkl(data)       # Save as pickle
path.unTar()              # Extract tar archive
path.unTarGz()            # Extract tar.gz archive
path.getMiMEFileType()    # Get MIME type tuple
path.getFileType()        # Get type category ("image", "text", etc.)
```

---

### 2. `Log` - Operation Logging

**Purpose**: Timestamped logging with namespace support for merging multiple log sources.

**Creation**:
```python
log = me.Log("Initial message", settings={"author": "Name"})
```

**Structure**: Each log entry is a dict with:
- `when`: Timestamp string (default format: "DD/MM/YYYY, HH:MM:SS")
- `what`: Message content
- `type`: Category (default: "procedure", or "ERROR", "start", etc.)
- `settings`: Optional metadata dict
- `log_name`: Optional namespace (added by `mergeLog`)

#### Core Methods

```python
# Add entries
log.append("Message", type="info", settings={"key": "value"})
log.appendError("Error occurred")  # Automatically uses ERROR type

# Merge logs with namespaces
log.mergeLog(other_log, log_name="subsystem")  # Tag all entries
log.mergeLog("log.json", log_name="external")  # From file
log.mergeLog([entry1, entry2], log_name="raw")  # From list

# Retrieve entries
all_entries = log.getLog()                      # All entries
filtered = log.getLog(log_name="subsystem")     # Specific namespace
namespaces = log.getLogNames()                  # List of namespaces

# Display
log.printWhatHappened()                         # Print all
log.printWhatHappened(log_name="subsystem")     # Print filtered

# Persistence
log.writeLogAs("output.json")  # Save to file
log.saveLogAs("output.json")   # Alias
log.dump()                     # Save to default temp location
```

**Time Format Customization**:
```python
log.setTimeFormat("%Y-%m-%d %H:%M:%S")
```

**Use Case - Multi-Component Application**:
```python
main = me.Log("App started")

db_log = me.Log("DB init")
db_log.append("Connected")
db_log.append("Schema loaded")

api_log = me.Log("API init")
api_log.append("Server started")

main.mergeLog(db_log, log_name="database")
main.mergeLog(api_log, log_name="api")

# Later: retrieve only database operations
db_ops = main.getLog(log_name="database")
```

---

### 3. `GarbageCollector` - Automatic Cleanup

**Purpose**: Manage temporary files/directories with automatic deletion on destruction.

**Creation**:
```python
gc = me.GarbageCollector()
gc.setForce()  # Enable force deletion (chmod + delete)
```

**Methods**:
```python
gc.throw(path)     # Add to deletion queue
gc.append(path)    # Alias for throw
gc.peek()          # View top item without removing
gc.undo()          # Remove and return top item
gc.trash()         # Delete all queued items immediately
len(gc)            # Number of queued items
```

**Automatic Cleanup**:
```python
def process_data():
    gc = me.GarbageCollector()
    temp = me.createRandomTemporaryPathableFromFileName("data.json")
    gc.throw(temp.getPosition())
    
    # Do work...
    temp.writeJson(data)
    
    # Automatic deletion when gc goes out of scope
```

**Force Mode**: Use `SudoGarbageCollector()` for automatic force mode (attempts chmod before deletion).

---

### 4. `Timer` - Performance Tracking

**Purpose**: Multi-stop timer for measuring operation durations.

**Creation and Usage**:
```python
timer = me.Timer()
timer.start("Phase 1")  # Optional message

# Do work...
timer.stop("Completed phase 1")

# More work...
timer.stop("Completed phase 2")

# Retrieve results
times = timer.getStops()  # List of {"time": float, "message": str}
timer.show()              # Print all stops
timer.toJson("times.json")  # Save with header
```

**Statistics** (if times are numeric):
```python
avg_time = timer.avg()
total_time = timer.sum()
```

---

### 5. `Stack` - LIFO Data Structure

**Purpose**: Linked-list based stack used internally by Pathable and GarbageCollector.

```python
stack = me.Stack()
stack.push(value)
value = stack.pop()    # Raises IndexError if empty
value = stack.peek()   # Raises IndexError if empty
size = stack.size()
size = len(stack)      # Same as size()
```

---

## Utility Functions

### File Operations

```python
# Secure copy with MD5 verification
result = me.securecopy(
    "source.dat", 
    "dest.dat",
    max_attempts=4,           # Retry count
    md5="precomputed_hash",   # Optional
    delete_after_copy=False,  # Move instead of copy
    follow_symlinks=False
)
# Returns: {"status": "ok"|"error", "message": str, "md5": str}

# MD5 calculation (chunked for large files)
hash_value = me.calculateMd5("file.dat", chunk_size=8192)

# JSON operations (with sanitization)
data = me.readJson("file.json")
me.writeJsonFile("file.json", data)  # Auto-sanitizes non-serializable types

# CSV operations
rows = me.readCsv("data.csv")  # Returns List[List[str]]

# Pickle operations
data = me.readPkl("data.pkl")
me.writePkl("data.pkl", data)  # Auto-wraps non-list in list
```

### Temporary File Helpers

```python
# Create temporary Pathable objects
temp = me.createTemporaryPathableFromFileName("data.json")
# Path: /tmp/data.json (or OS temp dir)

temp = me.createRandomTemporaryPathableFromFileName("data.json")
# Path: /tmp/data-<uuid>.json

temp_dir = me.createTemporaryPathableDirectory()
# Path: /tmp/<uuid>/ (directory created)
```

### Archive Extraction

```python
me.unTar("archive.tar", extract_path="/dest")      # Extract tar
me.unTarGz("archive.tar.gz", extract_path="/dest") # Extract tar.gz
# If extract_path is None, uses temp directory
```

### Package Version Detection

```python
version = me.getPackageVersion("numpy")  # Returns str or None
versions = me.getPackagesVersion([
    "numpy", "scipy", "pandas"
])
# Returns: {"numpy": "1.24.0", "scipy": "1.10.0", ...}
```

### System Information

```python
info = me.getPlatformInfo()
# Returns dict with: date, os, os_version, machine, processor, 
#                    python_version, hostname, user
```

### Data Type Checking

```python
me.isCollection([1, 2, 3])     # True
me.isCollection("string")      # False (strings excluded)
me.isCollection({1, 2, 3})     # True
me.isCollection(b"bytes")      # False (bytes excluded)
```

### Path Utilities

```python
# Split multi-part extensions
basename, ext = me.splitext_("file.tar.gz")
# Returns: ("file", "tar.gz")

# Deep copy Pathable
new_path = me.forkPathable(existing_path)
```

---

## Class `BashIt` - Shell Command Execution

**Purpose**: Execute shell commands with output capture.

```python
bash = me.BashIt()
bash.setCommand("ls -la /tmp")
bash.run()  # Returns bool

output = bash.getBashOutput()  # bytes
error = bash.getBashError()    # bytes or None
log = bash.Log.getLog()        # Internal log of execution
```

**Note**: Uses `subprocess.Popen` internally; may fall back to shell=True on errors.

---

## Common Patterns

### Pattern 1: Process Files with Cleanup
```python
def process_directory(input_dir):
    gc = me.GarbageCollector()
    log = me.Log("Processing started")
    
    input_path = me.Pathable(input_dir)
    files = input_path.getFilesInPathByExtension("json")
    
    for file in files:
        p = me.Pathable(file)
        temp = me.createRandomTemporaryPathableFromFileName(p.getBaseName())
        gc.throw(temp.getPosition())
        
        # Process...
        data = p.readJson()
        # ... transform data ...
        temp.writeJson(data)
        log.append(f"Processed {p.getBaseName()}")
    
    log.dump()
    # gc automatically cleans up temp files
```

### Pattern 2: Multi-Source Logging
```python
def pipeline():
    main_log = me.Log("Pipeline started")
    
    # Component 1
    extract_log = me.Log("Extract phase")
    # ... extraction work ...
    extract_log.append("Extracted 1000 records")
    
    # Component 2
    transform_log = me.Log("Transform phase")
    # ... transformation work ...
    transform_log.append("Transformed data")
    
    # Merge all logs
    main_log.mergeLog(extract_log, log_name="extract")
    main_log.mergeLog(transform_log, log_name="transform")
    
    # Save comprehensive log
    main_log.writeLogAs("pipeline_log.json")
    
    # Analyze specific component
    if main_log.getLog(log_name="extract"):
        print("Extract phase had entries")
```

### Pattern 3: Safe Path Transformations
```python
def transform_file(input_file, output_dir):
    p = me.Pathable(input_file)
    
    # Build output path safely
    output = p.fork()  # Deep copy
    output.changePath(output_dir)
    output.addSuffix("_processed")
    output.ensureDirectoryExistence()
    
    # If error, undo to try alternative
    if not do_processing(p, output):
        output.undo()
        output.addSuffix("_partial")
    
    return output.getPosition()
```

### Pattern 4: Timed Operations with Logging
```python
def benchmark_operation():
    timer = me.Timer()
    log = me.Log("Benchmark")
    
    timer.start()
    # Phase 1
    result1 = operation1()
    elapsed1 = timer.stop("Phase 1")
    log.append(f"Phase 1: {elapsed1['time']:.3f}s")
    
    # Phase 2
    result2 = operation2()
    elapsed2 = timer.stop("Phase 2")
    log.append(f"Phase 2: {elapsed2['time']:.3f}s")
    
    log.append(f"Total: {timer.sum():.3f}s")
    return log
```

---

## Error Handling Notes

- `Pathable.changeBaseName()` raises `Exception` if name is None (use `changeFileName()` for random)
- `Stack.pop()` and `Stack.peek()` raise `IndexError` when empty
- `Pathable.ensureDirectoryExistence()` raises `Exception` if path is not writable
- File operations (readJson, readPkl, etc.) may raise standard Python I/O exceptions
- `securecopy()` returns status dict instead of raising exceptions

---

## Implementation Details for AI Assistants

1. **Pathable uses a Stack internally**: Each transformation pushes to stack; `undo()` pops; `reset()` clears to first
2. **Extension detection**: Uses custom `splitext_()` that handles multi-dot extensions correctly
3. **Log entries are dicts**: Easy to filter, merge, and serialize
4. **GarbageCollector uses `__del__`**: Automatic cleanup on garbage collection
5. **Timer stores list of dicts**: Each stop appends `{"time": float, "message": str}`
6. **JSON sanitization**: `sanitize_for_json()` recursively converts non-serializable types to strings
7. **MD5 calculation**: Chunked reading for memory efficiency with large files
8. **Package imports**: Prefers `importlib.metadata` over legacy `pkg_resources`

---

## Code Generation Tips

When generating code with pynico:

1. **Always import as `me`**: `from pynico import pynico as me`
2. **Use GarbageCollector for temporary files**: Automatic cleanup prevents leaks
3. **Log with namespaces**: Makes debugging multi-component systems easier
4. **Fork Pathable before transformations**: Preserves original if you need to undo
5. **Call `ensureDirectoryExistence()` before writing**: Avoids missing directory errors
6. **Use `securecopy()` for important files**: MD5 verification catches corruption
7. **Prefer Pathable methods over os.path**: More robust extension handling

---

**Package Philosophy**: Provide simple, composable utilities that handle edge cases gracefully and clean up after themselves automatically.
