import argparse
import json
import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
META_ROOT = SCRIPT_DIR.parent
WORKSPACE_ROOT = META_ROOT.parent
CONFIG_PATH = META_ROOT / "paynode-config.json"


def workspace_path(*parts):
    return WORKSPACE_ROOT.joinpath(*parts)

def to_camel_case(snake_str):
    components = snake_str.split('_')
    return "".join(x.title() for x in components)

def sync_file(path, new_content, check_mode=False):
    """Writes to file or checks consistency depending on check_mode."""
    path = Path(path)
    if not path.parent.exists():
        return True  # Skip if directory doesn't exist

    if not path.exists():
        if check_mode:
            print(f"❌ Check Failed: {path} does not exist.")
            return False
        # If not check mode, we'll create it later
        pass

    if path.exists():
        with path.open("r") as f:
            current_content = f.read()
        if current_content == new_content:
            if not check_mode:
                print(f"  (Up-to-date): {path}")
            return True
        else:
            if check_mode:
                print(f"❌ Check Failed: {path} is out of sync with {CONFIG_PATH}")
                return False
    
    if not check_mode:
        with path.open("w") as f:
            f.write(new_content)
        print(f"✅ Synced: {path}")
    
    return True

def sync_config(check_mode=False):
    if not CONFIG_PATH.exists():
        print(f"Error: {CONFIG_PATH} not found.")
        sys.exit(1)

    with CONFIG_PATH.open("r") as f:
        config = json.load(f)

    all_synced = True
    min_amount = config["protocol"]["min_payment_amount"]
    protocol_version = config["protocol"].get("x402_version", 2)
    base_usdc = config["networks"]["base"]["tokens"]["USDC"]
    sepolia_usdc = config["networks"]["baseSepolia"]["tokens"]["USDC"]
    
    base_rpcs = config["networks"]["base"]["rpcUrls"]
    sepolia_rpcs = config["networks"]["baseSepolia"]["rpcUrls"]
    
    error_codes = config.get("error_codes", {})

    # JS SDK metadata (to keep version in sync)
    js_package_path = workspace_path("packages", "sdk-js", "package.json")
    sdk_version = "0.0.0"
    if js_package_path.exists():
        with js_package_path.open("r") as f:
            js_pkg = json.load(f)
            sdk_version = js_pkg.get("version", "0.0.0")

    # Shared Full JSON ABI
    FULL_ABI = [
        {"type": "constructor", "inputs": [{"name": "_protocolTreasury", "type": "address", "internalType": "address"}], "stateMutability": "nonpayable"},
        {"type": "function", "name": "MAX_BPS", "inputs": [], "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}], "stateMutability": "view"},
        {"type": "function", "name": "MIN_PAYMENT_AMOUNT", "inputs": [], "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}], "stateMutability": "view"},
        {"type": "function", "name": "PROTOCOL_FEE_BPS", "inputs": [], "outputs": [{"name": "", "type": "uint256", "internalType": "uint256"}], "stateMutability": "view"},
        {"type": "function", "name": "acceptOwnership", "inputs": [], "outputs": [], "stateMutability": "nonpayable"},
        {"type": "function", "name": "owner", "inputs": [], "outputs": [{"name": "", "type": "address", "internalType": "address"}], "stateMutability": "view"},
        {"type": "function", "name": "pause", "inputs": [], "outputs": [], "stateMutability": "nonpayable"},
        {"type": "function", "name": "paused", "inputs": [], "outputs": [{"name": "", "type": "bool", "internalType": "bool"}], "stateMutability": "view"},
        {"type": "function", "name": "pay", "inputs": [{"name": "token", "type": "address", "internalType": "address"}, {"name": "merchant", "type": "address", "internalType": "address"}, {"name": "amount", "type": "uint256", "internalType": "uint256"}, {"name": "orderId", "type": "bytes32", "internalType": "bytes32"}], "outputs": [], "stateMutability": "nonpayable"},
        {"type": "function", "name": "payWithPermit", "inputs": [{"name": "payer", "type": "address", "internalType": "address"}, {"name": "token", "type": "address", "internalType": "address"}, {"name": "merchant", "type": "address", "internalType": "address"}, {"name": "amount", "type": "uint256", "internalType": "uint256"}, {"name": "orderId", "type": "bytes32", "internalType": "bytes32"}, {"name": "deadline", "type": "uint256", "internalType": "uint256"}, {"name": "v", "type": "uint8", "internalType": "uint8"}, {"name": "r", "type": "bytes32", "internalType": "bytes32"}, {"name": "s", "type": "bytes32", "internalType": "bytes32"}], "outputs": [], "stateMutability": "nonpayable"},
        {"type": "function", "name": "pendingOwner", "inputs": [], "outputs": [{"name": "", "type": "address", "internalType": "address"}], "stateMutability": "view"},
        {"type": "function", "name": "protocolTreasury", "inputs": [], "outputs": [{"name": "", "type": "address", "internalType": "address"}], "stateMutability": "view"},
        {"type": "function", "name": "renounceOwnership", "inputs": [], "outputs": [], "stateMutability": "nonpayable"},
        {"type": "function", "name": "transferOwnership", "inputs": [{"name": "newOwner", "type": "address", "internalType": "address"}], "outputs": [], "stateMutability": "nonpayable"},
        {"type": "function", "name": "unpause", "inputs": [], "outputs": [], "stateMutability": "nonpayable"},
        {"type": "function", "name": "updateTreasury", "inputs": [{"name": "_newTreasury", "type": "address", "internalType": "address"}], "outputs": [], "stateMutability": "nonpayable"},
        {"type": "event", "name": "OwnershipTransferStarted", "inputs": [{"name": "previousOwner", "type": "address", "indexed": True, "internalType": "address"}, {"name": "newOwner", "type": "address", "indexed": True, "internalType": "address"}], "anonymous": False},
        {"type": "event", "name": "OwnershipTransferred", "inputs": [{"name": "previousOwner", "type": "address", "indexed": True, "internalType": "address"}, {"name": "newOwner", "type": "address", "indexed": True, "internalType": "address"}], "anonymous": False},
        {"type": "event", "name": "Paused", "inputs": [{"name": "account", "type": "address", "indexed": False, "internalType": "address"}], "anonymous": False},
        {"type": "event", "name": "PaymentReceived", "inputs": [{"name": "orderId", "type": "bytes32", "indexed": True, "internalType": "bytes32"}, {"name": "merchant", "type": "address", "indexed": True, "internalType": "address"}, {"name": "payer", "type": "address", "indexed": True, "internalType": "address"}, {"name": "token", "type": "address", "indexed": False, "internalType": "address"}, {"name": "amount", "type": "uint256", "indexed": False, "internalType": "uint256"}, {"name": "fee", "type": "uint256", "indexed": False, "internalType": "uint256"}, {"name": "chainId", "type": "uint256", "indexed": False, "internalType": "uint256"}], "anonymous": False},
        {"type": "event", "name": "TreasuryUpdated", "inputs": [{"name": "oldTreasury", "type": "address", "indexed": True, "internalType": "address"}, {"name": "newTreasury", "type": "address", "indexed": True, "internalType": "address"}], "anonymous": False},
        {"type": "event", "name": "Unpaused", "inputs": [{"name": "account", "type": "address", "indexed": False, "internalType": "address"}], "anonymous": False},
        {"type": "error", "name": "AmountTooLow", "inputs": []},
        {"type": "error", "name": "EnforcedPause", "inputs": []},
        {"type": "error", "name": "ExpectedPause", "inputs": []},
        {"type": "error", "name": "InvalidAddress", "inputs": []},
        {"type": "error", "name": "OwnableInvalidOwner", "inputs": [{"name": "owner", "type": "address", "internalType": "address"}]},
        {"type": "error", "name": "OwnableUnauthorizedAccount", "inputs": [{"name": "account", "type": "address", "internalType": "address"}]},
        {"type": "error", "name": "SafeERC20FailedOperation", "inputs": [{"name": "token", "type": "address", "internalType": "address"}]},
        {"type": "error", "name": "UnauthorizedCaller", "inputs": []}
    ]

    # --- 1. Python SDK ---
    python_constants_path = workspace_path("packages", "sdk-python", "paynode_sdk", "constants.py")
    python_content = f'''# Generated by meta/scripts/sync-config.py
PAYNODE_ROUTER_ADDRESS = "{config["networks"]["base"]["router"]}"
PAYNODE_ROUTER_ADDRESS_SANDBOX = "{config["networks"]["baseSepolia"]["router"]}"
BASE_USDC_ADDRESS = "{base_usdc}"
BASE_USDC_ADDRESS_SANDBOX = "{sepolia_usdc}"
BASE_USDC_DECIMALS = 6

PROTOCOL_VERSION = {protocol_version}
PROTOCOL_TREASURY = "{config["protocol"]["treasury"]}"
PROTOCOL_FEE_BPS = {config["protocol"]["fee_bps"]}
MIN_PAYMENT_AMOUNT = {min_amount}

BASE_RPC_URLS = {repr(base_rpcs)}
BASE_RPC_URLS_SANDBOX = {repr(sepolia_rpcs)}

ACCEPTED_TOKENS = {{
    8453: ["{base_usdc}"],
    84532: ["{sepolia_usdc}"]
}}

PAYNODE_ROUTER_ABI = {repr(FULL_ABI)}
'''
    if not sync_file(python_constants_path, python_content, check_mode): all_synced = False

    python_errors_path = workspace_path("packages", "sdk-python", "paynode_sdk", "errors.py")
    error_lines = [
        "# Generated by meta/scripts/sync-config.py",
        "from enum import Enum",
        "from typing import Any, Optional",
        "",
        "class ErrorCode(str, Enum):"
    ]
    for code in error_codes:
        error_lines.append(f"    {code} = '{code}'")
    error_lines.append("")
    error_lines.append("ERROR_MESSAGES = {")
    for code, msg in error_codes.items():
        error_lines.append(f"    ErrorCode.{code}: \"{msg}\",")
    error_lines.append("}")
    error_lines.extend([
        "",
        "class PayNodeException(Exception):",
        "    def __init__(self, code: ErrorCode, message: Optional[str] = None, details: Optional[Any] = None):",
        "        self.code = code",
        "        self.message = message or ERROR_MESSAGES.get(code, \"An unexpected error occurred.\")",
        "        self.details = details",
        "        super().__init__(self.message)"
    ])
    if not sync_file(python_errors_path, "\n".join(error_lines) + "\n", check_mode): all_synced = False

    # --- 2. JS SDK ---
    # NOTE: paynode-ai-skills indirect synchronization through @paynodelabs/sdk-js imports
    js_constants_path = workspace_path("packages", "sdk-js", "src", "constants.ts")
    js_content = f'''/** Generated by meta/scripts/sync-config.py */
export const PAYNODE_ROUTER_ADDRESS = "{config["networks"]["base"]["router"]}";
export const PAYNODE_ROUTER_ADDRESS_SANDBOX = "{config["networks"]["baseSepolia"]["router"]}";
export const BASE_USDC_ADDRESS = "{base_usdc}";
export const BASE_USDC_ADDRESS_SANDBOX = "{sepolia_usdc}";
export const PROTOCOL_TREASURY = "{config["protocol"]["treasury"]}";
export const PROTOCOL_FEE_BPS = {config["protocol"]["fee_bps"]};
export const MIN_PAYMENT_AMOUNT = BigInt({min_amount});
export const PROTOCOL_VERSION = {protocol_version};
export const SDK_VERSION = "{sdk_version}";

export const BASE_RPC_URLS = {json.dumps(base_rpcs)};
export const BASE_RPC_URLS_SANDBOX = {json.dumps(sepolia_rpcs)};

export const ACCEPTED_TOKENS: Record<number, string[]> = {{
    8453: ["{base_usdc}"],
    84532: ["{sepolia_usdc}"]
}};

export const PAYNODE_ROUTER_ABI = {json.dumps(FULL_ABI)};
'''
    if not sync_file(js_constants_path, js_content, check_mode): all_synced = False

    js_errors_path = workspace_path("packages", "sdk-js", "src", "errors", "index.ts")
    js_error_lines = [
        "/** Generated by meta/scripts/sync-config.py */",
        "export enum ErrorCode {"
    ]
    for code in error_codes:
        camel = to_camel_case(code)
        js_error_lines.append(f"  {camel} = \"{code}\",")
    js_error_lines.append("}")
    js_error_lines.append("")
    js_error_lines.append("export const ERROR_MESSAGES: Record<string, string> = {")
    for code, msg in error_codes.items():
        js_error_lines.append(f"  \"{code}\": \"{msg}\",")
    js_error_lines.append("};")
    js_error_lines.extend([
        "",
        "export class PayNodeException extends Error {",
        "  constructor(public code: ErrorCode, message?: string, public details?: any) {",
        "    const finalMessage = message || ERROR_MESSAGES[code] || \"An unexpected error occurred.\";",
        "    super(finalMessage);",
        "    this.name = \"PayNodeException\";",
        "    this.message = finalMessage;",
        "  }",
        "}"
    ])
    if not sync_file(js_errors_path, "\n".join(js_error_lines) + "\n", check_mode): all_synced = False

    # --- 3. Web Portal ---
    web_config_path = workspace_path("apps", "paynode-web", "app", "api", "pom", "config.ts")
    web_content = f'''import {{ 
  MIN_PAYMENT_AMOUNT,
  PROTOCOL_TREASURY,
  PROTOCOL_FEE_BPS,
  PAYNODE_ROUTER_ADDRESS,
  PAYNODE_ROUTER_ADDRESS_SANDBOX,
  BASE_USDC_ADDRESS,
  BASE_USDC_ADDRESS_SANDBOX,
  BASE_RPC_URLS,
  BASE_RPC_URLS_SANDBOX
}} from '@paynodelabs/sdk-js';

export {{ MIN_PAYMENT_AMOUNT, PROTOCOL_TREASURY, PROTOCOL_FEE_BPS }};

export const BASE_MAINNET_CONFIG = {{
  chainId: {config["networks"]["base"]["chainId"]},
  rpcUrls: BASE_RPC_URLS,
  routerAddress: PAYNODE_ROUTER_ADDRESS,
  usdcAddress: BASE_USDC_ADDRESS,
  treasury: PROTOCOL_TREASURY
}};

export const BASE_SEPOLIA_CONFIG = {{
  chainId: {config["networks"]["baseSepolia"]["chainId"]},
  rpcUrls: BASE_RPC_URLS_SANDBOX,
  routerAddress: PAYNODE_ROUTER_ADDRESS_SANDBOX,
  usdcAddress: BASE_USDC_ADDRESS_SANDBOX,
  treasury: PROTOCOL_TREASURY
}};

export const getNetworkConfig = (isMainnet: boolean) => isMainnet ? BASE_MAINNET_CONFIG : BASE_SEPOLIA_CONFIG;
'''
    if not sync_file(web_config_path, web_content, check_mode): all_synced = False

    # --- 4. Smart Contracts ---
    sol_config_path = workspace_path("packages", "contracts", "script", "Config.s.sol")
    def to_hex(addr): return addr if addr.startswith("0x") else f"0x{addr}"
    sol_content = f'''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// Generated by meta/scripts/sync-config.py
library Config {{
    address public constant ROUTER_MAINNET = {to_hex(config["networks"]["base"]["router"])};
    address public constant ROUTER_SEPOLIA = {to_hex(config["networks"]["baseSepolia"]["router"])};
    address public constant TREASURY = {to_hex(config["protocol"]["treasury"])};
    address public constant USDC_MAINNET = {to_hex(base_usdc)};
    address public constant USDC_SEPOLIA = {to_hex(sepolia_usdc)};
    uint256 public constant MIN_PAYMENT_AMOUNT = {config["protocol"]["min_payment_amount"]};
    uint256 public constant FEE_BPS = {config["protocol"]["fee_bps"]};
}}
'''
    if not sync_file(sol_config_path, sol_content, check_mode): all_synced = False
    
    # --- 5. AI Skills (Indirect Check) ---
    ai_skills_utils_path = workspace_path("packages", "paynode-ai-skills", "paynode-402", "scripts", "utils.ts")
    if ai_skills_utils_path.exists():
        with ai_skills_utils_path.open("r") as f:
            content = f.read()
        
        # Verify that constants imported from JS SDK match the intended values
        if 'PAYNODE_ROUTER_ADDRESS' not in content:
            print(f"⚠️ Warning: {ai_skills_utils_path} does not seem to import core constants.")
        elif check_mode:
            print(f"  (Verified): {ai_skills_utils_path} inherits consistent config from JS SDK.")

    if check_mode:
        if all_synced:
            print("✅ All configurations are consistent.")
            sys.exit(0)
        else:
            print("❌ Consistency check failed.")
            sys.exit(1)
    else:
        print("\n✨ Configuration synchronization complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sync or check configuration consistency.")
    parser.add_argument("--check", action="store_true", help="Check consistency without writing.")
    args = parser.parse_args()
    
    sync_config(check_mode=args.check)
