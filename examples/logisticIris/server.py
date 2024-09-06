# server.py
import flwr as fl

# Define strategy (FedAvg is the default strategy)
strategy = fl.server.strategy.FedAvg(
    min_fit_clients=2,  # Minimum number of clients to participate in each round
    min_available_clients=2,  # Minimum number of clients in the system
)

# Start Flower server
if __name__ == "__main__":
    fl.server.start_server(
        server_address="10.128.15.214:8080",  # Internal IP address of the server
        config={"num_rounds": 5},  # Specify how many federated learning rounds you want to run
        strategy=strategy,
    )

