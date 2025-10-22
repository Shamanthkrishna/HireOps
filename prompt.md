### ✅ **Final GitHub Copilot Prompt**

```
You are an expert Python full-stack developer and system designer.

TASK OVERVIEW:
You must build a web-based recruitment tracking system for a staffing company, based entirely on the business process described below. The system should be implemented using only Python-based technologies. The stack may include FastAPI or Flask, SQLModel/SQLAlchemy ORM, Jinja2 templates, and either SQLite (for development) or PostgreSQL (for production). No Node.js or JavaScript frameworks.

---

## PROJECT SCENARIO SUMMARY

The staffing company (call it Company D) manages hiring for clients (A, B, and C).  
Company D has the following hierarchy:

- **Business Head** → has full access
- **Business Support Team** → includes my client (the one requesting this app)
- **Sales Head** → manages **Sales Persons**
- **Accounts Manager (AM)** → manages **Recruiters**

### Process Flow
1. Sales Person gathers **job openings (requirements)** from client companies A, B, C.
2. They send requirements to the **Account Manager (AM)**.
3. The AM assigns requirements to **Recruiters**.
4. Recruiters source candidates and track each one’s progress through multiple **status stages** (Submission → Interview → Offered → Hired, etc.).
5. Candidates might be hired on **contract or permanent** basis.
6. Contracted candidates are employees of Company D but work for client companies.

Currently, all this is managed manually through a shared **Google Sheet** with two main sheets:
- **Requirement Tracker**
- **Candidate Tracker**

These have fields like Req ID, Client Name, Recruiter, AM, Mode of Employment, Status, Notes, Priority, Budget, Experience, etc.

### Client’s Core Problem
When Recruiters update candidate statuses, there’s **no easy way to track historical changes** — my client manually checks “Version History” on Google Sheets.  
He needs a **portal** where:
- All users can enter data through a web UI (not a shared sheet)
- All data is stored in a proper database
- There’s **audit tracking** (status change history)
- There’s a **role-based dashboard** (different access for Business Head, AM, Recruiter, and Sales)

---

## COPILOT INSTRUCTIONS

You must perform this task in **two main stages**:

### **Stage 1: Generate Clarification Document**
Before coding, generate a structured **Clarification Document** automatically.  
The goal is to gather all unknown requirements that must be confirmed with the client before starting development.  
Your clarification document must include detailed and well-organized questions on:
- User roles, permissions, and access levels
- Authentication and login preferences
- Dashboard KPIs and metrics
- Status change history detail (depth and retention)
- Import/export needs (Google Sheets or CSV)
- Notifications (email, alerts)
- File uploads (candidate CVs)
- Hosting, scaling, backups
- UI design and branding preferences
- Must-have vs nice-to-have features

Clearly label this section as:
> **“📄 Clarification Document (To be confirmed with client before development)”**

After generating this document, pause further development until the clarifications are filled in.

---

### **Stage 2: Application Generation**

Once clarifications are filled in, generate the complete **Python-based web application**, including:

#### Tech Stack
- **Backend:** FastAPI (preferred) or Flask
- **ORM:** SQLModel or SQLAlchemy
- **Database:** SQLite (local) → PostgreSQL (production-ready)
- **Templates:** Jinja2 (Bootstrap/Tailwind for basic styling)
- **Authentication:** Session-based login (bcrypt-hashed passwords)
- **Role-based Access Control:** Business Head (admin), AM, Recruiter, Sales (read-only)
- **Migrations:** Alembic
- **Tests:** pytest

#### Core Features
1. **Requirement Management**
   - CRUD for requirements (with ageing calculation)
   - Filter/sort/search by client, recruiter, AM, or status

2. **Candidate Management**
   - CRUD for candidates
   - Status dropdown with predefined options
   - Automatic timestamp on status change
   - Audit trail stored in a `CandidateStatusHistory` table
   - Candidate detail page shows full chronological history of status updates

3. **User Management**
   - Login/logout, password hashing, and session handling
   - Role-based permissions on all routes and actions

4. **Dashboards**
   - KPIs per role (open reqs, average ageing, submissions, hires, etc.)
   - Aggregated visualizations (server-rendered or chart images)

5. **Import/Export**
   - CSV import/export for Requirement and Candidate data

6. **Audit Logging**
   - Track all status changes, with “changed_by”, timestamps, and old/new values.

7. **Deployment**
   - Configurable `.env` for DB URLs, SMTP, and secrets
   - README with setup, migration, and run instructions

8. **Optional**
   - Email notifications for key actions (status changes, new hires)
   - File uploads (store CVs under `/media`)

---

### **Output Format**

1. Start by printing the **📄 Clarification Document** first (auto-generated).
2. After user fills in the clarification answers and types “Proceed with application”, then:
   - Generate the **system design plan** (tables, flow, endpoints, UI outline)
   - Generate **codebase** (models, routes, templates, migrations, README)
   - Provide **sample seed data** and test scripts

---

### STYLE REQUIREMENTS
- Use consistent naming and modular structure:
```

app/
├── main.py
├── models.py
├── schemas.py
├── crud.py
├── auth.py
├── routes/
├── templates/
├── static/
├── migrations/
└── tests/

```
- Comment major functions clearly.
- Enforce best practices (bcrypt password hashing, CSRF protection, role-check decorators, input validation).
- Provide migration and seeding scripts.

---

### SUMMARY
Step 1 → Copilot must first generate and output the **Clarification Document**.  
Step 2 → After confirmation, Copilot must generate the **complete Python-based recruitment portal** as described above.

END OF PROMPT.
```

---

### ✅ How to use it

1. Paste the full prompt above into **Copilot Chat** (in VS Code, Cursor, or GitHub.com).
2. Let it generate the “📄 Clarification Document” first.
3. Fill in answers from your client.
4. Type: **“Proceed with application”** — and Copilot will continue to generate the project structure and code accordingly.

---
