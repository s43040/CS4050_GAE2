import random
import time

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



# 2A - Greedy Largest-Denomination First
def greedy_largest_denomination_first(denominations, target_amount):
    coins_used = []
    for coin in reversed(denominations):
        while target_amount >= coin:
            coins_used.append(coin)
            target_amount -= coin
    return coins_used

# 2B - Naive Exact Recursive Solution (slide 81 of Dynamic Programming I v2)
def naive_exact_recursive(denominations, target_amount):
    if target_amount == 0:      # base case: if the target amount is zero, return an empty list (no coins needed)
        return []
    if target_amount < 0:       # base case: if the target amount is negative, return None (no solution possible)
        return None
    best_solution = None        # initialize the best solution as None
    for coin in denominations:
        remainder = target_amount - coin
        solution = naive_exact_recursive(denominations, remainder)      #make the recursive call to find the solution for the remainder
        if solution is not None:                        # this means that a solution was found for the remainder, so we can add the current coin to the solution and check if it's better than the best solution found so far
            solution = [coin] + solution
            if best_solution is None or len(solution) < len(best_solution):     # if the best solution is None (i.e., no solution has been found yet) or if the current solution is better (i.e., uses fewer coins), update the best solution
                best_solution = solution
    return best_solution

# 2A.C - Top-Down DP with Memoization
def top_down_dp_with_memoization(denominations, target_amount, mem=None):
    if mem is None:
        mem = {}
    if target_amount == 0:      # base case: if the target amount is zero, return an empty list (no coins needed)
        return []
    if target_amount < 0:       # base case: if the target amount is negative, return None (no solution possible)
        return None
    if target_amount in mem:    # if the answer is already cached, reuse the earlier answer
        return mem[target_amount]

    best_solution = None        # initialize the best solution as None
    for coin in denominations:
            remainder = target_amount - coin
            solution = top_down_dp_with_memoization(denominations, target_amount, mem)  # make the recursive call to find the solution for the remainder
            if solution is not None:    # this means that a solution was found for the remainder, so we can add the current coin to the solution and check if it's better than the best solution found so far
                solution = [coin] + solution
                if best_solution is None or len(solution) < len(best_solution):     # if the best solution is None (i.e., no solution has been found yet) or if the current solution is better (i.e., uses fewer coins), update the best solution
                    best_solution = solution
    mem[target_amount] = best_solution
    return best_solution

# 2D - Bottom-Up DP
def bottom_up_DP():
    return 0

def coin_algorithm_validation():

    for denominations in [[1, 5, 10, 25, 50], [1, 3, 4], [1, 2, 5, 10]]:
    
        target_amounts = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        expected_solutions = [
            [],
            [1],
            [1,1],
            [1,1,1],
            [1,1,1,1],
            [5],
            [5,1],
            [5,1,1],
            [5,1,1,1],
            [5,1,1,1,1],
            [10],
            [10,1],
            [10,1,1],
            [10,1,1,1],
            [10,5],
            [10,5]
        ]
        for target_amount in target_amounts:
            greedy_solution = greedy_largest_denomination_first(denominations,target_amount)
            naive_solution = naive_exact_recursive(denominations,target_amount)
            expected_solution = expected_solutions[target_amount]
            print(f"Target Amount: {target_amount}")
            print(f"Greedy Solution: {greedy_solution}")
            print(f"Naive Solution: {naive_solution}")
            print(f"Expected Solution: {expected_solution}")
            print(f"Greedy Correct: {greedy_solution == expected_solution}")
            print(f"Naive Correct: {naive_solution == expected_solution}")
            print("")






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