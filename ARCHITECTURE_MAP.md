# PayNode Multi-Repo — Feature Chain & Public Information Tree

---

## 1. Feature Chain

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        PayNode Ecosystem — Core Feature Chain                   │
│                              v1.4.0 / SDK v2.2.0                                │
└─────────────────────────────────────────────────────────────────────────────────┘

          ┌───────────────────────────────────────────────────────┐
          │              ⚙️ Config Hub (SSoT)                     │
          │  ┌──────────────────────────────────────────────────┐ │
          │  │  paynode-config.json                             │ │
          │  │  · Chain IDs, RPC URLs, Router Addresses        │ │
          │  │  · Token Addresses (USDC)                        │ │
          │  │  · Error Codes, Protocol Fee (100 BPS = 1%)     │ │
          │  └──────────────┬───────────────────────────────────┘ │
          │                 │                                     │
          │  ┌──────────────▼───────────────────────────────────┐ │
          │  │  scripts/sync-config.py  🔁 Sync Engine          │ │
          │  │  Auto-distribute config → All sub-packages       │ │
          │  └──────────────────────────────────────────────────┘ │
          └───────────────────────┬───────────────────────────────┘
                                  │
          ┌───────────────┬───────┼───────┬───────────────┐
          ▼               ▼       ▼       ▼               ▼
   ┌─────────────┐ ┌──────────┐ ┌──┐ ┌────────────┐ ┌──────────┐
   │  contracts  │ │  sdk-js  │ │  │ │ sdk-python │ │ paynode- │
   │   (Solidity)│ │  (TS)    │ │  │ │   (Py)     │ │  web     │
   └──────┬──────┘ └────┬─────┘ └──┘ └─────┬──────┘ └────┬─────┘
          │             │                   │              │
          │             │    SDK Layer (Developer API)      │
          │             │                   │              │
          │    ┌────────┴───────────────────┴────────┐     │
          │    │                                      │     │
          │    │  PayNodeAgentClient   (Payer)        │     │
          │    │  ├── requestGate()    Core Entry     │     │
          │    │  ├── signPermit()     EIP-2612       │     │
          │    │  ├── signTransferWithAuthorization()  │     │
          │    │  │                    EIP-3009        │     │
          │    │  └── payWithPermit()  On-chain submission  │     │
          │    │                                      │     │
          │    │  PayNodeVerifier     (Recipient)     │     │
          │    │  └── verify()        Payment Validation  │     │
          │    │                                      │     │
          │    │  PayNodeException    (Unified Error) │     │
          │    │  12 Standard Error Codes             │     │
          │    └──────────────────┬───────────────────┘     │
          │                      │                          │
          │                      │  Low-level Dependencies  │
          │                      │                          │
   ┌──────▼──────────────────────▼──────────────────────────▼──────┐
   │                                                                │
   │               🔗 x402 Protocol — Core Interaction Flow        │
   │                                                                │
   │   Agent (Buy)         HTTP 402          Merchant (Sell)        │
   │   ┌──────┐    ─────►  402 Required    ┌──────────┐            │
   │   │      │    ◄─────  PAYMENT-REQ     │ Express/ │            │
   │   │      │    ─────►  PAYMENT-SIG     │ FastAPI  │            │
   │   │      │    ◄─────  200 + DATA      │          │            │
   │   └──────┘           PAYMENT-RESP     └──────────┘            │
   │                                                                │
   └────────────────────────────────────────────────────────────────┘

          │             │                   │              │
          │    App Layer│                   │              │
          │             │                   │              │
   ┌──────▼──────┐ ┌────▼───────────────────▼─────┐ ┌─────▼─────┐
   │  contracts/ │ │        apps/                  │ │   ai-     │
   │  (On-chain) │ │  ┌──────────┬──────────┐     │ │  skills/  │
   │             │ │  │paynode-  │paynode-  │     │ │           │
   │ · Router    │ │  │  web     │  docs    │     │ │ · payment │
   │ · pay()     │ │  │(Next.js) │(Nextra3) │     │ │   -402    │
   │ · permit    │ │  │          │          │     │ │           │
   │ · events    │ │  │Dashboard │ API Ref  │     │ │ Autonomous │
   │             │ │  │Simulator │ Concepts │     │ │ Skill Set │
   │  Base L2    │ │  │Monitor   │ Guides   │     │ │           │
   └─────────────┘ │  └──────────┴──────────┘     │ └───────────┘
                   └──────────────────────────────-┘
