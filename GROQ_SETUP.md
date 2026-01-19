# ⚡ Groq Setup - 2 Minutes to FREE Resume Optimization

**Fastest way to get Applytune running!**

---

## 🎯 What You're Getting

```
Speed:       1-2 seconds per resume ⚡
Cost:        $0 forever
Quality:     95/100 (GPT-4 level)
Limits:      30 resumes/minute (plenty!)
Setup time:  2 minutes
Download:    0GB
```

---

## 🚀 Setup Steps

### **Step 1: Get FREE Groq API Key** (1 minute)

1. **Visit:** https://console.groq.com

2. **Sign Up:**
   - Click "Sign Up" (top right)
   - Use Google/GitHub or email
   - No credit card needed! ✅

3. **Create API Key:**
   - After login, click "API Keys" (left sidebar)
   - Click "Create API Key"
   - Give it a name: "Applytune"
   - Click "Create"

4. **Copy Key:**
   - Your key starts with `gsk_...`
   - Click "Copy" 📋
   - **Save it somewhere!** (You won't see it again)

---

### **Step 2: Add Key to Applytune** (30 seconds)

```bash
# 1. Open the config file
cd /Users/kartikchaudhary/Desktop/new\ folder/backend
nano .env

# 2. Find this line:
GROQ_API_KEY=

# 3. Paste your key after the =
GROQ_API_KEY=gsk_your_actual_key_here

# 4. Save and exit
# Press: Ctrl+X, then Y, then Enter
```

---

### **Step 3: Test It!** (30 seconds)

```bash
# Start backend
cd backend
source venv/bin/activate
python main.py

# You should see:
# 💰 COST: $0.00 FOREVER
# 🦙 Using 100% FREE Llama models
# 🦙 Llama provider: groq
# ✓ Groq API key found (FREE tier)
# Ready to optimize resumes! 🚀
```

---

### **Step 4: Open Frontend** (in new terminal)

```bash
cd frontend
npm run dev

# Visit: http://localhost:3000
```

---

## ✅ You're Done!

**That's it!** Upload a resume and watch Groq optimize it in **1-2 seconds**! ⚡

---

## 📊 What You Get with Groq Free Tier

```
Requests per minute:  30
Requests per day:     ~40,000 (more than enough!)
Requests per month:   ~1,200,000
Cost:                 $0

Model:                Llama 3.1 70B
Quality:              Same as GPT-4
Speed:                1-2 seconds (fastest!)
```

---

## 🎯 Testing Your Setup

### **Quick Test:**

```bash
# In backend directory
python -c "
from services.llama_optimizer import LlamaOptimizer
opt = LlamaOptimizer()
print('✓ Groq working!' if opt.is_available() else '✗ Not working')
"
```

Should print: `✓ Groq working!`

---

## 🚨 Troubleshooting

### **Error: "No Groq API key"**

**Solution:**
```bash
# Check your .env file
cat backend/.env | grep GROQ

# Should show:
# GROQ_API_KEY=gsk_...

# If empty, add your key:
nano backend/.env
# Paste key, save
```

---

### **Error: "Invalid API key"**

**Solution:**
1. Check key is correct (starts with `gsk_`)
2. No extra spaces before/after key
3. No quotes around key
4. Key should look like: `GROQ_API_KEY=gsk_abc123...`

---

### **Error: "Rate limit exceeded"**

**Solution:**
- You hit 30 requests/minute limit
- Wait 1 minute and try again
- Or install Ollama for unlimited (see `OLLAMA_VS_GROQ.md`)

---

## 💡 Pro Tips

### **1. Check Your Usage**
Visit https://console.groq.com to see:
- How many requests you've made
- Your rate limits
- API key status

### **2. Keep Your Key Safe**
- Don't share your API key
- Don't commit `.env` to git (it's in `.gitignore`)
- If leaked, regenerate at console.groq.com

### **3. Speed Tips**
Groq is already fastest! But you can:
- Use smaller resumes (under 2 pages)
- Keep job descriptions concise
- Avoid uploading during peak hours

### **4. Switch to Ollama Later**
Want 100% privacy and unlimited usage?
```bash
brew install ollama
ollama pull llama3.1:70b

# Edit .env:
LLAMA_PROVIDER=auto

# Will use Ollama if available, Groq as fallback!
```

---

## 📊 Speed Comparison

| Model | Time per Resume |
|-------|-----------------|
| **Groq (Llama 70B)** | **1-2s** ⚡⚡⚡⚡⚡ |
| Ollama (Llama 70B) | 5-10s ⚡⚡⚡ |
| GPT-4o | 3-8s ⚡⚡⚡⚡ |
| Claude 3.5 | 3-8s ⚡⚡⚡⚡ |

**Groq is the FASTEST!** 🚀

---

## 🎯 What Happens Behind the Scenes

```
You upload resume
     ↓
Applytune parses it
     ↓
Sends to Groq API (over internet)
     ↓
Groq runs Llama 3.1 70B on their LPUs
     ↓
Returns optimized resume (1-2 seconds!)
     ↓
Applytune generates PDF
     ↓
You download! 🎉
```

**LPUs** = Language Processing Units (Groq's custom chips, optimized for AI)

---

## 🆚 Why Groq is So Fast

Normal GPUs: 10-30 seconds for Llama 70B
Groq LPUs: **1-2 seconds** for same model!

**Secret sauce:**
- Custom hardware (LPUs)
- Optimized for Llama
- Industrial-scale infrastructure
- Smart batching

**Result:** 5-10x faster than normal! ⚡

---

## 💰 Cost Breakdown

### **Free Tier (What You Have)**
```
Cost:               $0/month
Requests/minute:    30
Requests/day:       ~40,000
Perfect for:        Personal use, testing, small projects
```

### **If You Need More (Optional)**
Groq also has paid tiers with higher limits. But for resume optimization, **free tier is more than enough**!

---

## 🎉 Success Checklist

✅ Visited https://console.groq.com  
✅ Created free account  
✅ Generated API key (starts with `gsk_`)  
✅ Added key to `backend/.env`  
✅ Started backend (saw "✓ Groq API key found")  
✅ Started frontend  
✅ Opened http://localhost:3000  
✅ Uploaded resume  
✅ Got optimized resume in 1-2 seconds! 🚀  

---

## 📚 Next Steps

**You're all set!** But if you want:

- **More privacy:** Install Ollama (see `OLLAMA_VS_GROQ.md`)
- **Understand costs:** Read `COST_COMPARISON.md`
- **Advanced features:** Check `AI_MODELS.md`
- **See all options:** Read `FREE_SETUP.md`

---

## 🤝 Need Help?

**Groq Issues:**
- Groq Status: https://status.groq.com
- Groq Docs: https://console.groq.com/docs
- Groq Discord: https://discord.gg/groq

**Applytune Issues:**
- Check other `.md` guides in project
- Make sure Python & Node are installed
- Restart backend after `.env` changes

---

## 🎯 Bottom Line

**Groq = Fastest FREE AI for resume optimization!**

```
Setup:    2 minutes ✅
Cost:     $0 forever ✅
Speed:    1-2 seconds ✅
Quality:  GPT-4 level ✅
Limits:   30/min (plenty!) ✅
```

**Now go optimize some resumes and land those interviews!** 🎯✨
