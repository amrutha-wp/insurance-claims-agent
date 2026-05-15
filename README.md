# Autonomous Insurance Claims Processing Agent

## Overview
This project is a lightweight insurance claims processing agent built using Python and Flask.

The system:
- Extracts key FNOL fields
- Detects missing fields
- Routes claims based on business rules
- Provides reasoning for routing decisions

---

## Features

- Policy information extraction
- Incident detail extraction
- Missing field detection
- Claim classification
- Routing engine
- JSON output generation

---

## Technologies Used

- Python
- Flask
- Regex
- JSON

---

## How to Run

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run application

```bash
python app.py
```

### Open browser

```text
http://127.0.0.1:5000
```

---

## Sample Routing Rules

- Damage < 25000 → Fast-track
- Missing fields → Manual Review
- Fraud keywords → Investigation Flag
- Injury claims → Specialist Queue

---

## Author

Amrutha