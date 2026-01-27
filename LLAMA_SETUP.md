# 🦙 FREE Llama Setup Guide

**Make Applytune 100% FREE** using Meta's open-source Llama 3.1 models!

---

## 🎯 Why Use Llama?

✅ **100% FREE** - No API costs ever  
✅ **No usage limits** - Optimize unlimited resumes  
✅ **Complete privacy** - Runs on your machine  
✅ **No tracking** - Your data never leaves your computer  
✅ **Quality comparable to GPT-4** - Llama 3.1 70B is excellent  
✅ **Open source** - Full control  

---

## 🚀 Three Ways to Use FREE Llama

### **Option 1: Ollama (RECOMMENDED)** ⭐
**Best for:** Local use, maximum privacy, no costs

**Setup (5 minutes):**
```bash
# 1. Install Ollama
# Mac:
brew install ollama

# Or download from: https://ollama.ai

# 2. Pull Llama 3.1 model
ollama pull llama3.1:70b

# 3. Start Ollama (it auto-starts, but you can also run):
ollama serve

# 4. Configure Applytune
cd backend
echo "AI_PROVIDER=llama" >> .env
echo "LLAMA_PROVIDER=ollama" >> .env

# Done! 🎉
```

**Benefits:**
- ✅ 100% FREE forever
- ✅ No API keys needed
- ✅ Complete privacy
- ✅ No internet required (after download)
- ✅ Unlimited usage

**Model Options:**
```bash
# Fastest (8B - good for testing)
ollama pull llama3.1:8b

# Balanced (8B instruct - recommended for most)
ollama pull llama3.1:8b-instruct

# Best quality (70B - GPT-4 level, needs 40GB RAM)
ollama pull llama3.1:70b

# Ultra quality (405B - best but needs 256GB RAM!)
ollama pull llama3.1:405b
```

---

### **Option 2: Groq (Cloud, FREE Tier)** ⚡
**Best for:** Fastest inference, no local setup

**Setup (2 minutes):**
```bash
# 1. Get free API key from: https://console.groq.com
#    (No credit card required!)

# 2. Configure Applytune
cd backend
echo "AI_PROVIDER=llama" >> .env
echo "LLAMA_PROVIDER=groq" >> .env
echo "GROQ_API_KEY=gsk_your_key_here" >> .env

# Done! 🎉
```

**Benefits:**
- ✅ FREE tier (rate limited but generous)
- ✅ Extremely fast (fastest Llama inference)
- ✅ No local setup needed
- ✅ No hardware requirements

**Limits:**
- Free tier: 30 requests/minute
- More than enough for personal use!

---

### **Option 3: Together AI (Cloud, FREE Credits)** 💰
**Best for:** Production use, reliable

**Setup (2 minutes):**
```bash
# 1. Get free $25 credit from: https://api.together.xyz
#    (No credit card required!)

# 2. Configure Applytune
cd backend
echo "AI_PROVIDER=llama" >> .env
echo "LLAMA_PROVIDER=together" >> .env
echo "TOGETHER_API_KEY=your_key_here" >> .env

# Done! 🎉
```

**Benefits:**
- ✅ $25 free credit (~25,000 resumes!)
- ✅ Reliable cloud service
- ✅ Good performance
- ✅ After credits: ~$0.001/resume (very cheap)

---

## 📊 Model Comparison

| Model | Quality | Speed | RAM Needed | Cost |
|-------|---------|-------|------------|------|
| **Llama 3.1 8B** | ⭐⭐⭐ | ⚡⚡⚡⚡ | 8GB | FREE |
| **Llama 3.1 70B** ⭐ | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | 40GB | FREE |
| Llama 3.1 405B | ⭐⭐⭐⭐⭐ | ⚡⚡ | 256GB | FREE |
| GPT-4o | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | N/A | $0.03 |

**Recommendation:** Llama 3.1 70B via Ollama = GPT-4 quality for FREE! 🎯

---

## 🎯 Complete Setup Example

### **For Local Use (Ollama):**
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull model (choose one)
ollama pull llama3.1:70b    # Best quality (40GB RAM needed)
ollama pull llama3.1:8b     # Faster, less RAM (8GB needed)

# Start Ollama (auto-starts on install)
ollama serve

# Configure Applytune backend/.env
AI_PROVIDER=llama
LLAMA_PROVIDER=ollama
OLLAMA_MODEL=llama3.1:70b

# Restart backend
cd backend
source venv/bin/activate
python main.py
```

### **For Cloud Use (Groq - Fastest):**
```bash
# Get free key: https://console.groq.com

# Configure Applytune backend/.env
AI_PROVIDER=llama
LLAMA_PROVIDER=groq
GROQ_API_KEY=gsk_your_key_here

# Restart backend
cd backend
source venv/bin/activate
python main.py
```

---

## ⚙️ Configuration Options

Edit `backend/.env`:

```bash
# Choose AI provider (openai or llama)
AI_PROVIDER=llama

# If using Llama, choose provider:
LLAMA_PROVIDER=ollama        # Local, free, private
# LLAMA_PROVIDER=groq        # Cloud, free tier, fast
# LLAMA_PROVIDER=together    # Cloud, free credits

