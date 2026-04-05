# Fixing push failures due to large example files

If `git push` fails with **GH001: Large files detected** for `examples/social_media_example/social_media_example.data.json`, that file is still in git history and must be removed before pushing.

This repo pushes to **github.com/Exonware/xwentity**. Apply the fix from the **xwmodels** (xwentity) repo root.

## One-time fix: remove file from history

```powershell
# From xwmodels repo root (remote = Exonware/xwentity)
cd d:\OneDrive\DEV\exonware\xwmodels

# Stash any local changes first
git stash -u

# Remove the file from entire history
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch examples/social_media_example/social_media_example.data.json" --prune-empty --tag-name-filter cat -- --all

# Optional: run git garbage collection to free space
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force-push (rewrites remote history)
git push origin --force --all
git push origin --force --tags
```

Then restore local changes: `git stash pop`.

## Prevention

- `examples/social_media_example/social_media_example.data.json` is in **.gitignore**.
- Generate or use large example data locally; do not commit files over GitHub’s 100 MB limit.
