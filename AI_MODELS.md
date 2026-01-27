# 🤖 AI Models Guide for Applytune

Complete guide to choosing the best AI model for your needs.

---

## 🎯 Quick Recommendation

**Just want the best?** → Use **GPT-4o** (default)

**Want to save money?** → Use **GPT-3.5-turbo**

**Need best style preservation?** → Use **Claude 3.5 Sonnet**

---

## 📊 Model Comparison

### OpenAI Models

| Model | Cost/Resume* | Speed | Quality | Best For |
|-------|-------------|-------|---------|----------|
| **GPT-4o** ⭐ | ~$0.03 | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | **Overall best choice** |
| GPT-4 Turbo | ~$0.05 | ⚡⚡⚡ | ⭐⭐⭐⭐ | Good balance |
| GPT-4 | ~$0.12 | ⚡⚡ | ⭐⭐⭐⭐⭐ | High quality (slower) |
| GPT-3.5 Turbo | ~$0.01 | ⚡⚡⚡⚡ | ⭐⭐⭐ | **Budget option** |

### Anthropic Models

| Model | Cost/Resume* | Speed | Quality | Best For |
|-------|-------------|-------|---------|----------|
| **Claude 3.5 Sonnet** | ~$0.03 | ⚡⚡⚡ | ⭐⭐⭐⭐⭐ | **Style preservation** |
| Claude 3 Opus | ~$0.12 | ⚡⚡ | ⭐⭐⭐⭐⭐ | Highest quality |

*Estimated cost per resume optimization (~2000 tokens input, ~800 tokens output)

---

## 🏆 Recommended Models by Use Case

### For Most Users
```
Model: GPT-4o
Why: Best balance of quality, speed, and cost
Cost: ~$0.03 per resume
Set in .env: AI_MODEL=gpt-4o
```

### For Budget-Conscious Users
```
Model: GPT-3.5 Turbo
Why: 3x cheaper, still good results
Cost: ~$0.01 per resume
Set in .env: AI_MODEL=gpt-3.5-turbo
```

### For Style Preservation
```
Model: Claude 3.5 Sonnet
Why: Excellent at maintaining writing tone
Cost: ~$0.03 per resume
Set in .env: AI_MODEL=claude-3-5-sonnet-20241022
```

### For Maximum Quality
```
Model: GPT-4o or Claude 3.5 Sonnet
Why: Both are top-tier for different reasons
Cost: ~$0.03 per resume
```

### For Long Resumes (5+ pages)
```
Model: Claude 3.5 Sonnet
Why: 200K token context window
Cost: ~$0.03-0.08 per resume
Set in .env: AI_MODEL=claude-3-5-sonnet-20241022
```

---

## 💡 Model Details

### GPT-4o (Recommended)
```
Provider: OpenAI
Released: November 2024
Context: 128K tokens (~100 pages)

Strengths:
✓ Latest technology
✓ Fast response time
✓ Great at preserving style
✓ Good cost/quality ratio
✓ Excellent instruction following

Weaknesses:
- None significant

Best for: General use, most resumes
Cost: $5/1M input, $15/1M output
```

### GPT-4 Turbo
```
Provider: OpenAI
Released: 2024
Context: 128K tokens

Strengths:
✓ Fast and capable
✓ Good quality
✓ Large context window

Weaknesses:
- Slightly more expensive than GPT-4o
- Not as good as GPT-4o at style

Best for: When you need speed + quality
Cost: $10/1M input, $30/1M output
```

### GPT-3.5 Turbo
```
Provider: OpenAI
Context: 16K tokens

Strengths:
✓ Very fast
✓ Very cheap
✓ Decent quality

Weaknesses:
- Less sophisticated than GPT-4
- May not preserve style as well
- Shorter context window

Best for: Budget option, simple resumes
Cost: $0.50/1M input, $1.50/1M output
```

### Claude 3.5 Sonnet ⭐
```
Provider: Anthropic
Released: October 2024
Context: 200K tokens (~150 pages)

Strengths:
✓ Excellent style preservation
✓ Huge context window
✓ Great at maintaining tone
✓ Very reliable
✓ Good at following constraints

Weaknesses:
- Need separate API key
- Slightly slower than GPT-4o

Best for: Style preservation, long resumes
Cost: $3/1M input, $15/1M output
```

### Claude 3 Opus
```
Provider: Anthropic
Context: 200K tokens

Strengths:
✓ Highest quality from Anthropic
✓ Huge context window
✓ Excellent reasoning

Weaknesses:
- Most expensive option
- Slower than other models

Best for: When quality is #1 priority
Cost: $15/1M input, $75/1M output
```

---

## 🔧 How to Switch Models

### Option 1: Environment Variable (Recommended)
```bash
# Edit backend/.env
AI_MODEL=gpt-4o                          # Default
AI_MODEL=claude-3-5-sonnet-20241022      # Claude
AI_MODEL=gpt-3.5-turbo                   # Budget
```

### Option 2: Code Configuration
```python
# In backend/services/resume_optimizer.py
self.model = "gpt-4o"  # Change this line
```

