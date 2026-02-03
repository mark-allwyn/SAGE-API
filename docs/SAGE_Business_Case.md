# SAGE API - Business Case

**Synthetic Audience Generation Engine**
Automated concept testing using AI-simulated consumer panels

---

## The Problem

Traditional concept testing is slow, expensive, and bottlenecked by recruitment:

- **Recruitment agencies**: 2-4 weeks lead time, $15,000-$50,000+ per study
- **Online panels**: 1-2 weeks, $5,000-$15,000 per study
- **Internal testing**: Limited demographics, inherent bias, days of coordination
- **Iteration cost**: Every creative revision requires a new round of testing

Teams either skip testing entirely (risking failed launches) or test too late to make meaningful changes.

## The Solution

SAGE runs a full consumer panel study in **2 minutes for under $2** using LLM-simulated personas.

- 90 demographically profiled personas evaluate a concept simultaneously
- Responses are mapped to validated Likert scales using peer-reviewed methodology (SSR)
- Results include composite scores, per-question metrics, distribution analysis, and markdown reports
- Supports text, image, and combined concepts (storyboards, ads, packaging)

## ROI Opportunities

### 1. Pre-Flight Screening (Highest Impact)

Run SAGE before committing budget to full research. Kill weak concepts early, refine promising ones.

- **Current cost to test 1 concept**: $10,000-30,000 (agency panel)
- **SAGE cost to test 10 variations**: ~$15
- **Saving per screening round**: $10,000-30,000
- **Annual saving** (monthly screening): **$120,000-360,000**

### 2. Creative Optimisation Loop

Test multiple creative variations in minutes rather than weeks. A/B test messaging, visuals, and positioning before production spend.

- Run 20 concept variations in 40 minutes for ~$30
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

| Component | Bedrock (Claude Sonnet 4.5) | OpenAI (GPT-4o) |
|-----------|----------------------------|-----------------|
| LLM Generation (450 calls) | $1.33 | $1.00 |
| Embeddings (SSR mapping) | $0.001 | $0.001 |
| **Total per experiment** | **~$1.33** | **~$1.00** |

### Monthly Usage Scenarios

| Scenario | Experiments/Month | Monthly LLM Cost | Annual LLM Cost |
|----------|-------------------|-------------------|-----------------|
| Light (1 team, weekly) | 4 | $5 | $60 |
| Medium (3 teams, weekly) | 12 | $16 | $190 |
| Heavy (daily across org) | 60 | $80 | $960 |
| Enterprise (multiple markets) | 200 | $270 | $3,200 |

### Infrastructure Cost

| Component | Monthly Cost | Notes |
|-----------|-------------|-------|
| AWS ECS/Fargate (API hosting) | $50-150 | Single container, auto-scaling |
| AWS Bedrock (model access) | No base cost | Pay-per-token only |
| AWS CloudWatch (logging) | $5-10 | Standard monitoring |
| **Total infrastructure** | **$55-160/month** | |

### Total Annual Cost of Ownership

| Scenario | LLM Costs | Infrastructure | Total Annual |
|----------|-----------|----------------|--------------|
| Light | $60 | $660 | **$720** |
| Medium | $190 | $960 | **$1,150** |
| Heavy | $960 | $1,440 | **$2,400** |
| Enterprise | $3,200 | $1,920 | **$5,120** |

---

## Comparison: SAGE vs Traditional Research

| Dimension | Traditional Panel | SAGE |
|-----------|-------------------|------|
| **Cost per study** | $10,000-50,000 | $1-2 |
| **Turnaround** | 2-4 weeks | 2 minutes |
| **Iterations** | 1-2 (budget constrained) | Unlimited |
| **Sample size** | 200-500 (expensive) | 90+ (trivial to scale) |
| **Availability** | Business hours, recruitment dependent | 24/7, instant |
| **Replaces traditional?** | - | No - complements and pre-screens |

**SAGE does not replace traditional research.** It sits upstream as a rapid screening and iteration tool, ensuring that only the strongest concepts proceed to expensive validation.

---

## Risk and Limitations

- **Not a replacement for real consumers** - SAGE provides directional signal, not definitive market truth
- **Methodology dependency** - based on published academic research (SSR); accuracy depends on prompt design and reference set quality
- **Model evolution** - LLM behaviour may shift with model updates; reproducibility testing shows excellent stability within model versions
- **Calibration required** - SAGE scores should be benchmarked against real-world outcomes to establish confidence intervals

---

## Recommendation

Deploy SAGE as an internal pre-screening tool. Annual cost under $2,500 even at heavy usage. Potential saving of $120,000-360,000/year in avoided panel costs, plus faster time-to-market.

**Next steps:**
1. Pilot with one brand team for 4 weeks
2. Run SAGE alongside one planned panel study to calibrate
3. Establish internal score benchmarks
4. Roll out to wider organisation
