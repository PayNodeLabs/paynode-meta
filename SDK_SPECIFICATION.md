# 🛠️ PayNode SDK Specification & Implementation Standard (v2.2.2)

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
| **Sign Permit** | `signPermit()` | `sign_permit()` | EIP-2612 offline signature |
| **Sign Authorization** | `signTransferWithAuthorization()` | `sign_transfer_with_authorization()` | EIP-3009 offline signature |
| **Pay With Permit** | `payWithPermit()` | `pay_with_permit()` | On-chain submission of Permit tx |
| **Verifier Class** | `PayNodeVerifier` | `PayNodeVerifier` | For merchant-side verification |
| **Verify Entry Point** | `verify()` | `verify()` | Unified verification method |

---

## 3. Wire Protocol (Official x402 V2 Standard)

All SDKs and Middlewares must prioritize these **Official V2 Headers** for interoperability:
*   `PAYMENT-REQUIRED`: Base64 encoded JSON containing payment requirements (Server -> Client).
*   `PAYMENT-SIGNATURE`: Base64 encoded JSON containing the payment proof (Client -> Server).
*   `PAYMENT-RESPONSE`: Base64 encoded JSON containing settlement confirmation (Server -> Client).

The following **PayNode-Specific & Compatibility Headers** are also supported:
*   `X-402-Required`: Alias for `PAYMENT-REQUIRED` (Legacy Support).
*   `X-402-Payload`: Alias for `PAYMENT-SIGNATURE` (Legacy Support).
*   `X-402-Order-Id`: Unique tracking ID for the specific request session.
*   `X-PAYMENT-RESPONSE`: Alias for `PAYMENT-RESPONSE`.
*   `x-paynode-receipt`: Transaction hash (alias for PAYMENT-SIGNATURE on retry).
*   `x-paynode-order-id`: Unique session ID (alias for X-402-Order-Id).
*   `x-paynode-contract`: Router address (SSoT from `paynode-config.json`).
*   `x-paynode-merchant`: Receiver address.
*   `x-paynode-amount`: Total amount in smallest unit.
*   `x-paynode-currency`: ISO Currency code (e.g. USDC).
*   `x-paynode-token-address`: ERC20 token address.
*   `x-paynode-chain-id`: Network ID (e.g., 8453 for Base).
*   `X-PayNode-Network`: Network name (`mainnet` or `testnet`).

---

## 4. Error Handling & Standard Codes

All SDKs must throw `PayNodeException` with a standardized `code` and `message`.

| Error Code (Enum) | Standard Message | HTTP Map | Description |
| :--- | :--- | :--- | :--- |
| `RPC_ERROR` | "Failed to connect to any provided RPC nodes." | 533 | Network/Provider failure |
| `INSUFFICIENT_FUNDS` | "Wallet lacks USDC or ETH for gas." | 402 | Balance check failed |
| `AMOUNT_TOO_LOW` | "Payment amount is below the protocol minimum (1000)." | 402 | Fee truncation protection |
| `TOKEN_NOT_ACCEPTED` | "The provided token address is not in the whitelist." | 403 | Security/Fake token block |
| `TRANSACTION_FAILED` | "On-chain transaction reverted or failed." | 402 | Blockchain execution error |
| `DUPLICATE_TRANSACTION` | "This transaction hash has already been consumed." | 403 | Double-spend protection |
| `INVALID_RECEIPT` | "The provided receipt (TxHash) is malformed or invalid." | 403 | Verification failure |
| `INTERNAL_ERROR` | "An unexpected error occurred." | 500 | General catch-all |
| `TRANSACTION_NOT_FOUND` | "Transaction not found on-chain." | 404 | Receipt hash search failure |
| `WRONG_CONTRACT` | "Payment event was not emitted by the official PayNode contract." | 403 | Contract spoofing block |
| `ORDER_MISMATCH` | "OrderId in receipt does not match requested ID." | 403 | Cross-order receipt reuse block |
| `MISSING_RECEIPT` | "Please pay to PayNode contract and provide 'PAYMENT-SIGNATURE' header." | 402 | Initial handshake error |

*Note: Enums should be mapped to language-specific conventions (e.g., JS `RpcError`, Python `rpc_error`).*

---

## 5. x402 Autonomous Loop Logic

The `requestGate` method must execute:
1.  **Handshake**: Capture `402` status, extract `PAYMENT-REQUIRED` header, and parse JSON.
2.  **Pre-flight Check**: Validate `amount >= 1000`, check `token` whitelist, and ensure network compatibility.
3.  **Signature-First Strategy**: 
    - Priority 1: Use `signTransferWithAuthorization` (EIP-3009) if the token supports it.
    - Priority 2: Use `signPermit` (EIP-2612) + `payWithPermit` if token supports Permit but not EIP-3009.
    - Priority 3: Fallback to direct `pay` if only standard ERC20 is supported.
4.  **Retry**: Re-initiate the request with the `PAYMENT-SIGNATURE` header populated.
5.  **Confirmation**: Detect and log the `PAYMENT-RESPONSE` settlement header from the server's successful response.

---

## 6. Hardened Constraints
*   **Gas Strategy**: Use `GasPrice * 1.2` to ensure timely inclusion on-chain.
*   **Idempotency**: Verifier MUST track `TxHash` or `Nonce` in an `IdempotencyStore` to prevent replay.
*   **Nonce Safety**: SDKs must implement a local lock or queue to prevent nonce collisions during concurrent requests.

---
---

## 7. Payload Normalization (X402PayloadHelper)
To support multiple versions of x402 and legacy internal formats, SDKs must include a `X402PayloadHelper.normalize()` utility:
1.  **Format Detection**: Distinguish between official v2 (JSON with `x402Version: 2`) and internal legacy (base64 JSON).
2.  **Type Inference**: If `type` is missing, infer `eip3009` if `signature` or `authorization` is present; otherwise `onchain`.
3.  **Domain Mapping**: 
    - Official Base USDC (v2) uses `USD Coin` as Domain Name on Testnet.
    - Custom/Legacy configurations may use `USDC` on Mainnet. SDKs must respect the `extra.name` provided by the server.

---

*PayNode Protocol - Standard RFC v2.2.2*
