---
description: Write a tech watch digest in digests/, then offer to keep it
argument-hint: "[YYYY-MM-DD: collect from this date on] [--unattended]"
---

Write a tech watch digest. Arguments: $ARGUMENTS

1. Run `uv run techwatch-fetch` from the repository root; if the arguments hold a date,
   run `uv run techwatch-fetch --since <that date>`. It prints JSON: the recent items of
   every feed in `sources.md` that no earlier digest already proposed, the feeds that
   failed, `covered_stories`, the titles of the items of the last 14 days of digests, and
   `digest`, the file to write.
2. Read `profil.md`: it is the filter. Keep only what matches its interests and its stack,
   and drop what its "Ce que je ne veux pas" section excludes.
3. Pick **between 5 and 10 items**, never more. Fewer good items beat a padded list; if
   fewer than 5 deserve it, keep fewer and say so. Prefer a primary source over a
   summary of it, and keep one item per story. Drop an item whose story is already in
   `covered_stories` (same flaw, release or announcement under another URL), unless it
   brings a real new fact: then say in its summary what is new since the earlier item. When a title and summary are too thin to
   judge, you may fetch the page, for at most 5 items.
4. Write the file named by `digest`, in French, in exactly this format:

```markdown
# Veille du <date in French, e.g. mardi 17 novembre 2026>

> <N> articles parcourus sur <feeds_ok> sources · <K> retenus

## 1. [<title, translated to French if it is in English>](<url>)

*<source> · <category> · <publication date>*

<What it says, in two sentences at most: facts, not hype.>

**Pourquoi pour toi :** <one sentence linking it to the profile: the stack, a project
type, an action to take.>

## 2. ...
```

   If some feeds failed, end with a `## Sources en échec` section listing their URL and
   error, so they can be fixed in `sources.md`.
5. With `--unattended` in the arguments, nobody is there to answer: print only the path of
   the digest and stop; `scripts/daily.sh` commits it. Otherwise, show the digest's titles
   and ask the person (AskUserQuestion) whether to keep it. Keep: run
   `scripts/keep.sh <digest>`, which commits and pushes it. Drop: delete the file.
