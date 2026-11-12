# CS 4050 Group Algorithm Engineering Assignment 2

Divide and conquer (inversion counting) and dynamic programming (coin change).

**Group:** Isaac Dierker, Noah Pipes, Andrew W. Smith

## Language and version

- Python 3.11.9
- Standard library only (`random`, `time`, `csv`, `os`); nothing to install.

## How to run

From the folder containing `CS_4050_GAE2.py`:

```
python .\CS_4050_GAE2.py        # Windows
python3 CS_4050_GAE2.py         # macOS / Linux
```

A full run takes roughly 20-60 seconds depending on the machine. Most of that time is the brute-force inversion counter at n = 20,000.

The program prints its results to the terminal and writes CSV files to a `results/` folder, which is created next to the script if it doesn't exist.

## Reproducibility

- The run starts with `random.seed(1)`, and the coin-change validation, Experiment 1 and Experiment 2 each re-seed (`random.seed(2)`, `3`, `4`) at their start.
- The inversion crossover search draws a timing-dependent number of random arrays, which is why the later experiments re-seed: their coin systems, solutions and recursion counts are the same on every run.
- Runtimes depend on the hardware and on what else the machine is doing, so they will vary between machines and between runs. Each timing is a single run.

## What the program runs, in order

| Step | Function | Assignment part |
|---|---|---|
| 1 | `validation()` | **Part 1B.** Checks 10 hand-built arrays against expected counts. Cross-checks merge-and-count against brute force on 200 random arrays of length 100. Finds the crossover size and times both methods for n = 1 to 20,000. |
| 2 | `coin_algorithm_validation()` | **Part 2B.** Runs all four solvers on 11 hand-built cases (including target 0, an impossible case and a case with more than one optimal answer). Then runs 100 random small instances and requires naive, top-down and bottom-up to agree on the coin count and every coin list to sum to the target. |
| 3 | `part_2c1()` | **Part 2C, Experiment 1.** Counts recursive calls, distinct target states and cache hits for naive recursion and top-down memoization for A = 1 to 24. |
| 4 | `part_2c2()` | **Part 2C, Experiment 2.** Runs bottom-up DP for A = 2^8 to 2^19 and records A, bit length, DP states processed and runtime. |
| 5 | `greedy_counterexample_search()` | **Part 2B.** Searches every coin system {1, a, b} with b <= 10 and targets 1 to 30 for cases where greedy uses more coins than the bottom-up optimum. Keeps the smallest failing target for each system. |

### Validation

Every correctness check uses `assert`. If the program finishes without an `AssertionError`, all of these passed:

- The hand-built inversion tests and the 200 random inversion cross-checks.
- The hand-built coin-change tests for naive, top-down and bottom-up.
- The random coin-change sum and agreement checks.
- The counterexample search found the required case D = {1, 3, 4}, A = 6, and at least 3 distinct counterexamples.

Greedy is not asserted, because it is not expected to always be optimal. Its result for each hand-built case is printed as `Greedy correct: True/False`.

## Output files (`results/`)

| File | Columns | Produced by |
|---|---|---|
| `inversion_crossover.csv` | `n, merge_seconds, brute_seconds` | First array size at which merge-and-count beat brute force |
| `inversion_runtime.csv` | `n, merge_seconds, brute_seconds, brute_over_merge` | Runtime of both inversion counters for n = 1, 10, 100, 1,000, 2,000, 5,000, 10,000, 20,000 |
| `experiment1_repeated_subproblems.csv` | `denominations, A, naive_recursive_calls, naive_distinct_states, topdown_recursive_calls, topdown_distinct_states, topdown_cache_hits, optimal_coin_count, solution` | Experiment 1 |
| `experiment2_pseudo_polynomial.csv` | `denominations, A, bit_length_A, dp_states_processed, runtime_seconds` | Experiment 2 |
| `greedy_counterexamples.csv` | `denominations, A, greedy_coins, greedy_count, optimal_coins, optimal_count` | Greedy counterexample search |

Coin lists are stored in one cell separated by spaces, for example `4 1 1` means the coins [4, 1, 1].

## Files in this submission

- `CS_4050_GAE2.py`: all algorithms, validators, generators, the counterexample search and the experiments
- `results/*.csv`: the data behind the tables and figures in the report
- `Engineering_Report.docx`: methods, correctness and complexity, validation, results and interpretation
- `Engineering_Reflection.docx`: Part III cross-paradigm reflection
- `Group_Contribution_Statement.docx`: each member's contributions
- `AI_Contribution_Statement.docx`: AI tools used and how their output was checked