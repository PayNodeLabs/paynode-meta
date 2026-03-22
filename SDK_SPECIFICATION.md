# 🛠️ PayNode SDK 开发规范与实现标准 (v1.2)

## 1. 设计哲学
*   **Autonomous First (自治优先)**：SDK 必须能够让 AI Agent 在无需人工干预的情况下，自动完成“请求 -> 识别 402 -> 支付 -> 重试”的闭环。
*   **Stateless & Non-Custodial (无状态与非托管)**：SDK 不存储私钥以外的持久化状态，不充当托管中介，直接与 Base L2 交互。
*   **Consistency (一致性)**：不同语言的 SDK 在 API 定义、参数顺序、错误代码和行为逻辑上必须保持高度镜像。

---

## 2. 核心组件命名规范

| 功能描述 | JS/TS (CamelCase) | Python/Go (SnakeCase) | 说明 |
| :--- | :--- | :--- | :--- |
| **主客户端类** | `PayNodeAgentClient` | `PayNodeAgentClient` | 统一类名 |
| **自治请求方法** | `requestGate()` | `request_gate()` | 核心入口，处理 402 循环 |
| **签名 Permit 方法** | `signPermit()` | `sign_permit()` | EIP-2612 离线签名 |
| **执行 Permit 支付** | `payWithPermit()` | `pay_with_permit()` | 链上提交 Permit 交易 |
| **验证器类** | `PayNodeVerifier` | `PayNodeVerifier` | 用于服务端/Merchant 验证 |

---

## 3. 构造函数标准 (Initialization)

所有 SDK 的初始化必须接受两个核心参数：
1.  **Private Key**: 字符串形式，初始化后应立即转换为内部 Account 对象并尝试销毁原始字符串。
2.  **RPC URLs**: 支持字符串或列表。必须内置 **Failover (故障转移)** 逻辑，自动尝试可用节点。

---

## 4. x402 自治循环逻辑 (The Autonomous Loop)

`requestGate` 方法必须执行以下原子步骤：

1.  **Step 1: Handshake**: 发起原始请求，捕获 `402 Payment Required`。
2.  **Step 2: Parse Headers**: 提取 `contract`, `merchant`, `amount`, `token-address`, `order-id`。
3.  **Step 3: Pre-flight Check**: 检查 USDC 余额。
4.  **Step 4: Permit-First Execution (Optimization)**:
    *   **优先逻辑**：SDK 应检查代币是否支持 EIP-2612 (USDC 原生支持)。
    *   **原子化支付**：若 Allowance 不足，SDK 应默认构造 Permit 签名，并调用 `payWithPermit`。这允许在**单笔交易**中完成授权与支付，节省一笔 `approve` 的 Gas。
    *   **回退逻辑**：仅在代币不支持 Permit 时，才回退到 `approve` + `pay` 的双交易模式。
5.  **Step 5: Retry**: 携带 `x-paynode-receipt` (TxHash) 重新发起请求。

---

## 5. 安全约束 (Hardened Constraints)

*   **Minimum Amount**: 强制校验 $amount \ge 1000$ (0.001 USDC)，保护协议手续费计算精度。
*   **Token Whitelist**: 默认仅准入官方 **USDC** 地址。
*   **Gas Strategy**: 默认使用 `GasPrice * 1.2` 溢价策略，确保 M2M 交易在拥堵时仍能快速成交。

---

## 6. 异常处理与错误码 (Errors)

统一错误命名：`RPC_ERROR`, `INSUFFICIENT_FUNDS`, `AMOUNT_TOO_LOW`, `TOKEN_NOT_ACCEPTED`, `TRANSACTION_FAILED`, `DUPLICATE_TRANSACTION`。

---

## 7. 配置同步机制 (Config Sync)

*   **单一事实来源**: 所有 SDK 的合约地址、ABI、常量必须由根目录 `paynode-config.json` 通过 `sync-config.py` 自动注入，严禁手动修改。

---

## 8. 服务端验证标准 (Verifier)

`PayNodeVerifier` 必须通过以下 5 维度校验：
1.  **Transaction Status**: 链上状态必须为 `Success`。
2.  **To Address**: 交易接收方必须是合法的 `PayNodeRouter`。
3.  **Event Logs**: 必须解析 `PaymentReceived` 事件，验证 `orderId` 和 `merchant` 是否匹配。
4.  **ChainID**: 验证 ChainID 防止跨链重放。
5.  **Idempotency (Double-Spend Protection)**: 
    *   **防双花检查**：Verifier 必须记录已处理的 `TxHash`。
    *   **拒绝重复**：若同一 `TxHash` 被二次提交，必须返回 `DUPLICATE_TRANSACTION` 错误，严禁放行。

---
*PayNode Protocol - Standard RFC v1.2*
