"""Training utilities for the PlantDiseaseDetector CNN."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Tuple

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models

IMAGE_SIZE = 256
BATCH_SIZE = 32
EPOCHS = 50
CHANNELS = 3

CLASS_NAMES = [
    "Pepper__bell___Bacterial_spot",
    "Pepper__bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Tomato_Bacterial_spot",
    "Tomato_Early_blight",
    "Tomato_Late_blight",
    "Tomato_Leaf_Mold",
    "Tomato_Septoria_leaf_spot",
    "Tomato_Spider_mites_Two_spotted_spider_mite",
    "Tomato__Target_Spot",
    "Tomato__Tomato_YellowLeaf__Curl_Virus",
    "Tomato__Tomato_mosaic_virus",
    "Tomato_healthy",
]

NUM_CLASSES = len(CLASS_NAMES)
MODEL_SAVE_PATH = "models/plant_disease_model.keras"
HISTORY_PLOT_PATH = "models/training_history.png"
SEED = 123


def load_dataset(data_dir: str) -> Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]:
    """Load PlantVillage images and split them into 80/10/10 train/val/test sets."""
    dataset = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        class_names=CLASS_NAMES,
        shuffle=True,
        seed=SEED,
        image_size=(IMAGE_SIZE, IMAGE_SIZE),
        batch_size=BATCH_SIZE,
    )

    total_batches = tf.data.experimental.cardinality(dataset).numpy()
    train_batches = int(0.8 * total_batches)
    val_batches = int(0.1 * total_batches)

    train_ds = dataset.take(train_batches)
    remaining_ds = dataset.skip(train_batches)
    val_ds = remaining_ds.take(val_batches)
    test_ds = remaining_ds.skip(val_batches)

    return train_ds, val_ds, test_ds


def prepare_datasets(
    train_ds: tf.data.Dataset,
    val_ds: tf.data.Dataset,
    test_ds: tf.data.Dataset,
) -> Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]:
    """Normalize datasets, augment training images, and enable prefetching."""
    resize_and_rescale = tf.keras.Sequential(
        [
            layers.Resizing(IMAGE_SIZE, IMAGE_SIZE),
            layers.Rescaling(1.0 / 255),
        ],
        name="resize_and_rescale",
    )

    data_augmentation = tf.keras.Sequential(
        [
            layers.RandomFlip("horizontal_and_vertical"),
            layers.RandomRotation(0.2),
            layers.RandomZoom(0.1),
        ],
        name="data_augmentation",
    )

    def augment(images: tf.Tensor, labels: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        images = resize_and_rescale(images)
        images = data_augmentation(images, training=True)
        return images, labels

    def normalize(images: tf.Tensor, labels: tf.Tensor) -> tuple[tf.Tensor, tf.Tensor]:
        return resize_and_rescale(images), labels

    autotune = tf.data.AUTOTUNE
    train_ds = train_ds.map(augment, num_parallel_calls=autotune)
    train_ds = train_ds.cache().shuffle(1000, seed=SEED).prefetch(autotune)
    val_ds = val_ds.map(normalize, num_parallel_calls=autotune).cache().prefetch(autotune)
    test_ds = test_ds.map(normalize, num_parallel_calls=autotune).cache().prefetch(autotune)

    return train_ds, val_ds, test_ds


def build_model() -> tf.keras.Model:
    """Build and compile the requested six-block CNN architecture."""
    model = models.Sequential(
        [
            layers.Input(shape=(IMAGE_SIZE, IMAGE_SIZE, CHANNELS)),
            layers.Conv2D(32, (3, 3), activation="relu", padding="same"),
            layers.MaxPooling2D(),
            layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
            layers.MaxPooling2D(),
            layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
            layers.MaxPooling2D(),
            layers.Conv2D(128, (3, 3), activation="relu", padding="same"),
            layers.MaxPooling2D(),
            layers.Conv2D(128, (3, 3), activation="relu", padding="same"),
            layers.MaxPooling2D(),
            layers.Conv2D(256, (3, 3), activation="relu", padding="same"),
            layers.MaxPooling2D(),
            layers.Flatten(),
            layers.Dense(256, activation="relu"),
            layers.Dropout(0.4),
            layers.Dense(NUM_CLASSES, activation="softmax"),
        ],
        name="plant_disease_cnn",
    )

    model.compile(
        optimizer=tf.keras.optimizers.Adam(),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


def plot_training_history(history: tf.keras.callbacks.History, output_path: str = HISTORY_PLOT_PATH) -> None:
    """Save training and validation accuracy/loss curves."""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    accuracy = history.history.get("accuracy", [])
    val_accuracy = history.history.get("val_accuracy", [])
    loss = history.history.get("loss", [])
    val_loss = history.history.get("val_loss", [])
    epochs = range(1, len(accuracy) + 1)

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.plot(epochs, accuracy, label="Training Accuracy")
    plt.plot(epochs, val_accuracy, label="Validation Accuracy")
    plt.title("Training and Validation Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss, label="Training Loss")
    plt.plot(epochs, val_loss, label="Validation Loss")
    plt.title("Training and Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Training history plot saved to {output_path}")


def train(
    data_dir: str,
    model_save_path: str = MODEL_SAVE_PATH,
    epochs: int = EPOCHS,
) -> tuple[tf.keras.Model, tf.keras.callbacks.History, tf.data.Dataset]:
    """Train the CNN and save the best/final model plus training curves."""
    Path(model_save_path).parent.mkdir(parents=True, exist_ok=True)

    print("Loading dataset...")
    train_ds, val_ds, test_ds = load_dataset(data_dir)
    train_ds, val_ds, test_ds = prepare_datasets(train_ds, val_ds, test_ds)

    print("Building model...")
    model = build_model()
    model.summary()

    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=5,
            restore_best_weights=True,
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=model_save_path,
            monitor="val_accuracy",
            save_best_only=True,
            mode="max",
        ),
    ]

    print(f"Training for up to {epochs} epochs...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks,
    )

    test_loss, test_accuracy = model.evaluate(test_ds)
    print(f"Test accuracy: {test_accuracy * 100:.2f}%")
    print(f"Test loss: {test_loss:.4f}")

    model.save(model_save_path)
    print(f"Model saved to {model_save_path}")

    plot_training_history(history)
    return model, history, test_ds


def predict(model: tf.keras.Model, img_array: np.ndarray) -> tuple[str, float]:
    """Return the predicted class name and confidence percentage for one image."""
    if img_array.ndim == 3:
        img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array, verbose=0)[0]
    predicted_index = int(np.argmax(predictions))
    predicted_class_name = CLASS_NAMES[predicted_index]
    confidence_percentage = round(float(predictions[predicted_index]) * 100, 2)
    return predicted_class_name, confidence_percentage


def predict_batch(model: tf.keras.Model, test_ds: tf.data.Dataset, n: int = 9) -> None:
    """Visualize predictions for up to nine samples from the test dataset."""
    rows = 3
    cols = 3
    plt.figure(figsize=(12, 12))

    plotted = 0
    for images, labels in test_ds:
        for i in range(images.shape[0]):
            if plotted >= n:
                plt.tight_layout()
                plt.show()
                return

            image = images[i].numpy()
            predicted_class, confidence = predict(model, image)
            actual_class = CLASS_NAMES[int(labels[i].numpy())]

            ax = plt.subplot(rows, cols, plotted + 1)
            ax.imshow(np.clip(image, 0.0, 1.0))
            ax.set_title(
                f"Actual: {actual_class}\nPredicted: {predicted_class}\nConfidence: {confidence}%",
                fontsize=8,
            )
            ax.axis("off")
            plotted += 1

    plt.tight_layout()
    plt.show()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train the PlantDiseaseDetector CNN.")
    parser.add_argument(
        "data_dir",
        nargs="?",
        default="data/PlantVillage",
        help="Path to the PlantVillage dataset directory.",
    )
    parser.add_argument(
        "--model-path",
        default=MODEL_SAVE_PATH,
        help="Where to save the trained Keras model.",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=EPOCHS,
        help=f"Number of epochs to train (default: {EPOCHS}).",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if not os.path.isdir(args.data_dir):
        raise SystemExit(
            f"Dataset directory not found: {args.data_dir}\n"
            "Download PlantVillage from https://www.kaggle.com/datasets/arjuntejaswi/plant-village "
            "and place it at data/PlantVillage/."
        )
    train(args.data_dir, args.model_path, epochs=args.epochs)
