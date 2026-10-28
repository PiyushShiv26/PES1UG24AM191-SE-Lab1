# Lab 5 — Static Code Analysis: Reflection

### 1. What is the importance of static code analysis?

Static code analysis helps identify potential bugs, security weaknesses, maintainability problems, and style violations without executing a program. It allows developers to detect issues early, improve code quality, and reduce the likelihood of problems during execution or maintenance.

### 2. What did Pylint, Bandit, and Flake8 help identify?

Pylint identified code-quality problems, including a mutable default argument, missing docstrings, broad exception handling, and a function naming violation. Bandit identified the use of a general-purpose random number generator for permit identifiers and silent exception suppression. Flake8 highlighted formatting and whitespace violations. Each tool focused on a different aspect of code quality.

### 3. What changes were made, and how did they improve the program?

The mutable default argument was replaced with `None`, and specific exceptions were handled instead of using bare exception clauses. Permit identifiers were generated using the `secrets` module. File operations were updated to use context managers and explicit UTF-8 encoding. Function names, documentation, and formatting were also improved. These changes made the program easier to understand and maintain while improving its error handling and security.

### 4. What did you learn from this lab?

I learned that static analysis tools complement one another and that a clean report is not necessarily proof that a program is completely correct. Pylint helped improve code quality, Bandit highlighted security-related concerns, and Flake8 enforced consistent formatting. I also learned to interpret warnings, make targeted changes, and rerun the tools to verify the results. Using these tools together provides a practical way to improve code quality before deployment, although functional testing and manual review are still necessary.