---

## 💰 Cost Breakdown

### Typical Resume Optimization
```
Input: ~2000 tokens (resume + job description)
Output: ~800 tokens (enhanced resume)

GPT-4o:
- Input:  2000 * ($5/1M) = $0.010
- Output:  800 * ($15/1M) = $0.012
- Total: $0.022 (~2.2 cents)

GPT-3.5-turbo:
- Input:  2000 * ($0.50/1M) = $0.001
- Output:  800 * ($1.50/1M) = $0.001
- Total: $0.002 (~0.2 cents)

Claude 3.5 Sonnet:
- Input:  2000 * ($3/1M) = $0.006
- Output:  800 * ($15/1M) = $0.012
- Total: $0.018 (~1.8 cents)
```

### Monthly Costs (estimated)
```
Light use (10 resumes/month):
- GPT-4o: $0.22
- GPT-3.5: $0.02
- Claude: $0.18

Medium use (100 resumes/month):
- GPT-4o: $2.20
- GPT-3.5: $0.20
- Claude: $1.80

Heavy use (1000 resumes/month):
- GPT-4o: $22
- GPT-3.5: $2
- Claude: $18
```

---

## 🚀 Setting Up Multiple Providers

### OpenAI Setup
```bash
# Get API key from: https://platform.openai.com/api-keys
# Add to backend/.env:
OPENAI_API_KEY=sk-proj-...
```

### Anthropic Setup (Optional)
```bash
# Get API key from: https://console.anthropic.com/
# Add to backend/.env:
ANTHROPIC_API_KEY=sk-ant-...
```

---

## 🎯 Model Selection Strategy

### For Production (Public Service)
```
Use: GPT-4o
Why: Best user experience, reasonable cost
Fallback: GPT-3.5-turbo (if budget constrained)
```

### For Personal Use
```
Use: GPT-4o or Claude 3.5 Sonnet
Why: Best quality for your own resumes
```

### For Development/Testing
```
Use: GPT-3.5-turbo
Why: Fast and cheap for testing
```

### For Enterprise
```
Use: Claude 3.5 Sonnet
Why: Excellent quality, predictable costs
Consider: Azure OpenAI for compliance
```

---

## 📈 Performance Comparison

### Speed (lower is better)
```
GPT-3.5-turbo:  ~1-2 seconds
GPT-4o:         ~2-4 seconds
GPT-4-turbo:    ~2-4 seconds
Claude 3.5:     ~3-5 seconds
GPT-4:          ~5-8 seconds
Claude Opus:    ~5-8 seconds
```

### Quality Score (0-100)
```
GPT-4o:          95/100 ⭐
Claude 3.5:      95/100 ⭐
GPT-4:           93/100
Claude Opus:     94/100
GPT-4-turbo:     90/100
GPT-3.5-turbo:   75/100
```

### Style Preservation (0-100)
```
Claude 3.5:      97/100 ⭐
GPT-4o:          93/100
Claude Opus:     95/100
GPT-4:           90/100
GPT-4-turbo:     88/100
GPT-3.5-turbo:   70/100
```

---

## 🔍 Testing Different Models

Want to try different models? Here's how:

```bash
# Test GPT-4o (recommended)
AI_MODEL=gpt-4o python main.py

# Test Claude (style preservation)
AI_MODEL=claude-3-5-sonnet-20241022 python main.py

# Test GPT-3.5 (budget)
AI_MODEL=gpt-3.5-turbo python main.py
```

---

## 🎓 Advanced: Multi-Model Setup

For power users who want to use different models for different tasks:

```python
# In your code
from services.multi_model_optimizer import MultiModelOptimizer

optimizer = MultiModelOptimizer()

# Use GPT-4o for general optimization
result = optimizer.optimize_text(prompt, model="gpt-4o")

# Use Claude for style-sensitive content
result = optimizer.optimize_text(prompt, model="claude-3-5-sonnet-20241022")

# Use GPT-3.5 for simple tasks
result = optimizer.optimize_text(prompt, model="gpt-3.5-turbo")
```

---

## ⚠️ Important Notes

1. **API Keys Required**: You need an API key for each provider
2. **Cost Monitoring**: Track your usage in respective dashboards
3. **Rate Limits**: Each provider has different rate limits
4. **Context Windows**: Longer resumes need models with larger context
5. **Quality vs Cost**: Higher quality = higher cost (usually)

---

## 📝 Our Recommendation

**Start with GPT-4o** → It offers the best balance of:
- ✅ Latest technology (Nov 2024)
- ✅ Great quality
- ✅ Fast speed
- ✅ Reasonable cost (~$0.03/resume)
- ✅ Good style preservation

**Upgrade to Claude 3.5** if you need:
- ✅ Best style preservation
- ✅ Huge context (200K tokens)
- ✅ Slightly lower cost

**Downgrade to GPT-3.5** if you need:
- ✅ Lowest cost (~$0.01/resume)
- ✅ Maximum speed
- ✅ Simple optimizations

---

**Bottom line:** GPT-4o is the sweet spot for most users! 🎯
