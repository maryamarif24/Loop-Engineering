# Loop Engineering: Project 12 - Agents

This project demonstrates loop engineering concepts using OpenCode.

## Key Agents

- **Maker**: Creates the priority rules and rate limit policy (designs the item network, priority assignments, and per-run processing caps)
- **Checker**: Reviews the priority ordering, rate limit adherence, and processing sequence for correctness and sustainability
- **Loop Runner**: Executes the rate-limited queue traversal, manages item processing order, and enforces per-run caps