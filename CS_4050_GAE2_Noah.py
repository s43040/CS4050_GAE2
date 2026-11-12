import random
import time
import math
import statistics

IMPOSSIBLE = "IMPOSSIBLE"
TIMING_REPS = 5      # every timing is repeated this many times and we report the median

class Globals:
    recursive_calls = 0
    target_states_solved = 0
    memoization_cache_hits = 0
    naive_states = set()

def median_time(function, *args, reps=TIMING_REPS):
    times = []
    for _ in range(reps):
        start = time.perf_counter()
        function(*args)
        times.append(time.perf_counter() - start)
    return statistics.median(times)

BOLD = "\033[1m"
RESET = "\033[0m"
UNDERLINE = "\033[4m"

def inv_count_merge(array):
    if len(array) <= 1:
        return array, 0
    left_array, left_inversions = inv_count_merge(array[:int(len(array)/2)])
    right_array, right_inversions =  inv_count_merge(array[int(len(array)/2):])
    Inversions = left_inversions + right_inversions
    New_array = [0] * len(array)
    left_index = 0
    right_index = 0
    for i in range(len(array)):
        if right_index < len(right_array) and (left_index == len(left_array) or left_array[left_index] > right_array[right_index]):
            Inversions += len(left_array) - left_index
            New_array[i] = right_array[right_index]
            right_index += 1
        else:
            New_array[i] = left_array[left_index]
            left_index += 1
    return New_array, Inversions

def brute_force_inversion(array):
    inversions = 0
    for i in range(len(array)):
        for x in range(i+1, len(array)):
            if array[i] > array[x]:
                inversions += 1
    return inversions

def validation():
    hand_crafted_arrays = [[3,2,1],
                           [1,2,3,4,5],
                           [5,6,7,4,9],
                           [9,4,0,-1],
                           [1,9],
                           [7,2,9,6,3,8],
                           [1],
                           [9,6,4,1],
                           [6,9,5,3,2,8],
                           [10,11,12,13,4,15],
                           [1,2,4,3,5,6]]
    expected_inversions = [3,
                           0,
                           3,
                           6,
                           0,
                           7,
                           0,
                           6,
                           10,
                           4,
                           1]
    inversions_got_merge = [inv_count_merge(array)[1] for array in hand_crafted_arrays]
    inversions_got_brute = [brute_force_inversion(array) for array in hand_crafted_arrays]
    print(inversions_got_brute)
    print(inversions_got_merge)
    assert inversions_got_merge==expected_inversions, "Inversions from merge is different than from expected"
    assert inversions_got_brute==expected_inversions, "Inversions from brute_force is different than from expected"
    for array in hand_crafted_arrays:
        assert inv_count_merge(array)[0] == sorted(array), "Merge did not return a sorted array"

    rng = random.Random(4050)   # seed for the random cross-checks
    for x in range(200):
        n = rng.randint(1, 100)
        array = rng.sample(range(10 * n), n)    # distinct values
        assert inv_count_merge(array)[1] == brute_force_inversion(array), f"Disagreement on {array}"
        assert inv_count_merge(array)[0] == sorted(array)
    print("All 200 random inversion cross-checks passed")

def inversion_benchmark():
    rng = random.Random(1)      # seed for the benchmark arrays
    sizes = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1_000, 2_000, 5_000, 10_000, 20_000]
    rows = []
    crossover = None
    for n in sizes:
        array = rng.sample(range(10 * n), n)
        merge_time = median_time(inv_count_merge, array)
        brute_time = median_time(brute_force_inversion, array, reps=TIMING_REPS if n <= 5_000 else 3)
        rows.append([n, brute_time, merge_time, brute_time / merge_time])
        print(f"n={n:>6}  brute={brute_time:.6f}s  merge={merge_time:.6f}s  brute/merge={brute_time/merge_time:.2f}")
    # crossover = smallest n from which merge wins at every larger size we tested
    crossover = None
    for n, brute_time, merge_time, ratio in reversed(rows):
        if merge_time < brute_time:
            crossover = n
        else:
            break
    print(f"Merge beats brute force for every tested n >= {crossover}")


