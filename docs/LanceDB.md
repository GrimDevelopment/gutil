# LanceDB Integration

gutil provides a minimal LanceDB helper and CLI commands for simple local data workflows.

## Install

```sh
pip install lancedb
```

Alternatively, include `lancedb` in your environment by installing from the project’s `requirement.txt`.

## CLI

List tables:

```sh
python -m gutil lancedb list ./data/mydb
```

Create a table from a JSON file (object or array of objects):

```sh
python -m gutil lancedb create ./data/mydb events ./seed/events.json
```

Query rows (printed as JSON lines):

```sh
python -m gutil lancedb query ./data/mydb events --limit 5
```

## Library API

```python
from gutil.LanceDB import LanceDBClient

client = LanceDBClient("./data/mydb")
print(client.list_tables())

# Create a table
client.create_table("events", [{"id": 1, "name": "start"}], exist_ok=True)

# Insert rows
client.insert("events", [{"id": 2, "name": "stop"}])

# Query
rows = client.query("events", limit=10)
```

Behavior:
- Library raises precise exceptions; the CLI reports errors and returns non-zero exit codes.
- JSON helpers accept either an object or an array of objects.

