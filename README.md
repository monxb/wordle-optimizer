# Wordle Optimizer

A Python script that identifies the best starting words for Wordle by scoring each allowed guess against all possible answer words.

## Overview

This optimizer uses a scoring metric to evaluate which starting words provide the most information about the solution. For each allowed word, the script calculates a score based on how many times its letters appear in the possible answer words.

## Scoring Methodology

- **+1 point** for each letter that appears anywhere in the answer word (yellow)
- **+1 additional point** if the letter appears in the same position (green bonus)
- Repeated letters within a word are deduplicated before scoring

This approach identifies words that maximize information gain on average.

## Usage

```bash
python wordleoptimizer.py
```

The script requires:
- `allowed_words.txt` – 12,972 valid Wordle guesses
- `possible_words.txt` – 2,315 possible answer words

Output is saved to `ranking.txt` with all words ranked by score.

## Top Starting Words

| Rank | Word | Score |
|------|------|-------|
| 1    | SOARE | 5559  |
| 2    | STARE | 5383  |
| 3    | ROATE | 5324  |
| 4    | SLATE | 5308  |
| 5    | ORATE | 5294  |

**SOARE** is statistically the best opening word.

## Files

- `wordleoptimizer.py` – Main optimization script
- `allowed_words.txt` – Valid Wordle guess words
- `possible_words.txt` – Possible solution words
- `ranking.txt` – Full ranking of all words (generated)
