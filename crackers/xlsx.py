"""
Excel Spreadsheet (.xlsx) cracker — stub
MDX Cyber Security Society

Install dependency:
    pip install msoffcrypto-tool

Uses the same msoffcrypto-tool library as docx.py.
The API is identical — only the file format changes.

Output protocol (same for all crackers):
    PROGRESS:<n>/<total>
    SUCCESS:<password>
    FAILED
    ERROR:<message>

How to create a locked .xlsx for testing:
    Open Excel → File → Info → Protect Workbook → Encrypt with Password
"""

import argparse
import sys

# TODO: import msoffcrypto
# import msoffcrypto


def crack(file_path: str, wordlist_path: str) -> None:
    # TODO: same pattern as docx.py — msoffcrypto handles both formats

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

        # TODO: implement your msoffcrypto attempt here
        pass  # remove this once implemented

    print("FAILED", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="XLSX password cracker")
    parser.add_argument("--file",     required=True, help="Path to locked .xlsx")
    parser.add_argument("--wordlist", required=True, help="Path to wordlist (.txt)")
    args = parser.parse_args()
    crack(args.file, args.wordlist)
