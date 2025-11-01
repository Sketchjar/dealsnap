# app.py
# ----------------------------- #
# Single-file Streamlit + Models
# ----------------------------- #
from __future__ import annotations

import json
from datetime import date
from typing import Any, Dict, List, Optional, Union, Literal
from enum import Enum

import streamlit as st
from pydantic import BaseModel, Field, ValidationError

# ===========================
# ENUMS (Dropdown Data)
# ===========================
class YesNo(str, Enum):
    Yes = "Yes"
    No = "No"

class YesNoNA(str, Enum):
    Yes = "Yes"
    No = "No"
    NA = "NA"

class BrokerOrMRU(str, Enum):
    Broker = "Broker"
    MRU = "MRU"

class CustomerStatus(str, Enum):
    New = "New"
    Existing = "Existing"  # corrected spelling

class ResidentialStatus(str, Enum):
    Aus = "Aus"
    Overseas = "Overseas"

class CitizenshipStatus(str, Enum):
    Aus = "Aus"
    NZ = "NZ"
    Other = "Other"

class NumberOfLoans(int, Enum):
    One = 1
    Two = 2
    Three = 3
    Four = 4

class LoanProduct(str, Enum):
    TailoredVariable = "Tailored Home Loan - Variable"
    TailoredFixed1 = "Tailored Home Loan - 1 year fixed"
    TailoredFixed2 = "Tailored Home Loan - 2 year fixed"
    TailoredFixed3 = "Tailored Home Loan - 3 year fixed"
    TailoredFixed4 = "Tailored Home Loan - 4 year fixed"
    TailoredFixed5 = "Tailored Home Loan - 5 year fixed"
    ChoiceVariable = "Tailored Home Loan, Choice Package - Variable"
    ChoiceFixed1 = "Tailored Home Loan, Choice Package - 1 year fixed"
    ChoiceFixed2 = "Tailored Home Loan, Choice Package - 2 year fixed"
    ChoiceFixed3 = "Tailored Home Loan, Choice Package - 3 year fixed"
    ChoiceFixed4 = "Tailored Home Loan, Choice Package - 4 year fixed"
    ChoiceFixed5 = "Tailored Home Loan, Choice Package - 5 year fixed"
    BaseVariable = "Base variable rate home loan"
    Flexiplus = "Flexiplus Mortgage"
    FlexiplusChoice = "Flexiplus Mortgage, Choice Package"

# ===========================
# Pydantic MODELS
# (minimal set used by UI)
# ===========================
class ApplicationSummary(BaseModel):
    submission_date: str = Field(..., description="ISO date string")
    budget_surplus: Optional[float] = None
    PAT: Optional[str] = None
    lender_id: str
    LVR: Optional[Union[str, float]] = None
    broker_name: Optional[str] = None
    broker_phone_no: Optional[str] = None
    aggregated_lending: Optional[YesNoNA] = None
    lmi_required: Optional[YesNo] = None
    broker_or_MRU: Optional[BrokerOrMRU] = None
    cas_decision: Optional[str] = None
    government_guarantee_scheme: Optional[str] = None

class LoanDetail(BaseModel):
    loan_amount: Optional[float] = None
    loan_type: Optional[str] = None
    loan_product: Optional[LoanProduct] = None
    repayment_type: Optional[str] = None
    loan_term_years: Optional[int] = None
    upc_code: Optional[str] = None
    pricing_docs_attached: Optional[str] = None
    interest_rate: Optional[float] = None
    construction: Optional[str] = None

class LoanSection(BaseModel):
    number_of_loans: NumberOfLoans
    loans: List[LoanDetail]
    loan_purpose_notes: Optional[str] = None

class PersonBase(BaseModel):
    name: str
    customer_number: Optional[str] = None
    dob: Optional[str] = None
    customer_status: Optional[CustomerStatus] = None
    residential_status: Optional[ResidentialStatus] = None
    citizenship_status: Optional[CitizenshipStatus] = None
    number_of_dependents: Optional[int] = None
    marital_status: Optional[str] = None
    vevo_check_completed: Optional[YesNo] = None

class Applicant(PersonBase):
    pass

class Guarantor(PersonBase):
    pass

