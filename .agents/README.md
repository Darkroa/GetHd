1) Project Overview

The project is an HD Wallet Dashboard, a system for managing Hierarchical Deterministic (HD) crypto wallets. It allows users to generate "Master Seeds" (BIP39 mnemonics), encrypt and store them, and derive "Bot Wallets" (child addresses for BTC and ETH/USDT) from those seeds. It includes a web dashboard for administrative control and an automated background task structure for address generation.

2) Tech Stack

Backend: Python 3.12, FastAPI (Web Framework), SQLAlchemy (ORM), PostgreSQL (Database), Alembic (Migrations).
Frontend: React 19 (TypeScript), Vite (Build tool), Axios (API client).
Cryptography/Crypto: bip-utils (BIP39/44/address generation), cryptography (Fernet symmetric encryption for mnemonics).
Auth: JWT (Jose), Passlib (Bcrypt).
Admin: sqladmin (Flask-admin-like interface for FastAPI).
Task Queue: Celery/Redis (infrastructure present in requirements.txt but code uses FastAPI BackgroundTasks as well).
3) Architecture

Relationship: The project uses a decoupled Frontend/Backend architecture.
Frontend: A Single Page Application (SPA) in the Hdapp/ directory. It communicates with the backend via REST APIs at http://localhost:8000.
Backend: A FastAPI server in the app/ directory. It handles business logic, encryption, and database interactions.
Data Flow:
User creates a Master Seed -> Backend generates a mnemonic, encrypts it with a server-side SECRET_KEY, and stores only the encrypted version.
User creates a Bot Wallet -> Backend uses the encrypted seed to derive specific blockchain addresses (BIP44 path) in a background task.
Admin Interface -> A separate /admin route provides direct database management via sqladmin.
4) Features/Endpoints

Authentication:
POST /auth/login: Simple hardcoded demo login (admin/admin123). Returns a JWT.
Wallet Management:
GET /api/seeds: List all created master seeds (names and metadata).
POST /api/master-seed: Generate a new BIP39 mnemonic, encrypt it, and save it. Returns the plain mnemonic only once.
GET /api/wallets: List all bot wallets and their derived BTC/ETH addresses.
POST /api/bot-wallet: Link a bot to a master seed and trigger address derivation.
Admin:
/admin: UI for managing MasterSeed and BotWallet models directly.
Documentation:
/docs: Interactive Swagger UI.
5) Notable Patterns, Gaps, or Issues

Patterns:
Security: Use of Fernet for symmetric encryption of mnemonics is a good practice for seed storage.
Background Processing: Uses FastAPI BackgroundTasks for address derivation to keep the API responsive.
Gaps:
Incomplete Logic: app/routers/wallets.py triggers a background task manager.get_addresses_from_db_seed that returns addresses but does not actually save them back to the BotWallet record in the DB (lines 41-43).
Task Implementation: task.py is a skeleton file with "implement lookup" comments and isn't fully integrated into the main flow.
Auth: The authentication in app/routers/auth.py is hardcoded for a demo (admin/admin123) and lacks a real User model or registration.
Issues:
Encryption Key Risk: If the SECRET_KEY in local.env is lost, all stored mnemonics become permanently unrecoverable.
Derivation Logic: The derivation currently defaults to the first 5 addresses but only returns one to the UI, and the mapping from the background task result to the database model is missing.
Frontend Constants: The API URL is hardcoded as http://localhost:8000 in App.tsx, which may cause issues in non-local environments.