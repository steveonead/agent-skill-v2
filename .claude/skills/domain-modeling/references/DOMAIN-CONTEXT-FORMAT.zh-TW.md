# Traditional Chinese Domain Context Templates

## DOMAIN-CONTEXT.md

```md
# {領域脈絡名稱}

## 目的與邊界

{用一至兩句話定義此領域脈絡的業務目的與邊界。}

## 領域通用語言

**訂單（Order）**：
客戶與企業針對特定商品或服務建立的商業承諾。
_避免使用_：購買、交易

**PI（Proforma Invoice）**:
一份寫有所銷售貨物名稱、規格、單價等訊息的非正式的參考性發票，沒有任何約束力。
_避免使用_: 形式發票、收據、發票、統一發票

**PO（Purchase Order）**:
買方發給賣方，用來請求購買商品或服務的文件。
_避免使用_: 訂單、採購單
```

## CONTEXT-MAP.md

```md
# 領域脈絡地圖

## 領域脈絡

- [訂購](./src/ordering/DOMAIN-CONTEXT.md)：擁有商業訂單
- [帳務](./src/billing/DOMAIN-CONTEXT.md)：擁有發票與付款義務
- [履約](./src/fulfillment/DOMAIN-CONTEXT.md)：擁有備貨與交付承諾

## 關係

- **訂購至履約**：訂購會發布 `OrderPlaced`，履約會接收此事件並建立履約承諾
- **履約至帳務**：履約會發布 `ShipmentDispatched`，帳務會接收此事件，讓發票符合收款條件
- **訂購與帳務**：共用 `CustomerId` 與 `Money`
```