class ApplicantSection(BaseModel):
    number_of_applicants: int
    number_of_guarantors: int
    applicants: List[Applicant]
    guarantors: List[Guarantor] = []
    alerts_narratives_details: Optional[str] = None

class IncomeLine(BaseModel):
    applicant: str
    income_type: Optional[str] = None
    employment_type: Optional[str] = None
    employment_basis: Optional[str] = None
    employment_start_date: Optional[str] = None
    income_docs_attached: Optional[str] = None
    allowances: Optional[YesNo] = None
    deductions: Optional[YesNo] = None
    verification_for_allowances: Optional[YesNo] = None
    flags: Optional[str] = None
    semp_proof_of_lodgement: Optional[YesNo] = None
    semp_broker_rationale: Optional[str] = None
    semp_company_search_verified: Optional[YesNo] = None

class IncomeSection(BaseModel):
    number_of_incomes: int
    incomes: List[IncomeLine] = []
    income_summary: Optional[str] = None

class ExpenseLine(BaseModel):
    financial_passport_run: Optional[str] = None
    zero_expenses_listed: Optional[str] = None
    discrepancies: Optional[str] = None
    commentary: Optional[str] = None

class ExpenseSection(BaseModel):
    number_of_households: int
    households: List[ExpenseLine] = []
    expenses_notes_summary: Optional[str] = None

class AssetLiabilitySection(BaseModel):
    ccr_complete: Optional[str] = None
    refinance_payment_history_verified: Optional[str] = None
    transaction_report_check_complete: Optional[str] = None
    genuine_savings_type: Optional[str] = None
    genuine_savings_docs_verified: Optional[str] = None
    commentary: Optional[str] = None
    existing_homeloan_repayments_validated: Optional[str] = None
    imminent_retirement_docs_verified: Optional[str] = None
    assets_liabilities_notes_summary: Optional[str] = None

class SecurityDetail(BaseModel):
    address: Optional[str] = None
    property_purpose: Optional[str] = None
    property_type: Optional[str] = None
    transaction: Optional[str] = None
    contract_of_sale_verified: Optional[str] = None
    purchase_price: Optional[float] = None
    valuation_report_verified: Optional[str] = None
    valuation_amount: Optional[float] = None
    valuation_risk_alerts: Optional[str] = None
    risk_ratings: Optional[str] = None
    title_search_verified: Optional[str] = None
    ownership: Optional[str] = None
    construction: Optional[str] = None
    construction_contract_verified: Optional[str] = None
    out_of_contract_items: Optional[str] = None

class SecuritySection(BaseModel):
    securities: List[SecurityDetail] = []

class HGSBlock(BaseModel):
    NOA_attached: Optional[YesNo] = None
    medicare_or_PMKeys_ID_held: Optional[YesNo] = None
    deposit_requirements_met: Optional[YesNo] = None
    first_home_buyer: Optional[YesNo] = None
    home_buyer_declaration_attached: Optional[YesNo] = None
    is_property_regional: Optional[YesNo] = None
    evidence_of_living_regionally: Optional[YesNo] = None
    currently_own_property: Optional[YesNo] = None
    single_parent_evidence: Optional[YesNo] = None
    retain_savings_notes: Optional[str] = None
    scheme_eligibility_notes: Optional[str] = None

class LMIBlock(BaseModel):
    lmi_applicable: Optional[str] = None
    lmi_calculation: Optional[Union[str, float]] = None
    lmi_provider: Optional[str] = None
    existing_LMI: Optional[YesNo] = None
    waiver_medical_practitioners_AHPRA: Optional[YesNo] = None
    waiver_professional_services_registration: Optional[YesNo] = None
    waiver_other_broker_notes: Optional[str] = None

class DealSnapshotForm(BaseModel):
    application_summary: ApplicationSummary
    loan_section: LoanSection
    applicant_section: ApplicantSection
    income_section: IncomeSection
    expense_section: ExpenseSection
    asset_liability_section: AssetLiabilitySection
    security_section: SecuritySection
    hgs_block: Optional[HGSBlock] = None
    lmi_block: Optional[LMIBlock] = None

# ===========================
# UI Helpers
# ===========================
def enum_options(enum_cls):
    return [e.value if hasattr(e, "value") else e.name for e in enum_cls]

