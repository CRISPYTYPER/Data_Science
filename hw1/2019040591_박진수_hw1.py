import sys
from itertools import combinations

def get_frequent_itemset_list(transactions, minimum_support) :
    """
        Generates frequent itemsets from transactional data using the Apriori algorithm.

        Parameters:
        transactions (list): A list of transactions(DB), where each transaction is represented as a list of items.
        Be aware that each element in a transaction is string (ex. '7')
        minimum_support (float): Minimum support with percentage (ex. 50.0)
        Return:
        list: A list of frequent itemsets discovered from the transactional data.
        ex) [{(16,): 212, (3,): 150, (8,): 226}, {(8, 16): 151}]
    """

    frequent_itemset_list = []  # list of dictionaries, each element in index i has itemset of length (i+1)

    # For size 1 itemset, make C1 (candidates)
    itemset_count_dict = dict()  # itemset_count_dict = {}
    for transaction in transactions:  # loop the DB to get frequent 1-itemset
        for item in transaction:  # traverse each transaction
            item = int(item)  # convert string into int type
            itemset = tuple([item])  # transform an integer into a tuple ( 3 -> (3,) )
            if itemset not in itemset_count_dict:  # if the itemset is not found as a key
                itemset_count_dict[itemset] = 1  # add the key and set the count to 1
            else:  # if the itemset is already in the dictionary
                itemset_count_dict[itemset] += 1  # add 1 to the value of the corresponding key

    # print(itemset_count_dict)

    # Now, let's find the frequent candidates (support >= minimum_support)

    # Find the keys that are not frequent, and put them(keys) into the list.
    keys_to_delete = []
    for key in itemset_count_dict:
        if itemset_count_dict[key] < minimum_support:  # delete itemsets which are not frequent.
            keys_to_delete.append(key)
    # Delete keys in the dictionary that are not frequent.
    for key in keys_to_delete:
        del itemset_count_dict[key]
    frequent_itemset_list.append(itemset_count_dict)  # frequent_item_list[0] -> size 1 itemset
    # print(frequent_itemset_list[0])
    # K = 1 done (made L_1)

    k = 1  # variable for iteration
    while True:
        # Make candidates (C_k+1) generated from L_k
        candidate_itemsets = set()
        for itemset_1 in frequent_itemset_list[k - 1]:  # itemset_1 -> ('9',)
            for itemset_2 in frequent_itemset_list[k - 1]:  # itemset_1 -> ('9',)
                # change tuple into set
                itemset_1 = set(itemset_1)
                itemset_2 = set(itemset_2)

                # union itemset in L_k to make the candidates
                union_set = itemset_1.union(itemset_2)

                # change the unioned set into a list. (To make it ascendent)
                union_set_list = sorted(union_set)

                # verify the length, and add into the candidate_itemsets
                if len(union_set_list) == k + 1:
                    candidate_itemsets.add(tuple(union_set_list))

        # 한국말로 써놓자면, L_k-1을 이용해서 합집합을 계산하여 C_k의 후보군을 구해놓았지만,
        # apriori 알고리즘의 핵심인, L_k-1에서 frequent하지 않은 것이 확인되었다면 이후에도 그것의 superset은 고려할 필요가 없다는 부분을 구현해야함.
        # keys_to_delete 라는 리스트에 이전 step에서 구한 frequent 하지 않은 itemset를 저장해 두었음
        pruned_candidate_itemsets = candidate_itemsets.copy()

        for itemset in candidate_itemsets:  # the item is sorted in ascending order. (ex. (6, 18))
            # frequent_itemset_list[k-1] == {(7,): 120, (14,): 128, (9,): 139}
            for itemset_to_delete in keys_to_delete:  # iterating keys_to_delete (ex. (6, ))
                if set(itemset_to_delete).issubset(set(itemset)):
                    pruned_candidate_itemsets.discard(
                        itemset)  # remove the item if its subset is not frequent(apriori algorithm)

        # print(len(pruned_candidate_itemsets))

        # Now, pruned_condidate_itemsets contain pruned candidates.
        # Also, need to remove unfrequent itemsets after DB-scan.

        # DB scan (DB: transactions)
        # count the support in DB
        itemset_count_dict = dict()  # itemset_count_dict = {}
        for transaction in transactions:  # loop the DB to get frequent 1-itemset
            transaction_set = set(
                [int(item) for item in transaction])  # transform the string list into the set of integers
            for pruned_itemset in pruned_candidate_itemsets:
                if set(pruned_itemset).issubset(
                        transaction_set):  # if the pruned_itemset is the subset of transaction (frequency += 1)
                    if pruned_itemset not in itemset_count_dict:  # if the itemset is not found as a key
                        itemset_count_dict[pruned_itemset] = 1  # add the key and set the count to 1
                    else:  # if the itemset is already in the dictionary
                        itemset_count_dict[pruned_itemset] += 1  # add 1 to the value of the corresponding key

        # Delete not frequent ones!
        # Find the keys that are not frequent, and put them(keys) into the list.
        keys_to_delete = []  # empty the list before adding
        for key in itemset_count_dict:
            if itemset_count_dict[key] < minimum_support:  # delete itemsets which are not frequent.
                keys_to_delete.append(key)
        # Delete keys in the dictionary that are not frequent.
        for key in keys_to_delete:
            del itemset_count_dict[key]

        # termination condition. (L_k == NULL)
        if len(itemset_count_dict) == 0:
            break  # Finish the apriori algorithm

        frequent_itemset_list.append(itemset_count_dict)  # frequent_item_list[k] -> size k+1 itemset
        k += 1  # same as i++ in for-loop
    # # for test
    # for frequent_itemset in frequent_itemset_list:
    #     print(frequent_itemset)
    return frequent_itemset_list  # ex) [{(16,): 212, (3,): 150, (8,): 226}, {(8, 16): 151}]

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

    # i from 1 to len(itemset_tuple)-1`
    for i in range(1, len(itemset_tuple)):
        # Generate all combinations(tuple) of length i (from 1 to len(itemset_tuple)-1)
        for subset in combinations(itemset_tuple, i):
            # Add the partition to the result list
            result.append((set(subset), all_subsets - set(subset)))
    return result

