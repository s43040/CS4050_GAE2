# 2A.C - Top-Down DP with Memoization
# uses the same recurrence as 2A.B but caches each target amount the first time it is solved and stores that in mem
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

# 2A.D - Bottom-Up DP
# compute optimal values for amounts 0,1,...,A in increasing order and store enough information to reconstruct an optimal solution
def bottom_up_dp(denominations, target_amount):
    # first compute the optimal values
    INFINITY = float("inf")
    min_coins = [INFINITY] * (target_amount + 1)    # min_coins[a] = OPT(a), initialize to infinity to make optimization easy
    last_coin = [0] * (target_amount + 1)           # last_coin[a] is a coin used in OPT(a), which we can use for reconstruction
    min_coins[0] = 0                                # base case: zero coins sum up to amount zero
    for amount in range(1, target_amount + 1):      # compute OPT(a) for 0,1,...,A in increasing order
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
        amount -= last_coin
    return coins_used