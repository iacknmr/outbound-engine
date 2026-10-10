# Security and safety principles

This is a public-safe discussion of principles, not a threat-model replacement
or production security runbook.

## Private-system principles

- External actions require explicit permission and human approval where needed.
- A global stop should remain independent of provider observations.
- Capacity, suppression, and cooldown checks constrain automation.
- Ambiguous delivery should fail closed rather than be blindly retried.
- Ambiguous human intent belongs in operator review.
- Sent synchronization failure must not trigger duplicate submission.
- Sensitive content and access credentials should not enter public artifacts.

No exact recovery transitions, internal tables, provider behaviors, credential
structure, or allocation algorithms are disclosed here.

## Public-example limitations

The examples have no network clients, database access, provider adapters,
credentials, runtime configuration loader, or application entrypoint. They
cannot send email, log into a mailbox, classify through a provider, launch a
console, or reconstruct the private schema.

The capacity result is not a reservation. The approval result is not authenticated
authorization. The routing destination is not an executed business operation.
A fake receipt is not delivery evidence. These limitations are intentional.

Tests use only fictional content and in-memory objects. Development dependency
installation is separate from offline execution of the examples.

## Publication review

Use only fictional/reserved identities in public material. Screenshots require
a separate redaction review, including browser chrome and image metadata.
No customer data, real campaign copy, operational paths, or production logs
should be added later.

Owner review remains necessary before publication. Automated scans cannot
establish ownership rights or guarantee that every possible sensitive detail
has been identified. This portfolio is not licensed as open source.