```

---

## 2. Dependency Matrix

```
                   contracts  sdk-js  sdk-python  ai-skills  web  docs  sync-config
                   ─────────  ──────  ──────────  ─────────  ───  ────  ──────────
contracts               ─       ←         ←          ↓       ←     ←       ←
sdk-js                  →       ─          ╳          ↑       →     →        ↓
sdk-python              →       ╳          ─          ↑       →     →        ↓
ai-skills               →       →          →          ─       ╳     ╳        ↓
paynode-web             →       →          →          ╳       ─     →        ↓
paynode-docs            →       →          →          ╳       →     ─        ↓
sync-config             →       →          →          →       →     →        ─

  → = "Depends on / Calls"    ← = "Depended on by"    ↑↓ = "Indirect Dependency"    ╳ = No Direct Relation
```

---

## 3. Public Information Tree (SSoT)

```
paynode/                                    # 🏠 Meta Repo (SSoT)
│
├── paynode-config.json                     # ⚙️ Global Config Hub
│   ├── protocol.version          = "1.4.0"
│   ├── protocol.treasury         = "0x598bF6..."
│   ├── protocol.fee_bps          = 100 (1%)
│   ├── protocol.min_payment      = 1000
│   ├── error_codes (12 Types)               # Cross-Language Unified Codes
│   │   ├── rpc_error             → All SDKs
│   │   ├── insufficient_funds    → All SDKs
│   │   ├── amount_too_low        → All SDKs
│   │   ├── token_not_accepted    → All SDKs
│   │   ├── transaction_failed    → All SDKs
│   │   ├── duplicate_transaction → Verifier
│   │   ├── invalid_receipt       → Verifier
│   │   ├── wrong_contract        → Verifier
│   │   ├── order_mismatch        → Verifier
│   │   ├── missing_receipt       → Handshake
│   │   ├── transaction_not_found → Verifier
│   │   └── internal_error        → All SDKs
│   └── networks
│       ├── base (8453)
│       │   ├── router = "0x4A736..."
│       │   ├── USDC   = "0x83358..."
│       │   └── rpcUrls (3)
│       └── baseSepolia (84532)
│           ├── router = "0x24cD8..."
│           ├── USDC   = "0x65c08..."
│           └── rpcUrls (2)
│
├── SDK_SPECIFICATION.md                    # 📜 SDK Constitution (v2.2.0)
│   ├── Core Class Naming (Consistent)
│   │   ├── PayNodeAgentClient    (JS/Py match)
│   │   ├── PayNodeVerifier       (JS/Py match)
│   │   └── PayNodeException      (JS/Py match)
│   ├── Wire Protocol (x402 V2 Headers)
│   │   ├── PAYMENT-REQUIRED      (Base64 JSON)
│   │   ├── PAYMENT-SIGNATURE     (Base64 JSON)
│   │   └── PAYMENT-RESPONSE      (Base64 JSON)
│   ├── Auto-Loop Logic (requestGate)
│   │   ├── 1. Handshake (Intercept 402)
│   │   ├── 2. Pre-flight (Amount/Token/Chain Check)
│   │   ├── 3. Signature-First (EIP-3009 → EIP-2612 → ERC20)
│   │   ├── 4. Retry (Attach Signature)
│   │   └── 5. Confirmation (Logging)
│   └── Hard Constraints
│       ├── Gas: Price * 1.2
│       ├── Idempotency: IdempotencyStore
│       └── Nonce: Local Locks / Queues
│
├── scripts/
│   └── sync-config.py                      # 🔁 Config Propagation Engine
│       ├── Input: paynode-config.json (SSoT)
│       └── Output:
│           ├── packages/sdk-js/src/constants.ts
│           ├── packages/sdk-js/src/errors/index.ts
│           ├── packages/sdk-python/paynode_sdk/constants.py
│           ├── packages/sdk-python/paynode_sdk/errors.py
│           ├── packages/contracts/script/Config.s.sol
│           └── apps/paynode-web/app/api/pom/config.ts
│
├── public/                                 # 🎨 Brand Assets
│   ├── logo.png                            # "$_" Shield Icon
│   ├── logo-full.png                       # Full Landscape Logo
│   └── og-image.png                        # Social Share Meta-Image
│
└── Distributed Repositories                # 📦 Maintained via GitHub Org
    ├── paynode-contracts                   # Smart Contracts
    ├── paynode-sdk-js                      # JS/TS SDK
    ├── paynode-sdk-python                  # Python SDK
    ├── paynode-ai-skills                   # AI Agent Tooling
    ├── paynode-web                         # Explorer & Portal
    └── paynode-docs                        # Documentation Site
