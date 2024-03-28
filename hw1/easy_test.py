from itertools import combinations

def divide_into_two_subsets(itemset_tuple):
    """
    Divide a tuple into all possible two disjoint subsets.

    Parameters:
        itemset_tuple (tuple): A tuple representing an itemset.
    Return:
        list: A list of tuples, each consists of two disjoint subsets of the input itemset.
    """

    all_subsets = set(itemset_tuple)
    result = []

    # Generate all combinations of length 1 to len(itemset_tuple)-`
    for i in range(1, len(itemset_tuple)):
        # Generate all combinations of length i
        for subset in combinations(itemset_tuple, i):
            # Add the partition to the result
            result.append((set(subset), all_subsets - set(subset)))
    return result

item_tuple = divide_into_two_subsets((1,3,5))
print(item_tuple)