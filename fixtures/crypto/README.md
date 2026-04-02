# Crypto Fixtures

This directory contains deterministic cryptographic vectors.

## Layering

- `eip3009_transfer_with_authorization.json`: upstream x402-aligned baseline
- `eip2612_permit.json`: upstream x402-aligned baseline
- `order_id_hash.json`: upstream x402-aligned baseline
- `market_proxy_hmac.json`: PayNode extension

## Purpose

Use these files to verify:

- typed-data domain correctness
- typed-data message correctness
- exact signature reproduction
- signer recovery parity
- canonical order ID hashing
- PayNode Market Proxy signature parity

The private key values in this directory are test-only vectors.
