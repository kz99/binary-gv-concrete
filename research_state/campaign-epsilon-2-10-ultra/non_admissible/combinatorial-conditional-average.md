# Non-admissible canonical conditional-average candidates

The submissions `combinatorial-01` and `combinatorial-02` give a finite,
deterministic conditional-expectation selector with claimed dimension
\(2971\). They do not give an algorithm that outputs their full generator
matrix in time polynomial in \(n=2^{30}\): evaluating the prescribed next-bit
choice requires exact averages over exponentially many matrix completions.

Under the active explicitness standard, these submissions are therefore
non-admissible for the leaderboard. This is not a refutation of their
probabilistic or finite-existence argument; it is a classification decision.
They remain archived as evidence about the finite GV threshold, not as explicit
code constructions.
