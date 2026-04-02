# Verification Fixtures

This directory contains scenario-level verification fixtures.

## Layering

- `direct_x402_cases.json`: upstream x402-aligned baseline
- `market_proxy_cases.json`: PayNode extension

## Purpose

Use these files to drive conformance tests that check pass/fail behavior across SDKs and merchant integrations.

The intent is:

- direct x402 cases prove the shared protocol floor
- Market Proxy cases prove PayNode-specific extension behavior

If more scenarios are added later, keep them grouped by layer rather than mixing upstream and PayNode-specific behavior in the same file.