```

---

## 4. Data / Config Flow Panorama

```
┌─────────────────────────────────────────────────────────────────┐
│                     Config Data Flow (Propagator)               │
│                                                                 │
│   paynode-config.json (SSoT)                                    │
│         │                                                       │
│         │  python3 scripts/sync-config.py                       │
│         │                                                       │
│    ┌────┼────────────┬──────────────┬──────────────┐            │
│    ▼    ▼            ▼              ▼              ▼            │
│  ┌────┐┌──────────┐┌────────────┐┌────────────┐┌──────────┐    │
│  │Solid││ sdk-js/  ││ sdk-python/││ paynode-   ││ web/     │    │
│  │ity  ││constants ││ constants  ││ web/api/   ││ api/pom/ │    │
│  │     ││+errors   ││ +errors    ││ config.ts  ││ config   │    │
│  └────┘└──────────┘└────────────┘└────────────┘└──────────┘    │
│                                                                 │
│  ⚠️ Must run sync-config.py after modifying paynode-config.json │
└─────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                     Payment Flow (Interaction)                  │
│                                                                 │
│  AI Agent                  Base L2               Merchant       │
│  ┌──────┐                 ┌──────────┐          ┌─────────┐     │
│  │request│──402 req──►   │          │          │Express/ │     │
│  │ Gate  │◄──402 resp──  │ Router   │◄─pay()── │FastAPI  │     │
│  │       │──Sig/Proof──►  │ Contract │──event──►│Verifier │     │
│  │       │◄──200+data──  │          │          │verify() │     │
│  └──────┘                 └──────────┘          └─────────┘     │
│                                                                 │
│  Signature Priority:                                            │
│  ① EIP-3009 (TransferWithAuthorization) — Recommended           │
│  ② EIP-2612 (Permit + payWithPermit)                            │
│  ③ Standard ERC20 (approve + pay)                               │
└─────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                     Dependency Graph Overview                    │
│                                                                 │
│   paynode-docs ──► sdk-js (Doc Reference)                       │
│       │                                                         │
│   paynode-web  ──► sdk-js (Internal Link)                       │
│       │            └──► contracts (ABI Dependency)              │
│       │                                                         │
│   sdk-js       ──────► ethers.js (Blockchain Interaction)       │
│   sdk-python   ──► web3.py   (Blockchain Interaction)           │
│   ai-skills    ──► sdk-js (TypeScript Call Chain)               │
│   contracts    ──► Foundry  (Compile/Test/Deploy)               │
└─────────────────────────────────────────────────────────────────┘
```
