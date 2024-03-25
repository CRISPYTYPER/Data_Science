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

    print(minimum_support)

    # {(3, 8, 16): 120, (1, 8, 16): 58}
    cnt = 0
    for transaction in transactions:
        int_transaction_set = set([int(item) for item in transaction])
        if ({6, 18}).issubset(int_transaction_set):
            cnt += 1
    print(cnt)