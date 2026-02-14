import streamlit as st
import pandas as pd
from mistralai import Mistral, UserMessage, SystemMessage
import os

# Initialize Mistral client
api_key = "aM92yjrlBPbRPqOYKkNFBZnjXhU6R01y"
client = Mistral(api_key=api_key)

# Custom CSS styling - Purple theme with excellent readability
custom_css = """
<style>
    /* Main background - Lighter Purple */
    .stApp {
        background: #7a5a9a;
    }
    
    /* Chat message styling */
    .stChatMessage {
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 8px;
    }
    
    /* User message - Light purple */
    .stChatMessage[data-testid="user-message"] {
        background: #7a5a9a;
        color: #ffffff;
        border-left: 4px solid #bb86fc;
    }
    
    /* Assistant message - Slightly different purple */
    .stChatMessage[data-testid="assistant-message"] {
        background: #6a4a8a;
        color: #ffffff;
        border-left: 4px solid #bb86fc;
    }
    
    /* Input area */
    .stChatInput {
        border-radius: 12px;
        border: 2px solid #bb86fc;
        background-color: #4a2a6a;
        padding: 12px;
        color: #ffffff;
    }
    
    /* Sidebar styling - Darker purple */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #4a2a6a 0%, #3a1a5a 100%);
        color: #ffffff;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #bb86fc;
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton > button {
        background: #7a5a9a;
        color: #ffffff;
        border: 1px solid #bb86fc;
        border-radius: 8px;
        font-weight: 500;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: #8a6aaa;
        box-shadow: 0 4px 8px rgba(187, 134, 252, 0.4);
        transform: translateY(-2px);
    }
    
    /* Markdown text in sidebar */
    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff;
    }
    
    /* Main text - ALL WHITE */
    body, p, span, div, label {
        color: #ffffff !important;
    }
    
    /* Markdown text in sidebar */
    [data-testid="stSidebar"] .stMarkdown {
        color: #ffffff !important;
    }
    
    /* All text elements */
    .stMarkdown {
        color: #ffffff !important;
    }
    
    .stText {
        color: #ffffff !important;
    }
    
    /* Links and hyperlinks - Make them bright yellow for visibility */
    a {
        color: #ffeb3b !important;
        text-decoration: underline;
    }
    
    a:visited {
        color: #ffeb3b !important;
    }
    
    a:hover {
        color: #fff59d !important;
    }
    
    /* Email and URL text styling */
    code {
        color: #ffeb3b !important;
        background-color: rgba(255, 235, 59, 0.1) !important;
        padding: 2px 6px;
        border-radius: 3px;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Load FAQ data
@st.cache_data
def load_faq_data():
    df = pd.read_csv("hbdb_banking_faqs (2) (1).csv")
    return df

# Create context from FAQ data with comprehensive banking details
def create_context(df):
    context = """You are a highly knowledgeable and professional HBDB Banking customer service assistant. 

HBDB BANK DETAILS:
- Bank Name: HBDB (Heritage Business Development Bank)
- Established: 2010
- Headquarters: Multiple International Branches
- Services: Full-service banking for retail and business customers
- Phone Support: 1-800-HBDB-101 (Available 24/7)
- Email: support@hbdb.com
- Website: www.hbdb.com

CORE BANKING SERVICES YOU CAN HELP WITH:
1. Savings & Checking Accounts - Opening, features, minimum balances, interest rates
2. Credit Cards - Application, benefits, rewards programs, APR information
3. Online & Mobile Banking - Access, security, password reset, features
4. Transfers & Payments - Wire transfers, direct deposits, bill pay, international transfers
5. Loans & Credit - Personal loans, home mortgages, business loans, credit inquiries
6. Investment Services - HBDB Premier, HBDB Advance programs, wealth management
7. Cards & Checks - Ordering checks, debit/credit cards, card features
8. Account Management - Minimum balance, overdraft protection, account types, eligibility

