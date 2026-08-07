# English Domain Context Templates

## DOMAIN-CONTEXT.md

```md
# {Context Name}

## Purpose and boundary

{One or two sentences defining the domain purpose and boundary of this bounded context.}

## Ubiquitous language

**Order**:
The commercial commitment between a Customer and the business for specified goods or services.
_Avoid_: purchase, transaction

**PI / Proforma Invoice**:
An informational document that provides a detailed estimate of the goods or services a supplier intends to deliver to a customer.
_Avoid_: invoice, receipt

**PO / Purchase Order**:
A document that asks a company to supply goods or services
_Avoid_: purchase request, purchase document
```

## CONTEXT-MAP.md

```md
# Context Map

## Contexts

- [Ordering](./src/ordering/DOMAIN-CONTEXT.md): owns commercial orders
- [Billing](./src/billing/DOMAIN-CONTEXT.md): owns invoices and payment obligations
- [Fulfillment](./src/fulfillment/DOMAIN-CONTEXT.md): owns preparation and delivery commitments

## Relationships

- **Ordering to Fulfillment**: Ordering publishes `OrderPlaced`. Fulfillment consumes it to establish a fulfillment commitment
- **Fulfillment to Billing**: Fulfillment publishes `ShipmentDispatched`. Billing consumes it to make an Invoice eligible for collection
- **Ordering and Billing**: share `CustomerId` and `Money`
```
