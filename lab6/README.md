# L6_L7_31 — Coupon Validator

## Lab 6: Code and Branch Coverage Analysis

### Student Details
- **Student Name:** Amar Patil
- **GitHub:** [amarpatil2004](https://github.com/amarpatil2004)
- **Source Repository:** [SETAPESU26/L6_L7_31_coupon_validator](https://github.com/SETAPESU26/L6_L7_31_coupon_validator)

---

## 1. Overview & Objective
This project implements automated testing and coverage analysis for a coupon validation module (`coupon_validator.py`).
The objective is to analyze the difference between **Code (Line) Coverage** and **Branch Coverage**, write comprehensive test suites covering all edge cases, decision branches, and boundary conditions, and achieve **100% Code and Branch Coverage**.

---

## 2. File Structure

| File | Description | Coverage Target |
|------|-------------|-----------------|
| `coupon_validator.py` | Core application module under test | Source |
| `CodeCoverageTest_coupon_validator.py` | Targeted test suite for code / statement coverage | **100% Code Coverage** |
| `BranchCoverageTest_coupon_validator.py` | Targeted test suite for all decision branches | **100% Branch Coverage** |
| `test_coupon_validator.py` | Complete unified test suite | **100% Overall Coverage** |
| `code_coverage_analysis.png` | Screenshot of code coverage report in terminal | Deliverable |
| `branch_coverage_analysis.png` | Screenshot of branch coverage report in terminal | Deliverable |

---

## 3. How to Run

### Install Dependencies
```bash
pip install pytest coverage
```

### Run Code Coverage Analysis
```bash
coverage run -m pytest CodeCoverageTest_coupon_validator.py
coverage report -m
```

### Run Branch Coverage Analysis
```bash
coverage run --branch -m pytest BranchCoverageTest_coupon_validator.py
coverage report -m
```

### Run Unified Test Suite
```bash
coverage run --branch -m pytest test_coupon_validator.py
coverage report -m
```

---

## 4. Coverage Analysis & Results

### Code Coverage Results (100%)
```text
============================= 13 passed in 0.06s ==============================
Name                                   Stmts   Miss  Cover   Missing
--------------------------------------------------------------------
CodeCoverageTest_coupon_validator.py      32      0   100%
coupon_validator.py                       32      0   100%
--------------------------------------------------------------------
TOTAL                                     64      0   100%
```

### Branch Coverage Results (100%)
```text
============================= 22 passed in 0.09s ==============================
Name                                     Stmts   Miss Branch BrPart  Cover   Missing
------------------------------------------------------------------------------------
BranchCoverageTest_coupon_validator.py      51      0      0      0   100%
coupon_validator.py                         32      0     24      0   100%
------------------------------------------------------------------------------------
TOTAL                                       83      0     24      0   100%
```

---

## 5. Code Coverage vs. Branch Coverage Explanation
- **Line/Statement Coverage:** Evaluates whether each statement in the code was executed at least once during test execution. In our initial test case, line coverage missed 72% of the code. Even when line coverage reaches 100%, it may fail to evaluate conditional decisions in all logical directions (e.g., when an `if` condition evaluates to `False` without an `else` branch).
- **Branch Coverage:** Examines every decision point (e.g., `if`, `while`, boolean branches) and verifies that every branch evaluates to both `True` and `False`. In `BranchCoverageTest_coupon_validator.py`, all 24 branches (including boundary values, non-member conditions, invalid cart totals, and expired coupon comparisons) were explicitly exercised, delivering **100% complete branch coverage**.
