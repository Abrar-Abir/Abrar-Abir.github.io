---
layout: post
title: Good Vibes Need Hard Boundaries
date: 2026-02-13 00:00:00
description: building a UI for AlphaGenome, failing at vibe coding, and trying again
tags: ai genomics vibe-coding
---

I had been talking about [AlphaGenome](https://deepmind.google/blog/alphagenome-ai-for-better-understanding-the-genome/) for maybe 10 minutes before I realized very few people were going to try it by themselves.[^1]

Not because they weren't interested (at least in my perception) but coding in this field means bash scripting for bioinformatics pipelines and [R for visualization](https://divingintogeneticsandgenomics.com/post/r-or-python-for-bioinformatics/). [Python isn't part of the toolchain](https://news.ycombinator.com/item?id=40603696) - not yet, not even with gen AI making code generation more accessible.[^2] I had miscalculated how much of a barrier that is. It's not too high a barrier. But it's *there*...

So I kept thinking about it - what if there was a user interface on top of it? Something you could just install and self-host. A wrapper that takes dealing with Python syntax out of the equation - not to dumb anything down but to get out of the way. Move things even slightly in the direction of [ML adoption in bio research](https://www.fiosgenomics.com/bioinformatics-2025-outlook-thoughts-from-bioinformaticians/), or at least toward understanding what these models can do.

Surely someone has thought about it already and built it (right?). Nope. I searched with hope, but couldn't find any (which kind of made me sad; the bioinformatics/genomics world really needs more attention, but anyway) so I decided to build one myself.

I also had a hidden motive. I'd been reading about [vibe coding](https://x.com/karpathy/status/1886192184808149383) for months - people [celebrating it](https://simonwillison.net/2025/Mar/19/vibe-coding/), people [ridiculing it](https://stackoverflow.blog/2026/01/02/a-new-worst-coder-has-entered-the-chat-vibe-coding-without-code-knowledge/) - but I hadn't formed any opinion of my own yet. I wanted to get into the water.

Vibe coding itself isn't well defined, or rather, I should say, it's ill-defined. But instead of going into another rabbit hole of definitions, I find Dan Shapiro's [framework](https://www.danshapiro.com/blog/2026/01/the-five-levels-from-spicy-autocomplete-to-the-software-factory/) very useful - a spectrum-like representation rather than a concrete one. I was aiming for Level 3, maybe 4. Don't touch the codebase. Minimally review. If it works, it works.

It did not work.

---

Streamlit + FastAPI + PostgreSQL. A reasonable stack for a proof of concept, or so I thought. Before I knew it, I was drowning in a constellation of `.md` files to handle plan, scope, architecture, README - at different levels of abstraction, mostly to handle context switches across agent sessions. 

~15 sessions across 3 days.

The codebase grew almost exponentially (line of code vs line of prompt). Not in one direction - everywhere at once. Fix a bug in the API layer and something breaks in the frontend. Fix the frontend and a new edge case surfaces in a route you haven't touched. Sessions would hit [context limits and compress](https://factory.ai/news/context-window-problem), and after [compaction](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) the agent became dangerously confident - it *thought* it had full context from the summary, so it stopped exploring the actual code. Which led to patches that contradicted other patches. And the `.md` files needed periodic updating too; stale docs meant the agent started every session with slightly wrong information, compounding in ways I couldn't see until everything was already tangled.

More sessions, more drift. More drift, more bugs. More bugs, more sessions. I kept telling myself *[one more session](https://www.nijho.lt/post/vibe-coding/)* would stabilize things.

It never did.

I started to think I should have listened to those wise people - who had already gone through the experience and warned us about its limitations. Once more I cursed the people who had pumped up AI's capabilities out of proportion - knowingly (for business profit) or unknowingly (how could that happen?). If Dante were alive, he might reserve the lowest circle of hell for them in his Inferno.

Anyway, a few days later on a 'luxurious afternoon', when the bitterness started to drift away, I decided to give it another attempt - starting from scratch.

---

This time, I stripped everything back. No PostgreSQL, no SQLite - the app only needs to store an API key, so just use browser localStorage. For the frontend: React, but allowed to use [shadcn/ui](https://ui.shadcn.com/) components only. I described exactly how I wanted the interface to look and - just as important - what *not* to add. [Agents love to over-architect](https://addyosmani.com/blog/agentic-engineering/).

Session one: generate a plan, split into frontend and backend plans. Session two: implement the backend. Session three: implement the frontend.

15 minutes. 3 sessions. Working app.

Of course, what I got was bare minimum. But from there it was controlled, incremental work. Add dark mode. Done. Add Docker support. Done. Add [Apptainer](https://apptainer.org/) for HPC systems... Each feature was one focused session. No more cursing. Small steps, clear scope, tangible progress.

---

Once I was satisfied with the feature set[^3], I realized the installation still had too much friction. React needs Node.js at build time, but users shouldn't have to worry about that. So I [built the frontend into static files, bundled everything with the FastAPI backend](https://medium.com/@asafshakarzy/embedding-a-react-frontend-inside-a-fastapi-python-package-in-a-monorepo-c00f99e90471), and published the whole thing as a Python package. Now it's just:

```bash
pip install alphagenome-viewer
alphagenome-viewer
```

That's it. Open `localhost:8000` and you're looking at a web interface for a genomic foundation model. No Node. No Docker (unless you want it). Just pip.

---

The striking contrast in experience made me reflect carefully - what happened and why (writing the post is part of unpacking things for myself). 

I learned more from the 3 days I spent failing than from the 15 minutes it took to succeed. I understand now why some developers - even after genuinely trying AI-assisted coding - come away skeptical. Coding agents make [inhuman mistakes](https://simonwillison.net/2025/Mar/2/hallucinations-in-code/). Not typos or off-by-ones, but structurally weird choices that no human would make. And working with them requires a fundamentally different mode of thinking. You're not programming anymore. You're managing a very fast, very confident [junior developer](https://sourcegraph.com/blog/the-death-of-the-junior-developer) who never asks clarifying questions.

There's no good formalization of this process yet.[^4] No best practices that actually feel [*practiced*](https://beyond.addy.ie/). Everyone's figuring it out in real time, and the loudest voices are either celebrating or mocking - rarely [analyzing](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/).

In the end, it's not about the coding agent's capabilities. It's about speaking the [instruction language](https://medium.com/@addyosmani/vibe-coding-is-not-the-same-as-ai-assisted-engineering-3f81088d5b98). AI doesn't speak the same English as humans. And as long as the communication gap remains, it will prevent maximal utilization of AI capabilities. (The concept I'm referring to as 'speaking the instruction language' has multiple dimensions - prompt engineering, context engineering, and so on.)  

In hindsight, another reason my first attempt failed is that the problem space was too open - too many files, too many possible architectures, too much room for the agent to wander. The second attempt worked because I had already explored the failure modes and could draw tight boundaries. The agent didn't get smarter. I got better at constraining it.

It'd be interesting to test the limits of vibe-coding (or rather my limits of how well I can speak the instruction language). So far I've only tried this on tech I already know - Python, React, FastAPI. Familiar territory where I can spot when the agent drifts and intervene before things spiral. That familiarity is doing a lot of heavy lifting. What happens when you try this on a completely unknown stack? When you *can't* tell good output from bad? That would push you well past Level 3 into Level 4 or 5 territory - real delegation, not just supervised generation. I'm curious enough to try it. That's probably the next experiment.

Oh I forgot, here's the [github link](https://github.com/Abrar-Abir/alphagenome-viewer)

PS: as you may have noticed, the writing is URL-heavy. This is somewhat intentional; as I have been reading & hearing from different crowds, I wanted to consolidate pieces that I found interesting and/or insightful - both for my future self and the readers.
---

[^1]: They announced AlphaGenome last June but the paper just got [published in Nature](https://www.nature.com/articles/s41586-025-10014-0), and - more importantly - the [weights are now public](https://github.com/google-deepmind/alphagenome_research).
[^2]: This is part of a [broader observation](https://www.fiosgenomics.com/bioinformatics-2025-outlook-thoughts-from-bioinformaticians/): a lot of researchers are not up to date with ML/AI's capabilities and applications in scientific discovery. But that needs another post.
[^3]: Somewhere in this process I also needed a logo. Couldn't find an official one on the Google page, so I took an image of alpha, an image of DNA, merged them using the color scheme from the official AlphaGenome page - with the help of Google's Nano banana. Applied Google's Inter font for the text. Since the app is a wrapper on AlphaGenome, I wanted to preserve as much of the official visual identity as I could. The AI-assisted art generation process itself deserves its own entry.
[^4]: I have a lot more to unpack about vibe coding - what works, what doesn't, why the [discourse is so polarized](https://jeremykreutzbender.com/blog/thoughts-and-experiences-vibe-coding-mid-2025) - but that needs (again) a separate post.
