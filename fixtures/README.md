# PayNode Protocol Fixtures

This directory contains shared fixtures for validating PayNode SDK behavior across languages.

These fixtures are intended to be consumed by JS, Python, Java, Go, and future SDK test suites.

The fixture tree follows the same layering model as `meta/SPEC.md`:

- upstream x402-aligned baseline
- PayNode extensions
- compatibility-only fixtures

## Layout

- `wire/`: Canonical wire-format payloads and their Base64 header forms
- `crypto/`: Deterministic cryptographic test vectors
- `verification/`: Expected pass/fail verification scenarios grouped by protocol layer
- `compatibility/`: Legacy compatibility fixtures kept outside the canonical protocol path

## Layering

### Upstream x402-aligned baseline

These files define the minimum shared protocol floor that every SDK should implement:

- `wire/base/payment_required.json`
- `wire/base/payment_signature_eip3009.json`
- `wire/base/payment_signature_onchain.json`
- `wire/base/payment_response_success.json`
- `wire/base/payment_response_failure.json`
- `crypto/eip3009_transfer_with_authorization.json`
- `crypto/eip2612_permit.json`
- `crypto/order_id_hash.json`
- `verification/direct_x402_cases.json`

These fixtures should be treated as foundational protocol assets.

### PayNode extensions

These files cover PayNode-specific behavior layered on top of the upstream-aligned baseline:

- `wire/extensions/paynode/payment_signature_eip3009.json`
- `wire/extensions/paynode/payment_signature_onchain.json`
- `crypto/market_proxy_hmac.json`
- `verification/market_proxy_cases.json`

These fixtures are first-class for PayNode SDKs, but they are not part of the upstream-aligned direct x402 floor.

### Compatibility-only assets

Everything in `compatibility/` is migration coverage only.

Compatibility fixtures must never redefine the canonical protocol.

## Usage Rules

1. Treat the upstream-aligned fixtures as the minimum conformance baseline for every SDK.
2. Treat PayNode extension fixtures as required only for SDKs that support PayNode-specific flows.
3. Treat `compatibility/` as migration coverage only.
4. Do not change fixture shapes casually. If protocol behavior changes, update `meta/SPEC.md` first.
5. If a fixture changes, update all SDK conformance tests together.

## Notes

- The cryptographic vectors use deterministic sample values and a fixed test private key.
- These fixtures are safe for testing only. They are not tied to production keys.
- The Base64 values are precomputed so non-JS SDKs can verify exact header interoperability.
