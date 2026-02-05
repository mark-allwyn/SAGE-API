# SAGE API - Business Case

**Synthetic Audience Generation Engine**
Automated concept testing using AI-simulated consumer panels

---

## The Problem

Concept testing remains slow and expensive, even with digital alternatives:

- **Recruitment agencies**: 2-4 weeks lead time, $15,000-$50,000+ per study
- **Online panels**: 1-2 weeks, $5,000-$15,000 per study
- **Digital tools (e.g. Maze.co)**: 3-5 days, ~$1,500 for a 90-person study - faster, but still costly for iterative testing
- **Internal testing**: Limited demographics, inherent bias, days of coordination
- **Iteration cost**: Every creative revision requires a new round of testing

Teams either skip testing entirely (risking failed launches) or test too late to make meaningful changes.

## The Solution

SAGE runs a full consumer panel study in **under 3 minutes for as little as $0.08** using LLM-simulated personas.

- 90 demographically profiled personas evaluate a concept simultaneously
- Responses are mapped to validated Likert scales using peer-reviewed methodology (SSR)
- Results include composite scores, per-question metrics, distribution analysis, and markdown reports
- Supports text, image, and combined concepts (storyboards, ads, packaging)

## ROI Opportunities

### 1. Pre-Flight Screening (Highest Impact)

Run SAGE before committing budget to full research. Kill weak concepts early, refine promising ones.

- **Current cost to test 1 concept**: $10,000-30,000 (agency panel)
- **SAGE cost to test 10 variations**: ~$0.80 (using optimised model)
- **Saving per screening round**: $10,000-30,000
- **Annual saving** (monthly screening): **$120,000-360,000**

### 2. Creative Optimisation Loop

Test multiple creative variations in minutes rather than weeks. A/B test messaging, visuals, and positioning before production spend.

- Run 20 concept variations in under 60 minutes for ~$1.60
- Identify top 3 performers before committing production budget
- **Avoided waste on underperforming creatives**: $50,000-200,000/year

### 3. Reduced Time-to-Market

Eliminate 2-4 week research lead times from the development cycle.

- Concept feedback in minutes instead of weeks
- More iterations within the same timeline
- Earlier go/no-go decisions
- **Value**: Faster launches, competitive advantage (hard to quantify but significant)

### 4. Democratised Testing

Enable teams beyond the research function to test concepts without specialist skills or budget approval.

- Brand managers self-serve concept checks
- Creative teams validate directions before review meetings
- Product teams test positioning variants
- **Value**: Better decisions across the organisation, reduced bottleneck on research team

### 5. Continuous Benchmarking

Build a library of SAGE scores across concepts, markets, and time periods to establish internal norms.

- Track concept strength trends over time
- Compare new concepts against historical baselines
- Calibrate SAGE scores against real-world outcomes
- **Value**: Proprietary competitive intelligence asset

---

## Cost Model

### Per-Experiment Cost (90 personas, 5 questions)

Validated across 36 model configurations (see Model Validation below). All models shown produce consensus results:

| Model Configuration | Cost/Experiment | Processing Time |
|---|---:|---:|
| Nova 2 Lite + Titan v2 (Best Value) | $0.08 | ~2 min |
| Nova Lite + Titan v1 | $0.11 | ~1.5 min |
| Haiku 3 + Titan v1 | $0.49 | ~1.5 min |
| Nova Pro + Titan v1 | $1.38 | ~2.5 min |
| Haiku 4.5 + Titan v2 | $1.94 | ~2 min |
| Sonnet 4.5 + Titan v1 | $5.81 | ~3 min |
| Opus 4.5 + Titan v2 | $9.68 | ~2.5 min |

### Monthly Usage Scenarios

