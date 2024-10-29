import os
from typing import List, Tuple

import keras
import matplotlib.pyplot as plt
import numpy as np
import scipy  # Used under the hood by Keras. This will cause an import error if scipy isn't installed.
import tensorflow as tf
from keras import Sequential  # Use the a simple feed forward NN model
from keras.callbacks import (
    CSVLogger,
    EarlyStopping,
    LearningRateScheduler,
    ModelCheckpoint,
)
from keras.layers import Dense, Flatten
from keras.models import load_model
from keras.optimizers import Adam
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator


class Hawkeye:
    # For easy access as os.getcwd() only provides the dir from which the manage.py file is executed
    current_directory_path: str = os.path.dirname(__file__)  # dir of the Hawkeye folder

    def __init__(self):
        self.model: Sequential = self._build_model()

    @staticmethod  # For debugging purposes
    def tensorflow_version() -> str:
        """
        Returns the Tensorflow version
        """
        return str(tf.__version__)

    @staticmethod  # Convert prediction indexes to corresponding names
    def get_class_name(index: int) -> str | None:
        """
        Convert prediction indexes to corresponding names.
        """
        class_names = [
            "T-shirt/top",
            "Trouser",
            "Pullover",
            "Dress",
            "Coat",
            "Sandal",
            "Shirt",
            "Sneaker",
            "Bag",
            "Ankle boot",
        ]

        try:
            return class_names[index]  # type: ignore
        except IndexError:
            print("Index out of range. Make sure the index is between 0 and 9")

    @staticmethod
    def get_model_name(index: int) -> str | None:
        """
        Convert prediction indexes to corresponding models.
        """

        class_names = [
            "T-shirt/top",
            "Trouser",
            "Pullover",
            "Dress",
            "Coat",
            "Sandal",
            "Shirt",
            "Sneaker",
            "Bag",
            "Ankle boot",
        ]

        name_model_pair = {
            "T-shirt/top": ("TW", "Topwear"),
            "Trouser": ("BW", "Bottomwear"),
            "Pullover": ("TW", "Topwear"),
            "Dress": ("TW", "Topwear"),
            "Coat": ("JK", "Jackets"),
            "Sandal": ("FW", "Footwear"),
            "Shirt": ("TW", "Topwear"),
            "Sneaker": ("FW", "Footwear"),
            "Bag": ("BG", "Bags"),
            "Ankle boot": ("FW", "Footwear"),
        }

        try:
            return name_model_pair[f"{class_names[index]}"]  # type: ignore
        except IndexError:
            print("Index out of range. Make sure the index is between 0 and 9")

    def _build_model(self) -> Sequential:
        """
        Build the Sequential model.
        """
        model = Sequential(  # Dimensions of the model.
            [
                Flatten(input_shape=(28, 28)),  # Squash the input into a single layer
                Dense(784, activation="relu"),  # Introduce non-linearity into the model
                Dense(392, activation="relu"),
                Dense(196, activation="relu"),
                Dense(98, activation="relu"),
                Dense(49, activation="relu"),
                Dense(10, activation="softmax"),  # Convert to probability
            ]
        )

        model.compile(
            optimizer=Adam(),
            loss="sparse_categorical_crossentropy",
            metrics=[
                "accuracy",
            ],
        )

        return model

    def _preprocess_train_data(
        self,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Preprocess the training data.
        """
        fashion_mnist = keras.datasets.fashion_mnist
        (train_images, train_labels), (test_images, test_labels) = (
            fashion_mnist.load_data()
        )

        train_images = train_images / 255.0  # Normalize the data
        test_images = test_images / 255.0
        # START Convert background from 0 as opposed to real world data, where it is 1
        # https://stackoverflow.com/questions/57034292/fashion-mnist-code-giving-bag-as-output-for-every-single-real-world-image
        train_images = 1 - train_images
        test_images = 1 - test_images
        # END Thank you Vishnu Rajan and Georgy90

        # Converts data into shape (1, 28, 28, 1) from (1, 28, 28)
        # This is to indicate that it has a color channel of 1 (Greyscale)
        # This is needed because data augmentation requires a 4D tensor including color channel.
        train_images = np.expand_dims(train_images, -1)
        test_images = np.expand_dims(test_images, -1)

        return train_images, train_labels, test_images, test_labels

    def _save_model(
        self, filepath: str = os.path.join(current_directory_path, "Hawkeye.keras")
    ) -> None:
        """
        Save the model to the specified filepath.
        """
        self.model.save(filepath)

    def load_hawkeye(
        self, filepath: str = os.path.join(current_directory_path, "Hawkeye.keras")
    ) -> None:
        """
        Load the model from the specified filepath.
        """
        self.model = load_model(filepath)  # type: ignore

    def _train_model(
        self, epochs: int = 100, current_directory_path: str = current_directory_path
    ) -> None:
        """
        Train the model with the specified number of epochs.
        """
        with tf.device(
            "/GPU:0"
        ):  # Use GPU if avaliable, CPU is available as fallback # type: ignore
            train_images, train_labels, test_images, test_labels = (
                self._preprocess_train_data()
            )
            # Used to augment "noise" into the training data to mitigate some issues with low accuracy when using real world data
            # BEGIN Inspired by the "Preprocessing" coloumn of some of the submissions for the benchmark for Fashion MINST
            # https://github.com/zalandoresearch/fashion-mnist?tab=readme-ov-file#benchmark
            # The code is written by the IBDP Candidate
            datagen = ImageDataGenerator(
                rotation_range=20,
                width_shift_range=0.2,
                height_shift_range=0.2,
                shear_range=0.3,
                zoom_range=0.2,
                horizontal_flip=True,
                vertical_flip=False,
            )  # END

            def lr_schedule(epoch: int):
                lr = 1e-3
                if epoch > 50:
                    lr *= 0.1
                return lr

            # Gradually decreasing the learning rate to prevent converging on an non-optimial solution
            lr_scheduler = LearningRateScheduler(lr_schedule)

            # Store the best weights
            checkpoint_cb = ModelCheckpoint(
                os.path.join(current_directory_path, "CallBack.keras"),
                save_best_only=True,
            )

            # Prevent overfitting
            early_stopping_cb = EarlyStopping(patience=10, restore_best_weights=True)

            # Store training metrics for easier debugging and evaluation
            training_log_cb = CSVLogger(
                os.path.join(current_directory_path, "Training.log"),
                separator=",",
                append=False,
            )

            # Train the model
            self.model.fit(
                datagen.flow(train_images, train_labels, batch_size=64),
                steps_per_epoch=len(train_labels) / 64,
                epochs=epochs,
                validation_data=datagen.flow(test_images, test_labels, batch_size=64),
                callbacks=[
                    lr_scheduler,
                    checkpoint_cb,
                    early_stopping_cb,
                    training_log_cb,
                ],
            )

        self._save_model()

    def _evaluate_model(self) -> Tuple[float, float]:
        """
        Evaluate the model and return the test loss and test accuracy.
        """
        with tf.device(
            "/GPU:0"
        ):  # Use GPU if avaliable, CPU is available as fallback # type: ignore
            train_images, train_labels, test_images, test_labels = (
                self._preprocess_train_data()
            )
            test_loss, test_acc = self.model.evaluate(
                test_images, test_labels, verbose="2"
            )
            return test_loss, test_acc

    def img_path_to_array(self, img_path: str) -> np.ndarray:
        """
        Convert the image at the specified path to a processed numpy array.
        """
        # Rescale and convert to grayscale to match the training dataset
        img = image.load_img(img_path, target_size=(28, 28), color_mode="grayscale")
        img = image.img_to_array(img)
        img = img.reshape(-1)  # Flatten the image
        return img

    def img_array_to_processed_array(
        self, img_array: np.ndarray, target_size=(28, 28)
    ) -> np.ndarray:
        """
        Convert the numpy array image to a processed numpy array.
        """

        img = image.array_to_img(img_array, scale=False, dtype=np.uint8)
        img = img.resize(target_size)
        img = image.img_to_array(img)
        img = img.reshape(-1)

        return img

    def predict(self, images: np.ndarray) -> int:
        """
        Predict the class of the provided images.
        """
        # Reshape and normalize the image
        images = images.reshape(-1, 28, 28) / 255.0
        predictions = self.model.predict(images)
        prediction = int(np.argmax(predictions[0]))
        return prediction
