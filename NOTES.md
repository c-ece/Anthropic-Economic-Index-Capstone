# Project Notes

## Dataset Information
- Dataset: Anthropic Economic Index
- Source: Anthropic
- Release: 2025-09-15
- Dataset URL: https://huggingface.co/datasets/Anthropic/EconomicIndex
- Release URL: https://huggingface.co/datasets/Anthropic/EconomicIndex/tree/main/release_2025_09_15
- Download date: September 11, 2026
- License: Creative Commons Attribution 4.0 (CC BY 4.0)
- Research question: Do consumers and businesses use AI differently on the same tasks?
- Paper citation: arXiv:2503.04761 [cs.CY]
- DOI: https://doi.org/10.48550/arXiv.2503.04761
- Citation: Appel, R., McCrory, P., Tamkin, A., Stern, M., McCain, M., & Neylon, T. (2025). Anthropic Economic Index Report: Uneven Geographic and Enterprise AI Adoption. Anthropic.

### Data Collection
The dataset contains aggregated usage data from Claude.ai and a sample of first-party (1P) API usage. The data was analyzed using privacy-preserving methods. In this project, Claude.ai represents consumer usage, while the 1P API data represents business usage. 

### Unit of Observation
Each row shows a summarized measurement for a specific category. The rows do not contain information about individual users or individual conversations.

### Key Variables
The main variables for this project are:

- `platform_and_product`: identifies Claude.ai or 1P API usage.
- `onet_task`: identifies the type of occupational task.
- `collaboration`: describes how the human and AI work together.
- `value`: contains the numeric value of the metric.
  
## Verification
The September 2025 Anthropic Economic Index report provides several results that I will compare with my analysis:

- Automation accounts for 77% of API use.
- Augmentation accounts for 12% of API use.
- In the API data, 97% of tasks are mainly used for automation, while this percentage is 47% for Claude.ai.

## Raw Data Examples
