# Deal Snapshot Form (Streamlit)

Single-file Streamlit application for capturing, validating, and exporting a structured mortgage deal snapshot using Pydantic models.

## Overview

This app provides a guided multi-section form for:
- Application summary
- Loan details (1-4 loans)
- Applicant and guarantor details
- Income and expense lines
- Assets and liabilities
- Security details
- Optional HGS and LMI blocks

On submission, data is validated with Pydantic and exported as clean JSON.

## Features

- Strong schema validation with `pydantic`
- Enum-driven dropdowns for consistent values
- Import existing JSON to prefill form fields
- Export validated JSON via download button
- Built-in submission summary metrics:
  - Total loan amount
  - Annual income
  - Monthly expenses
  - Net monthly position

## Tech Stack

- Python 3.10+
- Streamlit
- Pydantic

Project Structure

+-- app.py
+-- README.md



## Getting Started
Clone the repository:
git clone <your-repo-url>
cd <your-repo-folder>

## Create and activate a virtual environment:
python -m venv .venv

## Windows (PowerShell)
.venv\Scripts\Activate.ps1

## macOS/Linux
source .venv/bin/activate

## Install dependencies:
pip install streamlit pydantic
Run the app:
streamlit run app.py
## How to Use
Open the app in your browser after launch.
Optionally upload an existing JSON file from the sidebar to prefill fields.
Complete each form section.
Click Validate & Generate JSON.
Review validation and summary metrics.
Download the generated JSON.
Validation and Data Model
The output is validated against DealSnapshotForm, composed of:

ApplicationSummary
- LoanSection
- ApplicantSection
- IncomeSection
- ExpenseSection
- AssetLiabilitySection
- SecuritySection
- Optional HGSBlock
- Optional LMIBlock
## Notes
submission_date expects an ISO date string.
number_of_loans is constrained to values 1-4.
Enum-backed fields enforce controlled input values.
## License
Choose a license and add it here (for example: MIT).
