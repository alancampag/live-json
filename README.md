# live-json

Read/write json in real time using the python dict interface

![live-json in action gif](https://user-images.githubusercontent.com/56612310/189500026-8c34800d-6880-4bdd-9adc-0ecdd5b3f018.gif)

## Install

```
pip install git+https://github.com/alancampag/live-json
```

## Usage

Import it

```
from live_json import LiveJson
```

Set the path to the json file.

```
LiveJson.path = "test.json"
```

If path isn't set a random name will be used.

Create an instance, If path doesn't exist it will be created:

```
lj = LiveJson()
```

You can pass a dict on initialization:

```
lj = LiveJson({"a": "hello"})
```

If the file already exist, the existing json will be merged new one.

Use like a normal python dict. All items set will be immediately written to disk, lookups will read current value from disk.

Set items:

```
lj["a"] = {"b": ["c", "d"]}
```

Get items:

```
v = lj["a"]
v = lj.get("a")
v = lj.pop("a")
```

Delete items:

```
del lj["a"]
```

Update:

```
lj.update({"a": [1,2,3]})
```

Iterate:

```
for k in lj.keys(): ...
for v in lj.values(): ...
for i in lj.items(): ...
```

Call built-in functions:

```
len(lj)
iter(lj)
str(lj)
repr(lj)
```

### Serialization

All keys and values must be json serializable.

-   int keys will be converted to strings.
-   tuple values will be converted to lists.
-   strings, lists and dicts have json equivalents.
-   Any other type will raise an exception.

### Formatting

By default, the json file will be formatted for better readability.
To save compact json files, set:

```
LiveJson.indent = None
```

You can also set it to an integer for the number of spaces to use.
