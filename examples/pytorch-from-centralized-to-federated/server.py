"""Flower server example."""

from typing import List, Tuple

import flwr as fl
from flwr.common import Metrics
import time


from flwr.common.logger import log
from logging import INFO, DEBUG





class CustomFlowerServer(fl.server.Server):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cumulative_time = 0
        self.round_start_time = None

    def fit(self, *args, **kwargs):
        self.round_start_time = time.time()  # Record start time
        result = super().fit(*args, **kwargs)
        round_end_time = time.time()  # Record end time

        # Calculate and log round time
        round_time = round_end_time - self.round_start_time
        self.cumulative_time += round_time

        
        return result
        
    def evaluate(self, *args, **kwargs):
        result = super.evaluate(*args, **kwargs)
        log(INFO, "test printout, server")
        
        return result




# Define strategy


client_manager = fl.server.client_manager.SimpleClientManager()

# Create a server instance
server = CustomFlowerServer(client_manager=client_manager)


# Start Flower server
fl.server.start_server(
    server_address="10.128.15.195:8080",
    config=fl.server.ServerConfig(num_rounds=30),
    server = server
)
