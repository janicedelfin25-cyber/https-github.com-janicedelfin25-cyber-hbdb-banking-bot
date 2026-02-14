# 🏦 HBDB Banking Bot - AI-Powered Customer Service Assistant

A sophisticated AI-powered banking chatbot built with Streamlit and Mistral AI that provides 24/7 customer support for HBDB (Heritage Business Development Bank) banking services.

## 📋 Features

- **AI-Powered Conversations**: Uses Mistral Large language model for intelligent responses
- **Real-time Streaming**: Stream responses from the AI model for better UX
- **Comprehensive Banking Knowledge**: Built-in knowledge of:
  - Account opening and management
  - Credit cards and rewards programs
  - Online and mobile banking
  - Money transfers and payments
  - Loans and mortgages
  - Premium banking programs (HBDB Premier, HBDB Advance)
  - Business banking solutions
  
- **Beautiful UI**: Modern gradient design with intuitive interface
- **Sidebar Information**: Quick access to:
  - Bank details and contact information
  - Available services
  - Account types
  - Quick help features
  
- **Chat History**: Maintains conversation history throughout the session
- **FAQ Database**: 50+ frequently asked questions to enhance responses

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Mistral AI API Key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/janicedelfin/hbdb-banking-bot.git
cd hbdb-banking-bot
```

2. **Create and activate virtual environment**
```bash
python -m venv .venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
Create a `.env` file in the project root:
```
MISTRAL_API_KEY=your_api_key_here
```

5. **Run the application**
```bash
streamlit run banking_bot.py
```

The app will open at `http://localhost:8501`

## 📁 Project Structure

```
hbdb-banking-bot/
├── banking_bot.py                          # Main Streamlit application
├── hbdb_banking_faqs (2) (1).csv          # FAQ database
├── requirements.txt                        # Python dependencies
├── README.md                              # This file
└── .env                                   # Environment variables (create this)
```

## 🛠️ Technologies Used

- **Streamlit**: Web application framework
- **Mistral AI**: Large language model API
- **Pandas**: Data handling and processing
- **Python 3.13**: Programming language

## 💬 How to Use

1. **Start the bot** and open the Streamlit interface
2. **Ask questions** about HBDB banking services in the chat input
3. **Get instant responses** powered by Mistral AI
4. **View conversation history** in the chat interface
5. **Use sidebar features** for quick information and assistance

### Example Questions

- "How do I open a savings account with HBDB?"
- "What are the benefits of HBDB Premier?"
- "How do I apply for an HBDB credit card?"
- "What is HBDB's mobile banking app called?"
- "How do I set up direct deposit?"
- "What is HBDB Advance?"

## 🏪 HBDB Bank Details

- **Bank Name**: Heritage Business Development Bank
- **Established**: 2010
- **Phone Support**: 1-800-HBDB-101 (24/7)
- **Email**: support@hbdb.com
- **Website**: www.hbdb.com

### Services Offered
- Savings & Checking Accounts
- Credit Cards with Rewards
- Online & Mobile Banking
- Personal & Business Loans
- Wealth Management
- Premium Banking Programs

## 📊 FAQ Database

The bot is equipped with 50+ FAQs covering:
- Account management
- Banking products
- Online services
- Customer support
- And more

## 🔐 Security & Privacy

- Secure API communication with Mistral AI
- Bank-grade encryption for data handling
- No sensitive customer data is stored
- Privacy-focused design

## 🎨 UI Features

- **Purple gradient theme** for professional banking appearance
- **Responsive design** that works on all devices
- **Real-time chat streaming** for better user experience
- **Intuitive sidebar** with comprehensive information
- **Welcome screen** with helpful examples
- **Clear visual hierarchy** for easy navigation

## 🚀 Deployment

To deploy this application:

1. **Streamlit Cloud** (Recommended)
   - Push to GitHub
   - Connect to Streamlit Cloud
   - Deploy with one click

2. **Docker**
   ```bash
   docker build -t hbdb-banking-bot .
   docker run -p 8501:8501 hbdb-banking-bot
   ```

3. **Heroku** or other cloud platforms

## 📝 Environment Setup

Create a `.env` file:
```
MISTRAL_API_KEY=your_mistral_api_key
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👤 Author

- **Janice Delfin** - Initial work

## 📞 Support

For questions or issues:
- Email: support@hbdb.com
- Phone: 1-800-HBDB-101
- GitHub Issues: Submit an issue in this repository

## 🙏 Acknowledgments

- Mistral AI for the powerful language model
- Streamlit for the amazing web framework
- HBDB for the banking domain knowledge

---

**Version**: 1.0  
**Last Updated**: February 2026  
**Status**: Active & Maintained
