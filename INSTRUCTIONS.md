# 📘 INSTRUCTIONS — the simple version
## 1 · LEADER setup
```bash
# a) put real names on the folders (also fixes every internal link automatically)
chmod +x rename.sh
./rename.sh name2 name3 name4 name5 name6 name7     # in member2..member7 order

# b) put it on GitHub
git init && git add . && git commit -m "group scaffold: 7 files, 1 run file, pre-wired"
# create empty repo on github.com named inventory-reorder-system, then:
git branch -M main
git remote add origin https://github.com/<YOUR-USERNAME>/inventory-reorder-system.git
git push -u origin main
# c) invite the 6 teammates: repo → Settings → Collaborators
```

## 2 · MEMBER workflow (each person, every time)
```bash
git clone <repo-url> && cd inventory-reorder-system
# ✍️ open YOUR one file (see README table) and write between the WRITE HERE marks
python3 run.py                 # html/css/js people: check http://localhost:8000
python3 members/<you>/report.py   # python people: run your file directly
git add members/<your-folder> && git commit -m "<you>: <what changed>" && git push
```
If two people must edit the same day: push early, pull before you push (`git pull`), and if git complains about a conflict — call the leader, that's what leaders are for.

## 3 · Writing inside your file (10-minute tutorial, any role)
1. Open `members/member1/app.js` once and read it — it's the finished example of "a file that already works".
2. Open **your** file. Find the `═══ WRITE HERE ═══` marks (or the RULES comment at top).
3. Write between them. Most files include an example line you're allowed to copy.
4. Test (step 2 above). Break it locally, fix it locally, then push.
5. Stuck > 20 min? Group chat: what you tried + the exact error text. Then leader.

## 4 · Suggested week plan for the group
| Day | Everyone does |
|---|---|
| 1 | clone repo · run it · make your file show *something* (even static text) |
| 2–3 | your real feature working locally |
| 4 | polish + one nice touch (colors, counts, a friendly message) |
| 5 | push final · leader demos · each person says 3 sentences about their file |

## 5 · Leader's private checklist
- [ ] names renamed + README owner table updated
- [ ] repo created, 6 collaborators invited
- [ ] rules pinned in group chat (README "House rules")
- [ ] friday: demo from YOUR machine, `python3 run.py`, one click per module
- [ ] be the person who says "good job" in the chat more than "fix this"
