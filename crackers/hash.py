"""
Hash cracker — stub
MDX Cyber Security Society

Quick note on the hash file: it contains the MD5 hash of 123 rather than the plaintext. The hash cracker stub already has a detect_algorithm function that works out it's MD5 from the length, so you just need to implement the hashlib loop.

Drop a .txt file containing a single hash on one line.
Supported formats (once implemented): MD5, SHA1, SHA256

No external dependencies — uses Python's built-in hashlib.

Output protocol (same for all crackers):
    PROGRESS:<n>/<total>
    SUCCESS:<password>
    FAILED
    ERROR:<message>

How to generate a test hash:
    python -c "import hashlib; print(hashlib.md5(b'password123').hexdigest())"
"""

import argparse
import hashlib
import sys


def detect_algorithm(hash_str: str) -> str | None:
    """Return the likely hash algorithm based on string length."""
    length_map = {
        32:  "md5",
        40:  "sha1",
        64:  "sha256",
        128: "sha512",
    }
    return length_map.get(len(hash_str))


def crack(file_path: str, wordlist_path: str) -> None:
    try:
        with open(file_path, "r") as f:
            target_hash = f.read().strip().lower()
    except FileNotFoundError:
        print(f"ERROR:File not found: {file_path}")
        sys.exit(1)

    algorithm = detect_algorithm(target_hash)
    if algorithm is None:
        print("ERROR:Unrecognised hash length. Supported: MD5 (32), SHA1 (40), SHA256 (64), SHA512 (128)")
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

        # TODO: hash the candidate password using the detected algorithm
        #       and compare it to target_hash.
        #
        # Example for MD5:
        #   candidate = hashlib.md5(password.encode()).hexdigest()
        #   if candidate == target_hash:
        #       print(f"SUCCESS:{password}", flush=True)
        #       sys.exit(0)
        #
        # Hint: hashlib.new(algorithm, password.encode()).hexdigest()
        #       works for any algorithm in the length_map above.

        pass  # remove this once implemented

    print("FAILED", flush=True)
    sys.exit(0)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hash cracker")
    parser.add_argument("--file",     required=True, help="Path to .txt file containing the hash")
    parser.add_argument("--wordlist", required=True, help="Path to wordlist (.txt)")
    args = parser.parse_args()
    crack(args.file, args.wordlist)
