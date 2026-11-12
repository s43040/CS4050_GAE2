import random
import time
import csv
import os

RESULTS_DIR = "results"     # all CSV output goes in this folder

def write_csv(filename, header, rows):
    # writes one CSV file into RESULTS_DIR; called after timing is finished so file I/O never affects measurements
    os.makedirs(RESULTS_DIR, exist_ok=True)
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"Wrote {path}")

def coins_to_str(coins):
    # stores a coin list in a single CSV cell, e.g. [4, 1, 1] -> "4 1 1"
    return "" if coins is None else " ".join(str(c) for c in coins)

class Globals:
    recursive_calls = 0
    target_states_solved = 0
    memoization_cache_hits = 0
    naive_states_seen = set()

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
                           [6,9,6,3,2,8],
                           [10,11,12,13,4,15]]
    expected_inversions = [3,
                           0,
                           3,
                           6,
                           0,
                           7,
                           0,
                           6,
                           9,
                           4]
    inversions_got_merge = [inv_count_merge(array)[1] for array in hand_crafted_arrays]
    inversions_got_brute = [brute_force_inversion(array) for array in hand_crafted_arrays]
    print(f"Inversions from brute force: {inversions_got_brute}")
    print(f"Inversions from merge: {inversions_got_merge}")
    assert inversions_got_merge==expected_inversions, "Inversions from merge is different than from expected"
    assert inversions_got_brute==expected_inversions, "Inversions from brute_force is different than from expected"
    random_arrays = [[random.randint(1,100) for i in range(100)]for x in range(200)]
    inversions_got_merge = [inv_count_merge(array)[1] for array in random_arrays]
    inversions_got_brute = [brute_force_inversion(array) for array in random_arrays]
    assert inversions_got_merge==inversions_got_brute, "Inversions and Brute Force do not match for the 200 random arrays in part 1B"

    for i in range(2,200):
        array = [random.randint(1,100) for n in range(i)]
        start = time.perf_counter()
        inv_count_merge(array)
        time_for_merge = time.perf_counter()-start
        start = time.perf_counter()
        brute_force_inversion(array)
        time_for_brute = time.perf_counter()-start
        if time_for_merge < time_for_brute:
            print(f"At size: {i}, merge beats brute force with time: {time_for_merge} vs brute time: {time_for_brute}")
            write_csv("inversion_crossover.csv",
                      ["n", "merge_seconds", "brute_seconds"],
                      [[i, time_for_merge, time_for_brute]])
            break

    different_n = [1,10,100,1_000,2_000,5_000,10_000,20_000]
    random_array = [[random.randint(1,100)for i in range(n)] for n in different_n]
    times_brute = []
    times_merge = []
    for array in random_array:
        start = time.perf_counter()
        inv_count_merge(array)
        times_merge.append(time.perf_counter()-start)
        start = time.perf_counter()
        brute_force_inversion(array)
        times_brute.append(time.perf_counter()-start)
    print(f"Brute Force Increase: {times_brute[-1]/times_brute[-2]}")
    print(f"Merge Sort Increase: {times_merge[-1]/times_merge[-2]}")
    print(f"Brute/Merge Ratio at n=20,000: {times_brute[-1]/times_merge[-1]}")
    write_csv("inversion_runtime.csv",
              ["n", "merge_seconds", "brute_seconds", "brute_over_merge"],
              [[n, tm, tb, tb / tm] for n, tm, tb in zip(different_n, times_merge, times_brute)])


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
    if target_amount == 0:      # base case: if the target amount is zero, return an empty list (no coins needed)
        return []
    if target_amount < 0:       # base case: if the target amount is negative, return None (no solution possible)
        return None
    best_solution = None        # initialize the best solution as None
    for coin in denominations:
        remainder = target_amount - coin
        solution = naive_exact_recursive(denominations, remainder, count_stuff)      #make the recursive call to find the solution for the remainder
        if count_stuff == True:
            Globals.recursive_calls += 1
        if solution is not None:                        # this means that a solution was found for the remainder, so we can add the current coin to the solution and check if it's better than the best solution found so far
            solution = solution + [coin]
            if best_solution is None or len(solution) < len(best_solution):     # if the best solution is None (i.e., no solution has been found yet) or if the current solution is better (i.e., uses fewer coins), update the best solution
                best_solution = solution
    if count_stuff == True:
        Globals.naive_states_seen.add(target_amount)   # this amount has now been fully solved
    return best_solution

