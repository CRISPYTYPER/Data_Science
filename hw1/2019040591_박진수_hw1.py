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

    # For size 1 itemset
    itemset_count_dict = dict()  # itemset_count_dict = {}
    for transaction in transactions:  # loop the DB to get frequent 1-itemset
        for item in transaction:  # traverse each transaction
            itemset = tuple(item)  # transform an integer into a tuple ( 3 -> (3) )
            if itemset not in itemset_count_dict:  # if the itemset is not found as a key
                itemset_count_dict[itemset] = 1  # add the key and set the count to 1
            else:  # if the itemset is already in the dictionary
                itemset_count_dict[itemset] += 1  # add 1 to the value of the corresponding key
    frequent_itemset_list.append(itemset_count_dict)
    print(frequent_itemset_list)