def enum_from_value(enum_cls, value):
    if value is None or value == "":
        return None
    for e in enum_cls:
        if (hasattr(e, "value") and e.value == value) or e.name == value:
            return e
    return None

def to_json_bytes(payload: Dict[str, Any]) -> bytes:
    return json.dumps(payload, indent=2, ensure_ascii=False).encode("utf-8")

def section_header(title: str, help_text: Optional[str] = None):
    st.markdown(f"## {title}")
    if help_text:
        st.caption(help_text)
    st.divider()

# ===========================
# Streamlit App
# ===========================
st.set_page_config(page_title="Deal Snapshot Form", layout="wide")
st.title("Deal Snapshot – Streamlit Form (Single File)")

with st.sidebar:
    st.header("Import / Export")
    uploaded = st.file_uploader("Load existing JSON", type=["json"])
    prefill_data: Optional[Dict[str, Any]] = None
    if uploaded:
        try:
            prefill_data = json.load(uploaded)
            st.success("JSON loaded. Values will pre-fill where applicable.")
        except Exception as e:
            st.error(f"Invalid JSON: {e}")
    st.caption("On submit, a validated JSON download will be provided.")

with st.form("deal_form", clear_on_submit=False):
    # 1) Application Summary
    section_header("1. Application Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        submission_date = st.text_input(
            "Submission date (ISO)",
            value=(prefill_data or {}).get("application_summary", {}).get("submission_date", str(date.today()))
        )
    with col2:
        budget_surplus = st.number_input(
            "Budget surplus", value=float((prefill_data or {}).get("application_summary", {}).get("budget_surplus", 0.0)),
            step=0.01, format="%.2f"
        )
    with col3:
        pat = st.text_input("PAT", value=(prefill_data or {}).get("application_summary", {}).get("PAT", "") )
    with col4:
        lender_id = st.text_input("Lender ID", value=(prefill_data or {}).get("application_summary", {}).get("lender_id", "") )

    col5, col6, col7, col8 = st.columns(4)
    with col5:
        lvr_raw = (prefill_data or {}).get("application_summary", {}).get("LVR", "")
        lvr = st.text_input("LVR (e.g., 0.8 or '80%')", value=str(lvr_raw or ""))
    with col6:
        broker_name = st.text_input("Broker name", value=(prefill_data or {}).get("application_summary", {}).get("broker_name", ""))
    with col7:
        broker_phone_no = st.text_input("Broker phone no.", value=(prefill_data or {}).get("application_summary", {}).get("broker_phone_no", ""))
    with col8:
        lm_required = st.selectbox(
            "LMI required", enum_options(YesNo),
            index=1 if not (prefill_data or {}).get("application_summary") else
            enum_options(YesNo).index((prefill_data or {}).get("application_summary", {}).get("lmi_required", "No"))
        )

    col9, col10, col11, col12 = st.columns(4)
    with col9:
        aggregated_lending = st.selectbox(
            "Aggregated lending", enum_options(YesNoNA),
            index=2 if not (prefill_data or {}).get("application_summary") else
            enum_options(YesNoNA).index((prefill_data or {}).get("application_summary", {}).get("aggregated_lending", "NA"))
        )
    with col10:
        broker_or_mru = st.selectbox(
            "Broker or MRU", enum_options(BrokerOrMRU),
            index=0 if not (prefill_data or {}).get("application_summary") else
            enum_options(BrokerOrMRU).index((prefill_data or {}).get("application_summary", {}).get("broker_or_MRU", "Broker"))
        )
    with col11:
        cas_decision = st.text_input("CAS decision", value=(prefill_data or {}).get("application_summary", {}).get("cas_decision", ""))
    with col12:
        government_guarantee_scheme = st.text_input(
            "Government guarantee scheme",
            value=(prefill_data or {}).get("application_summary", {}).get("government_guarantee_scheme", "")
        )

    # 2) Loan Section
    section_header("2. Loan Section")
    num_loans_default = int((prefill_data or {}).get("loan_section", {}).get("number_of_loans", 1))
    number_of_loans = st.select_slider("Number of loans", options=[1, 2, 3, 4], value=num_loans_default)

    loan_details: List[Dict[str, Any]] = []
    for i in range(number_of_loans):
        st.markdown(f"**Loan {i+1}**")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            loan_amount = st.number_input(f"Loan {i+1} amount", min_value=0.0, step=1000.0, value=0.0)
        with c2:
            loan_type = st.text_input(f"Loan {i+1} type", value="")
        with c3:
            loan_product = st.selectbox(f"Loan {i+1} product", enum_options(LoanProduct), index=0, key=f"lp_{i}")
        with c4:
            repayment_type = st.text_input(f"Loan {i+1} repayment type", value="")
        c5, c6, c7, c8 = st.columns(4)
        with c5:
            loan_term_years = st.number_input(f"Loan {i+1} term (years)", min_value=0, step=1, value=30)
        with c6:
            upc_code = st.text_input(f"Loan {i+1} UPC code", value="")
        with c7:
            pricing_docs = st.text_input(f"Loan {i+1} pricing docs attached", value="")
        with c8:
            interest_rate = st.number_input(f"Loan {i+1} interest rate (%)", min_value=0.0, step=0.01, value=0.0)

        construction = st.text_input(f"Loan {i+1} construction", value="")
        loan_details.append(dict(
            loan_amount=loan_amount,
            loan_type=loan_type,
            loan_product=enum_from_value(LoanProduct, loan_product),
            repayment_type=repayment_type,
            loan_term_years=int(loan_term_years),
            upc_code=upc_code,
            pricing_docs_attached=pricing_docs,
            interest_rate=interest_rate,
            construction=construction,
        ))

    loan_purpose_notes = st.text_area("Loan purpose / broker notes", value="")

    # 3) Applicant & Guarantor
    section_header("3. Applicant & Guarantor Details")
    num_applicants = st.number_input("Number of applicants", min_value=1, step=1, value=1)
    num_guarantors = st.number_input("Number of guarantors", min_value=0, step=1, value=0)

    applicants_payload: List[Dict[str, Any]] = []
    for i in range(num_applicants):
        st.markdown(f"**Applicant {i+1}**")
        c1, c2, c3 = st.columns(3)
        with c1:
            name = st.text_input(f"Applicant {i+1} name")
        with c2:
            dob = st.text_input(f"Applicant {i+1} DOB (YYYY-MM-DD)")
        with c3:
            customer_number = st.text_input(f"Applicant {i+1} customer number")
        c4, c5, c6 = st.columns(3)
        with c4:
            customer_status = st.selectbox(f"Applicant {i+1} customer status", enum_options(CustomerStatus), index=0, key=f"cs_{i}")
        with c5:
            residential_status = st.selectbox(f"Applicant {i+1} residential status", enum_options(ResidentialStatus), index=0, key=f"rs_{i}")
        with c6:
            citizenship_status = st.selectbox(f"Applicant {i+1} citizenship status", enum_options(CitizenshipStatus), index=0, key=f"ct_{i}")
        c7, c8, c9 = st.columns(3)
        with c7:
            dependents = st.number_input(f"Applicant {i+1} # dependents", min_value=0, step=1, value=0)
        with c8:
            marital_status = st.text_input(f"Applicant {i+1} marital status")
        with c9:
            vevo_check = st.selectbox(f"Applicant {i+1} VEVO check completed", enum_options(YesNo), index=1, key=f"vv_{i}")

        applicants_payload.append(dict(
            name=name, dob=dob, customer_number=customer_number,
            customer_status=enum_from_value(CustomerStatus, customer_status),
            residential_status=enum_from_value(ResidentialStatus, residential_status),
            citizenship_status=enum_from_value(CitizenshipStatus, citizenship_status),
            number_of_dependents=int(dependents),
            marital_status=marital_status,
            vevo_check_completed=enum_from_value(YesNo, vevo_check),
        ))

    guarantors_payload: List[Dict[str, Any]] = []
    for i in range(num_guarantors):
        st.markdown(f"**Guarantor {i+1}**")
        gname = st.text_input(f"Guarantor {i+1} name")
        gdob = st.text_input(f"Guarantor {i+1} DOB (YYYY-MM-DD)")
        gnum = st.text_input(f"Guarantor {i+1} customer number")
        guarantors_payload.append(dict(name=gname, dob=gdob, customer_number=gnum))

    alerts_narratives = st.text_area("Alerts / narrative details", value="")

    # 4) Income
    section_header("4. Income")
    num_incomes = st.number_input("Number of income lines", min_value=0, step=1, value=0)
    incomes_payload: List[Dict[str, Any]] = []
    for i in range(num_incomes):
        st.markdown(f"**Income line {i+1}**")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            applicant_name = st.text_input(f"Income {i+1} – applicant")
        with c2:
            income_type = st.text_input(f"Income {i+1} – income type")
        with c3:
            employment_type = st.text_input(f"Income {i+1} – employment type")
        with c4:
            employment_basis = st.text_input(f"Income {i+1} – employment basis")
        c5, c6, c7, c8 = st.columns(4)
        with c5:
            start_date = st.text_input(f"Income {i+1} – employment start date (YYYY-MM-DD)")
        with c6:
            docs_attached = st.text_input(f"Income {i+1} – income docs attached")
        with c7:
            allowances = st.selectbox(f"Income {i+1} – allowances", enum_options(YesNo), index=1, key=f"al_{i}")
        with c8:
            deductions = st.selectbox(f"Income {i+1} – deductions", enum_options(YesNo), index=1, key=f"de_{i}")
        c9, c10, c11 = st.columns(3)
        with c9:
            verify_allow = st.selectbox(f"Income {i+1} – verification for allowances", enum_options(YesNo), index=1, key=f"va_{i}")
        with c10:
            proof_lodgement = st.selectbox(f"Income {i+1} – SEMP proof of lodgement", enum_options(YesNo), index=1, key=f"pl_{i}")
        with c11:
            company_search = st.selectbox(f"Income {i+1} – SEMP company search verified", enum_options(YesNo), index=1, key=f"csx_{i}")
        flags = st.text_input(f"Income {i+1} – flags / notes")
        broker_rationale = st.text_input(f"Income {i+1} – SEMP broker rationale")
        incomes_payload.append(dict(
            applicant=applicant_name,
            income_type=income_type,
            employment_type=employment_type,
            employment_basis=employment_basis,
            employment_start_date=start_date,
            income_docs_attached=docs_attached,
            allowances=enum_from_value(YesNo, allowances),
            deductions=enum_from_value(YesNo, deductions),
            verification_for_allowances=enum_from_value(YesNo, verify_allow),
            flags=flags,
            semp_proof_of_lodgement=enum_from_value(YesNo, proof_lodgement),
            semp_broker_rationale=broker_rationale,
            semp_company_search_verified=enum_from_value(YesNo, company_search),
        ))
    income_summary = st.text_area("Income summary", value="")

    # 5) Expenses
    section_header("5. Expenses")
    num_households = st.number_input("Number of households (expense lines)", min_value=0, step=1, value=0)
    expenses_payload: List[Dict[str, Any]] = []
    for i in range(num_households):
        st.markdown(f"**Expense line {i+1}**")
        c1, c2, c3 = st.columns(3)
        with c1:
            fin_passport = st.text_input(f"Household {i+1} – financial passport run")
        with c2:
            zero_listed = st.text_input(f"Household {i+1} – SO responses/zero expenses listed")
        with c3:
            discrepancies = st.text_input(f"Household {i+1} – discrepancies")
        commentary = st.text_input(f"Household {i+1} – commentary related to flags")
        expenses_payload.append(dict(
            financial_passport_run=fin_passport,
            zero_expenses_listed=zero_listed,
            discrepancies=discrepancies,
            commentary=commentary
        ))
    expenses_summary = st.text_area("Expenses notes summary", value="")

    # 6) Assets & Liabilities
    section_header("6. Assets & Liabilities")
    colA, colB, colC = st.columns(3)
    with colA:
        ccr_complete = st.text_input("CCR complete")
        refinance_hist = st.text_input("If refinance, payment history verified")
        txn_report = st.text_input("Customer transaction report check complete")
    with colB:
        genuine_savings_type = st.text_input("Genuine savings type")
        genuine_savings_docs = st.text_input("Genuine savings documents attached & verified")
        commentary_al = st.text_input("Commentary related to flags")
    with colC:
        repayments_validated = st.text_input("Existing home loan repayments validated")
        retire_docs = st.text_input("Imminent retirement/exit strategy docs attached & verified")
    al_summary = st.text_area("Assets/Liabilities Notes Summary", value="")

    # 7) Security Details
    section_header("7. Security Details")
    securities_count = st.number_input("Number of securities", min_value=0, step=1, value=0)
    securities_payload: List[Dict[str, Any]] = []
    for i in range(securities_count):
        st.markdown(f"**Security {i+1}**")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            address = st.text_input(f"Security {i+1} – address")
        with c2:
            property_purpose = st.text_input(f"Security {i+1} – property purpose")
        with c3:
            property_type = st.text_input(f"Security {i+1} – property type")
        with c4:
            transaction = st.text_input(f"Security {i+1} – transaction")
        c5, c6, c7, c8 = st.columns(4)
        with c5:
            cos_verified = st.text_input(f"Security {i+1} – contract of sale verified")
        with c6:
            purchase_price = st.number_input(f"Security {i+1} – purchase price", min_value=0.0, step=1000.0, value=0.0)
        with c7:
            val_verified = st.text_input(f"Security {i+1} – valuation report verified")
        with c8:
            valuation_amount = st.number_input(f"Security {i+1} – valuation amount", min_value=0.0, step=1000.0, value=0.0)
        risk_alerts = st.text_input(f"Security {i+1} – valuation risk alerts")
        risk_ratings = st.text_input(f"Security {i+1} – risk ratings")
        title_search = st.text_input(f"Security {i+1} – title search verified")
        ownership = st.text_input(f"Security {i+1} – ownership")
        construction = st.text_input(f"Security {i+1} – construction")
        cc_verified = st.text_input(f"Security {i+1} – construction contract verified")
        out_of_contract_items = st.text_input(f"Security {i+1} – out of contract items")
        securities_payload.append(dict(
            address=address, property_purpose=property_purpose, property_type=property_type,
            transaction=transaction, contract_of_sale_verified=cos_verified,
            purchase_price=purchase_price, valuation_report_verified=val_verified,
            valuation_amount=valuation_amount, valuation_risk_alerts=risk_alerts,
            risk_ratings=risk_ratings, title_search_verified=title_search, ownership=ownership,
            construction=construction, construction_contract_verified=cc_verified,
            out_of_contract_items=out_of_contract_items,
        ))

    # 8) Conditional Blocks
    section_header("8. Conditional Blocks")
    colh1, colh2 = st.columns(2)
    with colh1:
        hgs_enabled = st.checkbox("Include HGS Block", value=False)
    with colh2:
        lmi_enabled = st.checkbox("Include LMI Block", value=False)

    hgs_payload = None
    if hgs_enabled:
        st.markdown("**Home Guarantee Scheme (HGS)**")
        h1, h2, h3, h4 = st.columns(4)
        with h1:
            noa_attached = st.selectbox("NOA attached", enum_options(YesNo), index=1)
            fhb = st.selectbox("First home buyer", enum_options(YesNo), index=1)
            buyer_decl = st.selectbox("Home buyer declaration attached", enum_options(YesNo), index=1)
        with h2:
            id_held = st.selectbox("Medicare/PMKeys ID held", enum_options(YesNo), index=1)
            regional = st.selectbox("Is property regional?", enum_options(YesNo), index=1)
            evidence_reg = st.selectbox("Evidence of living regionally", enum_options(YesNo), index=1)
        with h3:
            deposit_met = st.selectbox("Deposit requirements met", enum_options(YesNo), index=1)
            own_property = st.selectbox("Currently own property", enum_options(YesNo), index=1)
            single_parent_ev = st.selectbox("Single parent evidence", enum_options(YesNo), index=1)
        with h4:
            retain_notes = st.text_input("Retain savings notes")
            scheme_notes = st.text_input("Scheme eligibility notes")
        hgs_payload = dict(
            NOA_attached=enum_from_value(YesNo, noa_attached),
            medicare_or_PMKeys_ID_held=enum_from_value(YesNo, id_held),
            deposit_requirements_met=enum_from_value(YesNo, deposit_met),
            first_home_buyer=enum_from_value(YesNo, fhb),
            home_buyer_declaration_attached=enum_from_value(YesNo, buyer_decl),
            is_property_regional=enum_from_value(YesNo, regional),
            evidence_of_living_regionally=enum_from_value(YesNo, evidence_reg),
            currently_own_property=enum_from_value(YesNo, own_property),
            single_parent_evidence=enum_from_value(YesNo, single_parent_ev),
            retain_savings_notes=retain_notes,
            scheme_eligibility_notes=scheme_notes,
        )

    lmi_payload = None
    if lmi_enabled:
        st.markdown("**Lenders Mortgage Insurance (LMI)**")
        l1, l2, l3 = st.columns(3)
        with l1:
            lmi_app = st.text_input("LMI applicable")
            lmi_calc = st.text_input("LMI calculation")
        with l2:
            lmi_provider = st.text_input("LMI provider")
            existing_lmi = st.selectbox("Existing LMI", enum_options(YesNo), index=1)
        with l3:
            waiver_ahpra = st.selectbox("Waiver – medical practitioners (AHPRA)", enum_options(YesNo), index=1)
            waiver_prof = st.selectbox("Waiver – professional services registration", enum_options(YesNo), index=1)
        waiver_other = st.text_input("Waiver – other (broker notes)")
        lmi_payload = dict(
            lmi_applicable=lmi_app,
            lmi_calculation=lmi_calc,
            lmi_provider=lmi_provider,
            existing_LMI=enum_from_value(YesNo, existing_lmi),
            waiver_medical_practitioners_AHPRA=enum_from_value(YesNo, waiver_ahpra),
            waiver_professional_services_registration=enum_from_value(YesNo, waiver_prof),
            waiver_other_broker_notes=waiver_other,
        )

    submitted = st.form_submit_button("Validate & Generate JSON")

