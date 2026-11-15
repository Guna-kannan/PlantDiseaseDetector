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

IMAGE_SIZE = 224
BATCH_SIZE = 64
EPOCHS = 10
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
    """Load PlantVillage images with deterministic train (80%), validation (10%), and test (10%) splits."""
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        class_names=CLASS_NAMES,
        validation_split=0.2,
        subset="training",
        seed=SEED,
        image_size=(IMAGE_SIZE, IMAGE_SIZE),
        batch_size=BATCH_SIZE,
    )

    val_full_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        class_names=CLASS_NAMES,
        validation_split=0.2,
        subset="validation",
        seed=SEED,
        image_size=(IMAGE_SIZE, IMAGE_SIZE),
        batch_size=BATCH_SIZE,
    )

    val_batches = tf.data.experimental.cardinality(val_full_ds).numpy() // 2
    val_ds = val_full_ds.take(val_batches)
    test_ds = val_full_ds.skip(val_batches)

    return train_ds, val_ds, test_ds


def prepare_datasets(
    train_ds: tf.data.Dataset,
    val_ds: tf.data.Dataset,
    test_ds: tf.data.Dataset,
) -> Tuple[tf.data.Dataset, tf.data.Dataset, tf.data.Dataset]:
    """Augment training images and enable prefetching. Rescaling is performed inside the CNN."""
    data_augmentation = tf.keras.Sequential(
        [
            layers.RandomFlip("horizontal_and_vertical"),
            layers.RandomRotation(0.1),
            layers.RandomZoom(0.08),
        ],
        name="data_augmentation",
    )

    autotune = tf.data.AUTOTUNE
    train_ds = train_ds.map(lambda x, y: (data_augmentation(x, training=True), y), num_parallel_calls=autotune)
    train_ds = train_ds.prefetch(autotune)
    val_ds = val_ds.prefetch(autotune)
    test_ds = test_ds.prefetch(autotune)

    return train_ds, val_ds, test_ds


def build_model(num_classes: int = NUM_CLASSES) -> tf.keras.Model:
    """Build and compile a 6-block Deep Convolutional Neural Network."""
    model = models.Sequential(
        [
            layers.Input(shape=(IMAGE_SIZE, IMAGE_SIZE, CHANNELS), name="input_leaf"),
            layers.Rescaling(1.0 / 255.0, name="rescaling"),
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
            layers.Dropout(0.35),
            layers.Dense(num_classes, activation="softmax", name="predictions"),
        ],
        name="plant_disease_cnn",
    )
    model.compile(
        optimizer=tf.keras.optimizers.legacy.Adam(learning_rate=1e-3),
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
    plt.plot(epochs, accuracy, label="Training Accuracy", marker="o", linewidth=2)
    plt.plot(epochs, val_accuracy, label="Validation Accuracy", marker="s", linewidth=2)
    plt.title("Training and Validation Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(epochs, loss, label="Training Loss", marker="o", linewidth=2)
    plt.plot(epochs, val_loss, label="Validation Loss", marker="^", linewidth=2)
    plt.title("Training and Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Training history plot saved to {output_path}")


def predictions_on_ds(model: tf.keras.Model, ds: tf.data.Dataset) -> tuple[np.ndarray, np.ndarray]:
    """Collect true labels and predicted labels for every batch in a dataset."""
    y_true: list[int] = []
    y_pred: list[int] = []
    for images, labels in ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(labels.numpy().tolist())
        y_pred.extend(np.argmax(preds, axis=1).tolist())
    return np.array(y_true), np.array(y_pred)


def plot_confusion_matrix(
    cm: np.ndarray,
    class_names: list[str],
    output_path: str = "models/confusion_matrix.png",
) -> None:
    """Save a labeled, row-normalized confusion-matrix heatmap as an image."""
    import itertools

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    cm_counts = cm.astype(int)
    cm = cm.astype(float)
    row_sums = cm.sum(axis=1, keepdims=True)
    cm_norm = np.divide(cm, row_sums, out=np.zeros_like(cm), where=row_sums != 0)

    fig, ax = plt.subplots(figsize=(12, 10))
    im = ax.imshow(cm_norm, interpolation="nearest", cmap=plt.cm.Blues)
    ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set(
        xticks=np.arange(cm.shape[1]),
        yticks=np.arange(cm.shape[0]),
        xticklabels=class_names,
        yticklabels=class_names,
        ylabel="True label",
        xlabel="Predicted label",
        title="Confusion Matrix (row-normalized)",
    )
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    thresh = cm_norm.max() / 2.0
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        ax.text(
            j,
            i,
            f"{cm_counts[i, j]:d}\n({cm_norm[i, j]:.2f})",
            ha="center",
            va="center",
            color="white" if cm_norm[i, j] > thresh else "black",
            fontsize=7,
        )
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Confusion matrix saved to {output_path}")


def evaluate(
    model_path: str = MODEL_SAVE_PATH,
    data_dir: str = "data/PlantVillage",
) -> tuple[float, np.ndarray]:
    """Evaluate the saved model on the test split; return accuracy + confusion matrix."""
    if not Path(model_path).exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    train_ds, val_ds, test_ds = load_dataset(data_dir)
    train_ds, val_ds, test_ds = prepare_datasets(train_ds, val_ds, test_ds)
    model = tf.keras.models.load_model(model_path)

    test_loss, test_accuracy = model.evaluate(test_ds)
    print(f"Test loss: {test_loss:.4f}")
    print(f"Test accuracy: {test_accuracy * 100:.2f}%")

    y_true, y_pred = predictions_on_ds(model, test_ds)
    accuracy = float(np.mean(y_true == y_pred))
    print(f"Prediction accuracy: {accuracy * 100:.2f}%")

    cm = np.zeros((NUM_CLASSES, NUM_CLASSES), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[t, p] += 1
    plot_confusion_matrix(cm, CLASS_NAMES)
    return accuracy, cm


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

    # Confusion matrix on the held-out test set
    y_true, y_pred = predictions_on_ds(model, test_ds)
    cm = np.zeros((NUM_CLASSES, NUM_CLASSES), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[t, p] += 1
    plot_confusion_matrix(cm, CLASS_NAMES)

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
    parser.add_argument(
        "--eval",
        action="store_true",
        help="Evaluate the saved model and produce accuracy + confusion matrix instead of training.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    if args.eval:
        evaluate(args.model_path, args.data_dir)
    else:
        if not os.path.isdir(args.data_dir):
            raise SystemExit(
                f"Dataset directory not found: {args.data_dir}\n"
                "Download PlantVillage from https://www.kaggle.com/datasets/arjuntejaswi/plant-village "
                "and place it at data/PlantVillage/."
            )
        train(args.data_dir, args.model_path, epochs=args.epochs)
