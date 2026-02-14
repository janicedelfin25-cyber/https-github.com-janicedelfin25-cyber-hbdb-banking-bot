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
    
    # Services - Clickable Expanders
    st.markdown("<h3 style='color: #bb86fc;'>✨ Services Available</h3>", unsafe_allow_html=True)
    
    services_details = {
        "💳 Savings & Checking Accounts": "Open new accounts online or at branch. Multiple account types with competitive rates. Minimum balance requirements vary by account type. Free online banking included.",
        "💰 Credit Cards & Rewards": "Multiple card tiers with cashback, travel points, and rewards. Apply online instantly. Flexible credit limits. Exclusive cardholder benefits and discounts.",
        "📱 Mobile & Online Banking": "24/7 secure access via mobile app and web portal. Real-time account monitoring. Mobile deposits and transfers. Biometric security available.",
        "💸 Money Transfers & Payments": "Domestic and international wire transfers. Bill pay services. ACH transfers. Same-day processing available. Competitive transfer rates.",
        "🏠 Loans & Mortgages": "Personal loans with flexible terms. Home mortgages with competitive rates. Business loans for entrepreneurs. Pre-qualification available online.",
        "📈 Investment & Wealth Management": "Investment portfolio management. Retirement planning services. Financial advisory services. Tax-efficient investment strategies.",
        "🎁 Premium Banking Programs": "HBDB Premier with exclusive benefits. Wealth management and global support. Priority customer service. Exclusive event access.",
        "💼 Business Banking Solutions": "Business checking and savings. Merchant services. Payroll processing. Business loans and lines of credit."
    }
    
    for service, details in services_details.items():
        with st.expander(service):
            st.markdown(details)
    
    st.markdown("<hr style='border: 1px solid #bb86fc; margin: 15px 0;'>", unsafe_allow_html=True)
    
    # Account Types - Clickable Expanders
    st.markdown("<h3 style='color: #bb86fc;'>🎯 Account Types</h3>", unsafe_allow_html=True)
    
    accounts_details = {
        "🔵 Basic Savings": 
            "**Features:**\n"
            "• Low minimum balance ($100)\n"
            "• Standard interest rates\n"
            "• Free debit card\n"
            "• Online banking access\n"
            "• Perfect for beginners",
        
        "🟢 Premium Savings": 
            "**Features:**\n"
            "• Higher interest rates (0.8-1.2% APY)\n"
            "• Minimum balance $5,000\n"
            "• Priority customer service\n"
            "• Free checks\n"
            "• Monthly rewards",
        
        "👑 HBDB Premier": 
            "**Features:**\n"
            "• Exclusive member benefits\n"
            "• Premium wealth management\n"
            "• Global travel support\n"
            "• Dedicated personal banker\n"
            "• Minimum balance $50,000",
        
        "⭐ HBDB Advance": 
            "**Features:**\n"
            "• Preferential rates on loans\n"
            "• Dedicated support team\n"
            "• Package deals available\n"
            "• Investment advisory included\n"
            "• Minimum balance $10,000",
        
        "💼 Business Account": 
            "**Features:**\n"
            "• Business checking & savings\n"
            "• Merchant services\n"
            "• Payroll processing\n"
            "• Business loans available\n"
            "• Scalable solutions"
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
