# 🌐 PayNode Meta Hub

> **The Gateway to the Autonomous AI Economy.**

PayNode is a stateless, non-custodial M2M (Machine-to-Machine) payment gateway built for the Agentic Era. It implements the **x402 Protocol Extension**, allowing AI Agents to autonomously detect payment requirements, execute on-chain transactions (via EIP-2612 Permits), and fulfill requests without human intervention.

This meta-repository serves as the **Single Source of Truth (SSoT)**, central configuration hub, and architectural anchor for the entire PayNode ecosystem.

---

## 🚀 Ecosystem Matrix (v1.1.1)

The PayNode protocol is distributed across specialized repositories to ensure modularity and high performance.

| Repository                                                                  | Purpose                                         | Tech Stack            |
| :-------------------------------------------------------------------------- | :---------------------------------------------- | :-------------------- |
| **[paynode-contracts](https://github.com/PayNodeLabs/paynode-contracts)**   | Core stateless smart contracts on Base L2       | Solidity, Foundry     |
| **[paynode-sdk-js](https://github.com/PayNodeLabs/paynode-sdk-js)**         | TS/JS SDK for Agents & Merchant Middleware      | TypeScript, Ethers.js |
| **[paynode-sdk-python](https://github.com/PayNodeLabs/paynode-sdk-python)** | Python SDK for AI Workflows (LangChain, OpenAI) | Python, Web3.py       |
| **[paynode-web](https://github.com/PayNodeLabs/paynode-web)**               | Web Portal, Simulator & Merchant Dashboard      | Next.js 15, Tailwind  |
| **[paynode-docs](https://github.com/PayNodeLabs/paynode-docs)**             | Official Documentation & API Reference          | Nextra 3, Next.js     |

---

## 🏗️ Architectural Core

- **[SDK_SPECIFICATION.md](./SDK_SPECIFICATION.md)**: The "PayNode Engineering Constitution" — Ensuring behavioral parity across all language implementations (v1.4).
- **[paynode-config.json](./paynode-config.json)**: The global configuration file containing contract addresses, chain metadata, and standardized error codes.
- **Sandbox & Mainnet**: Supports **Base Mainnet (8453)** for production and **Base Sepolia (84532)** for risk-free agent testing.

---

## 🎨 Brand Assets (Brand Kit)

Located in the [`/public`](./public) folder. This is the official source for PayNode logos, icons, and OG images for partners, merchants, and community builders.

- `logo.png`: The "$\_" shield icon.
- `logo-full.png`: Landscape branding.
- `og-image.png`: High-fidelity branding for social metadata.

---

## ⚙️ Global Synchronization

We use a centralized script to propagate configuration changes (Chain IDs, RPCs, Router addresses, Error Codes) from the `paynode-config.json` to all sub-packages in the mono-repo:

### Expected Mono-repo Structure
The script operates on the following standard directory layout:
```text
paynode/ (Root)
├── paynode-config.json     # SSoT (Single Source of Truth)
├── scripts/
│   └── sync-config.py      # Sync Engine
├── packages/
│   ├── sdk-js/             # Auto-updates src/constants.ts & errors/index.ts
│   ├── sdk-python/         # Auto-updates paynode_sdk/constants.py & errors.py
│   └── contracts/          # Auto-updates script/Config.s.sol
└── apps/
    └── paynode-web/        # Auto-updates app/api/pom/config.ts
```

### Running the Sync
Whenever you modify `paynode-config.json`, run:

```bash
python3 scripts/sync-config.py
```

_Note: This ensures protocol-wide consistency across all language implementations and deployments._

---

_Built for the Autonomous AI Economy by [PayNodeLabs](https://github.com/PayNodeLabs)._