# coin change solvers (Part 2)
# coin denominations are given as an array of ascending integers, with the smallest denomination being 1
# the target amount is given as an integer greater than or equal to zero

# we make the assumption that the denominations are strictly increasing and start with 1



# 2A - Greedy Largest-Denomination First
def greedy_largest_denomination_first(denominations, target_amount):
    coins_used = []
    for coin in sorted(denominations, reverse=True):
        while target_amount >= coin:
            coins_used.append(coin)
            target_amount -= coin

    if (target_amount > 0):  # if we have a remaining amount that cannot be made with the given denominations, return None
        return None

    return coins_used

# 2B - Naive Exact Recursive Solution (slide 81 of Dynamic Programming I v2)
def naive_exact_recursive(denominations, target_amount, count_stuff = False):
    if count_stuff == True:
        Globals.recursive_calls += 1            # count every call, including the first one
    if target_amount == 0:      # base case: if the target amount is zero, return an empty list (no coins needed)
        return []
    if target_amount < 0:       # base case: if the target amount is negative, return None (no solution possible)
        return None
    if count_stuff == True:
        Globals.naive_states.add(target_amount) # distinct positive amounts we actually had to solve
    best_solution = None        # initialize the best solution as None
    for coin in denominations:
        remainder = target_amount - coin
        solution = naive_exact_recursive(denominations, remainder, count_stuff)      #make the recursive call to find the solution for the remainder
        if solution is not None:                        # this means that a solution was found for the remainder, so we can add the current coin to the solution and check if it's better than the best solution found so far
            solution = solution + [coin]
            if best_solution is None or len(solution) < len(best_solution):     # if the best solution is None (i.e., no solution has been found yet) or if the current solution is better (i.e., uses fewer coins), update the best solution
                best_solution = solution
    return best_solution

# 2A.C - Top-Down DP with Memoization
def top_down_dp_with_memoization(denominations, target_amount, mem=None, count_stuff = False):
    if mem is None:
        mem = {}
    if count_stuff == True:
        Globals.recursive_calls += 1            # count every call, including the first one
    if target_amount == 0:      # base case: if the target amount is zero, return an empty list (no coins needed)
        return []
    if target_amount < 0:       # base case: if the target amount is negative, return None (no solution possible)
        return None
    if target_amount in mem:    # if the answer is already cached, reuse the earlier answer
        if count_stuff == True:
            Globals.memoization_cache_hits += 1
        return mem[target_amount]

    best_solution = None        # initialize the best solution as None
    for coin in denominations:
            remainder = target_amount - coin
            solution = top_down_dp_with_memoization(denominations, remainder, mem, count_stuff)  # make the recursive call to find the solution for the remainder
            if solution is not None:    # this means that a solution was found for the remainder, so we can add the current coin to the solution and check if it's better than the best solution found so far
                solution = solution + [coin]
                if best_solution is None or len(solution) < len(best_solution):     # if the best solution is None (i.e., no solution has been found yet) or if the current solution is better (i.e., uses fewer coins), update the best solution
                    best_solution = solution
    mem[target_amount] = best_solution
    if count_stuff == True:
        Globals.target_states_solved += 1
    return best_solution

# 2A.D - Bottom-Up DP
# compute optimal values for amounts 0,1,...,A in increasing order and store enough information to reconstruct an optimal solution
def bottom_up_dp(denominations, target_amount, count_stuff = False):
    # first compute the optimal values
    INFINITY = float("inf")
    min_coins = [INFINITY] * (target_amount + 1)    # min_coins[a] = OPT(a), initialize to infinity to make optimization easy
    last_coin = [0] * (target_amount + 1)           # last_coin[a] is a coin used in OPT(a), which we can use for reconstruction
    min_coins[0] = 0                                # base case: zero coins sum up to amount zero
    for amount in range(1, target_amount + 1):      # compute OPT(a) for 0,1,...,A in increasing order
        if count_stuff == True:
            Globals.target_states_solved += 1
        for coin in denominations:
            if coin <= amount and min_coins[amount - coin] + 1 < min_coins[amount]:
                min_coins[amount] = min_coins[amount - coin] + 1
                last_coin[amount] = coin

    if min_coins[target_amount] == INFINITY:    # no combination reached the target so it is impossible
        return None
    
    # now reconstruct an optimal solution
    coins_used = []
    amount = target_amount
    while amount > 0:
        coins_used.append(last_coin[amount])
        amount -= last_coin[amount]
    return coins_used[::-1]


