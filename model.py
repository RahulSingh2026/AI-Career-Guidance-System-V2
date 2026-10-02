import pandas as pd
from sklearn.tree import DecisionTreeClassifier


def train_model():

    # Training dataset
    data = pd.DataFrame({

        "Python": [
            9, 8, 9, 8, 9,
            8, 7, 6, 8, 8,
            9, 8, 7, 8, 7,
            9, 8, 9, 8, 7
        ],

        "Mathematics": [
            9, 9, 8, 7, 6,
            7, 5, 5, 6, 9,
            10, 8, 8, 7, 9,
            9, 6, 7, 10, 8
        ],

        "Data_Analysis": [
            9, 8, 8, 7, 5,
            4, 3, 2, 4, 7,
            8, 6, 3, 4, 3,
            9, 3, 5, 8, 4
        ],

        "Communication": [
            6, 5, 7, 8, 8,
            9, 8, 9, 8, 5,
            6, 6, 5, 6, 5,
            7, 9, 8, 6, 6
        ],

        "Web_Development": [
            3, 2, 3, 4, 3,
            4, 9, 10, 9, 2,
            2, 3, 2, 3, 2,
            3, 8, 4, 2, 2
        ],

        "Career": [
            "Data Scientist",
            "AI/ML Engineer",
            "Data Scientist",
            "Software Developer",
            "Software Developer",
            "Software Developer",
            "Web Developer",
            "Web Developer",
            "Web Developer",
            "AI/ML Engineer",
            "AI/ML Engineer",
            "AI/ML Engineer",
            "Cyber Security Analyst",
            "Cyber Security Analyst",
            "Cyber Security Analyst",
            "Data Scientist",
            "Web Developer",
            "Software Developer",
            "AI/ML Engineer",
            "Cyber Security Analyst"
        ]
    })

    features = [
        "Python",
        "Mathematics",
        "Data_Analysis",
        "Communication",
        "Web_Development"
    ]

    X = data[features]
    y = data["Career"]

    model = DecisionTreeClassifier(
        random_state=42,
        max_depth=5
    )

    model.fit(X, y)

    return model