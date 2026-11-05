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