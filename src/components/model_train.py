import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from xgboost import XGBRegressor

from src.pipeline.exception import CustomException
from src.pipeline.logger import logging
from src.pipeline.utils import evaluate_models, save_object


@dataclass
class ModelTrainConfig:
    trained_model_file_path = os.path.join("artifacts", "trained_model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_train_config = ModelTrainConfig()

    def initiate_model_trainer(self, train_array, test_array, preprocessor_path):
        try:
            logging.info("Split the train and test data")
            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "KNN": KNeighborsRegressor(),
                "XGBoost": XGBRegressor(),
                "CatBoost": CatBoostRegressor(verbose=False),
                "AdaBoost": AdaBoostRegressor(),
            }

            model_report: dict = evaluate_models(
                x_train=x_train,
                y_train=y_train,
                x_test=x_test,
                y_test=y_test,
                models=models,
            )

            #! To get the best model score from the dict
            best_model_score = max(model_report.values())

            #! To get the best model name
            best_model_name = [
                key for key, value in model_report.items() if value == best_model_score
            ][0]

            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found")
            logging.info("Best model found in the train and test data")

            save_object(
                file_path=self.model_train_config.trained_model_file_path,
                obj=best_model,
            )

            predicted = best_model.predict(x_test)
            r2_squre = r2_score(y_test, predicted)
            return r2_squre

        except Exception as e:
            raise CustomException(e, sys)