# Common interface: every solver returns (coin_count, chosen_coins) or IMPOSSIBLE
def to_result(coins):
    if coins is None:
        return IMPOSSIBLE
    return (len(coins), coins)

def solve_greedy(denominations, target_amount):
    return to_result(greedy_largest_denomination_first(denominations, target_amount))

def solve_naive(denominations, target_amount):
    return to_result(naive_exact_recursive(denominations, target_amount))

def solve_top_down(denominations, target_amount):
    return to_result(top_down_dp_with_memoization(denominations, target_amount))

def solve_bottom_up(denominations, target_amount):
    return to_result(bottom_up_dp(denominations, target_amount))

EXACT_SOLVERS = {"naive": solve_naive, "top_down": solve_top_down, "bottom_up": solve_bottom_up}


# Independent checker: does NOT trust the solver's own count
def validate_solution(denominations, target_amount, result):
    if result == IMPOSSIBLE:
        return True
    coin_count, coins = result
    assert sum(coins) == target_amount, f"coins {coins} sum to {sum(coins)}, not {target_amount}"
    assert all(coin in denominations for coin in coins), f"coins {coins} use a denomination not in {denominations}"
    assert coin_count == len(coins), f"reported count {coin_count} but returned {len(coins)} coins"
    return True

def optimal_count(result):
    return None if result == IMPOSSIBLE else result[0]


class CoinChangeTestCase:
    def __init__(self, denominations, target_amount, expected_count):
        self.denominations = denominations
        self.target_amount = target_amount
        self.expected_count = expected_count     # None means IMPOSSIBLE

def coin_algorithm_validation():
    test_cases = [
        CoinChangeTestCase([1, 3, 4], 6, 2),            # 3+3 (greedy gives 4+1+1)
        CoinChangeTestCase([1, 2, 5], 11, 3),           # 5+5+1
        CoinChangeTestCase([1, 3, 4], 7, 2),            # 4+3
        CoinChangeTestCase([1], 0, 0),                  # target 0
        CoinChangeTestCase([1, 5, 10, 25], 0, 0),       # target 0
        CoinChangeTestCase([1, 5, 10, 25], 41, 4),      # 25+10+5+1
        CoinChangeTestCase([2, 5, 10, 1], 27, 4),       # unsorted input: 10+10+5+2
        CoinChangeTestCase([30, 40, 50], 10, None),     # impossible
        CoinChangeTestCase([2, 4], 7, None),            # impossible (odd target, even coins)
        CoinChangeTestCase([30, 40, 50], 100, 2),       # 50+50
        CoinChangeTestCase([1, 2, 3], 4, 2),            # multiple optima: 2+2 or 1+3
        CoinChangeTestCase([1, 5, 6], 10, 2),           # greedy gives 6+1+1+1+1, optimal is 5+5
    ]

    print(f"{BOLD}{UNDERLINE}Coin Change Hand Tests{RESET}\n")
    for case in test_cases:
        D, A = case.denominations, case.target_amount
        greedy = solve_greedy(D, A)
        validate_solution(D, A, greedy)
        print(f"D={D}, A={A}: expected count {case.expected_count}, greedy {greedy}")
        for name, solver in EXACT_SOLVERS.items():
            result = solver(D, A)
            validate_solution(D, A, result)
            assert optimal_count(result) == case.expected_count, f"{name} gave {result} for D={D}, A={A}"
            print(f"    {name:>9}: {result}")
    print("All hand tests passed\n")

    rng = random.Random(2050)   # seed for the random coin tests
    for x in range(100):
        # 1 is always included so every target is feasible
        denominations = [1] + sorted(rng.sample(range(2, 20), rng.randint(1, 4)))
        target_amount = rng.randint(0, 30)
        results = {name: solver(denominations, target_amount) for name, solver in EXACT_SOLVERS.items()}
        for result in results.values():
            validate_solution(denominations, target_amount, result)
        counts = {optimal_count(r) for r in results.values()}
        assert len(counts) == 1, f"Exact solvers disagree on D={denominations}, A={target_amount}: {results}"
    print("All 100 random exact-solver cross-checks passed\n")


