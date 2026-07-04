"""
Wordle optimizer

For every allowed guess word, scores it against every possible answer word:
  - +1 ("yellow") for each letter in the guess that appears anywhere in the
    answer word
  - +1 more ("green" bonus) if that letter is in the same position in both
    words
Repeated letters within a word are collapsed first, keeping only the LAST
occurrence (matches the dedup loop in the original .m file, which only
checks positions 1-4 of each 5-letter word).

Requires 'allowed_words.txt' and 'possible_words.txt' (one word per line/
whitespace-separated) in the same folder as this script.
"""

import re
from collections import Counter


def load_words(path):
    """Read a whitespace-separated list of words from a text file."""
    with open(path) as f:
        return re.findall(r"\S+", f.read())


def dedup_letters(words):
    """
    For each word, return a list of its letters with all but the LAST
    occurrence of a repeated letter blanked out (as '').

    Mirrors the original MATLAB loop, which only checks positions 1-4
    (0-indexed 0-3 here) against the letters that come after them.
    """
    result = []
    for w in words:
        letters = list(w[:5])
        for bb in range(4):
            if letters[bb] in letters[bb + 1:5]:
                letters[bb] = ''
        result.append(letters)
    return result


def compute_ranking(allowed_words, possible_words):
    letters_allowed = dedup_letters(allowed_words)
    letters_possible = dedup_letters(possible_words)

    # counts_possible[ll][letter] = number of possible words that have
    # `letter` (after dedup) sitting at position ll
    counts_possible = [
        Counter(row[ll] for row in letters_possible) for ll in range(5)
    ]

    ranking = []
    for word, letters in zip(allowed_words, letters_allowed):
        rating = 0
        for kk in range(5):
            letter = letters[kk]
            if letter == '':
                continue
            # yellow: letter appears anywhere in the possible word
            for ll in range(5):
                rating += counts_possible[ll][letter]
            # green bonus: letter appears in the same position (kk == ll)
            rating += counts_possible[kk][letter]
        ranking.append((word, rating))

    # sortrows(allowedwords, [-2, 1]) -> rating descending, then word ascending
    ranking.sort(key=lambda x: (-x[1], x[0]))
    return ranking


def main():
    allowed_words = load_words('allowed_words.txt')
    possible_words = load_words('possible_words.txt')

    ranking = compute_ranking(allowed_words, possible_words)

    print(f"{len(allowed_words)} allowed words, {len(possible_words)} possible words\n")
    print("Top 5:")
    for word, rating in ranking[:5]:
        print(f"  {word}\t{rating}")

    with open('ranking.txt', 'w') as f:
        for word, rating in ranking:
            f.write(f"{word}\t{rating}\n")
    print("\nFull ranking saved to ranking.txt")

    return ranking


if __name__ == '__main__':
    main()
