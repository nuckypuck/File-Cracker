"""
PDF cracker — stub
MDX Cyber Security Society

Install dependency:
    pip install pikepdf

Output protocol (same for all crackers):
    PROGRESS:<n>/<total>
    SUCCESS:<password>
    FAILED
    ERROR:<message>
"""

import argparse
import sys

import pikepdf


def crack(file_path: str, wordlist_path: str) -> None:
    try:
        with open(wordlist_path, "r", encoding="latin-1") as f:
            passwords = [line.rstrip("\n") for line in f]
    except FileNotFoundError:
        print(f"ERROR:Wordlist not found: {wordlist_path}")
        sys.exit(1)

    try:
        with pikepdf.open(file_path):
            print("SUCCESS:", flush=True)
            sys.exit(0)
    except FileNotFoundError:
        print(f"ERROR:PDF not found: {file_path}", flush=True)
        sys.exit(1)
    except pikepdf.PasswordError:
        pass
    except Exception as exc:
        print(f"ERROR:{exc}", flush=True)
        sys.exit(1)

    total = len(passwords)

    for i, password in enumerate(passwords, start=1):
        if i % 200 == 0:
            print(f"PROGRESS:{i}/{total}", flush=True)

        try:
            with pikepdf.open(file_path, password=password):
                print(f"SUCCESS:{password}", flush=True)
                sys.exit(0)
        except pikepdf.PasswordError:
            continue
        except Exception as exc:
            print(f"ERROR:{exc}", flush=True)
            sys.exit(1)

    if total and total % 200 != 0:
        print(f"PROGRESS:{total}/{total}", flush=True)

    print("FAILED", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PDF password cracker")
    parser.add_argument("--file",     required=True, help="Path to locked PDF")
    parser.add_argument("--wordlist", required=True, help="Path to wordlist (.txt)")
    args = parser.parse_args()
    crack(args.file, args.wordlist)
