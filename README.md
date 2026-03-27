# 🌐 PayNode Meta Hub

> **The Sovereign Financial Infrastructure for the Agentic Era.**

PayNode is a **stateless, non-custodial M2M (Machine-to-Machine) payment gateway** built specifically for autonomous AI Agents. It standardizes the **x402 Protocol Extension (v2)**, enabling agents to handle `402 Payment Required` errors silently and securely across the API economy using USDC on Base L2.

This meta-repository is the **Single Source of Truth (SSoT)** for the PayNode ecosystem, housing core SDKs, brand assets, and the global configuration heartbeat.

---

## 🚀 Ecosystem Matrix (v1.4.0)

Distributed modularity for high-performance agentic workflows.

| Category | Repository / Path | Purpose | Tech Stack |
| :--- | :--- | :--- | :--- |
| **Core** | **[paynode-contracts](https://github.com/PayNodeLabs/paynode-contracts)** | Stateless Smart Contracts (CREATE2) | Solidity, Foundry |
| **SDK (JS)** | **[paynode-sdk-js](https://github.com/PayNodeLabs/paynode-sdk-js)** | SDK v2.2.0: ESM & CommonJS support | TypeScript, Ethers.js |
| **SDK (Py)** | **[paynode-sdk-python](https://github.com/PayNodeLabs/paynode-sdk-python)** | SDK v2.2.0: Thread-safe, FastAPI native | Python, Web3.py |
| **AI Skills** | **[paynode-ai-skills](https://github.com/PayNodeLabs/paynode-ai-skills)** | **paynode-402**: Autonomous payment skill | LangChain, OpenAI |
| **Web** | **[paynode-web](https://github.com/PayNodeLabs/paynode-web)** | Dashboard, Simulator & Explorer | Next.js 15, Supabase |
| **Docs** | **[paynode-docs](https://github.com/PayNodeLabs/paynode-docs)** | Official Protocol Documentation | Nextra 3, Next.js |


---

## 🏗️ Architectural Core

- **[ARCHITECTURE_MAP.md](./ARCHITECTURE_MAP.md)**: The global feature chain and dependency matrix (v1.4.0).
- **[SDK_SPECIFICATION.md](./SDK_SPECIFICATION.md)**: Behavioral parity standards for cross-language implementations (v2.2.0).
- **[paynode-config.json](./paynode-config.json)**: The **SSoT Heartbeat** containing contract addresses, whitelists, and 12+ standard error codes.
- **x402 v2 Extension**: Implements the `Handshake` -> `Pre-flight` -> `Signature-First` workflow.

### 🛡️ Payment Strategies (v2.2.0)
1. **EIP-3009 (Recommended)**: Gasless off-chain signing (`TransferWithAuthorization`). Merchant pays gas.
2. **EIP-2612**: Gasless approval (`permit`) with on-chain settlement via `payWithPermit`.
3. **Standard ERC20**: Traditional `approve` + `pay` fallback.

---

## ⚙️ Global Synchronization Engine

We use a centralized sync engine to propagate configuration changes (Chain IDs, RPCs, Router addresses, Error Codes) from `paynode-config.json` to all modules.

### Expected Mono-repo Structure
```text
paynode/ (Meta Hub Root)
├── paynode-config.json     # SSoT (Config Hub)
├── scripts/
│   └── sync-config.py      # Propagator
├── packages/
│   ├── sdk-js/             # Updates src/constants.ts & src/errors/index.ts
│   ├── sdk-python/         # Updates constants.py & errors.py
│   ├── contracts/          # Updates Config.s.sol
│   └── paynode-ai-skills/  # AI Tools & Logic
└── apps/
    ├── paynode-web/        # Updates config.ts & POM settings
    └── paynode-docs/       # Markdown sync
```

### Running the Sync
Whenever you modify `paynode-config.json` or contract addresses:
```bash
python3 scripts/sync-config.py
```

---

## ⚡ Quick Integration

PayNode is designed for sub-minute integration.

### JS/TS (Merchant Middleware)
```typescript
import { x402Gate } from '@paynodelabs/sdk-js';

app.get('/api/resource', x402Gate({
  merchantAddress: '0x...',
  price: '1.0' // 1.0 USDC
}), (req, res) => res.json({ data: 'success' }));
```

### Python (Agent Client)
```python
from paynode_sdk import PayNodeAgentClient

agent = PayNodeAgentClient(private_key="0x...")
response = agent.request_gate("https://api.merchant.com/data")
```

---

## 🎨 Visual Assets
Located in [`/public`](./public). Includes official logos, OG images, and UI component assets for ecosystem partners.

- `logo.png`: The trademark `$_` shield.
- `logo-full.png`: Landscape branding.
- `og-image.png`: High-fidelity metadata imagery.

---

_Built for the Sovereign Machine Economy by **[PayNodeLabs](https://github.com/PayNodeLabs)**._
_Protocol live on **Base Mainnet (8453)**._