# ---- Validate + Output ----
if submitted:
    try:
        payload = DealSnapshotForm(
            application_summary=ApplicationSummary(
                submission_date=submission_date,
                budget_surplus=budget_surplus,
                PAT=pat,
                lender_id=lender_id,
                LVR=lvr,
                broker_name=broker_name,
                broker_phone_no=broker_phone_no,
                aggregated_lending=enum_from_value(YesNoNA, aggregated_lending),
                lmi_required=enum_from_value(YesNo, lm_required),
                broker_or_MRU=enum_from_value(BrokerOrMRU, broker_or_mru),
                cas_decision=cas_decision,
                government_guarantee_scheme=government_guarantee_scheme,
            ),
            loan_section=LoanSection(
                number_of_loans=NumberOfLoans(number_of_loans),
                loans=[LoanDetail(**ld) for ld in loan_details],
                loan_purpose_notes=loan_purpose_notes
            ),
            applicant_section=ApplicantSection(
                number_of_applicants=num_applicants,
                number_of_guarantors=num_guarantors,
                applicants=[Applicant(**a) for a in applicants_payload],
                guarantors=[Guarantor(**g) for g in guarantors_payload],
                alerts_narratives_details=alerts_narratives,
            ),
            income_section=IncomeSection(
                number_of_incomes=num_incomes,
                incomes=[IncomeLine(**il) for il in incomes_payload],
                income_summary=income_summary,
            ),
            expense_section=ExpenseSection(
                number_of_households=num_households,
                households=[ExpenseLine(**el) for el in expenses_payload],
                expenses_notes_summary=expenses_summary,
            ),
            asset_liability_section=AssetLiabilitySection(
                ccr_complete=ccr_complete,
                refinance_payment_history_verified=refinance_hist,
                transaction_report_check_complete=txn_report,
                genuine_savings_type=genuine_savings_type,
                genuine_savings_docs_verified=genuine_savings_docs,
                commentary=commentary_al,
                existing_homeloan_repayments_validated=repayments_validated,
                imminent_retirement_docs_verified=retire_docs,
                assets_liabilities_notes_summary=al_summary,
            ),
            security_section=SecuritySection(
                securities=[SecurityDetail(**s) for s in securities_payload]
            ),
            hgs_block=HGSBlock(**hgs_payload) if hgs_payload else None,
            lmi_block=LMIBlock(**lmi_payload) if lmi_payload else None,
        )

        st.success("Validation successful.")
        json_data = json.loads(payload.model_dump_json())
        st.json(json_data)
        st.download_button(
            "Download JSON",
            data=to_json_bytes(json_data),
            file_name="deal_snapshot.json",
            mime="application/json",
        )
    except ValidationError as ve:
        st.error("Validation failed. See details below.")
        st.code(ve.json(), language="json")
    except Exception as e:
        st.error(f"Unexpected error: {e}")
