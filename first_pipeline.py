import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from typing import Tuple, Annotated
from zenml import pipeline, step
import itertools

@step
def training_data_loader() -> Tuple[
    Annotated[pd.DataFrame, "X_train"],
    Annotated[pd.DataFrame, "X_test"],
    Annotated[pd.Series, "y_train"],
    Annotated[pd.Series, "y_test"],
]:
    """Load the iris dataset as tuple of Pandas DataFrame / Series."""
    iris = load_iris(as_frame=True)
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, shuffle=True, random_state=42
    )
    return X_train, X_test, y_train, y_test

@step(enable_cache=False)
def svc_trainer(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    gamma: float = 0.001,
    C: float = 1.0,
    kernel: str = 'rbf',
    degree: int = 3,
    num_support_vectors: int = 10,
    feature_scaling_factor: float = 1.0,
    use_optimization: bool = True
) -> float:
    """Train a sklearn SVC classifier and log to MLflow."""
    model = SVC(gamma=gamma, C=C, kernel=kernel, degree=degree)
    model.fit(X_train.to_numpy(), y_train.to_numpy())
    test_acc = model.score(X_test.to_numpy(), y_test.to_numpy())

    table = f"""
    +-------------------------------------------------------------------+
    | Test Parameters                                                   |       
    +-----------------------------------+-------------------------------+
    | Hyperparameters                   |                               |
    +-----------------------------------+-------------------------------+
    | gamma                             | {gamma:<37}                   
    | C                                 | {C:<37}                       
    | kernel                            | {kernel:<37}                  
    | degree                            | {degree:<37}                  
    +-----------------------------------+-------------------------------+
    | Other Parameters                  |                               |
    +-----------------------------------+-------------------------------+
    | num_support_vectors               | {num_support_vectors:<37}     
    | feature_scaling_factor            | {feature_scaling_factor:<37}  
    | use_optimization                  | {use_optimization:<37}        
    +-----------------------------------+-------------------------------+
    | Test Accuracy                     | {test_acc:<37}                
    +-------------------------------------------------------------------+
    """

    print(table)
    return test_acc



@pipeline
def my_pipeline():
    hyperparameter_combinations = [
        (0.001, 0.1, 'rbf', 2),
        (0.01, 1.0, 'poly', 3)
    ]  # Example hyperparameter combinations

    parameter_combinations = [
        (5, 0.5, True),
        (10, 1.0, False)
    ]  # Example parameter combinations

    X_train, X_test, y_train, y_test = training_data_loader()

    for gamma, C, kernel, degree in hyperparameter_combinations:
        for param_set in parameter_combinations:
            svc_trainer(
                X_train=X_train,
                X_test=X_test,
                y_train=y_train,
                y_test=y_test,
                gamma=gamma,
                C=C,
                kernel=kernel,
                degree=degree,
                num_support_vectors=param_set[0],
                feature_scaling_factor=param_set[1],
                use_optimization=param_set[2]
            )

if __name__ == "__main__":
    my_pipeline()
