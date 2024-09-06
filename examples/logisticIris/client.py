# client.py
import argparse
import flwr as fl
from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import time

from typing import Dict, List, Tuple

# Parse command-line arguments for partition-id
parser = argparse.ArgumentParser(description="Flower Client")
parser.add_argument("--partition-id", type=int, required=True, help="Partition ID for the client")
args = parser.parse_args()

# Load and partition the Iris dataset
def load_partition(partition_id, num_partitions):
    """Split the Iris dataset into 'num_partitions' and return the data for a specific partition."""
    data = datasets.load_iris()
    X, y = data.data, data.target
    
    # Shuffle and partition the data
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    partition_size = len(X) // num_partitions
    partition_start = partition_id * partition_size
    partition_end = partition_start + partition_size

    # Assign the specific partition to the client
    X_part = X[indices[partition_start:partition_end]]
    y_part = y[indices[partition_start:partition_end]]

    return train_test_split(X_part, y_part, test_size=0.2, random_state=42)

# Define a Flower client
class IrisClient(fl.client.NumPyClient):
    def __init__(self, partition_id):
        self.model = LogisticRegression(max_iter=100)
        self.start_time = time.time()  # Record the start time
        
        # Load partitioned data
        self.X_train, self.X_test, self.y_train, self.y_test = load_partition(partition_id, num_partitions=5)

    def get_parameters(self, config: Dict[str, str]) -> List[np.ndarray]:
        return [self.model.coef_, self.model.intercept_]

    def set_parameters(self, parameters):
        self.model.coef_ = parameters[0]
        self.model.intercept_ = parameters[1]

    def fit(self, parameters, config: Dict[str, str]):
        # Set model parameters before fitting
        self.set_parameters(parameters)
        
        # Train the model on the local partition
        self.model.fit(self.X_train, self.y_train)
        
        # Return updated model parameters and the number of samples
        return self.get_parameters(config={}), len(self.X_train), {}

    def evaluate(self, parameters, config: Dict[str, str]):
        # Set model parameters before evaluating
        self.set_parameters(parameters)
        
        # Evaluate the model on the test set
        y_pred = self.model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_pred)
        
        # Calculate the time elapsed since the start of training
        elapsed_time = time.time() - self.start_time
        
        # Print the accuracy and time taken after every round
        print(f"Client {args.partition_id} - Accuracy: {accuracy:.4f}, Time Elapsed: {elapsed_time:.2f} seconds")
        
        # Return the loss and accuracy
        loss = -accuracy  # Loss is negative accuracy
        return loss, len(self.X_test), {"accuracy": accuracy}

# Start Flower client with the provided partition-id
if __name__ == "__main__":
    partition_id = args.partition_id
    fl.client.start_numpy_client(server_address="10.128.15.214:8080", client=IrisClient(partition_id))

