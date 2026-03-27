# PROJECT KNOWLEDGE BASE

**Generated:** 2026-03-25 09:13 UTC
**Commit:** a7006fc
**Branch:** develop

## OVERVIEW

PayNode is a stateless, non-custodial M2M payment gateway implementing the x402 protocol on Base L2 (Ethereum). AI Agents autonomously detect HTTP 402 responses, execute USDC transactions via EIP-2612 Permits, and retry requests. This repository is the SSoT (Single Source of Truth) for shared protocol constants, specs, and assets, and is used together with sibling PayNode repositories in a local aggregate workspace.

**Core Stack:** TypeScript (Ethers.js), Python (Web3.py), Solidity (Foundry), Next.js 15, Tailwind CSS

## STRUCTURE

```text
paynode-workspace/
├── meta/
│   ├── paynode-config.json     # SSoT — contract addresses, chain IDs, error codes
│   ├── SDK_SPECIFICATION.md    # "Engineering Constitution" — protocol spec
│   ├── scripts/
│   │   └── sync-config.py      # Propagates config to sibling repositories
│   └── public/                 # Brand assets (logos, OG images)
├── packages/
│   ├── sdk-js/                 # TypeScript SDK (Ethers.js, strict TS, Jest)
│   ├── sdk-python/             # Python SDK (Web3.py, PEP 8, Pytest)
│   ├── contracts/              # Solidity — PayNodeRouter, MockUSDC (Foundry)
│   └── paynode-ai-skills/      # Atomic AI scripts for payment integration
└── apps/
    ├── paynode-web/            # Next.js 15 landing page + merchant dashboard
    └── paynode-docs/           # Nextra 3 documentation site
```

## WHERE TO LOOK

| Task | Location | Notes |
|------|----------|-------|
| Contract addresses, chain IDs | `meta/paynode-config.json` | Edit here, then run sync |
| SDK behavior spec | `meta/SDK_SPECIFICATION.md` | Defines naming, headers, error codes |
| JS SDK source | `packages/sdk-js/src/` | `client.ts` (agent), `middleware/` (merchant) |
| Python SDK source | `packages/sdk-python/paynode_sdk/` | `client.py` (agent), `middleware.py` (merchant) |
| Smart contracts | `packages/contracts/src/` | `PayNodeRouter.sol`, `MockUSDC.sol` |
| Web app pages | `apps/paynode-web/app/` | App Router, `page.tsx` landing |
| API endpoints | `apps/paynode-web/app/api/` | POM backend at `app/api/pom/` |
| Documentation | `apps/paynode-docs/pages/` | Nextra markdown pages |
| AI agent skills | `packages/paynode-ai-skills/` | Each skill has `SKILL.md` + `scripts/` |
| Config sync engine | `meta/scripts/sync-config.py` | Run after editing `meta/paynode-config.json` |

## CODE MAP

| Symbol | Type | Location | Role |
|--------|------|----------|------|
| `PayNodeAgentClient` | Class | `sdk-js/src/client.ts` | Agent-side 402 loop |
| `x402Gate` | Function | `sdk-js/src/middleware/` | Merchant route protection |
| `PayNodeVerifier` | Class | `sdk-js/src/` | Tx verification |
| `requestGate()` | Method | Both SDKs | Core autonomous payment entry |
| `signPermit()` | Method | Both SDKs | EIP-2612 offline signature |
| `payWithPermit()` | Method | Both SDKs | On-chain permit payment |
| `PayNodeRouter` | Contract | `contracts/src/PayNodeRouter.sol` | Stateless payment router |
| `PaymentReceived` | Event | `PayNodeRouter.sol` | On-chain payment proof |

## CONVENTIONS

- **Autonomous First:** SDKs must complete the full 402 loop without human intervention.
- **Stateless:** No persistent state other than private keys. No order tracking on-chain.
- **Cross-Language Parity:** JS and Python SDKs must have mirrored APIs, parameter ordering, and error codes. See `SDK_SPECIFICATION.md`.
- **Naming:** `PascalCase` for classes (both langs), `camelCase` for JS methods, `snake_case` for Python methods.
- **Wire Protocol:** Use `X-402-*` headers as per x402 v2/v2.2.0 protocol. Legacy `x-paynode-*` headers are deprecated.
- **USDC Decimals:** Always 6. Use `ethers.parseUnits(amount, 6)` in JS.
- **Gas Strategy:** Default `GasPrice * 1.2`.
- **Idempotency:** Verifiers MUST track `TxHash` to prevent replay attacks.
- **Config Sync:** After editing `meta/paynode-config.json`, run `python3 meta/scripts/sync-config.py`.

## ANTI-PATTERNS (THIS PROJECT)

- **Never hardcode private keys.** Load from `.env` files.
- **Never expose private keys in frontend code.** Agents run server-side or in TEEs.
- **Never skip the config sync.** Editing constants in sub-packages directly will cause drift.
- **Never suppress type errors** with `as any`, `@ts-ignore`, or `@ts-expect-error`.
- **Never use storage for order tracking.** The contract is stateless by design—use events.
- **Never skip `safeTransferFrom`.** Use OpenZeppelin's SafeERC20 for all token transfers.
- **Never use `GasPrice * 1.0`.** Always apply the 1.2x multiplier for mainnet reliability.

## UNIQUE STYLES

- **AGENTS.md in every package:** Each sub-project has AI-specific developer instructions (treated as system prompts for LLMs).
- **SKILL.md format:** AI skills use a standardized markdown format defining capabilities.
- **SSoT pattern:** `meta/paynode-config.json` is the single source for protocol constants; sibling repositories are auto-generated targets.
- **Relaxed frontend builds:** `paynode-web` ignores ESLint and TS errors during production builds (`ignoreDuringBuilds: true`).

## COMMANDS

```bash
# Config sync (run after editing meta/paynode-config.json)
python3 meta/scripts/sync-config.py

# JS SDK
cd packages/sdk-js && npm install && npm run build && npm test

# Python SDK
cd packages/sdk-python && PYTHONPATH=. pytest tests/

# Smart contracts
cd packages/contracts && forge build && forge test -vvv

# Web app
cd apps/paynode-web && npm install && npm run dev

# Docs
cd apps/paynode-docs && npm install && npm run dev
```

## NOTES

- **Protocol minimum:** Payment amount must be >= 1000 (smallest unit) to prevent fee truncation.
- **Chain IDs:** Base Mainnet = 8453, Base Sepolia = 84532 (default for testing).
- **Contract addresses:** Mainnet `0x4A73696ccF76E7381b044cB95127B3784369Ed63`, Sepolia `0x24cD8b68aaC209217ff5a6ef1Bf55a59f2c8Ca6F`.
- **Fee structure:** 1% protocol fee (100 BPS). Merchant receives 99%.
- **Dependency cascade:** SDK changes affect examples, docs site, web demos, live-testing scripts, and AI skills. Verify all after modifications.
