import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

def load_and_prep_data(file_path):
    df = pd.read_csv(file_path)
    df = df.dropna()
    
    # 1. Drop text ID columns to prevent memory crashes during get_dummies
    cols_to_drop = [col for col in ['client_id', 'client_name'] if col in df.columns]
    df = df.drop(columns=cols_to_drop)
    
    # 2. Select target column (defaults to the last column: ownership_opacity_score)
    target_col = df.columns[-1] 
    
    X = df.drop(columns=[target_col])
    
    # 3. Convert decimal targets to strings so SMOTE recognizes them as distinct classes
    y = df[target_col].astype(str) 
    
    # 4. Convert text categories (like country, sector) into numeric features
    X = pd.get_dummies(X, drop_first=True)
    
    # 5. Apply SMOTE to balance the dataset
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)
    
    # 6. Convert the string targets into integer codes (0, 1, 2) for the neural network
    y_resampled = pd.Categorical(y_resampled).codes
    
    # 7. Split the training and testing data
    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.2, random_state=42
    )
    
    # Return as float32 to prevent TensorFlow dtype mismatch errors
    return X_train.values.astype(np.float32), y_train.astype(np.float32), X_test.values.astype(np.float32), y_test.astype(np.float32)