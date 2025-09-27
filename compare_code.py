# Homework 6.1 – Dynamic Programming & LCS: "Did we copy?"
# This script compares two text files:
#   1) web_code.txt  -> code copied from websites (LCS + Edit Distance)
#   2) my_code.txt   -> the version we edited/extended in class

import os

# ---------- helpers to read and clean code ----------
def read_lines(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return [ln.rstrip("\n\r") for ln in f]

def normalize_line(ln):
    
    # remove trailing and leading spaces
    s = ln.strip()
    # remove full-line comments and empty lines
    if s.startswith("#") or s == "":
        return ""
    return s

def cleaned_lines(lines):
    out = []
    for ln in lines:
        n = normalize_line(ln)
        if n:
            out.append(n)
    return out

# ---------- DP: LCS length on sequences of lines ----------
def lcs_len(a, b):
    n, m = len(a), len(b)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(1, n+1):
        for j in range(1, m+1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[n][m]

# ---------- DP: Edit distance on characters ----------
def edit_distance_chars(s, t):
    n, m = len(s), len(t)
    dp = [[0]*(m+1) for _ in range(n+1)]
    for i in range(n+1):
        dp[i][0] = i
    for j in range(m+1):
        dp[0][j] = j
    for i in range(1, n+1):
        for j in range(1, m+1):
            cost = 0 if s[i-1] == t[j-1] else 1
            dp[i][j] = min(
                dp[i-1][j] + 1,      # delete
                dp[i][j-1] + 1,      # insert
                dp[i-1][j-1] + cost  # substitute
            )
    return dp[n][m]

# ---------- metrics ----------
def exact_line_overlap(my_lines, web_lines):
    web_set = set(web_lines)
    match = sum(1 for ln in my_lines if ln in web_set)
    pct = (match / max(1, len(my_lines))) * 100.0
    return match, pct

def lcs_similarity(my_lines, web_lines):
    L = lcs_len(my_lines, web_lines)
    # ratio against my file so it reads like "how much of my file aligns with web"
    ratio = (L / max(1, len(my_lines))) * 100.0
    return L, ratio

def edit_similarity(my_text, web_text):
    dist = edit_distance_chars(my_text, web_text)
    max_len = max(1, max(len(my_text), len(web_text)))
    sim = (1.0 - dist / max_len) * 100.0
    return dist, sim

# ---------- main ----------
def main():
    print("----------Code Copy Check----------")
    web_path = input("Path to web code file (e.g., web_code.txt): ").strip()
    my_path  = input("Path to my code file  (e.g., my_code.txt): ").strip()

    if not os.path.isfile(web_path) or not os.path.isfile(my_path):
        print("File not found. Make sure both paths are correct.")
        return

    web_raw = read_lines(web_path)
    my_raw  = read_lines(my_path)

    # cleaned versions (ignore blanks and full-line comments)
    web_clean = cleaned_lines(web_raw)
    my_clean  = cleaned_lines(my_raw)

    # exact-line overlap on cleaned lines
    same_count, same_pct = exact_line_overlap(my_clean, web_clean)

    # lcs on cleaned lines
    L, lcs_pct = lcs_similarity(my_clean, web_clean)

    # char-level edit distance on raw (join with \n to keep structure)
    web_text = "\n".join(web_raw)
    my_text  = "\n".join(my_raw)
    edist, edit_sim = edit_similarity(my_text, web_text)

    # report
    print("\n--- Report ---")
    print(f"My file lines (cleaned): {len(my_clean)}")
    print(f"Web file lines (cleaned): {len(web_clean)}")
    print(f"Exact-line matches: {same_count}  ({same_pct:.1f}%)")
    print(f"LCS (lines) length: {L}  (≈ {lcs_pct:.1f}% of my file)")
    print(f"Char-level edit distance: {edist}  (similarity ≈ {edit_sim:.1f}%)")

    # quick interpretation
    print("\nHow to read this:")
    print("- Exact-line % high  → more direct copying of lines.")
    print("- LCS % high         → my file follows web structure/order closely.")
    print("- Edit similarity % high → text is very close overall.")
    print("\nLower numbers usually mean more of my own writing/changes.")

if __name__ == "__main__":
    main()
