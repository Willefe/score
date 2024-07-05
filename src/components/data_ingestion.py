import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransfromationConfig

from src.components.model_trainer import ModelTrainerConfig, ModelTrainer

from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train_csv')
    test_data_path: str = os.path.join('artifacts', 'test_csv')
    raw_data_path: str = os.path.join('artifacts', 'raw_csv')


class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info('Started data ingestion component')
        try:
            df = pd.read_csv(
                r'C:\Users\Will\Desktop\CA\AI\MLOPs\student_score\notebook\stud.csv')
            logging.info('read dataset as dataframe')

            os.makedirs(os.path.dirname(
                self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path,
                      index=False, header=True)

            logging.info('initiate train_test_split')
            train_set, test_set = train_test_split(
                df, test_size=0.2, random_state=42)

            train_set.to_csv(
                self.ingestion_config.train_data_path, index=False, header=True)

            test_set.to_csv(self.ingestion_config.test_data_path,
                            index=False, header=True)

            logging.info('ingestion of the data is completed')

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )

        except Exception as e:
            raise CustomException(e, sys)


if __name__ == '__main__':
    obj = DataIngestion()
    # obj.initiate_data_ingestion()
    train_data, test_data = obj.initiate_data_ingestion()

    data_transformation = DataTransformation()
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(
        train_data, test_data)

    modeltrainer = ModelTrainer()
    print(modeltrainer.initiate_model_trainer(
        train_array=train_arr, test_array=test_arr))
