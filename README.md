# Homework 6.1 – Dynamic Programming and Code Copy Check  

## Project Overview  
In this homework, I worked with **Dynamic Programming** using the **Edit Distance algorithm** to compare two code files. The purpose was to check how much of my code was similar to the web version and how much I wrote/changed myself.  

I used three files:  
- `web_code.txt` → original code from the web  
- `my_code.txt` → my own edited code with ranking and confidence  
- `compare_code.py` → Python program that compares both files and generates results  

---

## How It Works  
1. The program reads both text files (web and my code).  
2. It removes spaces and cleans the lines.  
3. It applies **Longest Common Subsequence (LCS)** and **Edit Distance** to calculate:  
   - Exact-line matches (%)  
   - LCS overlap (%)  
   - Character-level similarity (%)  
4. It prints a summary showing the differences and similarities.
