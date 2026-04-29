---
layout: page
title: now
permalink: /now/
description: what I'm exploring right now. inspired by Derek Sivers' <a href="https://nownownow.com/about">/now page movement</a>
nav: true
nav_order: 2
---

_last updated: very recently (trust me)_

&nbsp;

### ambigrams &amp; constrained typography

Reading up on the [history of ambigrams](https://en.wikipedia.org/wiki/Ambigram). [John Langdon](https://www.johnlangdon.net/) and [Scott Kim](https://www.scottkim.com/ambigrams) came up with them independently in the mid-'70s. Douglas Hofstadter named them later. Kim's [_Inversions_ (1981)](https://www.amazon.com/Inversions-Scott-Kim/dp/1559532807) and Langdon's _Wordplay_ (1992) are the canonical texts.

Also pulling on the math/geometry thread: reflections, rotations, glide reflections, figure/ground designs, fractal ambigrams. [Burkard Polster's _Mathemagical Ambigrams_](https://www.qedcat.com/articles/ambigram.pdf) is a decent primer on the symmetry group side of things.

I wonder how non-trivial, constrained typography will evolve with the wave of gen AI? Early works like [AmbiGen](https://arxiv.org/html/2312.02967v1) distills DeepFloyd IF to optimize letter outlines for legibility in two orientations. Other approaches run [PyTorch optimization over path vectors](https://medium.com/@noufalsamsudin/generating-ambigrams-using-deep-learning-a-typography-approach-c829d0ee4d51) with OCR-embedding losses. Interesting stuff, but the hand-crafted work still wins on aesthetics. Whether that holds is the question.

&nbsp;

### colonization of the bangla language

Reading [Mohammad Azam](https://www.du.ac.bd/faculty/faculty_details/BNG/57)'s _Bangla Bhashar Uponibeshayan O Rabindranath_. His work sits at the intersection of language planning, grammar politics, and the social/cultural history of 19th-20th century Bengal. He was recently appointed [DG of Bangla Academy](https://www.dhakatribune.com/bangladesh/education/357367/dr-mohammad-azam-appointed-new-director-general-of), which gives the whole reading a different texture.

Picking up tangential literature around it. Also reading [Rok Monu](https://www.rokomari.com/book/author/78531/rok-monu)'s [_Khash Bangla_](https://www.rokomari.com/book/420080/khas-bangla): 15-20 years of essays on the language, informal and sharp.

Slowly getting into Rok Monu's palace at [bacbichar.net](https://bacbichar.net/) too.

&nbsp;

### epigenomics &times; machine learning

Methylation data has been understudied for a while. Now that [ONT long-read sequencing](https://nanoporetech.com/applications/investigations/epigenetics-and-methylation-analysis) gives us large-scale, high-quality data (direct detection, no bisulfite treatment, [real-time methylation calling in the basecaller](https://nanoporetech.com/news/news-oxford-nanopore-releases-new-machine-learning-model-enable-real-time-high-accuracy)), the ML surface feels ripe.

Currently looking at:

- [**MethylBERT**](https://www.nature.com/articles/s41467-025-55920-z) : transformer-based read-level methylation pattern identification and tumor deconvolution. [[code](https://github.com/CompEpigen/methylbert)]
- [**EpiSegMixMeth**](https://www.biorxiv.org/content/10.1101/2025.07.25.666820v2.full) : extension of [EpiSegMix](https://academic.oup.com/bioinformatics/article/40/4/btae178/7639383), an HMM with flexible mixture and duration modeling that integrates chromatin marks with DNA methylation for segmentation.

The goal is to understand the play between methylation and computation, and may be pick up some biology on the side.

&nbsp;

---

_inspired by [nownownow.com](https://nownownow.com/about). this page will drift over time; that's the point._
