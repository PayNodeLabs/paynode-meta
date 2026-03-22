# PayNode Full-Stack Changelog

## [1.1.0] - 2026-03-21 (Production-Ready)

This is the first production-ready release of the **PayNode Protocol** on Base L2 Mainnet.

### 🚀 Key Highlights
- **Base Mainnet Support**: Officially deployed to `0x92e20164FC457a2aC35f53D06268168e6352b200`.
- **EIP-2612 Permit Support**: Agents can now pay with offline signatures, enabling true agent-mediated payments.
- **Centralized Configuration**: All network metadata is now managed via a single `paynode-config.json` in the root directory.
- **Enhanced Security**:
  - Contracts: Added `Pausable`, `Ownable2Step`, and Custom Errors for Gas efficiency.
  - SDKs: Implemented real on-chain `Verifier` with fallback RPC support and Redis idempotency.

### 📂 Sub-Project Updates
- **JS SDK (v1.1.0)**: New `PayNodeVerifier`, `FallbackProvider`, and Redis-based idempotency.
- **Python SDK (v1.1.0)**: New `Verifier` with thread-safe nonce management and private key safety.
- **Contracts (v1.1)**: Stateless router with zero-SSTORE fee split and EIP-2612 support.
- **Web Portal**: Added server-side chain validation and BigInt precision for all calculations.

---

## [1.0.1] - 2026-02-15
- Initial MVP release for Base Sepolia Testnet.
- Basic payment forwarding (99%/1% split).
- Early JS/Python SDK prototypes.
