# PayNode Full-Stack Changelog

## [1.1.1] - 2026-03-22 (Security Hardened & Meta Hub)

This release marks the establishment of the **PayNode Meta Architecture** and critical security hardening for autonomous AI payments.

### 🛡️ Security Hardening
- **Dust Exploit Protection**: SDKs now enforce a minimum payment of **0.001 USDC** (1000 units) to ensure protocol fees (1%) never truncate to zero.
- **Fee-on-transfer Defense**: SDK token whitelist is now strictly restricted to **Official USDC** only, preventing fake-token and inflationary/deflationary attacks.
- **Multinode Redundancy (Failover)**: 
  - **JS SDK**: Integrated `ethers.FallbackProvider` for automatic RPC failover and retry.
  - **Python SDK**: Implemented proactive RPC detection and failover logic in the Client.

### 🏛️ Meta & Ecosystem
- **Meta Repository (SSoT)**: Launched `paynode-meta` as the **Single Source of Truth** for global configuration, branding, and engineering specs.
- **Engineering Constitution**: Published **SDK_SPECIFICATION.md (v1.2)**, standardizing "Permit-First" and "Idempotency" across all language implementations.
- **Official Brand Kit**: Unified all logos, icons, and OG-images in the central `public/` directory.

### 📂 SDK Updates
- **JS SDK (v1.1.1)**: Unified `PayNodeAgentClient` class name and `requestGate` methods. Added publishing instructions to NPM.
- **Python SDK (v1.1.1)**: Standardized initialization parameters and `request_gate` method for parity with JS SDK. Added PyPI publishing guide.

---

## [1.1.0] - 2026-03-21 (Production-Ready)

This is the first production-ready release of the **PayNode Protocol** on Base L2 Mainnet.

### 🚀 Key Highlights
- **Base Mainnet Support**: Officially deployed to `0x92e20164FC457a2aC35f53D06268168e6352b200`.
- **EIP-2612 Permit Support**: Agents can now pay with offline signatures, enabling true agent-mediated payments.
- **Centralized Configuration**: All network metadata is now managed via a single `paynode-config.json` in the root directory.

---

## [1.0.1] - 2023-02-15
- Initial MVP release for Base Sepolia Testnet.
- Basic payment forwarding (99%/1% split).
- Early JS/Python SDK prototypes.
