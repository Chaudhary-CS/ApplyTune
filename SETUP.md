# 🎵 Setup Guide - Applytune

Quick start guide to get Applytune running locally and start fine-tuning your applications!

## Prerequisites

- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))

---

## Backend Setup (5 minutes)

### 1. Navigate to backend directory
```bash
cd backend
```

### 2. Create virtual environment
```bash
# On macOS/Linux:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate
```

### 3. Install Python packages
```bash
pip install -r requirements.txt
```

### 4. Download spaCy language model
```bash
python -m spacy download en_core_web_sm
```

### 5. Set up environment variables
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
# On macOS/Linux:
nano .env

# On Windows:
notepad .env
```

Add this line to `.env`:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 6. Run the backend server
```bash
python main.py
```

✅ Backend should now be running at `http://localhost:8000`
📖 API docs available at `http://localhost:8000/docs`

---

## Frontend Setup (3 minutes)

### 1. Open a NEW terminal and navigate to frontend
```bash
cd frontend
```

### 2. Install Node packages
```bash
npm install
```

### 3. Create environment file
```bash
# On macOS/Linux:
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# On Windows:
echo NEXT_PUBLIC_API_URL=http://localhost:8000 > .env.local
```

### 4. Run the development server
```bash
npm run dev
```

✅ Frontend should now be running at `http://localhost:3000`

---

## Testing the App

1. Open your browser and go to `http://localhost:3000`
2. Upload a sample resume (PDF or DOCX)
3. Paste a job description
4. Click "Optimize My Resume"
5. Wait 15-30 seconds for AI optimization
6. View your improved ATS score! 🎉

---

## Troubleshooting

### "ModuleNotFoundError" in Python
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### "Module not found" in Next.js
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### "No response from server"
- Make sure backend is running on port 8000
- Check if `.env.local` has correct API URL
- Try restarting both servers

### OpenAI API errors
- Check if your API key is correct in `backend/.env`
- Make sure you have credits in your OpenAI account
- Check API key permissions

---

## Production Deployment

### Backend (Railway/Render/Heroku)
1. Set environment variables in your hosting platform
2. Make sure to set `OPENAI_API_KEY`
3. Update `CORS_ORIGINS` to include your frontend URL

### Frontend (Vercel/Netlify)
1. Connect your GitHub repo
2. Set `NEXT_PUBLIC_API_URL` to your backend URL
3. Deploy!

---

## Getting OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (you won't see it again!)
5. Add $5-10 credit to your account
6. Paste key into `backend/.env`

**Cost estimate:** ~$0.02-0.05 per resume optimization with GPT-4

---

## Need Help?

- Check the [README.md](README.md) for more details
- API documentation: `http://localhost:8000/docs`
- Make sure both servers are running simultaneously

**Happy tuning!** 🎵🎯