# 2A.C - Top-Down DP with Memoization
# mem[a] stores (min coin count for a, last coin used) instead of a whole coin list, so each state does O(k) work
# and no lists are copied: O(kA) time, O(A) space. Recursive calls (is_top_level=False) return just the min count;
# the outermost call rebuilds the coin list once at the end in O(A).
def top_down_dp_with_memoization(denominations, target_amount, mem=None, count_stuff = False, is_top_level = True):
    if mem is None:
        mem = {}
    if target_amount == 0:      # base case: zero coins needed (empty list for the caller, count 0 for recursion)
        return [] if is_top_level else 0
    if target_amount < 0:       # base case: if the target amount is negative, return None (no solution possible)
        return None
    if target_amount in mem:    # if the answer is already cached, reuse the earlier answer
        if count_stuff == True:
            Globals.memoization_cache_hits += 1
        best = mem[target_amount]
    else:
        best = None             # best (count, last_coin) found so far
        for coin in denominations:
            remainder = target_amount - coin
            sub_count = top_down_dp_with_memoization(denominations, remainder, mem, count_stuff, False)  # min coins for the remainder
            if count_stuff == True:
                Globals.recursive_calls += 1
            if sub_count is not None and (best is None or sub_count + 1 < best[0]):   # using this coin last beats the best so far
                best = (sub_count + 1, coin)
        mem[target_amount] = best
        if count_stuff == True:
            Globals.target_states_solved += 1

    if not is_top_level:        # inside the recursion, only the count is needed
        return None if best is None else best[0]
    if best is None:            # no combination reaches the target
        return None

    # reconstruct one optimal solution by following the cached last coins back down to 0
    best_solution = []
    amount = target_amount
    while amount > 0:
        coin = mem[amount][1]
        best_solution.append(coin)
        amount -= coin
    return best_solution[::-1]

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


class CoinChangeTestCase:
    def __init__(self, denominations, target_amount, expected_solution):
        self.denominations = denominations
        self.target_amount = target_amount
        self.expected_solution = expected_solution

