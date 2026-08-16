---
title: "AgentOS"
subtitle: "Personal agent control plane"
category: "AI"
tech: ["Claude Agent SDK", "TypeScript", "R2 Filesystem", "MCP Integration"]
---
### Architecture Overview
A robust control plane engineered to coordinate, monitor, and govern autonomous agents managed via the Claude Agent SDK. This platform serves as an operational dashboard rather than a user-facing utility, focusing heavily on security isolation and deterministic task tracking.

### Core Capabilities
- **Task Management:** Provides a centralized, Kanban-style interface for monitoring active goals loops, task queues, and global system triggers.
- **Scheduling Engine:** Built-in cron execution scheduler for automated, routine agent dispatches.
- **Storage & Tooling:** Seamless Model Context Protocol (MCP) integration over an R2 cloud filesystem.
- **Security Fabric:** Implements zero-trust execution by enforcing strict, per-agent **least-privilege permissions** across filesystems and runtime tools.