Below is a **formal, academic-style Workload Policy Document** tailored specifically for your **University Workload Allocation & Management (WAM) System**.
It is written at a **final-year university project level**, aligned with **UGC Sri Lanka guidelines**, and suitable to be included as:

- Chapter / Appendix in your Final Year Report
- `/documents/workload_policy.md`
- A reference document during viva

You can later convert this directly into **PDF** if needed.

---

# University Academic Workload Allocation Policy

_(For Workload Allocation & Management System – WAM)_

---

## 1. Introduction

The purpose of this document is to define a structured and policy-compliant approach for allocating academic workload among university staff members.
This policy serves as the foundational guideline for the **University Workload Allocation & Management (WAM) System**, ensuring that workload distribution is:

- Fair and transparent
- Aligned with University Grants Commission (UGC) Sri Lanka guidelines
- Compliant with standard academic and labour expectations
- Flexible enough to handle semester-based, monthly, and weekly workload variations

---

## 2. Scope of the Policy

This policy applies to:

- All **full-time academic staff**
- Teaching, research, administrative, and academic support activities
- Weekly, monthly, and semester-level workload planning
- Automated workload allocation using optimization algorithms

This policy **does not** replace university regulations but operationalizes them in a software system.

---

## 3. Definitions

### 3.1 Staff

An academic or administrative member employed by the university, categorized as:

- Academic Staff
- Administrative Staff
- Management Staff

### 3.2 Task

A unit of work that contributes to staff workload. Examples include:

- Lectures
- Laboratory sessions
- Tutorials
- Examination duties
- Evaluation and marking
- Research supervision
- Administrative and committee work

### 3.3 Task Instance

A time-bound execution of a task within a specific week, month, or semester.

---

## 4. Workload Categories

Academic workload is divided into the following categories:

1. **Teaching Activities**

   - Lectures
   - Labs
   - Tutorials
   - Practicals

2. **Assessment Activities**

   - Exam paper setting
   - Invigilation
   - Marking and grading
   - Viva examinations

3. **Research Activities**

   - Research supervision
   - Publications
   - Grant-related work

4. **Administrative Activities**

   - Departmental roles
   - Committee memberships
   - Coordination duties

Each task category has an associated **standard workload tariff** measured in hours.

---

## 5. Weekly Workload Expectations (UGC-Aligned)

### 5.1 Total Weekly Workload

According to UGC Sri Lanka guidelines, a **full-time academic staff member** is expected to contribute:

> **A minimum of 40 hours per week**
> including teaching, preparation, research, assessment, and administrative work.

This 40-hour workload is treated as the **baseline expectation** in the WAM system.

---

### 5.2 Direct Teaching (Contact Hours)

UGC guidelines specify minimum weekly teaching (contact) hours depending on academic rank:

| Academic Role                     | Minimum Teaching Hours / Week |
| --------------------------------- | ----------------------------- |
| Assistant Lecturer / Lecturer     | 15 – 16 hours                 |
| Senior Lecturer                   | 14 – 15 hours                 |
| Associate Professor               | 14 hours                      |
| Professor                         | 14 hours                      |
| Administrative / Management Roles | Reduced teaching hours        |

These are treated as **target values**, not rigid limits.

---

## 6. Workload Calculation Principles

### 6.1 Workload Measurement Unit

All workload is measured in **hours**.

Each task has:

- A predefined **tariff value** (hours required to complete)
- A category (teaching, admin, research, etc.)

### 6.2 Weekly Workload Calculation

For each staff member:

```
Weekly Workload = Sum of tariff hours of all assigned task instances in that week
```

---

### 6.3 Semester Workload Calculation

```
Semester Workload = Weekly Workload × Number of Academic Weeks
```

This allows evaluation of:

- Semester-level fairness
- Long-term workload balance

---

## 7. Underload and Overload Definitions

### 7.1 Underload

A staff member is considered **underloaded** if:

- Total weekly workload < 40 hours
  OR
- Teaching hours < expected teaching target for the role

### 7.2 Overload

A staff member is considered **overloaded** if:

- Total weekly workload significantly exceeds expected limits
- Teaching workload exceeds reasonable academic limits repeatedly

Both conditions are flagged by the system for review.

---

## 8. Task Eligibility Rules

To ensure academic quality:

1. **Qualification Requirement**

   - Staff must meet or exceed the minimum qualification required for a task

2. **Specialization Matching**

   - Subject specialization must match task domain (e.g., Physics vs Computer Science)

3. **Department Constraints**

   - Teaching tasks are assigned only within the same department unless overridden

4. **Role Constraints**

   - Administrative staff are excluded from teaching tasks by default

---

## 9. Administrative Override Policy

The system allows **administrative override** in exceptional cases:

- Emergency staffing
- Staff shortages
- Special approvals

Overrides:

- Are logged
- Require explicit authorization
- Are excluded from optimization penalties

---

## 10. Automation and Optimization

The WAM system uses an optimization algorithm (Genetic Algorithm) to:

- Minimize workload imbalance
- Avoid overload and underload
- Respect qualification and specialization constraints
- Produce fair, explainable allocations

Optimization is advisory and subject to human approval.

---

## 11. Review and Adjustment

- Workload assignments can be revised weekly or monthly
- Staff may submit change requests
- Administrators can approve, reject, or modify assignments

---

## 12. Compliance and Transparency

The system ensures:

- Transparent workload computation
- Policy-based allocation decisions
- Auditable workload records
- Fair treatment of academic staff

---

## 13. Conclusion

This workload policy provides a structured, fair, and policy-compliant foundation for academic workload management.
By combining UGC guidelines with automated optimization and administrative oversight, the WAM system ensures both **institutional efficiency** and **staff well-being**.

---

If you want, next I can:

- Convert this into a **PDF**
- Map each policy rule to **database fields**
- Show exactly how each rule is enforced in the **GA fitness function**
- Add this to your **memory_bank.md**

Just tell me the next step.
