import os, zipfile, stat
import pathlib
import logging

class ziplink:

    MODE_MASK = 0xF000

    def extractall(z: zipfile.ZipFile, root: str = None):
        for zi in z.infolist():
            xa = zi.external_attr >> 16
            # logging.debug(f"name {zi.filename} size {zi.file_size} attr {zi.internal_attr:08x} xattr {zi.external_attr:08x} fmt {xa & ziplink.MODE_MASK:08x}")
            
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

    # zipsrc path will be stored into the archive with the 'zipcwd' prefix stripped if specified
    # default mask is all files/folders
    def addfolder(z: zipfile.ZipFile, zipsrc, zipcwd=None, mask: str=None):

        g = zipsrc if isinstance(zipsrc, os.PathLike) else pathlib.Path(zipsrc)
        if zipcwd and not isinstance(zipcwd, os.PathLike): zipcwd = pathlib.Path(zipcwd)

        mask = mask if mask else '*'

        if os.path.exists(g):
            if os.path.isfile(g):
                mask = g.name
                g = g.parent
        else:
            # logging.debug(f"path {g} -> {g.absolute()} not found")
            raise RuntimeError(f"{g} was not found or is not a directory")

        for x in g.rglob(mask):
            arcname = x.relative_to(zipcwd) if zipcwd else x
            # logging.debug(f"store '{x}' as '{arcname}'")
            ziplink.write(z, x, arcname)

def main():

    logging.basicConfig(level=logging.DEBUG)

    s = pathlib.Path('tests')
    with zipfile.ZipFile("zz.zip", mode="w") as z:
        for file_path in s.rglob("*"):
            ziplink.write(z, file_path)

    with zipfile.ZipFile("T_z1.zip", mode="w") as z:
        ziplink.addfolder(z, 'tests')
    with zipfile.ZipFile("T_z2.zip", mode="w") as z:
        ziplink.addfolder(z, 'tests', 'tests')
    with zipfile.ZipFile("T_z3.zip", mode="w") as z:
        ziplink.addfolder(z, 'tests', None, '*')
    with zipfile.ZipFile("T_z4.zip", mode="w") as z:
        ziplink.addfolder(z, 'tests', None, '*.txt')

    with zipfile.ZipFile('zz.zip') as z:
        ziplink.extractall(z, '__out_zz')

    pass

# To run tests, launch 'python3 -m doctest ziplink.py'
if __name__ == "__main__":
    main()
