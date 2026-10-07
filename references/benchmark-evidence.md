# Model comparison evidence

Checked 2026-09-30 (Asia/Shanghai). Relevant official and independent primary sources were compared; this does not claim every review was collected. [model-routing.md](model-routing.md) contains recommendations. All measured scores below are external test results, not an individual's Codex success rates or consumption.

## Comparable effort snapshot

Artificial Analysis Intelligence Index **v4.3.2**, 10 evaluations. Filtered to the strengths compared in this snapshot; these API configurations do not validate live Codex controls.

| Model | Low | Medium | High | X-High |
|---|---:|---:|---:|---:|
| GPT-6.1 Sol | 42 | 48 | 50 | 51 |
| GPT-6 Astra | 46 | 50 | 51 | 52 |
| GPT-6 Sol | 34 | 40 | 43 | 44 |
| GPT-5.6 Sol | 33 | 39 | 42 | 44 |
| GPT-5.6 Terra | 27 | 30 | 34 | 38 |
| GPT-6 Luna | 21 | 29 | 32 | 34 |
| GPT-5.6 Luna | 21 | 25 | 32 | 35 |
| GPT-5.5 | 31 | 34 | 37 | 38 |

[AA current OpenAI table](https://artificialanalysis.ai/models/creators/openai). Use this for aggregate direction only; equal scores do not establish task-level equivalence. Do not mix older AA index versions with this snapshot.

For 6.1 Sol, weighted API cost per Intelligence Index task is Low $0.13, Medium $0.21, High $0.32, X-High $0.39. These are measured costs in AA's test mix, not rates, Codex quotas, or forecasts. They suggest diminishing aggregate gains at higher strength, not that High/X-High cannot help a particular task. [Low profile](https://artificialanalysis.ai/es/models/gpt-6-1-sol-low), [Medium profile](https://artificialanalysis.ai/es/models/gpt-6-1-sol-medium), [High profile](https://artificialanalysis.ai/es/models/gpt-6-1-sol-high), [X-High profile](https://artificialanalysis.ai/es/models/gpt-6-1-sol-xhigh)

AA reports strong 6.1 Sol coding-agent results at xhigh, with a point advantage over Astra at under 15% of its task cost in that harness. It also reports about 10–30% more output tokens than old Sol across Intelligence Index efforts, and a small presentation-Elo decline despite analytical gains. Thus improved capability/economy is task-specific; it is not simply "fewer tokens" or uniformly better visual output. [AA release analysis](https://artificialanalysis.ai/articles/gpt-6-1-sol-replaces-gpt-6-sol-after-just-7-days-with-near-astra-intelligence)

AA cost weights observed input/cache/reasoning/output usage at API prices. Its index is mainly English and text-based; it does not directly measure Chinese dictated-intent fidelity or local UI completion. [Definitions](https://artificialanalysis.ai/methodology), [Index methodology](https://artificialanalysis.ai/methodology/intelligence-benchmarking)

## Other task families and independent checks

OpenAI's launch evaluation reports 6.1 Sol improvements in software engineering, document work, and automation, while retaining Astra for the hardest science. These are vendor evaluations in specified research/API environments, not independent Codex measurements. [Official launch](https://openai.com/index/introducing-gpt-6-1-sol/)

ARC Prize's available **X-High** results show Astra's strong abstract reasoning and unfamiliar interactive adaptation: ARC-AGI-2 93.3%, ARC-AGI-3 59.34% with standard harness versus 98.44% with its provider adapter. GPT-5.6 Sol's X-High ARC-AGI-2 is 90%; GPT-6 Luna's is 41.9%. Different harnesses matter greatly. These findings preserve reasons to compare Astra and older Sol on specific hard reasoning tasks; they do not establish superiority over 6.1 Sol, whose ARC result was not retrieved. [Astra results](https://arcprize.org/results/openai-gpt-6-astra), [5.6 results](https://arcprize.org/results/openai-gpt-5-6), [6 Luna results](https://arcprize.org/results/openai-gpt-6-luna)

Vals' old-6-Sol page was also reviewed. Its benchmark mix and API configuration differ from the above available-strength comparison; its new-6.1 page could not be retrieved. It helps check whether another evaluation agrees but is not a Codex setting recommendation. No unavailable-setting Vals result is used to choose a picker strength. [Vals old Sol evaluation](https://www.vals.ai/models/openai_gpt-6-sol)

No defensible source here measures a model's special superiority at Chinese voice-to-task translation. Do not invent that specialty for Luna, Sol, or Astra. Distinguish document analysis, presentation evaluation, image perception, and image generation. Older vision anecdotes can also predate the September 25 image-encoding fix for 6 Sol/Luna. [API changelog](https://developers.openai.com/api/docs/changelog)

## Codex economy

The Standard credit rate table below was rechecked against official pricing on **2026-10-04**; no rates changed. Other benchmark/availability observations retain their original September 30 dates. For weighted cost, hybrid eligibility, and delegation rules, read [hybrid-delegation.md](hybrid-delegation.md).

Standard **credits per 1M tokens**, where token-based credit billing applies:

| Model | Input | Cached input | Output |
|---|---:|---:|---:|
| GPT-6 Luna | 2.5 | 0.25 | 12.5 |
| GPT-5.6 Luna | 5 | 0.5 | 30 |
| GPT-6.1 Sol | 50 | 2.5 | 250 |
| GPT-6 Sol | 50 | 5 | 250 |
| GPT-5.6 Terra | 50 | 5 | 300 |
| GPT-5.6 Sol | 100 | 10 | 500 |
| GPT-5.5 | 125 | 12.5 | 750 |
| GPT-6 Astra | 250 | 25 | 1250 |

Codex has no separate cache-write credit charge. This table does not predict included subscription usage; account limits and agreements apply. Work and Codex share usage. [Official pricing](https://learn.chatgpt.com/docs/pricing)

Identical uncached input/output token mixes make Astra 5× 6.1 Sol, and 6.1 Sol 20× 6 Luna. Actual task consumption can differ because of reasoning, cache hits, tool/context reads, retries, and integration. API prices are a separate billing system; AA's dollar figures above belong to API tests, not the user's Codex plan.

| Speed mode | Included usage multiplier | Credits / Enterprise pay-as-you-go multiplier |
|---|---:|---:|
| Fast, where available | 2.5× | 2× |
| Astra Ultrafast, where eligible | 8× | 6× |

Multipliers are billing, not speedup promises. 6.1 Sol supports Standard/Fast at this check, with Ultrafast forthcoming. Ultra delegation and Fast/Ultrafast speed are separate controls. API support does not establish which options are available in a particular picker. [Speed](https://learn.chatgpt.com/docs/agent-configuration/speed), [Models](https://learn.chatgpt.com/docs/models)

## What remains uncertain

No controlled comparison across individual users' actual tasks has been performed. The new model's independent coverage is incomplete: AA profiles were retrieved, but new-model ARC/Vals results were not. No exact Codex task prices, success probabilities, Chinese-prompt savings, or hidden-setting mechanisms are asserted. This is a dated starting policy with task-specific calibration still needed, not a universal optimal allocation.
