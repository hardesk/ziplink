# ziplink

zipfile wrapper for Python with symlink support

### Example

Unpacking an archive

```python
dest = 'unzipped'
with zipfile.ZipFile('arch.zip') as z:
    ziplinks.extractall(z, dest)
```

Packing
```python
with zipfile.ZipFile('a1.zip', 'w') as z:
    ziplink.addfolder(z, 'x') # add x/* at x/*
    ziplink.addfolder(z, 'y', 'y') # add y/* at zip's root
    ziplink.addfolder(z, 'z', 'z', '*.txt') # add z/* at zip's root, but only .txt files
```

Or, you can add the files one by one
```python
with zipfile.ZipFile('a1.zip', 'w') as z:
    for f in pathlib.Path('.').rglob('*'):
        ziplink.write(z, f, f.name) # junk paths
```
