import re
import os
from flask import Flask, jsonify

app = Flask(__name__)

# READ FILE
def read_file(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

# EXTRACT FIELDS
def extract_fields(text):

    fields = {}

    patterns = {
        "Policy Number": r"Policy Number:\s*(.*)",
        "Policyholder Name": r"Policyholder Name:\s*(.*)",
        "Effective Dates": r"Effective Dates:\s*(.*)",
        "Incident Date": r"Incident Date:\s*(.*)",
        "Incident Time": r"Incident Time:\s*(.*)",
        "Location": r"Location:\s*(.*)",
        "Description": r"Description:\s*(.*)",
        "Claimant": r"Claimant:\s*(.*)",
        "Third Parties": r"Third Parties:\s*(.*)",
        "Contact Details": r"Contact Details:\s*(.*)",
        "Asset Type": r"Asset Type:\s*(.*)",
        "Asset ID": r"Asset ID:\s*(.*)",
        "Estimated Damage": r"Estimated Damage:\s*(.*)",
        "Claim Type": r"Claim Type:\s*(.*)",
        "Attachments": r"Attachments:\s*(.*)",
        "Initial Estimate": r"Initial Estimate:\s*(.*)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text)

        if match:
            fields[key] = match.group(1).strip()
        else:
            fields[key] = None

    return fields

# FIND MISSING FIELDS
def find_missing(fields):

    missing = []

    for key, value in fields.items():
        if value is None or value == "":
            missing.append(key)

    return missing

# ROUTING LOGIC
def route_claim(fields, missing):

    description = str(fields.get("Description", "")).lower()
    claim_type = str(fields.get("Claim Type", "")).lower()

    try:
        damage = int(fields.get("Estimated Damage", 0))
    except:
        damage = 0

    if missing:
        return "Manual Review", "Mandatory fields are missing"

    if "fraud" in description or "staged" in description or "inconsistent" in description:
        return "Investigation Flag", "Suspicious keywords detected"

    if claim_type == "injury":
        return "Specialist Queue", "Claim type is injury"

    if damage < 25000:
        return "Fast-track", "Damage amount below 25000"

    return "Normal Processing", "Standard claim"

# MAIN API
@app.route("/")
def home():

    all_claims = []

    folder_path = "sample_docs"

    for filename in os.listdir(folder_path):

        if filename.endswith(".txt"):

            full_path = os.path.join(folder_path, filename)

            text = read_file(full_path)

            extracted = extract_fields(text)

            missing = find_missing(extracted)

            route, reason = route_claim(extracted, missing)

            result = {
                "fileName": filename,
                "extractedFields": extracted,
                "missingFields": missing,
                "recommendedRoute": route,
                "reasoning": reason
            }

            all_claims.append(result)

    return jsonify(all_claims)

if __name__ == "__main__":
    app.run(debug=True)