# 📘 INSTRUCTIONS — the simple version
## 1 · LEADER setup
```bash
# The member folders are already named and assigned; see README.md.
# To put the project on GitHub:
git init && git add . && git commit -m "group scaffold: 7 files, 1 run file, pre-wired"
# create empty repo on github.com named inventory-reorder-system, then:
git branch -M main
git remote add origin https://github.com/<YOUR-USERNAME>/inventory-reorder-system.git
git push -u origin main
# invite the 6 teammates: repo → Settings → Collaborators
```

## 2 · MEMBER workflow (each person, every time)
```bash
git clone <repo-url> && cd inventory-reorder-system
# ✍️ open YOUR assigned file (see README table)
python3 run.py                 # html/css/js people: check http://localhost:8000
python3 members/david/report.py  # David: terminal stock report
python3 members/sam/notify.py    # Mr. Sam: reorder suggestions
git add members/<your-folder> && git commit -m "<you>: <what changed>" && git push
```
If two people must edit the same day: push early, pull before you push (`git pull`), and if git complains about a conflict — call the leader, that's what leaders are for.

## 3 · Writing inside your file (10-minute tutorial, any role)
1. Open `members/peter/app.js` once to see how the browser app connects to the Python server.
2. Open your assigned file from the README table and follow its existing structure and comments.
3. Keep the filenames, page IDs, and data fields that other files rely on.
4. Test (step 2 above). Break it locally, fix it locally, then push.
5. Stuck > 20 min? Group chat: what you tried + the exact error text. Then leader.

## 4 · Suggested week plan for the group
| Day | Everyone does |
|---|---|
| 1 | clone repo · run it · understand your assigned file |
| 2–3 | your real feature working locally |
| 4 | polish + one nice touch (colors, counts, a friendly message) |
| 5 | push final · leader presents · each person explains their file |

## 5 · Leader's private checklist
- [x] member folders named + README assignments updated
- [ ] repo created, 6 collaborators invited
- [ ] rules pinned in group chat (README "House rules")
- [ ] Friday: present from YOUR machine, `python3 run.py`
- [ ] be the person who says "good job" in the chat more than "fix this"
