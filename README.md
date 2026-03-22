# 🌐 PayNode Meta

> **The Gateway to the Autonomous AI Economy.**

PayNode is a stateless, non-custodial M2M (Machine-to-Machine) payment gateway built for the Agentic Era. This meta-repository serves as the central hub, brand asset kit, and architectural source of truth for the entire PayNode ecosystem.

---

## 🚀 Ecosystem Matrix

The PayNode protocol is distributed across specialized repositories to ensure modularity and high performance.

| Repository | Purpose | Tech Stack |
| :--- | :--- | :--- |
| **[paynode-contracts](https://github.com/PayNodeLabs/paynode-contracts)** | Core stateless smart contracts on Base L2 | Solidity, Foundry |
| **[paynode-sdk-js](https://github.com/PayNodeLabs/paynode-sdk-js)** | TS/JS SDK for Agents & Merchant Middleware | TypeScript, Ethers.js |
| **[paynode-sdk-python](https://github.com/PayNodeLabs/paynode-sdk-python)** | Python SDK for AI Workflows (LangChain, AutoGen) | Python, Web3.py |
| **[paynode-web](https://github.com/PayNodeLabs/paynode-web)** | Web Portal, Simulator & Doodle Wall (POM) | Next.js 15, Tailwind |
| **[paynode-docs](https://github.com/PayNodeLabs/paynode-docs)** | Official Documentation Site | Nextra 3, Next.js |

---

## ⚖️ Governance & Specs

*   **[SDK_SPECIFICATION.md](./SDK_SPECIFICATION.md)**: The "PayNode Engineering Constitution" — Ensuring parity across all language implementations.
*   **[paynode-config.json](./paynode-config.json)**: The **Single Source of Truth** for contract addresses, chain metadata, and protocol constants.

---

## 🎨 Brand Assets (Brand Kit)

Located in the [`/public`](./public) folder. This is the official repository for PayNode logos, icons, and OG images for partners and merchants.

- `logo.png`: Main icon.
- `logo-full.png`: Landscape logo with text.
- `og-image.png`: High-fidelity branding for social sharing.

---

## ⚙️ Global Synchronization

We use a centralized script to propagate configuration changes across all 5 repositories:

```bash
python3 scripts/sync-config.py
```
*Always run this after updating `paynode-config.json` before pushing to sub-repositories.*

---
*Built for the Autonomous AI Economy by [PayNodeLabs](https://github.com/PayNodeLabs).*
