# Architecture overview

This document describes the private project's responsibilities at a conceptual
level. It is not a build plan, runtime topology, database design, or integration
contract. The public examples are independent teaching material.

## Responsibilities

- Intake and validation establish whether proposed work is suitable for review.
- Human approval keeps content decisions visible and explicit.
- Scheduling and safety control whether outbound work may proceed.
- Transport abstracts external delivery from application decisions.
- Inbound processing turns replies into operational attention.
- Selective AI assistance supplies proposals; deterministic policy and humans
  retain authority over consequential actions.
- The operator interface presents work requiring attention.

## Boundaries

Persistence supports durable decisions. Transport outcomes are external
evidence, not automatically proof of delivery. Mailbox synchronization is
separate from delivery. Operational access and secrets remain outside this
portfolio.

The public package has no persistence or network implementation and does not
connect these responsibilities into an application. It contains no private
schemas, recovery transitions, orchestration ordering, or deployment layout.

See the high-level diagram in the [README](../README.md).
