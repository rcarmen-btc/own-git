from importlib.resources import path
import sys
import os
import zlib
import hashlib

from numpy import size


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
            with open(file_name, 'r') as f:
                data = f.read()
            header = f"blob {len(data.encode('utf-8'))}\0"
            store = header + data

            sha1 = hashlib.sha1(store.encode()).hexdigest()
            print(sha1)

            dir_name = sha1[:2]
            file_name = sha1[2:]
            path_to_dir = f'.git/objects/{dir_name}/'
            try:
                os.mkdir(path_to_dir)
                zlib_content = zlib.compress(store.encode())
                with open(path_to_dir + file_name, 'wb') as f:
                    f.write(zlib_content)
            except FileExistsError:
                pass
    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
