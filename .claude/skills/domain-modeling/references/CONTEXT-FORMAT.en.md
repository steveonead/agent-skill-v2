# English Context Templates

## CONTEXT.md

```md
# {Context Name}

{One or two sentences defining the domain purpose and boundary of this context.}

## Language

**Order**:
The commercial commitment between a Customer and the business for specified goods or services.
_Avoid_: Purchase, transaction
_Example_: Order 1042 is the commitment accepted for Northwind Traders.
```

## CONTEXT-MAP.md

```md
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md): owns commercial orders
- [Billing](./src/billing/CONTEXT.md): owns invoices and payment obligations
- [Fulfillment](./src/fulfillment/CONTEXT.md): owns preparation and delivery commitments

## Relationships

- **Ordering to Fulfillment**: Ordering publishes `OrderPlaced`. Fulfillment consumes it to establish a fulfillment commitment
- **Fulfillment to Billing**: Fulfillment publishes `ShipmentDispatched`. Billing consumes it to make an Invoice eligible for collection
- **Ordering and Billing**: share `CustomerId` and `Money`
```
