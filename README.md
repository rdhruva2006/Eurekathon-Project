[Eurekathon-Project_README.md](https://github.com/user-attachments/files/29559575/Eurekathon-Project_README.md)
# Federated Fraud Detection Dashboard

A federated learning system for market-manipulation and fraud detection that trains a shared model across distributed client nodes — without any client ever exposing its raw transaction data — and defends against poisoning attacks from malicious nodes.

Built at Eurekathon 2025 (24-hour hackathon).

## Architecture

- **`server_app.py`** — Flower (`flwr`) federated learning server running a custom `SecureFedAvg` strategy.
- **`client_app.py`** — A legitimate client: trains a local Keras model on transaction/KYC data and reports back a SHA-256 hash of its weights for integrity verification.
- **`malicious_client_app.py`** — An adversarial client that simulates a data-poisoning attack (zeroes out its weights before submitting) and sends a spoofed hash — used to test the server's defenses.
- **`data_prep.py`** — Loads and preprocesses the transaction/KYC dataset (SMOTE oversampling for class balance).
- **`app.py`** — Real-time Streamlit dashboard for monitoring the system.

## How it works

1. **Federated training**: each client trains a local neural network (`64 → 32 → 3`, softmax output) on its own transaction data for one epoch per round, then sends only the updated weights (not the data) to the server.
2. **Integrity verification**: every client computes a SHA-256 hash of its own weight update and reports it alongside the update.
3. **Poisoning defense**: the server's `SecureFedAvg` strategy checks each incoming hash. Updates with a known-bad or malformed hash are **quarantined and excluded** from aggregation, while all rounds (accepted and quarantined) are logged to `training_metrics.csv` for auditability.
4. **Live dashboard**: the Streamlit app shows real-time system health (CPU/RAM), a simulated incoming transaction feed, a rule-based fraud engine (flags high cancellation rates as potential spoofing), a "Red Team" console to trigger a simulated poisoning attack, and an explainable feature-impact chart showing why a transaction was flagged.

## Tech Stack

- **Federated Learning**: Flower (`flwr`), TensorFlow/Keras
- **Data**: pandas, NumPy, `imbalanced-learn` (SMOTE)
- **Dashboard**: Streamlit, Plotly, `psutil`
- **Explainability**: SHAP-style feature-impact visualization
- **Classical ML (dashboard demo)**: scikit-learn RandomForestClassifier

## Running Locally

```bash
pip install flwr tensorflow pandas numpy imbalanced-learn streamlit plotly psutil scikit-learn

# Terminal 1 — start the server
python server_app.py

# Terminal 2 — start a legitimate client
python client_app.py

# Terminal 3 — start an adversarial client (optional, to test defenses)
python malicious_client_app.py

# Dashboard
streamlit run app.py
```

## Status

Hackathon prototype. Dataset (`transaction and kyc.csv`) is used for local demo purposes only.
