# Marketing budget decision

Identify whether the increase is monthly recurring or one-time. The marketing calculator
only accepts a positive recurring monthly increment. Do not silently reinterpret a
one-time campaign budget. Use an explicit historical baseline and its evidence quality.

Run `marketing-budget` to produce a Decision record. Required incremental revenue is
increment / contribution margin. The margin is an explicit scenario assumption, never
inferred from revenue minus all operating expenses. The downside case assumes no uplift:
new monthly burn = max(-historical profit * 30 / baseline days + increment, 0).
The cash snapshot is already the closing balance. Do not subtract a recurring monthly
increment from it and then count that same increment again as burn.

The deterministic CLI provides decision prompts, not evidence of market response.
The host model should examine founder-supplied evidence through these perspectives:

- CEO: strategic goal, founder capacity, reserve requirement and alternatives.
- CFO: baseline quality, downside runway, obligations, affordability and payback.
- CMO: measured acquisition costs, attribution, incremental conversion and test design.

Show disagreements. A positive sales hypothesis does not resolve an affordability gap.
Offer hold, bounded experiment and full increase as alternatives when evidence permits.
Explain missing evidence and what would change the recommendation. Define experiment
cap, success measure, stop rule and review date with the founder; no universal acceptable
runway, CAC or return threshold is imposed by the skill. Do not invent a profit forecast
from the no-uplift scenario or call break-even revenue an expected outcome.

Record the result as proposed. There is no advertising-account or payment connector;
return the exact budget action for review. The optional GitHub connector can only
create a separately approved issue, not change marketing spend.
