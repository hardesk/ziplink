# ziplink

zipfile wrapper for Python with symlink support

### Example

Unpacking an archive

```python
dest = 'unzipped' # it's optional
with zipfile.ZipFile('arch.zip') as z:
    ziplinks.extractall(z, dest)
```
Packing

```python
with zipfile.ZipFile('a1.zip', 'w') as z:
    ziplink.addfolder(z, 'x/*') # add x/* at x/*
    ziplink.addfolder(z, '*', 'y') # add x/* at *
```

Or, you can add file one by one
```python
with zipfile.ZipFile('a1.zip', 'w') as z:
    for f in pathlib.Path('.').rglob('*'):
        ziplink.write(f, f.name) # junk paths
```
