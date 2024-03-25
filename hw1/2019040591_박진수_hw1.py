import sys

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
    minimum_support = int(minimum_support_str) / 100 * num_of_transactions

    # 'transactions' variable is now such like [['7', '14'], ['9'], ['18', '2', '4', '5', '1']]
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
        for itemset_1 in frequent_itemset_list[k-1]:  # itemset_1 -> ('9',)
            for itemset_2 in frequent_itemset_list[k-1]:  # itemset_1 -> ('9',)
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


        # TODO: We need to remove the candidates in the set if the subset of each itemset is not frequent
        # 한국말로 써놓자면, L_k-1을 이용해서 합집합을 계산하여 C_k의 후보군을 구해놓았지만,
        # apriori 알고리즘의 핵심인, L_k-1에서 frequent하지 않은 것이 확인되었다면 이후에도 그것의 superset은 고려할 필요가 없다는 부분을 구현해야함.
        # keys_to_delete 라는 리스트에 이전 step에서 구한 frequent 하지 않은 itemset를 저장해 두었음
        pruned_candidate_itemsets = candidate_itemsets.copy()

        for itemset in candidate_itemsets:  # the item is sorted in ascending order. (ex. (6, 18))
            # frequent_itemset_list[k-1] == {(7,): 120, (14,): 128, (9,): 139}
            for itemset_to_delete in keys_to_delete:  # iterating keys_to_delete (ex. (6, ))
                if set(itemset_to_delete).issubset(set(itemset)):
                    pruned_candidate_itemsets.discard(itemset)  # remove the item if its subset is not frequent(apriori algorithm)

        print(len(pruned_candidate_itemsets))


        # 이제 pruned_condidate_itemsets에 pruned 완료된 candidates가 담겨있음.
        # 이제 DB-scan 작업 후, frequent하지 않은 itemset은 없애기


        # DB scan (DB: transactions)
        # count the support in DB
        itemset_count_dict = dict()  # itemset_count_dict = {}
        for transaction in transactions:  # loop the DB to get frequent 1-itemset
            transaction_set = set([int(item) for item in transaction])  # transform the string list into the set of integers
            for pruned_itemset in pruned_candidate_itemsets:
                if transaction_set.issuperset(pruned_itemset):  # if the pruned_itemset is the subset of transaction (frequency += 1)
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

        # termination condition. (Lk == NULL)
        if len(itemset_count_dict) == 0:
            break  # Finish the apriori algorithm

        frequent_itemset_list.append(itemset_count_dict)  # frequent_item_list[k] -> size k+1 itemset












