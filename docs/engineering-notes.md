# Engineering notes

These lessons summarize work on the private project without distributing its
implementation or operational procedures.

## Automating without removing judgment

Automation reduces repetitive coordination. It should not turn a model's
suggestion, a mailbox health observation, or a visible button into permission
for an external action. Human review and deterministic safety boundaries serve
different purposes.

The standalone approval example demonstrates an immutable decision about a
labelled revision. It intentionally omits identity, access control, persistence,
and the additional checks a real system needs.

## Keeping uncertainty explicit

A network outcome and a local write are different kinds of evidence. Uncertainty
must remain visible instead of becoming a silent retry. Observability should
help an operator distinguish known success from assumptions.

The portfolio does not disclose the private recovery design.

## Separating transport and synchronization

Delivery acceptance, Sent-folder synchronization, and recipient receipt are
distinct. A mailbox synchronization problem should not become a reason to
send the prospect message again.

The fake transport only records Python objects in memory. It is not an SMTP
or IMAP implementation and its receipts are not delivery evidence.

## Testing boundaries

Offline adapters help test expected behavior and failure cases without exposing
customers or relying on external services. Small boundary tests also make
assumptions explicit: equality exhausts a budget, missing review denies approval,
and absent routing evidence asks for human attention.

The public arithmetic check does not allocate capacity or guarantee concurrency
safety. The three-way routing example does not reproduce production policy.

## A deliberately limited portfolio

The examples were written for this repository rather than extracted from the
private implementation. Adding source lines for their own sake would not improve
the evidence. Full application code, tests, prompts, schemas, and operational
know-how remain private.
