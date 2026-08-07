# Domain Context Content Rules

Use `DOMAIN-CONTEXT.md` for one bounded context's domain purpose, boundary, and ubiquitous language. Use root `CONTEXT-MAP.md` for bounded-context locations and cross-context relationships. A file named `GLOSSARY.md` is appropriate when a project stores term definitions separately from context purpose and boundary.

Apply these rules to every ubiquitous-language entry:

- Choose one canonical term within the applicable bounded context and list misleading synonyms under the selected template's avoid label.
- Define what the concept is in one or two sentences.
- Add a domain example only when it distinguishes the concept from a nearby meaning.
- Limit entries to project-specific domain concepts.
- Write semantic domain content only. Put storage, framework, API, UI, processing, orchestration, and other implementation details in their owning technical documents.
- Group terms under subheadings only when a natural domain grouping improves lookup.

Finish when each changed entry names one domain term, gives its meaning within the applicable bounded context, and contains no implementation detail.

For `CONTEXT-MAP.md`, describe the domain meaning and ownership of each relationship. Include a domain event, published contract, synchronous API, or shared type when it defines how the contexts relate. Put endpoint configuration, framework wiring, storage layout, and other code-level implementation details in technical documents.

Finish when every bounded context links to its `DOMAIN-CONTEXT.md` and every listed relationship states its domain meaning plus any integration contract needed to understand how the contexts relate.
