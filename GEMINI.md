# 🤖 PayNode AI 协作指令 (Meta Hub Edition)

## 🏛️ 项目架构与治理中心 (SSoT)

本项目采用 **Meta Repository** 治理模式。`/root/agentpay-dev/paynode` 是整个生态的 **Single Source of Truth (SSoT)**。

### 1. 配置变更红线 (The Golden Rule)
- **严禁**直接在子项目（`apps/`, `packages/`）中手动修改合约地址、ABI 或协议常量。
- **唯一路径**：
    1. 修改根目录的 `paynode-config.json`。
    2. 执行同步脚本：`python3 scripts/sync-config.py`。
    3. 检查变更并推送到受影响的子仓库。

### 2. 多端一致性守则
- 所有 SDK 开发必须严格遵循 `SDK_SPECIFICATION.md` (v1.2)。
- **核心逻辑**：必须实现 `requestGate` 自治循环，优先使用 `payWithPermit` 优化 Gas，并内置多节点 Failover 机制。
- **错误码**：保持跨语言镜像（JS 的 `CamelCase` vs Python 的 `snake_case`）。

### 3. 环境与执行建议
- **Python**: 始终使用 Conda 环境。
- **JS/TS**: 在 `demo/` 目录下运行时，注意 `package.json` 的 `type: "module"` 配置及 `ts-node/esm` 的兼容性。
- **Meta Repo Tracking**: `.gitignore` 仅追踪根目录的配置、脚本、规范和品牌资产，严禁将子项目业务逻辑误提交到 `paynode-meta`。

---

## 🎨 品牌资产维护 (Brand Kit)
- 所有的官方 Logo 和 OG-Image 存储在 `public/` 目录下。
- 当媒体或合作伙伴需要资产时，直接提供 `paynode-meta/public/` 的链接。

---
*Built for the Autonomous AI Economy. Maintain the Standard.*