def coin_algorithm_validation():
    random.seed(2)
    # set up all the test cases
    test_cases = [
        CoinChangeTestCase([1, 3, 4], 6, [3, 3]),
        CoinChangeTestCase([1, 2, 5], 11, [5, 5, 1]),
        CoinChangeTestCase([1, 3, 4], 7, [4, 3]),
        CoinChangeTestCase([1], 0, []),
        CoinChangeTestCase([1, 5, 10, 25], 0, []),
        CoinChangeTestCase([1, 5, 10, 25], 1, [1]),
        CoinChangeTestCase([1, 5, 10, 25], 41, [25, 10, 5, 1]),
        CoinChangeTestCase([2, 5, 10, 1], 27, [10, 10, 5, 2]),
        CoinChangeTestCase([30, 40, 50], 10, None),  # No solution possible
        CoinChangeTestCase([30, 40, 50], 100, [50, 50]),  # Exact solution possible
        CoinChangeTestCase([1,3,4,5], 8, [4,4])  # Exact solution possible
    ]

    print(f"{BOLD}{UNDERLINE}Coin Change Algorithm Validation{RESET}\n")
    
    for test_case in test_cases:
        greedy_solution = greedy_largest_denomination_first(test_case.denominations, test_case.target_amount)
        naive_solution = naive_exact_recursive(test_case.denominations, test_case.target_amount)
        top_down_solution = top_down_dp_with_memoization(test_case.denominations, test_case.target_amount)
        bottom_up_solution = bottom_up_dp(test_case.denominations, test_case.target_amount)
        print(f"{BOLD}{UNDERLINE}Test Case: {test_case.target_amount} with denominations {test_case.denominations}{RESET}")
        print(f"Greedy solution for target {test_case.target_amount} with denominations {test_case.denominations}: {greedy_solution}")
        print(f"Naive solution for target {test_case.target_amount} with denominations {test_case.denominations}: {naive_solution}")
        print(f"Top Down solution for target {test_case.target_amount} with denominations {test_case.denominations}: {top_down_solution}")
        print(f"Bottom Up solution for target {test_case.target_amount} with denominations {test_case.denominations}: {bottom_up_solution}")
        print(f"Expected solution: {test_case.expected_solution}")
        print(f"Greedy correct: {greedy_solution == test_case.expected_solution or len(greedy_solution) == len(test_case.expected_solution)}")
        assert naive_solution == test_case.expected_solution or len(naive_solution) == len(test_case.expected_solution), "Naive Incorrect"
        assert top_down_solution == test_case.expected_solution or len(top_down_solution) == len(test_case.expected_solution), "Top Down Incorrect"
        assert bottom_up_solution == test_case.expected_solution or len(bottom_up_solution) == len(test_case.expected_solution), "Bottom Up Incorrect"

    # 100 random small test cases
    print(f"\n{BOLD}{UNDERLINE}Random Small Test Cases{RESET}\n")
    for x in range(100):
        # random denominations between 1 and 20, with 1 to 4 denominations, and we alaways include 1 as a denomination to ensure that a solution is always possible
        denominations = [1] + sorted(random.sample(range(2, 20), random.randint(1, 4)))
        target_amount = random.randint(10, 30)
        naive_solution = naive_exact_recursive(denominations, target_amount)
        top_down_solution = top_down_dp_with_memoization(denominations, target_amount)
        bottom_up_solution = bottom_up_dp(denominations, target_amount)
        greedy_solution = greedy_largest_denomination_first(denominations, target_amount)
        assert sum(naive_solution) == target_amount, f"Niave solution got: {sum(naive_solution)}, when target amount is: {target_amount}"
        assert sum(top_down_solution) == target_amount, f"Top Down solution got: {sum(top_down_solution)}, when target amount is: {target_amount}"
        assert sum(bottom_up_solution) == target_amount, f"Bottom Up solution got: {sum(bottom_up_solution)}, when target amount is: {target_amount}"
        print(f"{BOLD}{UNDERLINE}Random Test Case {x}: {target_amount} with denominations {denominations}{RESET}")
        print(f"Naive solution for target {target_amount} with denominations {denominations}: {naive_solution}")
        print(f"Top Down solution for target {target_amount} with denominations {denominations}: {top_down_solution}")
        print(f"Bottom Up solution for target {target_amount} with denominations {denominations}: {bottom_up_solution}")
        print(f"They all agree?: {len(naive_solution) == len(top_down_solution) and len(top_down_solution) == len(bottom_up_solution)}")
        assert len(naive_solution) == len(top_down_solution) == len(bottom_up_solution), \
            f"Naive, top-down and bottom-up disagree for denominations {denominations}, target {target_amount}"
        if greedy_solution != None and len(greedy_solution) > len(top_down_solution):
            print(f"Greedy works but is not optimal. Target: {target_amount}, denominations: {denominations}, solution: {greedy_solution}")

def part_2c1():
    random.seed(3)
    denominations = sorted(set([1]+[random.randint(1,10) for i in range(3)]+[random.randint(10,50) for i in range(3)]))
    print(f"Denominations for part 2c1: {denominations}")
    # target_num = 34
    rows = []   # one CSV row per target amount
    for i in range(1,25):
        sol = naive_exact_recursive(denominations, i, True)
        naive_calls = Globals.recursive_calls
        naive_states = len(Globals.naive_states_seen)
        print("\n")
        print(f"{BOLD}{UNDERLINE}Test calls with target amount: {i} with denominations {denominations}{RESET}")
        print(f"Target Number: {i}")
        print("Naive Recurssive")
        print(f"Total Recursive Calls: {Globals.recursive_calls}")
        print(f"Total Target States Solved: {len(Globals.naive_states_seen)}")
        print(f"Solution: {sol}")

        Globals.recursive_calls = 0
        Globals.naive_states_seen.clear()
        sol = top_down_dp_with_memoization(denominations, i, {}, True)
        print("Top Down with Memoization")
        print(f"Total Recursive Calls: {Globals.recursive_calls}")
        print(f"Total Target States Solved: {Globals.target_states_solved}")
        print(f"Total Cache Hits: {Globals.memoization_cache_hits}")
        print(f"Solution: {sol}")
        rows.append([coins_to_str(denominations), i, naive_calls, naive_states,
                     Globals.recursive_calls, Globals.target_states_solved, Globals.memoization_cache_hits,
                     len(sol), coins_to_str(sol)])
        Globals.recursive_calls = 0
        Globals.target_states_solved = 0
        Globals.memoization_cache_hits = 0
    write_csv("experiment1_repeated_subproblems.csv",
              ["denominations", "A", "naive_recursive_calls", "naive_distinct_states",
               "topdown_recursive_calls", "topdown_distinct_states", "topdown_cache_hits",
               "optimal_coin_count", "solution"],
              rows)

