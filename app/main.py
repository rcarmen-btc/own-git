import sys
import os
import zlib


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this block to pass the first stage
    #
    command = sys.argv[1]
    if command == "init":
        os.mkdir(".git")
        os.mkdir(".git/objects")
        os.mkdir(".git/refs")
        with open(".git/HEAD", "w") as f:
            f.write("ref: refs/heads/master\n")
        print("Initialized git directory")
    if command == "cat-file" and sys.argv[2] == "-p":
        sha1 = sys.argv[3]
        dir_name = sha1[:2]
        file_name = sha1[2:]
        with open(f'.git/objects/{dir_name}/{file_name}', 'rb') as f:
            data = f.read()
            decomp_data = zlib.decompress(data).decode("utf-8")
            print(decomp_data, end="")


    else:
        raise RuntimeError(f"Unknown command #{command}")


if __name__ == "__main__":
    main()
