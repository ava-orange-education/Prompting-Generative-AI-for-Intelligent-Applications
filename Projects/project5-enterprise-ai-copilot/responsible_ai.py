# responsible_ai.py
# Responsible AI layer: safety checks, disclaimers, and content filtering

# --- Blocked Query Patterns ---
# These patterns indicate queries that the copilot should not answer

BLOCKED_PATTERNS = [
    "personal phone",
    "personal email",
    "home address",
    "salary of",
    "how much does",
    "password for",
    "login credentials",
    "social security",
    "credit card",
    "bank account",
    "private information",
    "confidential data about",
    "access someone else",
]

# --- Speculation Patterns ---
# These patterns indicate requests for guesses or predictions

SPECULATION_PATTERNS = [
    "predict",
    "guess",
    "speculate",
    "what will happen",
    "forecast",
    "next quarter",
    "future revenue",
    "stock price",
    "will the company",
    "what do you think will",
]


def check_blocked_query(query):
    """
    Check if a query asks for restricted or personal information.

    Returns:
        is_blocked (bool): True if the query should be blocked
        reason (str): Explanation of why the query was blocked
    """
    query_lower = query.lower()

    for pattern in BLOCKED_PATTERNS:
        if pattern in query_lower:
            return True, (
                "I cannot provide personal, confidential, or restricted "
                "information. This type of query is outside the scope of "
                "this knowledge assistant. If you need this information, "
                "please contact the relevant department directly."
            )

    return False, ""


def check_speculation_query(query):
    """
    Check if a query asks for speculation or predictions.

    Returns:
        is_speculative (bool): True if the query asks for speculation
        reason (str): Explanation of why the query was flagged
    """
    query_lower = query.lower()

    for pattern in SPECULATION_PATTERNS:
        if pattern in query_lower:
            return True, (
                "I am designed to answer questions based on existing "
                "company documents. I cannot make predictions, guesses, "
                "or speculative statements. Please ask a question that "
                "can be answered using available documentation."
            )

    return False, ""


def run_safety_check(query):
    """
    Run all safety checks on a query before processing.

    Returns:
        is_safe (bool): True if the query is safe to process
        rejection_message (str): Message to show if query is not safe
    """
    # Check for blocked content
    is_blocked, reason = check_blocked_query(query)
    if is_blocked:
        return False, reason

    # Check for speculation
    is_speculative, reason = check_speculation_query(query)
    if is_speculative:
        return False, reason

    return True, ""


def get_disclaimer():
    """
    Return the standard responsible AI disclaimer
    that is appended to every response.
    """
    return (
        "This response is generated based on available company documents "
        "and may not reflect the most recent updates. For critical "
        "decisions, please verify with the relevant department."
    )


def get_grounding_instructions():
    """
    Return the grounding instructions that are included
    in every RAG prompt to prevent hallucination.
    """
    return (
        "Answer only using the provided context. "
        "Do not add information that is not present in the context. "
        "If the context does not contain enough information to answer "
        "the question fully, say clearly: 'The available documents do "
        "not contain enough information to answer this question fully. "
        "Please contact the relevant department for more details.' "
        "Never guess, assume, or speculate."
    )
