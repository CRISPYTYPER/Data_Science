import math

# Helper function to load data from a file
def load_training_data(filename):
    """
        Read the data from the given filename.

        Parameters:
            filename (str): File name to read.
                ex. "dt_train.txt"
        Return:
            examples (dict): A list of dictionaries of each training data.
                ex. [{'age': '<=30', 'income': 'high', 'student': 'no', 'credit_rating': 'fair', 'Class:buys_computer': 'no'},...]
            feature_attributes (list): A list of feature names (except target).
                ex. ['age', 'income', 'student', 'credit_rating']
            target_attribute (str): A name of target attribute.
                ex. "Class:buys_computer"
    """
    with open(filename, 'r') as file:
        attributes = file.readline().strip().split('\t')
        examples = [dict(zip(attributes, line.strip().split('\t'))) for line in file]
        feature_attributes = attributes[:-1]
        target_attribute = attributes[-1]
        return examples, feature_attributes, target_attribute

# Main function to execute the workflow
def main(train_file, test_file, result_file):
    # Load training data
    train_data, feature_attributes, target_attribute = load_training_data(train_file)
    # Build a decision tree


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])