def get_association_rules_list(frequent_itemset_list, transactions_length):
    """
        Return a list of all association rules

        Parameters:
            frequent_itemset_list (list): A list of frequent itemsets discovered from the transactional data.
                ex) [{(16,): 212, (3,): 150, (8,): 226}, {(8, 16): 151}]
            transactions_length (int): A number of transactions of the input file.
        Return:
            list: A list of all association rules. Each row is like this -> [(2,), (4,), 8.6, 32.58]
        """
    result_list = []
    for i in range(1, len(frequent_itemset_list)): # start from 1 to start from length-2 itemsets
        itemset_count_dict = frequent_itemset_list[i]  # itemset_count_dict == {(3, 8, 16): 120, (1, 8, 16): 58}
        # iterate over the dictionary
        for itemset, support in itemset_count_dict.items():  # itemset is a key of the dict
            # now, divide each itemset into two disjoint subsets
            # Derive association rule using the result of divide_into_two_subsets
            divided_sets_list = divide_into_two_subsets(itemset)
            for pair in divided_sets_list:  # pair == ({1}, {5})
                sub_itemset = pair[0]  # divided first sub-itemset. {1} from {1, 5}
                sub_associative_itemset = pair[1]  # divided second sub_itemset {5} from {1, 5}
                sub_itemset_tuple = tuple(sorted(sub_itemset))  # transform into ascendent tuple
                sub_associative_itemset_tuple = tuple(sorted(sub_associative_itemset))  # transform into ascendent tuple

                sub_itemset_support = frequent_itemset_list[len(sub_itemset)-1][sub_itemset_tuple]
                sub_associative_itemset_support = frequent_itemset_list[len(sub_associative_itemset)-1][sub_associative_itemset_tuple]
                # print(sub_itemset_support)
                # print(sub_associative_itemset_support)

                # All pairs share same support, since their unions are the same. (Originated from the same set)
                # make a list that will be an element of the result_list.
                each_row_list = []
                each_row_list.append(sub_itemset_tuple)
                each_row_list.append(sub_associative_itemset_tuple)
                each_row_list.append(round((support / transactions_length) * 100, 2)) # support
                each_row_list.append(round((support / sub_itemset_support) * 100, 2))  #confidence
                result_list.append(each_row_list)
    # print(result_list)
    return result_list



if __name__ == '__main__':
    # Argument num checking
    if len(sys.argv) != 4:
        print("<ERROR> Please input three arguments!")
        sys.exit()
    minimum_support_str = sys.argv[1]  # 10(%)
    input_file_name = sys.argv[2]  # input.txt
    output_file_name = sys.argv[3]  # output.txt

    # Open the file to read
    with open(input_file_name, 'r') as file:
        # Initialize empty list to store transactions
        transactions = []

        # Iterate over each line to read each transaction(item_id's)
        for line in file:
            # Split the line into item IDs with ('\t') as a delimiter
            item_ids = line.strip().split('\t')
            # Add each transaction into the list "transactions"
            transactions.append(item_ids)

    # number of transactions (used to calculate minimum support)
    num_of_transactions = len(transactions)

    # minimum support (counts) -> 500 * 10% = 50.0
    minimum_support = float(minimum_support_str) / 100 * num_of_transactions   # minimum support input can be a float type

    # 'transactions' variable is now such like [['7', '14'], ['9'], ['18', '2', '4', '5', '1']]
    # get frequent itemset list using apriori algorithm. Index 0 refers to L_1
    frequent_itemset_list = get_frequent_itemset_list(transactions, minimum_support)  # frequent_itemset_list == [{(16,): 212, (3,): 150, (8,): 226}, {(8, 16): 151}]
    # print(frequent_itemset_list)
    # find association rules for each frequent itemset, and put it into the list.
    association_rules_list = get_association_rules_list(frequent_itemset_list, num_of_transactions)

    # Open the file to write
    with open(output_file_name, 'w') as file:
        for row in association_rules_list:  # iterate over rows
            file.write("{" + ",".join(str(item) for item in row[0]) + "}\t")  # item_set
            file.write("{" + ",".join(str(item) for item in row[1]) + "}\t")  # associative_item_set
            file.write("%.2f\t" %row[2])  # support
            file.write("%.2f\n" %row[3])  # confidence






