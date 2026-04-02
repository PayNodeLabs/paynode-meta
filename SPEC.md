# PayNode x402 v2 Protocol Specification

This document defines the protocol contract that all PayNode SDKs must follow.

This is a protocol document, not a JavaScript implementation guide. Wire format, verification rules, compatibility behavior, and security requirements defined here apply to all SDKs, including JS, Python, Java, and Go.

## 1. Scope

This specification covers two distinct protocol layers:

1. **Part I: Direct x402 Protocol (Upstream-Aligned)**: A stateless payment handshake between an Agent and a Merchant.
2. **Part II: PayNode Market Proxy Protocol**: A trust-based flow where a Merchant verifies requests signed by the PayNode Market Proxy.

These layers have different trust assumptions, headers, and verification rules. They must not be confused.

---

## Part I: Direct x402 Protocol

### 2. Upstream-Aligned Model

The canonical payment loop is:
1. Merchant returns `402 Payment Required` challenge.
2. Agent chooses a payment option and produces a payment proof.
3. Agent retries the original request with the proof.
4. Merchant verifies proof and returns the protected response.

### 3. Merchant Challenge (402)

When a protected resource requires payment, the merchant must respond with:
- HTTP status `402`.
- JSON response body.
- `PAYMENT-REQUIRED` header (Base64-encoded version of the JSON body).
- `X-402-Order-Id` header (Merchant-generated unique request identifier).

#### 3.1 Challenge Body JSON Shape
(Reference: `meta/fixtures/wire/base/payment_required.json`)

```json
{
  "x402Version": 2,
  "error": "Payment Required by PayNode",
  "resource": {
    "url": "https://api.merchant.com/v1/tools",
    "description": "Premium AI reasoning engine",
    "mimeType": "application/json"
  },
  "orderId": "merchant-order-123",
  "accepts": [
    {
      "scheme": "exact",
      "type": "eip3009",
      "network": "eip155:8453",
      "amount": "100000",
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "payTo": "0xMerchantWallet",
      "maxTimeoutSeconds": 3600,
      "extra": { "name": "USDC", "version": "2" }
    },
    {
      "scheme": "exact",
      "type": "onchain",
      "network": "eip155:8453",
      "amount": "100000",
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "payTo": "0xMerchantWallet",
      "maxTimeoutSeconds": 3600,
      "router": "0xPayNodeRouter"
    }
  ]
}
```

#### 3.2 Normative Rules (Challenge)
- `x402Version` MUST be `2`.
- `orderId` MUST be present in the root of the body and in the `X-402-Order-Id` header.
- `scheme` MUST be `"exact"` for this version.
- `network` MUST use CAIP-2 identifiers (`eip155:<chainId>`).
- `amount` MUST be an integer string in base units (e.g. 100000 for 0.1 USDC with 6 decimals).

### 4. Agent Retry (Payment Proof)

The agent retries the original request with:
- `PAYMENT-SIGNATURE` header (Base64-encoded JSON envelope).
- `X-402-Order-Id` header (matching the challenge).

#### 4.1 Payment Signature Envelope
(Reference: `meta/fixtures/wire/base/payment_signature_eip3009.json`)

```json
{
  "x402Version": 2,
  "resource": { "url": "https://api.merchant.com/v1/tools" },
  "accepted": {
    "scheme": "exact",
    "type": "eip3009",
    "network": "eip155:8453",
    "amount": "100000",
    "asset": "0xToken",
    "payTo": "0xMerchantWallet"
  },
  "payload": { ... }
}
```

### 5. Settlement Modes

#### 5.1 EIP-3009 (Off-chain Signature)
Payload MUST contain `signature` and `authorization` fields. (Reference: `meta/fixtures/crypto/eip3009_transfer_with_authorization.json`).

#### 5.2 On-chain Receipt
Payload MUST contain `txHash`. (Reference: `meta/fixtures/wire/base/payment_signature_onchain.json`).

### 6. Merchant Verification Rules

1. **Amount**: MUST be >= required amount.
2. **Token**: MUST be on the merchant-configured whitelist.
3. **Destination**: MUST match the merchant address.
4. **Order ID**: MUST match the request session.
5. **Replay**: MUST NOT have been processed before (nonce or txHash check).

---

## Part II: PayNode Market Proxy Protocol

### 7. Market Proxy Model

In this flow, the Merchant trusts the PayNode Market Proxy. The Proxy handles the 402 handshake and sends a verified request to the Merchant over HTTPS, signed with a shared HMAC secret.

### 8. Proxy Request Headers

The Proxy includes these headers in its request to the Merchant:
- `X-PayNode-Signature`: HMAC-SHA256 signature.
- `X-PayNode-Timestamp`: Unix timestamp (milliseconds).
- `X-PayNode-Request-Id`: Unique identifier for the proxied request.
- `X-PayNode-Discovery`: (Optional) `true` for discovery probes.

### 9. HMAC Signature Generation (Frozen)

The signature MUST be calculated as:
`HMAC-SHA256(sharedSecret, requestId + ":" + timestamp)`

(Reference: `meta/fixtures/crypto/market_proxy_hmac.json`)

#### 9.1 Verification Procedure
1. Check `timestamp` is within allowed drift (e.g. ±5 minutes).
2. Use constant-time comparison to verify `X-PayNode-Signature`.
3. Check `X-PayNode-Request-Id` for replays.

---

## Part III: Protocol Hardening & Conformance

### 10. Canonical Cryptographic Inputs

All SDKs MUST use these exact transformation rules:

1. **Order ID Hashing**: `keccak256(utf8(orderId))` -> `bytes32`. (Reference: `meta/fixtures/crypto/order_id_hash.json`).
2. **EIP-3009 Domain**: Standard USDC/ERC-20 domain fields (name, version, chainId, verifyingContract).
3. **Market Proxy Input**: `${requestId}:${timestamp}`.

### 11. Conformance Checklist

For an SDK to be compliant, it MUST:
1. Pass all `meta/fixtures/crypto/` golden vectors.
2. Correctly handle the canonical headers: `PAYMENT-REQUIRED`, `PAYMENT-SIGNATURE`, `PAYMENT-RESPONSE`, `X-402-Order-Id`.
3. Implement `Part I` for direct x402.
4. (Optional) Implement `Part II` for PayNode Market integration.

### 12. Implementation Metadata (Extensions)

PayNode-specific implementations MAY include a `_paynode` field in the JSON envelope for implementation-specific metadata (e.g., `sdkVersion`). This field is an extension and NOT part of the upstream core protocol.

Example:
```json
{
  "_paynode": {
    "sdkVersion": "2.3.0",
    "type": "eip3009",
    "orderId": "merchant-order-123"
  }
}
```

---

## Relationship To Other Documents

- [MULTI_LANGUAGE_BASELINE.md](./MULTI_LANGUAGE_BASELINE.md) lists the tasks remaining for full cross-language stabilization.
- [fixtures/README.md](./fixtures/README.md) describes the shared test assets.
