# Decisions made for 48-hour Submission

## Lender Requirements Prioritized

Given the time constraints, I prioritized the most critical "knockout" criteria generic across most lenders. The matching engine focuses heavily on quantitative financial health indicators:

1.  **FICO Score (`fico_score`)**: Assigned the highest scoring weight (50). This is almost universally the first filter for lenders.
2.  **Business Duration (`business_duration`)**: Weighted significantly (30). Proxy for business stability.
3.  **Paynet Score (`paynet_score`)**: Weighted (20). A specific industry standard for small business credit.
4.  **Hard Stops vs. Soft Matches**:
    - **Hard Stops**: Implemented strictly. If a rule (like "Revenue > $1M") is marked as a hard stop, failure immediately disqualifies the application regardless of other strengths.
    - **Soft Matches**: contribute to a "Fit Score" (0-100), allowing lenders to see "good fit" applicants even if they don't meet every single preference.

## Scalability & Multi-Tenancy

**Decision**: Designed the system to be inherently **scalable and multi-tenant** to support multiple lenders and policies simultaneously.

**Why**:

- **Multi-Lender Support**: The database schema is normalized (`Lender` -> `LenderPolicy`) to allow an unlimited number of lenders, each with their own distinct set of policies.
- **Parallel Execution**: The matching engine is designed to evaluate an incoming application against _all_ stored policies (or a filtered subset) efficiently. This ensures that as the platform grows to hundreds of lenders, the architecture remains stable and responsive, capable of finding the best match across a diverse marketplace.

## Simplifications Made & Why

### 1. In-Memory Matching Logic (Python vs. SQL)

- **Decision**: Loaded logic-bearing policies into memory to process in Python loops.
- **Why**: Writing a dynamic SQL query compiler to translate arbitrary JSON rules into PostgreSQL `WHERE` clauses is complex and error-prone for a 48-hour build. Python allows for easier debugging of logic (operators like `GREATER_THAN`, `IN`, `CONTAINS`).

### 2. Fixed Input Schema

- **Decision**: The `/match` endpoint uses a strict Pydantic model (`fico_score`, `revenue`, etc.) rather than a dynamic `Dict[str, Any]`.
- **Why**: Ensures type safety and clear API documentation (Swagger UI) for judges/testers. supporting arbitrary keys would require complex validation logic.

### 3. "All-or-Nothing" Extraction

- **Decision**: The AI agent extracts rules once upon upload. If the extraction misses a field, it's missed forever until re-upload.
- **Why**: Building an interactive "Human-in-the-Loop" review UI to correct AI extractions was out of scope.

### 4. Basic Operator Support

- **Decision**: Supported standard operators (`EQUAL`, `GREATER_THAN`, `IN`, etc.) but skipped complex nested logic (e.g., "If Industry is X, then Revenue must be Y").
- **Why**: Simplifies the database schema to a flat list of rules per policy.

## Improvements with More Time

1.  **Dynamic Field Mapping**:
    - Currently, if the LLM extracts "minimum_credit" but the API expects "fico_score", they won't match. I would add a semantic mapping layer (perhaps using simple string similarity or an alias table) to normalize field names.
2.  **Database-Level Filtering**:

    - Move the "Hard Stop" logic to the database query itself to avoid fetching policies that definitely won't match (e.g., using PostgreSQL `JSONB` operators).

3.  **Complex Rule Chains**:

    - Implement support for conditional logic (DAG-based rules) to handle cases where requirements change based on other attributes (e.g., "Lower FICO allowed if Revenue > $5M").

4.  **Feedback Loop**:
    - Allow lenders to manually "Accept" or "Reject" matches to train a classification model that eventually supplements the rule-based engine.