def greedy_counterexample_search(max_coin=10, max_target=30, how_many=5):
    # Try every coin system {1, a, b} with 1 < a < b <= max_coin and every target up to max_target.
    # A counterexample is a target where greedy is feasible but uses more coins than bottom-up DP.
    found = []
    for a in range(2, max_coin + 1):
        for b in range(a + 1, max_coin + 1):
            denominations = [1, a, b]
            for target_amount in range(1, max_target + 1):
                greedy = solve_greedy(denominations, target_amount)
                exact = solve_bottom_up(denominations, target_amount)
                if greedy != IMPOSSIBLE and greedy[0] > exact[0]:
                    found.append((denominations, target_amount, greedy, exact))
                    break           # smallest failing target for this system, then move on
    print(f"{BOLD}{UNDERLINE}Greedy Counterexamples{RESET} ({len(found)} coin systems where greedy fails)")
    for denominations, target_amount, greedy, exact in found[:how_many]:
        print(f"D={denominations}, A={target_amount}: greedy {greedy[1]} ({greedy[0]} coins) vs optimal {exact[1]} ({exact[0]} coins)")
    assert any(D == [1, 3, 4] and A == 6 for D, A, g, e in found), "Sanity check failed: {1,3,4}, A=6 not found"
    print("Sanity check passed: D={1,3,4}, A=6 detected\n")


NAIVE_CALL_CUTOFF = 5_000_000   # safety cutoff: stop once naive recursion needs more calls than this

def part_2c1():
    denominations = [1, 3, 4]
    print(f"{BOLD}{UNDERLINE}Part 2C Experiment 1: D={denominations}, cutoff {NAIVE_CALL_CUTOFF:,} naive calls{RESET}")
    for target_amount in range(1, 100):
        Globals.recursive_calls = 0
        Globals.naive_states = set()
        naive_exact_recursive(denominations, target_amount, True)
        naive_calls, naive_states = Globals.recursive_calls, len(Globals.naive_states)

        Globals.recursive_calls = 0
        Globals.target_states_solved = 0
        Globals.memoization_cache_hits = 0
        top_down_dp_with_memoization(denominations, target_amount, {}, True)
        print(f"A={target_amount:>2}  naive calls={naive_calls:>10,}  naive states={naive_states:>3}  "
              f"memo calls={Globals.recursive_calls:>4}  memo states={Globals.target_states_solved:>3}  cache hits={Globals.memoization_cache_hits:>4}")
        if naive_calls > NAIVE_CALL_CUTOFF:
            print(f"Naive recursion exceeded the cutoff at A={target_amount}; stopping.\n")
            break

def part_2c2():
    denominations = [1, 5, 10, 25]    # k = 4, fixed
    print(f"{BOLD}{UNDERLINE}Part 2C Experiment 2: D={denominations}{RESET}")
    for exponent in range(8, 21):
        A = 2 ** exponent
        Globals.target_states_solved = 0
        bottom_up_dp(denominations, A, True)
        states = Globals.target_states_solved
        runtime = median_time(bottom_up_dp, denominations, A, reps=TIMING_REPS if exponent <= 16 else 3)
        print(f"A=2^{exponent:<2} = {A:>8}  bits={A.bit_length():>2}  states={states:>8}  "
              f"state*coin checks={states*len(denominations):>8}  median runtime={runtime:.5f}s")


if __name__ == "__main__":
    validation()
    inversion_benchmark()
    coin_algorithm_validation()
    greedy_counterexample_search()
    part_2c1()
    part_2c2()
