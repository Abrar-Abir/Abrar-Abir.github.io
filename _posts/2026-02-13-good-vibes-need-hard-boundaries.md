---
layout: post
title: Good Vibes Need Hard Boundaries
date: 2026-02-13 00:00:00
description: building a UI for AlphaGenome, failing at vibe coding, and trying again
tags: ai genomics vibe-coding
---

I'd been talking about [AlphaGenome](https://deepmind.google/blog/alphagenome-ai-for-better-understanding-the-genome/) for maybe 10 minutes before I realized nobody in the room was going to try it.[^1]

Not because they weren't interested. They were. But coding in this field means bash for bioinformatics pipelines and [R for visualization](https://divingintogeneticsandgenomics.com/post/r-or-python-for-bioinformatics/). [Python isn't part of the toolchain](https://news.ycombinator.com/item?id=40603696) — not yet, not even with gen AI making code generation more accessible.[^2] I'd miscalculated how much of a barrier that is. It's not a high barrier. But it's *there*, and that's enough.

So I kept thinking about it afterward. What if there was a point-and-click interface? Something you could `pip install` and just use. A wrapper that takes the Python out of the equation entirely — not to dumb anything down, but to get out of the way. Move things even slightly in the direction of [ML adoption in bio research](https://www.fiosgenomics.com/bioinformatics-2025-outlook-thoughts-from-bioinformaticians/), or at least toward understanding what these models can do.

I also had a second motive. I'd been reading about [vibe coding](https://x.com/karpathy/status/1886192184808149383) for months — people [celebrating it](https://simonwillison.net/2025/Mar/19/vibe-coding/), people [ridiculing it](https://stackoverflow.blog/2026/01/02/a-new-worst-coder-has-entered-the-chat-vibe-coding-without-code-knowledge/) — and I'd formed no opinion of my own. I wanted to get into the water.

Dan Shapiro has [a useful framework](https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/) for this — 5 levels of AI-assisted coding, modeled after autonomous driving levels. I was aiming for Level 3, maybe 4. Don't touch the codebase. Minimally review. If it works, it works.

It did not work.

---

Streamlit + FastAPI + PostgreSQL. A reasonable stack for a proof of concept, or so I thought. I created a constellation of `.md` files — plan, scope, architecture, README — at different levels of abstraction, mostly to handle context switches across agent sessions. Being a Python person, this felt natural. Organized. Professional.

~15 sessions across 3 days.

The codebase grew the way mold grows. Not in one direction — everywhere at once. Fix a bug in the API layer and something breaks in the frontend. Fix the frontend and a new edge case surfaces in a route you haven't touched. Sessions would hit [context limits and compress](https://factory.ai/news/context-window-problem), and after [compaction](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) the agent became dangerously confident — it *thought* it had full context from the summary, so it stopped exploring the actual code. Which led to patches that contradicted other patches. And the `.md` files needed periodic updating too; stale docs meant the agent started every session with slightly wrong information, compounding in ways I couldn't see until everything was already tangled.

More sessions, more drift. More drift, more bugs. More bugs, more sessions. I kept telling myself *[one more session](https://www.nijho.lt/post/vibe-coding/)* would stabilize things.

It never did.

I gave up. Nuked the repo. Started from scratch.

---

The second time, I stripped everything back. No PostgreSQL, no SQLite — the app only needs to store an API key, so just use browser localStorage. For the frontend: React, but constrained to [shadcn/ui](https://ui.shadcn.com/) components only. I described exactly how I wanted the interface to look and — just as important — what *not* to add. [Agents love to over-architect](https://addyosmani.com/blog/agentic-engineering/). Tell them you need a full-stack app and they'll propose a database for everything. [Constraints matter more than instructions](https://www.softr.io/blog/vibe-coding-best-practices).

Session one: generate a plan, split into frontend and backend plans. Session two: implement the backend. Session three: implement the frontend.

15 minutes. 3 sessions. Working app.

Of course, what I got was bare minimum. But from there it was controlled, incremental work. Add dark mode. Add Docker support. Add [Apptainer](https://apptainer.org/) for HPC systems. Each feature was one focused session. No more wall-banging. Small steps, clear scope, tangible progress.

---

Once I was satisfied with the feature set[^3], I realized the installation still had too much friction. React needs Node.js at build time, but users don't care about that. So I [built the frontend into static files, bundled everything with the FastAPI backend](https://medium.com/@asafshakarzy/embedding-a-react-frontend-inside-a-fastapi-python-package-in-a-monorepo-c00f99e90471), and published the whole thing as a Python package. Now it's just:

```bash
pip install alphagenome-viewer
alphagenome-viewer
```

That's it. Open `localhost:8000` and you're looking at a web interface for a genomic foundation model. No Node. No Docker (unless you want it). Just pip.

---

I learned more from the 3 days I spent failing than from the 15 minutes it took to succeed. I understand now why some developers — even after genuinely trying AI-assisted coding — come away skeptical. Coding agents make [inhuman mistakes](https://simonwillison.net/2025/Mar/2/hallucinations-in-code/). Not typos or off-by-ones, but structurally weird choices that no human would make. And working with them requires a fundamentally different mode of thinking. You're not programming anymore. You're managing a very fast, very confident [junior developer](https://sourcegraph.com/blog/the-death-of-the-junior-developer) who never asks clarifying questions.

There's no good formalization of this process yet.[^4] No best practices that actually feel [*practiced*](https://beyond.addy.ie/). Everyone's figuring it out in real time, and the loudest voices are either celebrating or mocking — rarely [analyzing](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/).

Here's what I took away: the key variable isn't the agent's capability. It's [*constraint surface*](https://medium.com/@addyosmani/vibe-coding-is-not-the-same-as-ai-assisted-engineering-3f81088d5b98). My first attempt failed because the problem space was too open — too many files, too many possible architectures, too much room for the agent to wander. The second attempt worked because I'd already explored the failure modes and could draw tight boundaries. The agent didn't get smarter. I got better at constraining it.

But there's a caveat: so far I've only tried this on tech I already know — Python, React, FastAPI. Familiar territory where I can spot when the agent drifts and intervene before things spiral. That familiarity is doing a lot of heavy lifting. What happens when you try this on a completely unknown stack? When you *can't* tell good output from bad? That would push you well past Level 3 into Level 4 or 5 territory — real delegation, not just supervised generation. I'm curious enough to try it. That's probably the next experiment.

---

[^1]: They announced AlphaGenome last June but the paper just got [published in Nature](https://www.nature.com/articles/s41586-025-10014-0), and — more importantly — the [weights are now public](https://github.com/google-deepmind/alphagenome_research).
[^2]: This is part of a [broader observation](https://www.fiosgenomics.com/bioinformatics-2025-outlook-thoughts-from-bioinformaticians/): a lot of researchers are not up to date with ML/AI's capabilities and applications in scientific discovery. But that's a bigger post.
[^3]: Somewhere in this process I also needed a logo. Couldn't find an official one on the Google page, so I took an image of alpha, an image of DNA, merged them using the color scheme from the official AlphaGenome page — with the help of Google's Nano banana. Applied Google's Inter font for the text. Since the app is a wrapper on AlphaGenome, I wanted to preserve as much of the official visual identity as I could. The AI-assisted art generation process itself deserves its own entry.
[^4]: I have a lot more to unpack about vibe coding — what works, what doesn't, why the [discourse is so polarized](https://jeremykreutzbender.com/blog/thoughts-and-experiences-vibe-coding-mid-2025) — but that needs a separate post.