| Scenario | Experiments/Month | Monthly Cost (Budget) | Monthly Cost (Mid-range) |
|----------|-------------------|----------------------:|-------------------------:|
| Light (1 team, weekly) | 4 | $0.32 | $2 |
| Medium (3 teams, weekly) | 12 | $0.96 | $6 |
| Heavy (daily across org) | 60 | $4.80 | $29 |
| Enterprise (multiple markets) | 200 | $16 | $98 |

*Budget = Nova 2 Lite ($0.08/experiment), Mid-range = Haiku 3 ($0.49/experiment)*

### Infrastructure Cost

| Component | Monthly Cost | Notes |
|-----------|-------------|-------|
| AWS ECS/Fargate (API hosting) | $50-150 | Single container, auto-scaling |
| AWS Bedrock (model access) | No base cost | Pay-per-token only |
| AWS CloudWatch (logging) | $5-10 | Standard monitoring |
| **Total infrastructure** | **$55-160/month** | |

### Total Annual Cost of Ownership (using mid-range Haiku 3)

| Scenario | LLM Costs | Infrastructure | Total Annual |
|----------|-----------|----------------|--------------|
| Light | $24 | $660 | **$684** |
| Medium | $72 | $960 | **$1,032** |
| Heavy | $352 | $1,440 | **$1,792** |
| Enterprise | $1,176 | $1,920 | **$3,096** |

---

## Model Validation

Permutation testing across 36 model configurations (9 vision models x 4 embedding models) confirms the robustness of the SAGE methodology:

- **91% consensus rate** - 33 of 36 configurations produce statistically consistent concept rankings
- **120x cost range** - cheapest consensus model ($0.08) to most expensive ($9.68), all producing equivalent directional results
- **Vision model drives variation** - choice of vision model contributes 1.8x more variance than embedding model choice
- **Only 3 outlier configurations** - all involving older/smaller models, easily avoided through configuration defaults
- **Methodology is model-independent** - model selection can be driven by budget rather than accuracy concerns, since all mainstream models converge on the same results

This validation means organisations can start with budget models (Nova 2 Lite at $0.08/experiment) and upgrade to premium models only if specific use cases demand it, without sacrificing result quality.

---

## Comparison: SAGE vs Traditional Research

| Dimension | Traditional Panel | Digital Tools (e.g. Maze.co) | SAGE |
|-----------|-------------------|------------------------------|------|
| **Cost per study** | $10,000-50,000 | ~$1,500 | $0.08-$10 |
| **Turnaround** | 2-4 weeks | 3-5 days | 2-3 minutes |
| **Iterations** | 1-2 (budget constrained) | 2-3 (cost constrained) | Unlimited |
| **Sample size** | 200-500 (expensive) | 50-100 | 90+ (trivial to scale) |
| **Respondent type** | Real consumers, recruited | Real users, self-selected | AI-simulated, profiled |
| **Availability** | Business hours, recruitment dependent | Online, recruitment required | 24/7, instant |
| **Replaces traditional?** | - | Partially | No - pre-screens |

**SAGE does not replace traditional research.** It sits upstream as a rapid screening and iteration tool, ensuring that only the strongest concepts proceed to expensive validation.

---

## Risk and Limitations

- **Not a replacement for real consumers** - SAGE provides directional signal, not definitive market truth
- **Methodology dependency** - based on published academic research (SSR); accuracy depends on prompt design and reference set quality
- **Model evolution** - LLM behaviour may shift with model updates; permutation testing across 36 model configurations shows 91% produce consensus results, and configuration can be locked to a validated model
- **Calibration required** - SAGE scores should be benchmarked against real-world outcomes to establish confidence intervals

---

## Recommendation

Deploy SAGE as an internal pre-screening tool. Annual cost under $1,800 even at heavy usage with an optimised model configuration. Potential saving of $120,000-360,000/year in avoided panel costs, plus faster time-to-market.

**Next steps:**
1. Pilot with one brand team for 4 weeks
2. Run SAGE alongside one planned panel study to calibrate
3. Establish internal score benchmarks
4. Roll out to wider organisation
