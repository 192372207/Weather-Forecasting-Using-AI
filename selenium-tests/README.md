# Selenium E2E Tests — SkySense AI

## Overview
This directory contains end-to-end (E2E) Selenium WebDriver tests for the **SkySense AI** web frontend.

## Directory Structure
```
selenium-tests/
├── tests/
│   └── login-tests.js        # 300+ E2E tests covering login, registration, auth flows
├── reports/                  # Generated test reports (auto-created)
├── screenshots/              # Failed test screenshots (auto-created)
├── package.json
├── .env.example
└── README.md
```

## Prerequisites
- Node.js >= 18.x
- Google Chrome (latest) or Firefox
- ChromeDriver (matching Chrome version)

## Installation
```bash
cd selenium-tests
npm install
```

## Configuration
Copy `.env.example` to `.env` and fill in values:
```bash
cp .env.example .env
```

## Running Tests
```bash
# Run all tests
npm test

# Run only login tests
npm run test:login

# Run in headed/visible mode
npm run test:headed
```

## Test Coverage
The test suite covers:
- Login page UI/UX (elements, labels, placeholders)
- Email/password form validation
- Authentication flows (success, failure)
- Google OAuth login
- Session persistence & logout
- Registration page flows
- Password visibility toggle
- Accessibility & keyboard navigation
- Error message display
- Navigation & routing post-login
- Responsive design (mobile/tablet/desktop)
- Security tests (XSS, SQL injection attempts)
- Performance & load time checks
