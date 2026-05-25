# PlantDiseaseDetector

PlantDiseaseDetector is a CNN-based plant disease classifier for leaf images. It predicts the disease class, confidence score, severity level, treatment recommendation, and top three candidate classes for Tomato, Potato, and Bell Pepper leaves.

The model is trained on the PlantVillage dataset with 15 supported classes.

## Supported Classes

| Class name | Crop | Severity |
| --- | --- | --- |
| `Pepper__bell___Bacterial_spot` | Bell Pepper | Moderate |
| `Pepper__bell___healthy` | Bell Pepper | None |
| `Potato___Early_blight` | Potato | Moderate |
| `Potato___Late_blight` | Potato | High |
| `Potato___healthy` | Potato | None |
| `Tomato_Bacterial_spot` | Tomato | Moderate |
| `Tomato_Early_blight` | Tomato | Moderate |
| `Tomato_Late_blight` | Tomato | High |
| `Tomato_Leaf_Mold` | Tomato | Moderate |
| `Tomato_Septoria_leaf_spot` | Tomato | Moderate |
| `Tomato_Spider_mites_Two_spotted_spider_mite` | Tomato | Moderate |
| `Tomato__Target_Spot` | Tomato | Moderate |
| `Tomato__Tomato_YellowLeaf__Curl_Virus` | Tomato | High |
| `Tomato__Tomato_mosaic_virus` | Tomato | High |
| `Tomato_healthy` | Tomato | None |

## Tech Stack

- Python 3.10
- TensorFlow/Keras 2.15
- NumPy
- Pillow
- Matplotlib
- FastAPI
- Jinja2
- Uvicorn
- Docker and Docker Compose

## Project Structure

```text
PlantDiseaseDetector/
├── app.py
├── Dockerfile
├── docker-compose.yml
├── README.md
├── requirements.txt
├── models/
│   └── plant_disease_model.keras       # generated after training
├── src/
│   ├── __init__.py
│   ├── model.py
│   └── predictor.py
├── static/
│   └── uploads/
│       └── .gitkeep
└── templates/
    └── index.html
```

## Dataset

Download PlantVillage from [Kaggle](https://www.kaggle.com/datasets/arjuntejaswi/plant-village) and place it at:

```text
data/PlantVillage/
```

The folder must contain one subdirectory per supported class, using the exact class names listed above.

## Setup

Create and activate a virtual environment:

```bash
python3.10 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Train the model:

```bash
python -m src.model data/PlantVillage
```

Training creates:

```text
models/plant_disease_model.keras
models/training_history.png
```

Run the web app:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Open:

```text
http://localhost:8000
```

## API

| Route | Method | Description |
| --- | --- | --- |
| `/` | GET | Web upload interface |
| `/predict` | POST | Accepts an image upload and returns prediction JSON |
| `/health` | GET | Returns model loaded status |
| `/classes` | GET | Returns all supported class names |

Example prediction response:

```json
{
  "predicted_class": "Tomato_Early_blight",
  "confidence": 96.42,
  "description": "Early blight causes target-like brown lesions, commonly starting on older tomato leaves.",
  "treatment": "Prune infected lower leaves, stake or mulch plants, rotate crops, and apply a labeled fungicide if disease continues spreading.",
  "severity": "Moderate",
  "top3": [
    {"class": "Tomato_Early_blight", "confidence": 96.42},
    {"class": "Tomato_Late_blight", "confidence": 2.13},
    {"class": "Tomato_Septoria_leaf_spot", "confidence": 0.91}
  ],
  "is_healthy": false
}
```

## Docker

Build and run:

```bash
docker compose up --build
```

The app runs at:

```text
http://localhost:8000
```

The compose file mounts these local folders into the container:

```text
./models:/app/models
./static/uploads:/app/static/uploads
```

Train locally first so `models/plant_disease_model.keras` exists, then start Docker for inference.

## Model Architecture

Input images are resized to `256x256` with batch size `32`. Training runs for up to `50` epochs with `EarlyStopping(patience=5)` and `ModelCheckpoint`.

```text
Conv2D(32)  -> MaxPooling2D
Conv2D(64)  -> MaxPooling2D
Conv2D(64)  -> MaxPooling2D
Conv2D(128) -> MaxPooling2D
Conv2D(128) -> MaxPooling2D
Conv2D(256) -> MaxPooling2D
Flatten
Dense(256)
Dropout(0.4)
Dense(15, softmax)
```

Training uses:

- Data loading with `tf.keras.preprocessing.image_dataset_from_directory`
- 80% train, 10% validation, 10% test split
- Data augmentation with `RandomFlip`, `RandomRotation(0.2)`, and `RandomZoom(0.1)`
- Adam optimizer
- `sparse_categorical_crossentropy` loss

## Results

After training, test accuracy and test loss are printed in the terminal. Accuracy and loss curves are saved to:

```text
models/training_history.png
```

Add your trained metrics here after running training on the downloaded PlantVillage dataset.
