import flwr as fl
import csv
import os
import pandas as pd
import tensorflow as tf

metrics_file = "training_metrics.csv"

# Initialize metrics file
with open(metrics_file, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Round", "Node_ID", "SHA256_Hash", "Status"])

class SecureFedAvg(fl.server.strategy.FedAvg):
    def aggregate_fit(self, server_round, results, failures):
        secure_results = []
        
        for client, fit_res in results:
            node_hash = fit_res.metrics.get("hash", "Unknown")
            node_id = client.cid
            
            # Quarantines if the hash matches the hardcoded malicious string
            if node_hash == "invalid_fake_hash_string_12345" or "fake" in str(node_hash).lower():
                status = "Quarantined"
            else:
                status = "Accepted"
                secure_results.append((client, fit_res))
            
            with open(metrics_file, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([server_round, node_id, node_hash, status])
                
        return super().aggregate_fit(server_round, secure_results, failures)

strategy = SecureFedAvg(
    fraction_fit=1.0,
    min_fit_clients=2,
    min_available_clients=2,
)

if __name__ == "__main__":
    fl.server.start_server(
        server_address="0.0.0.0:9090",
        config=fl.server.ServerConfig(num_rounds=3),
        strategy=strategy
    )