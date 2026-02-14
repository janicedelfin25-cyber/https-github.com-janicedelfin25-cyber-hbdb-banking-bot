# 🚀 GitHub Setup Guide - HBDB Banking Bot

## Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Enter repository name: `hbdb-banking-bot`
3. Description: "AI-Powered Banking Chatbot with Mistral AI and Streamlit"
4. Choose **Public** or **Private**
5. Click **Create Repository**

## Step 2: Push to GitHub

After creating the repository, run these commands:

```bash
cd "C:\Users\delfi\Banking Project"

# Add the remote repository
git remote add origin https://github.com/YOUR_USERNAME/hbdb-banking-bot.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username**

## Step 3: Update Files

Before pushing, update these files with your information:

### In `README.md`:
- Replace GitHub link with your repository URL
- Update author information if needed

### Create `.env` file (DON'T commit this):
```
MISTRAL_API_KEY=your_api_key_here
```

This file is in `.gitignore` and won't be pushed to GitHub.

## Step 4: Verify on GitHub

1. Visit your repository: `https://github.com/YOUR_USERNAME/hbdb-banking-bot`
2. Check that all files are there:
   - ✅ banking_bot.py
   - ✅ README.md
   - ✅ requirements.txt
   - ✅ .gitignore
   - ✅ hbdb_banking_faqs (2) (1).csv

## Step 5: Deploy to Streamlit Cloud (Optional)

1. Go to https://share.streamlit.io
2. Click "New app"
3. Connect your GitHub repository
4. Select the repository and banking_bot.py as the main file
5. Add secrets (MISTRAL_API_KEY) in Advanced Settings
6. Deploy!

## 📝 Useful Git Commands

```bash
# Check status
git status

# View commit history
git log --oneline

# Make changes and commit
git add .
git commit -m "Your commit message"
git push origin main

# View remote
git remote -v
```

## 🔐 Managing Sensitive Data

**Never commit API keys!** Use `.env` file:

1. Create `.env` file locally
2. Add to `.gitignore` (already done)
3. Use environment variables in your code

## 📞 Support

- GitHub Issues: For bug reports and feature requests
- Email: janicedelfin25@gmail.com

---

**Your repository is now ready to be shared with the world! 🌍**