HBDB ACCOUNT TYPES:
- Basic Savings Account: Low minimum balance, standard interest rates
- Premium Savings: Higher interest rates, higher minimum balance requirement
- HBDB Premier: Exclusive benefits, wealth management, global support
- HBDB Advance: Preferential rates, dedicated support, package deals
- Business Accounts: Tailored for entrepreneurs and business owners
- Checking Accounts: Standard and premium options available

BANKING PRODUCTS:
- Mobile Banking App: Available on iOS and Android
- Online Banking: Secure portal with full account management
- Credit Cards: Multiple tiers with rewards and benefits
- Overdraft Protection: Links checking to savings/line of credit
- Direct Deposit: Easy setup with employer information
- Wire Transfer: Domestic and international options

FAQ DATABASE:"""
    
    for idx, row in df.iterrows():
        context += f"\nQ: {row['Question']}\nA: {row['Answer']}"
    
    context += "\n\nALWAYS BE HELPFUL: Provide accurate, friendly, and professional responses. If you don't know something, offer to connect the customer with a specialist."
    return context

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit UI
st.set_page_config(page_title="HBDB Banking Bot", layout="wide", initial_sidebar_state="expanded")

# Title with custom styling
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("🏦", unsafe_allow_html=True)
with col2:
    st.markdown("<h1 style='color: white; margin-top: -35px;'>HBDB Banking Assistant</h1>", unsafe_allow_html=True)

# Subtitle
st.markdown("<p style='color: #e0e0e0; font-size: 18px; text-align: center; margin-top: -10px;'>Powered by Mistral AI - Your 24/7 Banking Support</p>", unsafe_allow_html=True)

# Divider
st.markdown("---")

# Load FAQ data
faq_df = load_faq_data()
context = create_context(faq_df)

# Display chat messages with styling
if len(st.session_state.messages) == 0:
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("")
    
    with col2:
        st.markdown("## 👋 Welcome to HBDB Banking Assistant")
        st.markdown("Your personal AI-powered banking companion, available 24/7")
        
        st.markdown("### ✨ What I Can Help You With:")
        st.markdown("""
        - 💳 **Account Opening & Management**
        - 💰 **Credit Cards & Rewards Programs**
        - 📱 **Online & Mobile Banking**
        - 💸 **Transfers & Payments**
        - 🏠 **Loans & Mortgages**
        - 👑 **Premium Banking Programs**
        - 💼 **Business Banking Solutions**
        """)
        
        st.markdown("### 💡 Try Asking:")
        st.markdown("""
        - How do I open a savings account with HBDB?
        - What are the benefits of HBDB Premier?
        - How do I apply for an HBDB credit card?
        - What is HBDB's mobile banking app?
        - How do I set up direct deposit?
        - What are the interest rates on savings accounts?
        """)
        
        st.markdown("### 📞 Need Immediate Assistance?")
        st.markdown("**Call us at:** 1-800-HBDB-101 | **Email:** support@hbdb.com")

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="🧑‍💼" if message["role"] == "user" else "🤖"):
        st.markdown(f"<div style='font-size: 15px; line-height: 1.6;'>{message['content']}</div>", unsafe_allow_html=True)

# Chat input
if user_input := st.chat_input("💬 Ask me anything about HBDB banking services...", key="user_input"):
    # Add user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Prepare messages for Mistral
    system_message = SystemMessage(content=context)
    messages = [system_message]
    
    # Add conversation history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            messages.append(UserMessage(content=msg["content"]))
        else:
            from mistralai import AssistantMessage
            messages.append(AssistantMessage(content=msg["content"]))
    
    # Get response from Mistral
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Call Mistral API with streaming
        response = client.chat.stream(
            model="mistral-large-latest",
            messages=messages,
            max_tokens=1024,
            temperature=0.7
        )
        
        for chunk in response:
            if chunk.data.choices[0].delta.content:
                full_response += chunk.data.choices[0].delta.content
                message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
    
    # Add assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar info
with st.sidebar:
    st.markdown("<h2 style='color: #bb86fc; text-align: center;'>📋 HBDB Banking</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 2px solid #bb86fc;'>", unsafe_allow_html=True)
    
    # Bank Info Section
    st.markdown("<h3 style='color: #bb86fc;'>🏦 Bank Information</h3>", unsafe_allow_html=True)
    st.markdown("**HBDB - Heritage Business Development Bank**")
    st.markdown("📞 **24/7 Support:** 1-800-HBDB-101")
    st.markdown("📧 **Email:** support@hbdb.com")
    st.markdown("🌐 **Website:** www.hbdb.com")
    st.markdown("📍 **Multiple International Branches**")
    
    st.markdown("<hr style='border: 1px solid #bb86fc; margin: 15px 0;'>", unsafe_allow_html=True)
    
    # Services - Clickable Expanders with Helpful Details
    st.markdown("<h3 style='color: #bb86fc;'>✨ Services Available</h3>", unsafe_allow_html=True)
    
    services_details = {
        "💳 Savings & Checking Accounts": 
            "**PROBLEM SOLVED:** Need a safe place to save money or pay bills?\n\n"
            "**WHAT IT DOES:**\n"
            "• Secure account to deposit & withdraw money\n"
            "• Interest earned on savings\n"
            "• Debit card for easy payments\n"
            "• Online access 24/7\n\n"
            "**HOW TO GET STARTED:**\n"
            "1. Visit www.hbdb.com or call 1-800-HBDB-101\n"
            "2. Choose account type (Savings or Checking)\n"
            "3. Provide basic info & ID verification\n"
            "4. Fund your account (minimum $100-$5000)\n"
            "5. Start using immediately!\n\n"
            "**WHY CHOOSE HBDB:** Competitive rates, no hidden fees, mobile app included",
        
        "💰 Credit Cards & Rewards": 
            "**PROBLEM SOLVED:** Build credit history and earn rewards?\n\n"
            "**WHAT IT DOES:**\n"
            "• Borrow money with flexible repayment\n"
            "• Earn cashback or travel points\n"
            "• Build credit history (improves your credit score)\n"
            "• Purchase protection & fraud coverage\n"
            "• Exclusive cardholder benefits\n\n"
            "**HOW TO GET STARTED:**\n"
            "1. Check eligibility (credit score 600+)\n"
            "2. Apply online (instant decision)\n"
            "3. Receive card in 7-10 business days\n"
            "4. Activate & start earning rewards\n\n"
            "**REWARDS:** 1-2% cashback or 1 point per $1 spent",
        
        "📱 Mobile & Online Banking": 
            "**PROBLEM SOLVED:** Bank anytime, anywhere without branches?\n\n"
            "**WHAT IT DOES:**\n"
            "• Access account from phone/computer\n"
            "• Transfer money instantly\n"
            "• Pay bills automatically\n"
            "• Deposit checks via mobile camera\n"
            "• Real-time transaction notifications\n\n"
            "**SECURITY FEATURES:**\n"
            "• Biometric login (fingerprint/face)\n"
            "• Encryption & fraud monitoring\n"
            "• Password protection\n\n"
            "**HOW TO USE:** Download HBDB app → Sign in → Full account access",
        
        "💸 Money Transfers & Payments": 
            "**PROBLEM SOLVED:** Send money fast to family/businesses?\n\n"
            "**TRANSFER OPTIONS:**\n"
            "• Domestic transfers (same-day processing)\n"
            "• International wire (to 150+ countries)\n"
            "• Bill payments (auto-pay available)\n"
            "• ACH transfers (free)\n"
            "• Mobile wallet (Venmo, PayPal linked)\n\n"
            "**FEES:**\n"
            "• Domestic: $0-$15 (depends on method)\n"
            "• International: $35-$50\n"
            "• Domestic ACH: FREE\n\n"
            "**FASTEST METHOD:** Same-day domestic via online banking (1-2 hours)",
        
        "🏠 Loans & Mortgages": 
            "**PROBLEM SOLVED:** Need funds for major purchases or emergencies?\n\n"
            "**LOAN TYPES:**\n"
            "• Personal loans ($1,000-$50,000)\n"
            "• Home mortgages (5-30 year terms)\n"
            "• Business loans (for entrepreneurs)\n"
            "• Auto loans (for vehicles)\n"
            "• Lines of credit (flexible access)\n\n"
            "**APPROVAL PROCESS (3-5 days):**\n"
            "1. Pre-qualify online (soft credit check)\n"
            "2. Provide documents (pay stubs, ID)\n"
            "3. Final approval decision\n"
            "4. Funds received in account\n\n"
            "**RATES:** From 5.99% APR (depends on credit score)",
        
        "📈 Investment & Wealth Management": 
            "**PROBLEM SOLVED:** Build wealth & plan for retirement?\n\n"
            "**SERVICES:**\n"
            "• Investment portfolio management\n"
            "• Retirement planning (IRA, 401k)\n"
            "• Financial advisory (personalized)\n"
            "• Tax-efficient investments\n"
            "• Estate planning assistance\n\n"
            "**WHO SHOULD USE:** Anyone with $10,000+ to invest\n\n"
            "**HOW TO START:**\n"
            "1. Meet with advisor (free consultation)\n"
            "2. Discuss goals & risk tolerance\n"
            "3. Create custom investment strategy\n"
            "4. Begin investing with expert guidance\n\n"
            "**EXPECTED RETURNS:** 6-10% annually (varies by strategy)",
        
        "🎁 Premium Banking Programs": 
            "**PROBLEM SOLVED:** Want exclusive perks & dedicated support?\n\n"
            "**HBDB PREMIER (Premium Tier):**\n"
            "• Dedicated personal banker (24/7)\n"
            "• Concierge service\n"
            "• Waived fees on all products\n"
            "• Priority customer support\n"
            "• Exclusive event invitations\n"
            "• Travel & insurance benefits\n\n"
            "**REQUIREMENTS:**\n"
            "• Minimum balance: $50,000\n"
            "• Average monthly: $30,000+\n\n"
            "**BENEFITS:** Save $500-$2000/year in fees alone",
        
        "💼 Business Banking Solutions": 
            "**PROBLEM SOLVED:** Manage business finances easily?\n\n"
            "**FOR SMALL BUSINESS OWNERS:**\n"
            "• Business checking & savings\n"
            "• Merchant card processing\n"
            "• Payroll processing service\n"
            "• Business loans & lines of credit\n"
            "• Invoice financing\n"
            "• Business credit card\n\n"
            "**WHY IT HELPS:**\n"
            "• Separate business & personal finances (tax benefit)\n"
            "• Faster payments from customers\n"
            "• Easier payroll management\n"
            "• Build business credit\n\n"
            "**SETUP:** 5 minutes online with business license & ID"
    }
    
    for service, details in services_details.items():
        with st.expander(service):
            st.markdown(details)
    
    st.markdown("<hr style='border: 1px solid #bb86fc; margin: 15px 0;'>", unsafe_allow_html=True)
    
    # Account Types - Clickable Expanders with detailed guidance
    st.markdown("<h3 style='color: #bb86fc;'>🎯 Account Types</h3>", unsafe_allow_html=True)
    
    accounts_details = {
        "🔵 Basic Savings": 
            "**BEST FOR:** Students, beginners, or those building emergency fund\n\n"
            "**KEY FEATURES:**\n"
            "• Minimum balance: $100 only\n"
            "• Interest rate: 0.2-0.4% APY\n"
            "• No monthly fees\n"
            "• Free debit card included\n"
            "• 6 free withdrawals/month\n\n"
            "**PROS:**\n"
            "✓ Easy to open (online in 5 min)\n"
            "✓ No hidden fees\n"
            "✓ Perfect to start saving\n\n"
            "**WHEN TO UPGRADE:** When balance reaches $5,000",
        
        "🟢 Premium Savings": 
            "**BEST FOR:** Regular savers wanting higher returns\n\n"
            "**KEY FEATURES:**\n"
            "• Minimum balance: $5,000\n"
            "• Interest rate: 0.8-1.2% APY (5x better!)\n"
            "• Free checks included\n"
            "• Priority support\n"
            "• Monthly bonus interest on high balance\n\n"
            "**REAL EXAMPLE:**\n"
            "• Deposit: $10,000\n"
            "• Annual interest: ~$100-120\n"
            "• Basic account would earn: ~$20-40\n\n"
            "**COST SAVINGS:** Extra $60-80/year just from interest!",
        
        "👑 HBDB Premier": 
            "**BEST FOR:** High-income individuals, executives, business owners\n\n"
            "**EXCLUSIVE BENEFITS:**\n"
            "• Dedicated personal banker (call 24/7)\n"
            "• Concierge service\n"
            "• Premium interest rates\n"
            "• All fees waived\n"
            "• Free priority customer service\n"
            "• Exclusive travel deals & insurance\n"
            "• Free financial planning\n\n"
            "**FINANCIAL IMPACT:**\n"
            "• Save $500-2000/year in fees\n"
            "• Higher interest on savings\n"
            "• Lower rates on loans\n\n"
            "**REQUIREMENT:** Minimum $50,000 balance",
        
        "⭐ HBDB Advance": 
            "**BEST FOR:** Professionals, growing families, business managers\n\n"
            "**PREFERENTIAL RATES:**\n"
            "• Better mortgage rates (up to 0.5% lower)\n"
            "• Lower credit card APR\n"
            "• Reduced loan origination fees\n"
            "• Higher savings interest\n\n"
            "**DEDICATED SUPPORT:**\n"
            "• Assigned relationship manager\n"
            "• Free financial health check\n"
            "• Quarterly portfolio review\n\n"
            "**SAVINGS EXAMPLE:**\n"
            "• $200,000 mortgage at 0.5% lower = $1000/year savings\n"
            "• Higher savings interest = $200+/year\n\n"
            "**REQUIREMENT:** Minimum $10,000 balance",
        
        "💼 Business Account": 
            "**BEST FOR:** Entrepreneurs, freelancers, small business owners\n\n"
            "**CRITICAL BENEFITS:**\n"
            "• Separate business & personal finances (tax deduction!)\n"
            "• Faster customer payments via merchant services\n"
            "• Automatic payroll processing\n"
            "• Build business credit (essential for growth)\n"
            "• Business-only features & tools\n\n"
            "**PAYMENT OPTIONS:**\n"
            "• Accept credit/debit cards (2.5% fee)\n"
            "• ACH transfers (free)\n"
            "• Mobile payments\n\n"
            "**TAX BENEFIT:** Easily track business expenses for deductions\n\n"
            "**SETUP:** 5 minutes with business license + ID"
    }
    
    for account, details in accounts_details.items():
        with st.expander(account):
            st.markdown(details)
    
    st.markdown("<hr style='border: 1px solid #bb86fc; margin: 15px 0;'>", unsafe_allow_html=True)
    
    # Quick Info
    st.markdown("<h3 style='color: #bb86fc;'>📊 Quick Info</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.metric("FAQs", len(faq_df))
    with col2:
        st.metric("AI Model", "Mistral")
    st.markdown("⚡ **Response:** Instant")
    st.markdown("🔒 **Security:** Bank-Grade")
    
    st.markdown("<hr style='border: 1px solid #bb86fc; margin: 20px 0;'>", unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("<h3 style='color: #bb86fc;'>⚡ Quick Actions</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💡 Examples", use_container_width=True, key="btn_examples"):
            st.info("""
            **Questions you can ask:**
            - How do I open an account?
            - What are the interest rates?
            - How do I apply for a credit card?
            - What is HBDB Premier?
            """)
    with col2:
        if st.button("📞 Contact", use_container_width=True, key="btn_contact"):
            st.info("""
            **Get help from our team:**
            📞 1-800-HBDB-101
            📧 support@hbdb.com
            💬 Chat with specialist
            """)
    
    if st.button("🔄 Clear Chat", use_container_width=True, key="btn_clear"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("<p style='color: #bb86fc; font-size: 11px; text-align: center; margin-top: 20px;'>v1.0 | Mistral AI</p>", unsafe_allow_html=True)
