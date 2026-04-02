# PayNode Multi-Language SDK Baseline

This document defines the stabilization work required before `sdk-js` can serve as the formal baseline for Python, Java, Go, and other language SDKs.

`@paynodelabs/sdk-js` is currently the first complete implementation. It is usable as a reference implementation, but it is not yet a fully normalized protocol baseline. The goal of this document is to separate:

- protocol rules that every SDK must implement
- JS-specific implementation details that must not leak into the protocol
- cleanup work that must be completed before downstream SDK ports begin

## Current Position

Today `sdk-js` is strong enough to prove the main payment flows:

- HTTP `402` challenge and retry
- EIP-3009 authorization-based payment flow
- on-chain receipt-based payment flow
- PayNode Market Proxy verification flow

What is still missing is a clean contract for other languages. A Python or Java team can follow the code today, but they still need to infer protocol intent from JS behavior. That is the gap this document is meant to close.

## Baseline Principles

These rules should be treated as non-negotiable for all future SDKs.

1. Protocol versioning must be independent from SDK package versioning.
2. All wire-level fields must be defined in one place and used consistently by code, docs, tests, and examples.
3. Every language SDK must pass against the same protocol fixtures and golden vectors.
4. Merchant-side APIs must have clear boundaries between direct x402 verification and Market Proxy verification.
5. Compatibility behavior is allowed, but compatibility shims must be documented as legacy behavior rather than presented as the main protocol.

## Protocol Surface That Must Be Frozen

The following items need to be finalized and then treated as the stable wire contract:

- `402` response JSON body shape
- `PAYMENT-REQUIRED` and `PAYMENT-SIGNATURE` header encoding rules
- `PAYMENT-RESPONSE` settlement header shape
- `X-402-Order-Id` lifecycle and body/header precedence
- allowed values for `scheme`, `network`, `type`, and `x402Version`
- canonical order ID hashing rule for on-chain settlement
- EIP-3009 typed-data domain fields
- Market Proxy signature inputs, header names, timestamp format, and replay window
- error code mapping returned by merchant verification

If any of these remain ambiguous, downstream SDKs will drift.

## Required Cleanup Before Porting

### 1. Separate protocol version from SDK version

Current code still uses a JS-specific string in unified payloads, for example `version: "2.3.0"`.

That field cannot remain tied to the JS package version if Python, Java, and Go SDKs are expected to interoperate cleanly.

Required change:

- define a protocol version field and its allowed values explicitly
- define an SDK implementation version field separately if metadata is needed
- stop using JS release numbers as a wire-level compatibility gate

Recommended direction:

- keep `x402Version: 2` as the protocol discriminator
- if internal metadata is needed, move SDK version into a namespaced metadata field such as `_paynode.sdkVersion`
- if a PayNode payload format version is needed, define it as a protocol artifact, not a package artifact

### 2. Normalize the 402 challenge format

The current code and `SPEC.md` are not yet aligned on the challenge schema.

Open issues that must be resolved:

- `scheme` meaning is unclear and currently inconsistent between docs and implementation
- `network` value format is inconsistent between docs and implementation
- `orderId` is described in the spec body, but current middleware primarily returns it in the response header

Required change:

- publish one canonical challenge example
- make code emit exactly that format
- treat all older variants as legacy compatibility paths only

### 3. Split direct x402 and Market Proxy contracts

There are two distinct flows in this SDK:

- direct x402 payment verification via `x402Gate`
- PayNode Market Proxy verification via `PayNodeMerchant`

These should be specified separately. They have different trust assumptions, headers, replay semantics, and deployment models.

Required change:

- define separate spec sections for direct x402 and Market Proxy
- ensure README and public APIs do not imply they are interchangeable
- remove or implement options that currently have no effect

### 4. Freeze canonical cryptographic inputs

Any cross-language SDK effort will fail if the signing inputs are not written down precisely.

Required change:

- publish the exact EIP-3009 typed-data domain and message fields
- publish the exact EIP-2612 permit typed-data domain and message fields
- publish the exact order ID to `bytes32` transformation rule
- publish the exact Market Proxy HMAC input string

This must be expressed with concrete fixtures, not prose only.

### 5. Define compatibility policy explicitly

The current JS implementation accepts some legacy formats. That is useful operationally, but the compatibility matrix is not yet written down.

Required change:

