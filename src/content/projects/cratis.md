---
order: 3
title: "Cratis Build Reference App"
subtitle: "Event sourcing reference kit"
category: "Architecture"
summary: "A streamlined expense tracking system built with Cratis."
tech: [".NET", "Cratis (Chronicle/Arc)", "React", "Event Sourcing"]
---
### Framing: Pattern Clarity Over Feature Completeness
This project serves as a minimal, highly opinionated reference implementation designed to showcase clean architectural patterns without the noise of production feature bloat.

### Core Implementation
* **Features:** Kanban-style tasks, goals loop, inbox, triggers, cron scheduling, R2 filesystem MCP integration, per-agent least-privilege permissions[cite: 1].
- **Domain:** A streamlined expense tracking system.
- **Configurable Gates:** Implements a configurable approval gate that dynamically adjusts its behavior (e.g., completely skippable for a sole trader, or auto-approving transactions under a specific monetary threshold).
- **Patterns Demonstrated:** Focuses purely on clean, decoupled examples of:
  - State change capturing
  - Materialized state views
  - Workflow automation
  - Reliable persistence
  - System integration
  - Structured logging