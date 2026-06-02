<div align="center">

# BEAK 🕯️

### the savant · automated intel, gathered by candlelight

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![candles](https://github.com/DavidWise01/beak/actions/workflows/candles.yml/badge.svg)](https://github.com/DavidWise01/beak/actions/workflows/candles.yml)
[![doors: 2](https://img.shields.io/badge/doors-2-b8862b?style=flat-square)](#the-doors)
[![scope](https://img.shields.io/badge/scope-subjects%20only-0f6e6a?style=flat-square)](#what-beak-will-not-do)

**→ Beak's Candle: [davidwise01.github.io/beak](https://davidwise01.github.io/beak/)**

> A candle that cannot cite its light does not burn.
> The white candle — the synthesis — burns last.

</div>

---

## Who he is

In Erikson's *Malazan Book of the Fallen*, **Beak** is a savant — slow of speech,
written off by everyone — who sees every warren of magic as a **candle** of a different
color in his mind, kept dark until the moment of need. In his last act he lights them one
by one to shield his companions, saving the **white candle** for last: the one that
consumes him, and proves his worth. He is the **Red wizard** ("both") on the
[Bridge Burners muster roll](https://github.com/DavidWise01/bridge-burners).

This Beak sees **intel sources** as candles. Give him a subject; he lights what he can,
and gathers a **cited brief**. A candle that cannot cite its light stays dark — and he
says so. The white candle, the honest synthesis, burns last.

---

## The candles

| Candle | The light | The source |
|--------|-----------|------------|
| 🤍 **white** | the steady truth | Wikipedia extract + last-revision date |
| 🖤 **black** | the cutting edge | the newest arXiv papers |
| ❤️ **red** | *is it moving?* | encyclopedia date vs. newest paper — the gap |
| 💜 **purple** | the shadow | adjacent topics + what stays unlit |

Every line in a brief carries its source. The red candle borrows the
[nom](https://github.com/DavidWise01/nom) doctrine: it measures how far the literature has
moved past the record. The white candle never lies about how many candles failed to light.

---

## The doors

Read-only, two doors only — the same two as the monk:

```
en.wikipedia.org      export.arxiv.org
```

No other source exists to Beak. If it can't be reached and cited through those two doors,
it doesn't make the brief.

---

## Use

```bash
python beak.py "topological insulator"        # gather, print the brief
python beak.py "qubit" --save                  # also write briefs/qubit.md
python beak.py --selftest                       # prove the candles assemble (offline)
```

**Automated intel:** the [`gather`](.github/workflows/gather.yml) workflow takes a `topic`
input — fire it from the Actions tab and Beak commits a cited brief to `briefs/`. The
[`candles`](.github/workflows/candles.yml) workflow runs the offline self-test on every push.

A gathered brief ([example](briefs/topological-insulator.md)) reads like:

```
# Intel Brief — Topological insulator
## white candle — the steady truth     <wikipedia extract + last revised + url>
## black candle — the cutting edge      <newest arXiv papers + urls>
## red candle — is it moving?           "the field is 5 days ahead of the article."
## purple candle — the shadow           <adjacent topics>
## the white candle, last               <synthesis · N/4 candles lit · verify at source>
```

---

## What Beak will not do

Beak gathers intel on **subjects and concepts** — physics, mathematics, ideas. He does
**not** profile people, compile dossiers on persons, or do surveillance of any kind. His
two doors are an encyclopedia and a research preprint server; his output is a reading list
with dates. "Intel" here means *what's known and what's new about an idea* — cited, so you
can check every word yourself.

---

```
ROOT0-ATTRIBUTION-v1.0 · Beak — the savant · David Lee Wise / ROOT0 / TriPod LLC · MIT
Beak is a character of Steven Erikson's Malazan Book of the Fallen, referenced as inspiration only.
```
