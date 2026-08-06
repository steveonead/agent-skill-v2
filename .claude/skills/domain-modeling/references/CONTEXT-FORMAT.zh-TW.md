# Traditional Chinese Context Templates

## CONTEXT.md

```md
# {領域脈絡名稱}

{用一至兩句話定義此領域脈絡的業務目的與邊界。}

## 用語

**訂單**：
客戶與企業針對特定商品或服務建立的商業承諾。
_避免使用_：購買、交易
_例子_：訂單 1042 是企業為北風貿易公司接受的商業承諾。
```

## CONTEXT-MAP.md

```md
# 領域脈絡地圖

## 領域脈絡

- [訂購](./src/ordering/CONTEXT.md)：擁有商業訂單
- [帳務](./src/billing/CONTEXT.md)：擁有發票與付款義務
- [履約](./src/fulfillment/CONTEXT.md)：擁有備貨與交付承諾

## 關係

- **訂購至履約**：訂購會發布 `OrderPlaced`，履約會接收此事件並建立履約承諾
- **履約至帳務**：履約會發布 `ShipmentDispatched`，帳務會接收此事件，讓發票符合收款條件
- **訂購與帳務**：共用 `CustomerId` 與 `Money`
```
