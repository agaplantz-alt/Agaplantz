# Hypothesis System (PART 14)

Every material optimisation needs all seven fields before it runs. No field may be blank.

```
ID              EXP-000
PROBLEM         What is measurably wrong. With the number.
HYPOTHESIS      What we believe is causing it, and why.
CHANGE          Exactly what changes. One variable.
EXPECTED RESULT  Which metric moves, in which direction, by how much.
MEASUREMENT     Metric, baseline value, baseline window.
TIME HORIZON    How long before reading. Justified by conversion volume.
DECISION RULE   Explicit thresholds for KEEP / MODIFY / REVERT.
```

## Sizing the time horizon
At ~24 paid conversions/month, detecting a change smaller than roughly a third requires several weeks. Default windows:

| Change type | Minimum window |
|---|---|
| Checkout / CRO | 4 weeks (~180 checkouts/mo) |
| Google Ads bidding or budget | 4–6 weeks |
| Meta creative | 4–5 days per ad to exit learning; 2 weeks to judge |
| Feed / title changes | 4 weeks |
| Offer / pricing | 4 weeks, watching margin not just volume |

**If a test cannot reach its window without another change interfering, don't start it.**