def part_2c2():
    random.seed(4)
    print("\nPart 2c2")
    denominations = sorted(set([1]+[random.randint(1,10) for i in range(3)]+[random.randint(10,50) for i in range(3)]))
    print(f"Denominations: {denominations}")
    starting_a = 2
    rows = []   # one CSV row per A
    for i in range(8,20):
        start = time.perf_counter()
        bottom_up_dp(denominations, starting_a**i, True)
        runtime = time.perf_counter()-start     # measured right after the call so printing isn't timed
        print(f"A: {starting_a**i}")
        print(f"Bit_length_A: {(starting_a**i).bit_length()}")
        print(f"Number of DP states processed: {Globals.target_states_solved}")
        print(f"Runtime: {runtime}")
        print("")
        rows.append([coins_to_str(denominations), starting_a**i, (starting_a**i).bit_length(),
                     Globals.target_states_solved, runtime])
        Globals.target_states_solved = 0
    write_csv("experiment2_pseudo_polynomial.csv",
              ["denominations", "A", "bit_length_A", "dp_states_processed", "runtime_seconds"],
              rows)

def greedy_counterexample_search(max_coin=10, max_target=30, needed=3):
    # Searches every coin system {1, a, b} with 1 < a < b <= max_coin and every target 1..max_target.
    # A counterexample is a case where greedy finds a solution but uses more coins than the exact optimum
    # (bottom_up_dp is the ground truth). We keep one counterexample per coin system: the smallest failing target.
    counterexamples = []    # each entry: (denominations, target, greedy_coins, optimal_coins)
    for a in range(2, max_coin + 1):
        for b in range(a + 1, max_coin + 1):
            denominations = [1, a, b]
            for target in range(1, max_target + 1):
                greedy_solution = greedy_largest_denomination_first(denominations, target)
                optimal_solution = bottom_up_dp(denominations, target)
                if greedy_solution is not None and len(greedy_solution) > len(optimal_solution):
                    counterexamples.append((denominations, target, greedy_solution, optimal_solution))
                    break   # smallest failing target found for this system, move on to the next system

    print(f"\n{BOLD}{UNDERLINE}Greedy Counterexample Search{RESET}\n")
    print(f"Searched coin systems {{1, a, b}} with b <= {max_coin} and targets 1..{max_target}")
    print(f"Found {len(counterexamples)} coin systems where greedy is not optimal:")
    for denominations, target, greedy_solution, optimal_solution in counterexamples:
        print(f"D={denominations}, A={target}: greedy {greedy_solution} ({len(greedy_solution)} coins) "
              f"vs optimal {optimal_solution} ({len(optimal_solution)} coins)")

    # required sanity check from the assignment: D={1,3,4}, A=6 must be detected
    assert any(d == [1, 3, 4] and t == 6 for d, t, _, _ in counterexamples), "Search failed to detect D={1,3,4}, A=6"
    assert len(counterexamples) >= needed, f"Fewer than {needed} distinct counterexamples found"
    write_csv("greedy_counterexamples.csv",
              ["denominations", "A", "greedy_coins", "greedy_count", "optimal_coins", "optimal_count"],
              [[coins_to_str(d), t, coins_to_str(g), len(g), coins_to_str(o), len(o)]
               for d, t, g, o in counterexamples])
    return counterexamples

if __name__ == "__main__":
    random.seed(1)
    array = [random.randint(1,100000) for i in range(100)]
    new_array, inversions = inv_count_merge(array)
    print(inversions)
    inversions = brute_force_inversion(array)
    print(inversions)
    validation()
    coin_algorithm_validation()
    part_2c1()
    part_2c2()
    greedy_counterexample_search()