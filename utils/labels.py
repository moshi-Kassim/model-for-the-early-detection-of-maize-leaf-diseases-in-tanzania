"""Class labels and disease information for the maize leaf disease dashboard."""

# Alphabetical order matches the saved model's output indices
CLASS_NAMES = ["Blight", "Common_Rust", "Gray_Leaf_Spot", "Healthy"]

DISPLAY_NAMES = {
    "Common_Rust": "Common Rust",
    "Blight": "Northern Leaf Blight",
    "Healthy": "Healthy",
    "Gray_Leaf_Spot": "Cercospora Leaf Spot",
}

SCIENTIFIC_NAMES = {
    "Common_Rust": "Puccinia sorghi",
    "Blight": "Exserohilum turcicum",
    "Healthy": "Zea mays (healthy)",
    "Gray_Leaf_Spot": "Cercospora zeae-maydis",
}

DISEASE_INFO = {
    "Common_Rust": {
        "description": "Orange to brown pustules on leaf surfaces caused by fungal infection.",
        "symptoms": "Small, circular to elongated rust-colored pustules on both leaf surfaces.",
        "management": "Plant resistant varieties, apply fungicides early, and remove infected debris.",
    },
    "Blight": {
        "description": "Large elliptical gray-green lesions that can merge and kill leaf tissue.",
        "symptoms": "Cigar-shaped lesions with tan centers and dark borders on lower leaves first.",
        "management": "Crop rotation, resistant hybrids, timely fungicide application at first sign.",
    },
    "Healthy": {
        "description": "No visible disease symptoms; leaf tissue appears normal and green.",
        "symptoms": "Uniform green color, no lesions, spots, or discoloration.",
        "management": "Continue good agronomic practices: balanced fertilization and field monitoring.",
    },
    "Gray_Leaf_Spot": {
        "description": "Rectangular gray lesions bounded by leaf veins, reducing photosynthesis.",
        "symptoms": "Narrow rectangular gray-tan spots aligned parallel to leaf veins.",
        "management": "Use tolerant varieties, rotate crops, and apply fungicides when needed.",
    },
}

MODEL_METRICS = {
    "custom_cnn": {
        "name": "Custom CNN",
        "test_accuracy": 0.9237,
        "test_loss": 0.3725,
        "per_class": {
            "Common_Rust": {"precision": 0.97, "recall": 0.96, "f1": 0.97},
            "Blight": {"precision": 0.83, "recall": 0.94, "f1": 0.88},
            "Healthy": {"precision": 1.00, "recall": 1.00, "f1": 1.00},
            "Gray_Leaf_Spot": {"precision": 0.85, "recall": 0.65, "f1": 0.74},
        },
    },
    "resnet50": {
        "name": "ResNet50 (Transfer Learning)",
        "test_accuracy": 0.7742,
        "test_loss": 0.5277,
    },
}

CONFUSION_MATRIX_CNN = [
    [162, 5, 5, 0],
    [3, 188, 5, 0],
    [22, 8, 56, 0],
    [0, 0, 0, 175],
]
