# 🛠️ PayNode SDK Specification & Implementation Standard (v1.3)

## 1. Design Philosophy
*   **Autonomous First**: SDKs must enable AI Agents to autonomously complete the "Request -> Detect 402 -> Pay -> Retry" loop without human intervention.
*   **Stateless & Non-Custodial**: SDKs do not store persistent state other than the private key, acting as a direct interface to Base L2.
*   **Consistency**: SDKs across different languages must maintain highly mirrored API definitions, parameter ordering, error codes, and behavioral logic.

---

## 2. Core Component Naming Standards

| Feature | JS/TS (CamelCase) | Python/Go (SnakeCase) | Description |
| :--- | :--- | :--- | :--- |
| **Main Client Class** | `PayNodeAgentClient` | `PayNodeAgentClient` | Unified class name |
| **Exception Class** | `PayNodeException` | `PayNodeException` | Standardized error type |
| **Autonomous Request** | `requestGate()` | `request_gate()` | Core entry point, handles 402 loop |
| **Sign Permit Method** | `signPermit()` | `sign_permit()` | EIP-2612 offline signature |
| **Pay With Permit** | `payWithPermit()` | `pay_with_permit()` | On-chain submission of Permit tx |
| **Verifier Class** | `PayNodeVerifier` | `PayNodeVerifier` | For merchant-side verification |

---

## 3. Wire Protocol (x402 Headers)

All SDKs and Middlewares must use these exact Header keys:
*   `x-paynode-contract`: Router address.
*   `x-paynode-merchant`: Receiver address.
*   `x-paynode-amount`: Total amount in smallest unit (e.g. Wei).
*   `x-paynode-token-address`: ERC20 token address (USDC).
*   `x-paynode-chain-id`: Network ID (8453).
*   `x-paynode-order-id`: Unique session/tracking ID.
*   `x-paynode-receipt`: Transaction hash (submitted on retry).

---

## 4. Error Handling & Standard Codes

All SDKs must throw `PayNodeException` with a standardized `code` and `message`.

| Error Code | Standard Message | HTTP Map | Description |
| :--- | :--- | :--- | :--- |
| `RPC_ERROR` | "Failed to connect to any provided RPC nodes." | 503 | Network/Provider failure |
| `INSUFFICIENT_FUNDS` | "Wallet lacks USDC or ETH for gas." | 400 | Balance check failed |
| `AMOUNT_TOO_LOW` | "Payment amount is below the protocol minimum (1000)." | 400 | Fee truncation protection |
| `TOKEN_NOT_ACCEPTED` | "The provided token address is not in the whitelist." | 403 | Security/Fake token block |
| `TRANSACTION_FAILED` | "On-chain transaction reverted or failed." | 400 | Blockchain execution error |
| `DUPLICATE_TRANSACTION` | "This transaction hash has already been consumed." | 403 | Double-spend protection |
| `INVALID_RECEIPT` | "The provided receipt (TxHash) is malformed or invalid." | 403 | Verification failure |
| `INTERNAL_ERROR` | "An unexpected error occurred within the PayNode SDK." | 500 | General catch-all |

---

## 5. x402 Autonomous Loop Logic

The `requestGate` method must execute:
1.  **Handshake**: Capture `402` status and extract headers.
2.  **Pre-flight**: Validate `amount >= 1000` and `token` whitelist.
3.  **Permit-First Execution**: Default to `payWithPermit` if token supports EIP-2612.
4.  **Retry**: Re-initiate with `x-paynode-receipt`.

---

## 6. Hardened Constraints
*   **Gas Strategy**: Default to `GasPrice * 1.2`.
*   **Idempotency**: Verifier MUST track `TxHash` to prevent replay.

---
*PayNode Protocol - Standard RFC v1.3*
