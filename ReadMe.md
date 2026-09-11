# Online UCI Retail Sales Analysis
   
## Objective
Analyze online retail sales to understand revenue trends, product performance, geographic differences, and cancellations.

## Ket findings
**Revenue:** Overall, the analysis indicates that the business experienced a significant revenue shift in late 2010, and revenue growth primarily coincided with a substantial increase in transaction volume and new customer acquisition. Revenue subsequently remained at a much higher level throughout 2011, although the September peak was partly influenced by an exceptionally large order. Revenue is also highly concentrated geographically, with the United Kingdom accounting for approximately 83% of total revenue, highlighting both the importance of the domestic market and the potential for further international growth.

**Products:** From a product perspective, revenue is relatively diversified, with the top 10 products contributing only around 10% of total revenue. However, inventory management should distinguish between products generating revenue through exceptional individual orders and products demonstrating consistently high transaction volumes. Products such as the REGENCY CAKESTAND 3 TIER, WHITE HANGING HEART T-LIGHT HOLDER and JUMBO BAG RED RETROSPOT may therefore warrant particular attention when prioritising stock levels.

**Cancellations:** The analysis also identifies opportunities to reduce lost revenue from cancellations. Although cancellations represent a relatively small proportion of transactions, they account for approximately 5.42% of total revenue. Germany has a notably higher cancellation rate than the UK and France, while the REGENCY CAKESTAND 3 TIER and JAM MAKING SET WITH JARS are among the most frequently cancelled products. Further investigation into the causes of cancellations for these products and markets could therefore help reduce avoidable revenue loss.

## Recommendations
Based on these findings, the business should:
- Prioritise customer acquisition and retention.

- Maintain adequate inventory for consistently high-demand products.

- Investigate the causes of cancellations in higher-risk markets and product categories. 

- Expand sales in established international markets: the strong dependence on the UK market suggests that expanding sales could provide an opportunity to diversify revenue and reduce geographic concentration.

- Unusually large individual orders should be monitored separately from underlying demand trends to ensure that future revenue and inventory decisions are based on sustainable purchasing patterns rather than exceptional transactions.

## Dataset
Dataset can be downloaded from https://archive.ics.uci.edu/dataset/352/online+retail DOI: 10.24432/C5BW33

## Data Quality & Assumptions
Invoice numbers containing an A (pertaining to "bad debt") were filtered from all analyses.

Descriptions that were not captialized (not describing actual products) were filtered from all analyses. 

Rows with non-positive quantities were treated as returns/cancellations and excluded from all analyses, except cancellation analyses.

Both Price and Quantity are strongly right skewed. 

Revenue was calculated as Quantity × UnitPrice. 

## Methodology
Raw data was examined for quality and transformed into analytical tables in SQL. 

Initial summary analyses were performed on analytical tables in SQL

Visualizations were made in python.
    
    
