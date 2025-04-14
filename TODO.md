### TODO List: Expense Tracker & Data Analysis App

## Frontend Tasks

- [ ] Setup Base HTML Template (`base.html`)
  - [ ] Bootstrap integration
  - [ ] Responsive layout
  - [ ] Navbar (home, upload, dashboard, share, logout)

- [ ] Create Pages
  - [ ] `home.html` – Intro and login/register links
  - [ ] `login.html` and `register.html`
  - [ ] `upload.html` – Expense entry form
  - [ ] `visualise.html` – Charts and stats
  - [ ] `share.html` – Share interface
  - [ ] `dashboard.html` – User's overall view

- [ ] Styling
  - [ ] Write `styles.css`
  - [ ] Use Bootstrap components for consistency
  - [ ] Improve form design and responsiveness

---

## Backend Tasks

- [ ] Flask App Factory (`__init__.py`)
- [ ] Create Models
  - [ ] `User` model (username, email, password)
  - [ ] `Expense` model (user_id, amount, category, date, description)
  - [ ] `Share` model (user_id, shared_with_id, expense_id)

- [ ] Routing Logic
  - [ ] `/register`, `/login`, `/logout`
  - [ ] `/upload`, `/dashboard`, `/share`, `/visualise`

- [ ] Forms (Flask-WTF)
  - [ ] RegistrationForm
  - [ ] LoginForm
  - [ ] ExpenseForm
  - [ ] ShareForm (or dropdown selection)
