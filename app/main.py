from ftplib import error_perm
from pkgutil import iter_modules
import sys
import os
import zlib
import hashlib

class Tree:
    
    def __init__(self, path) -> None:
        arr = os.listdir(path)
        if '.git' in arr:
            arr.remove('.git')
        if '__pycache__' in arr:
            arr.remove('__pycache__')
        store = {
            'blobs': {
                
            },
            'trees': {
                
            }
        }
        for item in arr:
            isFile = os.path.isfile(os.path.join(path, item))
            if isFile:
                store['blobs'][item] = hash_object(os.path.join(path, item))
            else:
                store['trees'][item] = Tree(os.path.join(path, item))

        data = ""
        for key, val in store['blobs'].items():
            data += f"100644 {key}\0{val.encode()}"
        for key, val in store['trees'].items():
            data += f"040000 {key}\0{val.sha.encode()}"
        
        header = f"tree {len(data.encode('utf-8')) + 1000}\0"

        store = header + data

        sha1 = hashlib.sha1(store.encode()).hexdigest()

        self.sha = sha1

        dir_name = sha1[:2]
        file_name = sha1[2:]
        path_to_dir = f'.git/objects/{dir_name}/'
        try:
            os.mkdir(path_to_dir)
        except FileExistsError:
            pass
        zlib_content = zlib.compress(store.encode())
        with open(path_to_dir + file_name, 'wb') as f:
            f.write(zlib_content)
    
    def __str__(self):
        return self.sha


def hash_object(file_name: str):
    with open(file_name, 'r') as f:
        data = f.read()
    header = f"blob {len(data.encode('utf-8'))}\0"
    store = header + data

    sha1 = hashlib.sha1(store.encode()).hexdigest()

    dir_name = sha1[:2]
    file_name = sha1[2:]
    path_to_dir = f'.git/objects/{dir_name}/'
    try:
        os.mkdir(path_to_dir)
    except FileExistsError:
        pass
    zlib_content = zlib.compress(store.encode())
    try:
        with open(path_to_dir + file_name, 'wb') as f:
            f.write(zlib_content)
    except PermissionError:
        pass
    return sha1

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    # print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")

        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/master\n")
        print("Initialized git directory")
    elif command == "cat-file":
        if  sys.argv[2] == "-p":
            sha1 = sys.argv[3]
            dir_name = sha1[:2]
            file_name = sha1[2:]
            with open(f'.git/objects/{dir_name}/{file_name}', 'rb') as f:
                data = f.read()
                decomp_data = zlib.decompress(data).split(b'\x00')[1].decode("utf-8")
                print(decomp_data, end="")
    elif command == "hash-object":
        if sys.argv[2] == "-w":
            file_name = sys.argv[3]
            print(hash_object(file_name))
    elif command == "ls-tree":
        if sys.argv[2] == "--name-only":
            tree_sha1 = sys.argv[3]
            dir_name = tree_sha1[:2]
            file_name = tree_sha1[2:]
            with open(f'.git/objects/{dir_name}/{file_name}', 'rb') as f:
                data = f.read()
                for i in range(2, len(zlib.decompress(data).split(b' '))):
                    decomp_data = zlib.decompress(data).split(b' ')[i].split(b'\0')[0].decode()
                    print(decomp_data)
    elif command == "write-tree":
        tree = Tree('.')
        print(tree)
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
