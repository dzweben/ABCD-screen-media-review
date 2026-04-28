"""Fix common JSON bugs across c1/c2 v5 files:
  Bug A: missing comma after `"FT_EC7_reason": "..."` before next key.
  Bug B: spurious `},` between FT_EC7_reason and binding_rules_applied.
"""
import re, json, os, glob

V5 = "/Users/dannyzweben/Desktop/ABCD-smartphon-socialmedia-review/claude-search-subrepo/v6_screening"

KEYS = ["binding_rules_applied","FT_EC7_reason","FT_EC7_applies","notes","FT_IC1","FT_IC2","FT_IC3","FT_IC4","FT_IC5","FT_IC6"]

def fix(text):
    n_total = 0
    # Bug B: remove spurious `},` line between FT_EC7_reason value and binding_rules_applied
    pat_b = re.compile(r'("[^"\n]*")\s*\n\s*\},\s*\n(\s*"binding_rules_applied")')
    text, nb = pat_b.subn(r'\1,\n\2', text)
    n_total += nb
    # Bug A: missing comma between value and next key
    pat_a = re.compile(r'(")\s*\n(\s*"(?:' + "|".join(KEYS) + r')"\s*:)')
    text, na = pat_a.subn(r'\1,\n\2', text)
    n_total += na
    return text, n_total

def try_fix_file(path):
    raw = open(path).read()
    try:
        json.loads(raw); return 0,"ok"
    except Exception:
        pass
    # Apply fix repeatedly until valid or no progress
    cur = raw
    for _ in range(10):
        new, n = fix(cur)
        if new == cur: break
        cur = new
    try:
        json.loads(cur)
    except Exception as e:
        return -1, f"still bad: {e}"
    open(path,"w").write(cur)
    return 1, "fixed"

if __name__=="__main__":
    files = sorted(glob.glob(os.path.join(V5,"c1_*.json"))+glob.glob(os.path.join(V5,"c2_*.json")))
    nfix=0
    for f in files:
        n,msg = try_fix_file(f)
        if msg!="ok":
            print(f"{os.path.basename(f)}: {msg}")
            if msg=="fixed": nfix+=1
    print(f"Total fixed: {nfix}")
