import random
import time
import math

class Globals:
    recursive_calls = 0
    target_states_solved = 0
    memoization_cache_hits = 0

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
    left_index = len(left_array)-1
    right_index = len(right_array)-1
    for i in range(len(array)):
        if right_index < 0 or (left_index >= 0 and left_array[left_index] > right_array[right_index]):
            Inversions += right_index + 1
            New_array[len(array)-i-1] = left_array[left_index]
            left_index -=1
        else:
            New_array[len(array)-i-1] = right_array[right_index]
            right_index -=1
    return New_array, Inversions

def brute_force_inversion(array):
    inversions = 0
    new_array = array.copy()
    for i in range(len(new_array)):
        for x in range(len(new_array)-1):
            if new_array[x] > new_array[x+1]:
                new_array[x], new_array[x+1] = new_array[x+1], new_array[x]
                inversions += 1
    return new_array, inversions

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
    inversions_got_brute = [brute_force_inversion(array)[1] for array in hand_crafted_arrays]
    print(inversions_got_brute)
    print(inversions_got_merge)
    print(inversions_got_merge==expected_inversions)
    print(inversions_got_brute==expected_inversions)
    random_arrays = [[random.randint(1,100) for i in range(100)]for x in range(200)]
    inversions_got_merge = [inv_count_merge(array)[1] for array in random_arrays]
    inversions_got_brute = [brute_force_inversion(array)[1] for array in random_arrays]
    print(inversions_got_merge==inversions_got_brute)

    different_n = [1,10,100,1_000,10_000,20_000]
    random_array = [[random.randint(1,100)for i in range(n)] for n in different_n]
    times_brute = []
    times_merge = []
    for array in random_array:
        start = time.time()
        inv_count_merge(array)
        times_merge.append(time.time()-start)
        start = time.time()
        brute_force_inversion(array)
        times_brute.append(time.time()-start)
    print(f"Brute Force Increase: {times_brute[-1]/times_brute[-2]}")
    print(f"Merge Sort Increase: {times_merge[-1]/times_merge[-2]}")
    print(f"Brute/Merge Ratio at n=20,000: {times_brute[-1]/times_merge[-1]}")


# coin change solvers (Part 2)
# coin denominations are given as an array of ascending integers, with the smallest denomination being 1
# the target amount is given as an integer greater than or equal to zero

# we make the assumption that the denominations are strictly increasing and start with 1



# 2A - Greedy Largest-Denomination First
def greedy_largest_denomination_first(denominations, target_amount):
    coins_used = []
    for coin in sorted(denominations, reverse=True):
    for coin in sorted(denominations, reverse=True):
        while target_amount >= coin:
            coins_used.append(coin)
            target_amount -= coin

    if (target_amount > 0):  # if we have a remaining amount that cannot be made with the given denominations, return None
        return None


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
                    Globals.target_states_solved += 1
    return best_solution

