from datetime import datetime
import os, zipfile, pathlib, stat
import zipapp
import time

class ziplink:

    MODE_MASK = 0xF000

    def extractall(z: zipfile.ZipFile, root: str = None):
        for zi in z.infolist():
            xa = zi.external_attr >> 16
            #  print(f"name {zi.filename} size {zi.file_size} attr {zi.internal_attr:08x} xattr {zi.external_attr:08x} fmt {xa & ziplink.MODE_MASK:08x}")
            
            if stat.S_ISLNK(xa):
                f = os.path.join(root, zi.filename)
                s = z.read(zi).decode('utf-8')
                if os.path.exists(f):
                    os.remove(f)
                os.symlink(s, f)
            else:
                z.extract(zi, root)

    def write(z: zipfile.ZipFile, file: str, arcname: str = None):
        st:os.stat_result = os.stat(file, follow_symlinks=False)

        zi = zipfile.ZipInfo.from_file(file, arcname)
        zi.external_attr = (st.st_mode & 0xFFFF) << 16
        if stat.S_ISLNK(st.st_mode):
            s = os.readlink(file)
            z.writestr(zi, s, compress_type=z.compression, compresslevel=z.compresslevel)
        else:
            z.write(file, arcname)

    # zip path will be stored into the archive and root will be not, it will be stripped
    # zipsrc is a folder with optional mask (default is all files)
    def addfolder(z: zipfile.ZipFile, zipsrc: pathlib.Path, root: pathlib.Path = None):

        g = pathlib.Path() / zipsrc

        mask = '*'
        if not g.is_dir():
            mask = g.name
            g = g.parent

        for q in g.parts: 
            ziplink.write(z, q)

        if root:
            g = root / g
        for x in g.rglob(mask):
            arcname = x.relative_to(root) if root else x
            # print(f"store '{x}' as '{arcname}'")
            ziplink.write(z, x, arcname)

def main():
    s = pathlib.Path('tests')
    with zipfile.ZipFile("zz.zip", mode="w") as z:
        for file_path in s.rglob("*"):
            ziplink.write(z, file_path)

    with zipfile.ZipFile("T_z1.zip", mode="w") as z:
        ziplink.addfolder(z, 'tests/*')
    with zipfile.ZipFile("T_z2.zip", mode="w") as z:
        ziplink.addfolder(z, '*', 'tests')

    with zipfile.ZipFile('zz.zip') as z:
        ziplink.extractall(z, '__out_zz')

    pass

# To run tests, launch 'python3 -m doctest ziplink.py'
if __name__ == "__main__":
    main()
