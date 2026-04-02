# Wire Fixtures

This directory contains canonical wire-format fixtures.

These files belong to the upstream x402-aligned baseline unless explicitly documented otherwise.

## Included Assets (Baseline Room: `base/`)

- `base/payment_required.json`
- `base/payment_required.base64.txt`
- `base/payment_signature_eip3009.json`
- `base/payment_signature_eip3009.base64.txt`
- `base/payment_signature_onchain.json`
- `base/payment_signature_onchain.base64.txt`
- `base/payment_response_success.json`
- `base/payment_response_success.base64.txt`
- `base/payment_response_failure.json`
- `base/payment_response_failure.base64.txt`

## Purpose

Use these files to verify:

- exact JSON payload shape
- exact Base64 header representation
- cross-language header interoperability

These are part of the foundation layer and should remain stable.