# 2A.C - Top-Down DP with Memoization
def top_down_dp_with_memoization(denominations, target_amount, mem=None, count_stuff = False):
    if mem is None:
        mem = {}
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
            if count_stuff == True:
                Globals.recursive_calls += 1
            if solution is not None:    # this means that a solution was found for the remainder, so we can add the current coin to the solution and check if it's better than the best solution found so far
                solution = solution + [coin]
                if best_solution is None or len(solution) < len(best_solution):     # if the best solution is None (i.e., no solution has been found yet) or if the current solution is better (i.e., uses fewer coins), update the best solution
                    best_solution = solution
                    if count_stuff == True:
                        Globals.target_states_solved += 1
    mem[target_amount] = best_solution
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
        for coin in denominations:
            if coin <= amount and min_coins[amount - coin] + 1 < min_coins[amount]:
                if count_stuff == True:
                    Globals.target_states_solved += 1
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
        CoinChangeTestCase([30, 40, 50], 100, [50, 50])  # Exact solution possible
    ]

    print(f"{BOLD}{UNDERLINE}Coin Change Algorithm Validation{RESET}\n")
    
    for test_case in test_cases:
        greedy_solution = greedy_largest_denomination_first(test_case.denominations, test_case.target_amount)
        naive_solution = naive_exact_recursive(test_case.denominations, test_case.target_amount)
        print(f"{BOLD}{UNDERLINE}Test Case: {test_case.target_amount} with denominations {test_case.denominations}{RESET}")
        print(f"Greedy solution for target {test_case.target_amount} with denominations {test_case.denominations}: {greedy_solution}")
        print(f"Naive solution for target {test_case.target_amount} with denominations {test_case.denominations}: {naive_solution}")
        print(f"Expected solution: {test_case.expected_solution}")
        print(f"Greedy correct: {greedy_solution == test_case.expected_solution}")
        print(f"Naive correct: {naive_solution == test_case.expected_solution}")

    # 100 random small test cases
    print(f"\n{BOLD}{UNDERLINE}Random Small Test Cases{RESET}\n")
    for x in range(100):
        # random denominations between 1 and 20, with 1 to 4 denominations, and we alaways include 1 as a denomination to ensure that a solution is always possible
        denominations = [1] + sorted(random.sample(range(2, 20), random.randint(1, 4)))
        target_amount = random.randint(10, 30)
        naive_solution = naive_exact_recursive(denominations, target_amount)
        top_down_solution = top_down_dp_with_memoization(denominations, target_amount)
        bottom_up_solution = bottom_up_dp(denominations, target_amount)
        print(f"{BOLD}{UNDERLINE}Random Test Case {x}: {target_amount} with denominations {denominations}{RESET}")
        print(f"Naive solution for target {target_amount} with denominations {denominations}: {naive_solution}")
        print(f"Top Down solution for target {target_amount} with denominations {denominations}: {top_down_solution}")
        print(f"Bottom Up solution for target {target_amount} with denominations {denominations}: {bottom_up_solution}")
        print(f"They all agree?: {naive_solution == top_down_solution and top_down_solution == bottom_up_solution}")
        if not (naive_solution == top_down_solution and top_down_solution == bottom_up_solution):
            print("help")
            raise SystemExit

def part_2c1():
    denominations = sorted(set([1]+[random.randint(1,10) for i in range(3)]+[random.randint(10,50) for i in range(3)]))
    print(denominations)
    target_num = 34
    sol = naive_exact_recursive(denominations, target_num, True)
    print("\n")
    print("Naive Recurssive")
    print(f"Target Number: {target_num}")
    print(f"Total Recursive Calls: {Globals.recursive_calls}")
    print(f"Total Target States Solved: {Globals.target_states_solved}")
    print(f"Solution: {sol}")

    Globals.recursive_calls = 0
    Globals.target_states_solved = 0
    sol = top_down_dp_with_memoization(denominations, target_num, {}, True)
    print("\n")
    print("Top Down with Memoization")
    print(f"Target Number: {target_num}")
    print(f"Total Recursive Calls: {Globals.recursive_calls}")
    print(f"Total Target States Solved: {Globals.target_states_solved}")
    print(f"Total Cache Hits: {Globals.memoization_cache_hits}")
    print(f"Solution: {sol}")
    Globals.recursive_calls = 0
    Globals.target_states_solved = 0
    Globals.memoization_cache_hits = 0

def part_2c2():
    print("\nPart 2c2")
    denominations = sorted(set([1]+[random.randint(1,10) for i in range(3)]+[random.randint(10,50) for i in range(3)]))
    print(f"Denominations: {denominations}")
    starting_a = 10
    for i in range(8):
        start = time.time()
        bottom_up_dp(denominations, starting_a**i, True)
        print(f"A: {starting_a**i}")
        print(f"Bit_length_A: {math.floor(math.log2(starting_a**i))+1}")
        print(f"Number of DP states processed: {Globals.target_states_solved}")
        print(f"Runtime: {time.time()-start}")
        print("")
        Globals.target_states_solved = 0


if __name__ == "__main__":
    random.seed(1)
    array = [random.randint(1,100000) for i in range(100)]
    start = time.time()
    new_array, inversions = inv_count_merge(array)
    print(time.time()-start)
    # print(array)
    # print(new_array)
    print(inversions)
    start = time.time()
    new_array, inversions = brute_force_inversion(array)
    print(time.time()-start)
    # print(array)
    # print(new_array)
    print(inversions)
    validation()
    coin_algorithm_validation()
    part_2c1()
    part_2c2()