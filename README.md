# File Cracker

An Electron app that brute-forces password-protected files using a wordlist.

Built by the [MDX Cyber Security Society](https://mdxcyberhub.netlify.app) as a collaborative session project.

---

## How it works

Drop a locked file onto the app, select a wordlist, and hit **Crack File**. The app calls the matching Python cracker script from the `crackers/` folder and streams progress back to the UI.

The ZIP cracker is the working reference implementation. All other file types are stubbed out — that's what you're here to fix.

---

## Setup

**Requirements:** Node.js, Python 3.x

```bash
git clone https://github.com/<your-fork>/file-cracker
cd file-cracker
npm install
npm start
```

---

## Contributing a new cracker

1. Fork this repo
2. Create a branch: `git checkout -b feat/pdf-cracker`
3. Open `crackers/<filetype>.py` and follow the TODO comments
4. Test it: `python crackers/pdf.py --file test.pdf --wordlist wordlist.txt`
5. Update `supported-types.json` — change `"status": "stub"` to `"status": "working"` for your file type
6. Open a PR with a short description of what library you used

### Output protocol

Every cracker must write to stdout in this format so the app can parse it:

| Line | Meaning |
|------|---------|
| `PROGRESS:200/14000` | Tried 200 of 14000 passwords — updates the progress bar |
| `SUCCESS:hunter2` | Password found |
| `FAILED` | Wordlist exhausted, no match |
| `ERROR:some message` | Something went wrong |

See `crackers/zip.py` for a complete working example.

### Adding a new file type entirely

1. Add a new entry to `supported-types.json`
2. Create `crackers/<extension>.py` using the stub template from any existing stub
3. Open a PR

---

## Wordlists

The app works with any plaintext wordlist. A good starting point is `rockyou.txt`, which is included with Kali Linux at `/usr/share/wordlists/rockyou.txt`.

For quick testing, create a short wordlist and put the real password somewhere in the middle.

---

## File types

| Extension | Library | Status |
|-----------|---------|--------|
| `.zip` | `zipfile` (stdlib) | Working |
| `.pdf` | `pikepdf` | Stub |
| `.docx` | `msoffcrypto-tool` | Stub |
| `.xlsx` | `msoffcrypto-tool` | Stub |
| `.txt` | `hashlib` (stdlib) | Stub |

---

MDX Cyber Security Society &mdash; [mdxcyberhub.netlify.app](https://mdxcyberhub.netlify.app)
