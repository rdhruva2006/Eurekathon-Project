import flwr as fl
import tensorflow as tf
from data_prep import load_and_prep_data

# Load data
X_train, y_train, X_test, y_test = load_and_prep_data("transaction and kyc.csv")

# Synchronized Architecture: 64 -> 32 -> 3 (Softmax)
model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(3, activation='softmax') 
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

class MaliciousClient(fl.client.NumPyClient):
    def get_parameters(self, config):
        return model.get_weights()

    def fit(self, parameters, config):
        model.set_weights(parameters)
        
        # Poisoning: Zero out weights to sabotage global model
        malicious_weights = [w * 0.0 for w in model.get_weights()]
        model.set_weights(malicious_weights)
        
        model.fit(X_train, y_train, epochs=1, batch_size=32, verbose=0)
        
        # Security: Sending a fake hash that the server will detect
        return model.get_weights(), len(X_train), {"hash": "invalid_fake_hash_string_12345"}

    def evaluate(self, parameters, config):
        model.set_weights(parameters)
        loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
        return loss, len(X_test), {"accuracy": accuracy}

if __name__ == "__main__":
    fl.client.start_client(
        server_address="10.1.36.200:9090", 
        client=MaliciousClient().to_client()
    )