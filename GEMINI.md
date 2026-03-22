# PayNode Protocol

## 🚀 Project Overview

The **PayNode Workspace** is a monorepo-style physical container that orchestrates 5 independent Git repositories. The PayNode Protocol is a stateless, non-custodial Machine-to-Machine (M2M) payment gateway built for the AI economy, leveraging the x402 standard to allow AI agents to securely pay for digital resources using USDC on Base L2. 

The workspace is organized into two primary layers: `apps/` (front-facing products) and `packages/` (core protocol and developer tools).

### Architecture & Components

1. **`apps/paynode-web/`**
   - **Type:** Frontend Application (Next.js 15, React 19, Tailwind CSS)
   - **Purpose:** The main web portal, merchant dashboard, and block explorer for PayNode.
2. **`apps/paynode-docs/`**
   - **Type:** Documentation Site (Next.js 15, Nextra 3)
   - **Purpose:** The official documentation portal available at `docs.paynode.dev`.
3. **`packages/contracts/`**
   - **Type:** Smart Contracts (Solidity, Foundry)
   - **Purpose:** Stateless smart contracts deployed on Base L2 designed for low-latency M2M payments, executing an atomic 99% merchant / 1% protocol fee split without storing states (SSTORE).
4. **`packages/sdk-js/`**
   - **Type:** JavaScript/TypeScript Library (NPM)
   - **Purpose:** The official JS/TS SDK providing Agent client functionality and Merchant server middleware (Express) for interpreting x402 headers and settling payments.
5. **`packages/sdk-python/`**
   - **Type:** Python Library (PyPI)
   - **Purpose:** The official Python SDK optimized for Python-based AI workflows (LangChain, AutoGen) and modern Python backends (FastAPI) to handle autonomous x402 payments.

---

## 🛠️ Building and Running

Because this directory is just an organizational folder containing distinct projects, **all commands must be run within their respective sub-directories.**

### 1. Web Portal (`apps/paynode-web/`)
- **Install:** `npm install`
- **Development:** `npm run dev`
- **Build:** `npm run build`
- **Start Production:** `npm run start`
- **Linting:** `npm run lint`

### 2. Documentation (`apps/paynode-docs/`)
- **Install:** `yarn install`
- **Development:** `yarn dev`
- **Build:** `yarn build`
- **Start Production:** `yarn start`

### 3. Smart Contracts (`packages/contracts/`)
- **Build/Compile:** `forge build`
- **Test:** `forge test -vvv`
- **Deploy:** `forge script script/Deploy.s.sol --rpc-url $BASE_RPC --broadcast`

### 4. JavaScript SDK (`packages/sdk-js/`)
- **Install:** `npm install`
- **Build:** `npm run build` (uses `tsc`)
- **Test:** `npm run test`

### 5. Python SDK (`packages/sdk-python/`)
- **Install dependencies:** `pip install -e .` or via a virtual environment.
- **Build Package:** `python -m build`
- **Testing:** `pytest` (Inferring standard python testing practices)

---

## ⚙️ Configuration Management

To maintain consistency across all 5 repositories, PayNode uses a **Source of Truth** approach:

- **Config File**: `paynode-config.json` (Root) - Contains all network metadata and router addresses.
- **Sync Tool**: `python3 scripts/sync-config.py` (Root) - Propagates changes to all sub-projects.

**Workflow for Network Updates:**
1. Update addresses in `paynode-config.json`.
2. Run `python3 scripts/sync-config.py`.
3. Verify and commit the generated changes in each sub-repository.

---

## 🔐 Development Conventions & Rules

1. **Version Control & Repository Boundaries:**
   - The root `/paynode` directory is **NOT** a git repository. Do not run `git` commands at the root level.
   - You must navigate (`cd`) into the specific `apps/` or `packages/` directory before staging or committing changes, as each is a standalone Git repository linked to its own remote on GitHub under `PayNodeLabs`.

2. **Branch Protection:**
   - All `main` branches across the 5 repositories are **strictly protected**.
   - **Direct pushes to `main` are prohibited.** 
   - **Workflow:** 
     1. Create a new branch: `git checkout -b feature/<name>`
     2. Make changes and commit.
     3. Push to the remote: `git push origin feature/<name>`
     4. Submit a **Pull Request (PR)** on GitHub.
     5. Ensure all CI/CD status checks (e.g., Vercel builds, linting) pass before merging using a linear history (Rebase) strategy.

3. **Core Protocol Principles:**
   - **"Don't Trust, Verify":** The protocol is stateless. Do not introduce central databases for order tracking. Verification relies exclusively on the Base L2 RPC and TxHashes.
   - **Security:** Ensure environment variables are strictly used for private keys. Agents run securely and should never expose credentials on the client side.

4. **Environment Settings:**
   - Always ensure API Keys (like `BASESCAN_API_KEY`) and RPC URLs (e.g., Alchemy, Infura for Base L2) are appropriately loaded in the `.env` files of their respective projects before running deployments or tests.