# Ollama settings (if using ollama)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:70b

# Groq settings (if using groq)
GROQ_API_KEY=gsk_your_key_here

# Together settings (if using together)
TOGETHER_API_KEY=your_key_here
```

---

## 🔍 Testing Your Setup

```bash
# Test Ollama
curl http://localhost:11434/api/tags

# Should return list of models

# Test with Applytune
cd backend
source venv/bin/activate
python -c "from services.llama_optimizer import LlamaOptimizer; \
           opt = LlamaOptimizer(); \
           print(opt.optimize_text('Test prompt', 'You are helpful'))"
```

---

## 💻 System Requirements

### **For Ollama (Local):**

| Model | RAM Needed | Speed | Quality |
|-------|------------|-------|---------|
| llama3.1:8b | 8GB | Fast | Good |
| llama3.1:8b-instruct | 8GB | Fast | Better |
| llama3.1:70b | 40GB | Medium | Excellent |
| llama3.1:405b | 256GB | Slow | Best |

**Recommended:** 
- Mac M1/M2/M3 with 16GB+ RAM → Use llama3.1:70b
- Regular laptops with 8-16GB → Use llama3.1:8b
- Servers with 64GB+ → Use llama3.1:70b or 405b

### **For Groq/Together (Cloud):**
- Any computer with internet
- No special hardware needed!

---

## 🎨 Quality Comparison

### Resume Optimization Test:

**Original Bullet:**
```
- Worked on backend APIs
```

**GPT-4o Output:**
```
- Developed RESTful backend APIs using Node.js and Express, 
  improving system performance by 30%
```

**Llama 3.1 70B Output:**
```
- Developed scalable RESTful backend APIs using Node.js and Express,
  enhancing system performance and reliability by 30%
```

**Result:** Llama 3.1 70B is comparable to GPT-4o! 🎯

---

## 💰 Cost Comparison (100 resumes/month)

| Provider | Cost | Notes |
|----------|------|-------|
| **Ollama** | **$0.00** ⭐ | 100% free forever |
| **Groq** | **$0.00** ⭐ | Free tier (rate limited) |
| **Together** | **$0.10** | After free credits |
| GPT-4o | $2.20 | Ongoing cost |
| GPT-3.5 | $0.20 | Cheaper but lower quality |

---

## 🚨 Troubleshooting

### **Ollama not found**
```bash
# Mac
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Download from: https://ollama.ai/download
```

### **Model not downloaded**
```bash
# Download the model
ollama pull llama3.1:70b

# Check available models
ollama list
```

### **Ollama not running**
```bash
# Start Ollama
ollama serve

# Or restart
brew services restart ollama  # Mac
systemctl restart ollama      # Linux
```

### **Out of memory**
```bash
# Use smaller model
ollama pull llama3.1:8b

# Or use cloud providers (Groq/Together)
```

### **Slow inference**
```bash
# Options:
1. Use smaller model (8B instead of 70B)
2. Use Groq (cloud, very fast)
3. Upgrade RAM
```

---

## 🎯 Best Practices

### **For Development:**
```bash
Use: llama3.1:8b via Ollama
Why: Fast, uses less RAM
```

### **For Production:**
```bash
Use: llama3.1:70b via Ollama
Why: Best quality, free, private
Alternative: Groq for speed
```

### **For Personal Use:**
```bash
Use: llama3.1:70b via Ollama
Why: Best quality, no costs
```

### **For Public Service:**
```bash
Use: Groq free tier or Together
Why: No hardware requirements
Can handle more users
```

---

## 🔄 Switching Between Providers

Easy! Just change one line in `.env`:

```bash
# Use OpenAI (paid)
AI_PROVIDER=openai

# Use Llama (free)
AI_PROVIDER=llama

# Change Llama provider
LLAMA_PROVIDER=ollama   # Local
LLAMA_PROVIDER=groq     # Cloud, free
LLAMA_PROVIDER=together # Cloud, cheap
```

Restart backend - done! 🎉

---

## 📊 Feature Matrix

| Feature | Ollama | Groq | Together | OpenAI |
|---------|--------|------|----------|--------|
| **Cost** | FREE | FREE | $25 free | Paid |
| **Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Speed** | Medium | Very Fast | Fast | Fast |
| **Privacy** | 100% | Cloud | Cloud | Cloud |
| **Setup** | 5 min | 2 min | 2 min | 2 min |
| **Limits** | None | 30/min | $25 credit | Pay per use |

---

## 🎉 Summary

**Want 100% FREE with best privacy?** → **Ollama** ⭐  
**Want fastest cloud option?** → **Groq** ⚡  
**Want production-ready cloud?** → **Together** 💰  

**All three are FREE to start and give GPT-4 level quality!** 🚀

---

## 📚 Additional Resources

- Ollama: https://ollama.ai
- Groq Console: https://console.groq.com
- Together AI: https://api.together.xyz
- Llama 3.1 Info: https://ai.meta.com/llama

---

**Make Applytune completely FREE with Llama!** 🦙✨