- define which headers are canonical
- define which headers are accepted only for backward compatibility
- define deprecation windows for legacy payload formats

Without this, each new SDK may preserve or drop compatibility behavior arbitrarily.

## Test Baseline Required For All SDKs

Before downstream ports start, add shared fixtures that every SDK must pass.

### A. Wire-format fixtures

Create JSON fixtures for:

- canonical `402 Payment Required` response
- canonical `PAYMENT-SIGNATURE` payload for EIP-3009
- canonical `PAYMENT-SIGNATURE` payload for on-chain receipt flow
- canonical `PAYMENT-RESPONSE` success header
- canonical `PAYMENT-RESPONSE` failure header

### B. Crypto fixtures

Create deterministic vectors for:

- EIP-3009 `TransferWithAuthorization` typed-data payload
- EIP-2612 permit typed-data payload
- recovered signer address
- expected order ID hash
- expected HMAC signature for Market Proxy

### C. Verification fixtures

Create pass/fail cases for:

- wrong token
- amount below minimum
- wrong merchant
- wrong router contract
- wrong order ID
- expired authorization
- future authorization
- duplicate nonce
- duplicate transaction hash
- invalid timestamp drift

### D. Compatibility fixtures

Define a separate legacy fixture set for:

- old payload wrappers still accepted by JS
- old header aliases still accepted by JS

Legacy fixtures should not define the main protocol. They should only protect migrations.

## API Design Rules For Future SDKs

To keep the ecosystem coherent, all language SDKs should expose equivalent conceptual APIs even if naming differs slightly per language style.

Required top-level capabilities:

- Agent client that can execute the `402` handshake and retry automatically
- Merchant verifier for direct x402 settlement
- Market Proxy verifier for PayNode Market requests
- Idempotency store interface with pluggable backend
- Payload normalization helper for compatibility handling

Recommended API split:

- `AgentClient`
- `X402Verifier` or `X402Middleware`
- `MarketVerifier` or `MarketMiddleware`
- `IdempotencyStore`
- `PayloadHelper`

Avoid combining direct x402 and Market Proxy logic into one ambiguous surface unless the distinction is still obvious in configuration and behavior.

## Security Hardening Required Before Declaring Baseline Stable

The first non-JS ports should not begin until the following items are addressed or explicitly accepted:

- replace raw string equality for Market Proxy signature checks with constant-time comparison
- formally specify timestamp format and acceptable drift
- document replay protection requirements for merchant deployments
- document production expectation for persistent idempotency storage
- document trust assumptions around token whitelist and router contract configuration

## Suggested Execution Order

1. Freeze the wire protocol in `SPEC.md`.
2. Update `sdk-js` code to emit and consume the frozen format.
3. Add shared golden vectors and compatibility fixtures.
4. Update README and integration docs to point at the frozen spec and fixtures.
5. Cut a release that declares `sdk-js` as the formal baseline.
6. Start Python SDK against those fixtures.
7. Start Java and Go SDKs only after Python validates that the baseline is complete enough.

## Definition Of Ready For Other SDKs

## Status Report (2026-04-02)

The `sdk-js@2.4.0` package has been verified as the formal protocol baseline. All identified issues, including broken imports, lack of middleware tests, and protocol versioning ambiguity, have been resolved.

| Condition | Status | Verification |
|-----------|--------|--------------|
| Build & tests pass | ✅ Passed | `npm test` passed including new `x402Gate` tests |
| `SPEC.md` matches implementation | ✅ Aligned | `PROTOCOL_VERSION = 2` exported from sync script |
| README examples match implementation | ✅ Aligned | References `v2.4.0` architecture |
| Protocol vs SDK version separated | ✅ Done | `x402Version` (root) vs `_paynode.sdkVersion` (metadata) |
| Canonical fixtures exist | ✅ Complete | Golden vectors in `meta/fixtures/` validated |
| Direct vs Market Proxy split | ✅ Defined | `SPEC.md` Part I and Part II separation |
| Compatibility documented | ✅ Complete | Detailed in `meta/COMPATIBILITY.md` |

## Definition Of Ready For Other SDKs

`@paynodelabs/sdk-js` v2.4.0 is now the **Formal Multi-Language Baseline**. 

Downstream SDKs (Python, Go, Java) SHOULD begin development using the logic in this repository and use `meta/scripts/sync-config.py` to keep protocol constants in sync with `meta/paynode-config.json`.

