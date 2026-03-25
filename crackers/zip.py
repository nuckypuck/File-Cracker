"""
ZIP cracker — reference implementation
MDX Cyber Security Society

Usage:
    python zip.py --file <path/to/locked.zip> --wordlist <path/to/wordlist.txt>

Output protocol (read by the Electron app):
    PROGRESS:<n>/<total>   — printed every 200 attempts
    SUCCESS:<password>     — password found, script exits
    FAILED                 — wordlist exhausted, no match
    ERROR:<message>        — something went wrong
"""

import zipfile
import argparse
import sys


def crack(file_path: str, wordlist_path: str) -> None:
    try:
        zf = zipfile.ZipFile(file_path)
    except zipfile.BadZipFile:
        print("ERROR:Not a valid ZIP file.")
        sys.exit(1)
    except FileNotFoundError:
        print(f"ERROR:File not found: {file_path}")
        sys.exit(1)

    try:
        with open(wordlist_path, "r", encoding="latin-1") as f:
            passwords = [line.rstrip("\n") for line in f]
    except FileNotFoundError:
        print(f"ERROR:Wordlist not found: {wordlist_path}")
        sys.exit(1)

    total = len(passwords)

    for i, password in enumerate(passwords):
        if i % 200 == 0:
            print(f"PROGRESS:{i}/{total}", flush=True)

        try:
            zf.extractall(pwd=password.encode("latin-1"))
            print(f"SUCCESS:{password}", flush=True)
            zf.close()
            sys.exit(0)
        except (RuntimeError, zipfile.BadZipFile):
            continue
        except Exception as e:
            print(f"ERROR:{e}", flush=True)
            sys.exit(1)

    zf.close()
    print("FAILED", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ZIP password cracker")
    parser.add_argument("--file",     required=True, help="Path to locked ZIP")
    parser.add_argument("--wordlist", required=True, help="Path to wordlist (.txt)")
    args = parser.parse_args()
    crack(args.file, args.wordlist)
