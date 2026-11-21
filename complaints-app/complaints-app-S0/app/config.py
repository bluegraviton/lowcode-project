"""All enumerations and tunables for the Complaints App.

Enumerated values are validated text (Core Spec Section 7) and are defined
here only. Code elsewhere must use these names, never string literals.
"""

# --- Roles (Core Spec Section 3) ---------------------------------------------
ROLE_HANDLER = "handler"
ROLE_COMPLIANCE = "compliance"
ROLES = (ROLE_HANDLER, ROLE_COMPLIANCE)

# --- Complaint lifecycle (Core Spec Section 4) -------------------------------
STATUS_LOGGED = "logged"
STATUS_INVESTIGATING = "investigating"
STATUS_PENDING_APPROVAL = "pending_approval"
STATUS_APPROVED = "approved"
STATUS_CLOSED = "closed"

# Display text for each status, in lifecycle order.
STATUS_LABELS = {
    STATUS_LOGGED: "Logged",
    STATUS_INVESTIGATING: "Investigating",
    STATUS_PENDING_APPROVAL: "Pending approval",
    STATUS_APPROVED: "Approved",
    STATUS_CLOSED: "Closed",
}
STATUSES = tuple(STATUS_LABELS)

# --- Receipt channels (Core Spec Section 7) ----------------------------------
CHANNEL_EMAIL = "email"
CHANNEL_PHONE = "phone"
CHANNEL_LETTER = "letter"
CHANNEL_IN_PERSON = "in_person"
CHANNEL_OTHER = "other"
CHANNELS = (
    CHANNEL_EMAIL,
    CHANNEL_PHONE,
    CHANNEL_LETTER,
    CHANNEL_IN_PERSON,
    CHANNEL_OTHER,
)

# --- Products and categories --------------------------------------------------
# ASSUMPTION: the Core Spec says these are "validated enumerations" but does
# not list the values. These are placeholders for the project owner to confirm.
PRODUCT_MOTOR = "motor"
PRODUCT_HOME = "home"
PRODUCT_TRAVEL = "travel"
PRODUCT_HEALTH = "health"
PRODUCT_LABELS = {
    PRODUCT_MOTOR: "Motor insurance",
    PRODUCT_HOME: "Home insurance",
    PRODUCT_TRAVEL: "Travel insurance",
    PRODUCT_HEALTH: "Health insurance",
}
PRODUCTS = tuple(PRODUCT_LABELS)

CATEGORY_SERVICE = "service_quality"
CATEGORY_CLAIMS = "claims_handling"
CATEGORY_PREMIUMS = "premiums_and_charges"
CATEGORY_POLICY_ADMIN = "policy_administration"
CATEGORY_ADVICE = "advice_and_sales"
CATEGORY_LABELS = {
    CATEGORY_SERVICE: "Service quality",
    CATEGORY_CLAIMS: "Claims handling",
    CATEGORY_PREMIUMS: "Premiums and charges",
    CATEGORY_POLICY_ADMIN: "Policy administration",
    CATEGORY_ADVICE: "Advice and sales",
}
CATEGORIES = tuple(CATEGORY_LABELS)

# --- Investigation outcome (values from Core Spec Section 7) -----------------
OUTCOME_UPHELD = "upheld"
OUTCOME_PARTIALLY_UPHELD = "partially_upheld"
OUTCOME_NOT_UPHELD = "not_upheld"
OUTCOMES = (OUTCOME_UPHELD, OUTCOME_PARTIALLY_UPHELD, OUTCOME_NOT_UPHELD)

# ASSUMPTION: Core Spec Section 7 names root_cause_category but lists no
# values. Placeholders for the project owner to confirm.
ROOT_CAUSE_PROCESS = "process_error"
ROOT_CAUSE_COMMUNICATION = "communication"
ROOT_CAUSE_SYSTEM = "system_issue"
ROOT_CAUSE_NONE_FOUND = "no_fault_found"
ROOT_CAUSES = (
    ROOT_CAUSE_PROCESS,
    ROOT_CAUSE_COMMUNICATION,
    ROOT_CAUSE_SYSTEM,
    ROOT_CAUSE_NONE_FOUND,
)

# --- Day-40 outcome (values from Core Spec R-CLOSE-02) ------------------------
DAY40_ANSWERED_IN_TIME = "answered_in_time"
DAY40_NOTIFIED_BEFORE_OUTCOME = "notified_before_outcome"
DAY40_BREACHED = "breached"
DAY40_OUTCOMES = (
    DAY40_ANSWERED_IN_TIME,
    DAY40_NOTIFIED_BEFORE_OUTCOME,
    DAY40_BREACHED,
)


class Config:
    """Default configuration."""

    TESTING = False
    PROTOTYPE_BANNER = "Prototype S0: sample data only, no login, not real data."


class TestConfig(Config):
    """Configuration used by the automated tests."""

    __test__ = False  # not a pytest test class, despite the name
    TESTING = True
