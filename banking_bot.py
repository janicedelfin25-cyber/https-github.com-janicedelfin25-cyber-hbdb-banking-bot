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
    /* Main background - Purple */
    .stApp {
        background: #5a3a7a;
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
    st.markdown("<h2 style='color: white; text-align: center;'>📋 HBDB Banking Assistant</h2>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 2px solid rgba(255,255,255,0.3);'>", unsafe_allow_html=True)
    
    # Bank Information
    st.markdown("<h3 style='color: #f093fb; font-size: 18px;'>🏦 Bank Information</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; border-left: 4px solid #f093fb; font-size: 13px; color: white; line-height: 1.8;'>
    <strong>HBDB - Heritage Business Development Bank</strong><br>
    📞 <strong>24/7 Support:</strong> 1-800-HBDB-101<br>
    📧 <strong>Email:</strong> support@hbdb.com<br>
    🌐 <strong>Website:</strong> www.hbdb.com<br>
    📍 <strong>Multiple International Branches</strong>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2); margin: 15px 0;'>", unsafe_allow_html=True)
    
    # Services
    st.markdown("<h3 style='color: #f093fb; font-size: 18px;'>✨ Services Available</h3>", unsafe_allow_html=True)
    services = [
        "💳 Savings & Checking Accounts",
        "💰 Credit Cards & Rewards",
        "📱 Mobile & Online Banking",
        "💸 Money Transfers & Payments",
        "🏠 Loans & Mortgages",
        "📈 Investment & Wealth Management",
        "🎁 Premium Banking Programs",
        "💼 Business Banking Solutions"
    ]
    for service in services:
        st.markdown(f"<p style='color: #e0e0e0; font-size: 13px; margin: 8px 0;'>{service}</p>", unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2); margin: 15px 0;'>", unsafe_allow_html=True)
    
    # Account Types
    st.markdown("<h3 style='color: #f093fb; font-size: 18px;'>🎯 Account Types</h3>", unsafe_allow_html=True)
    account_types = {
        "🔵 Basic Savings": "Low minimum balance, standard rates",
        "🟢 Premium Savings": "Higher rates, competitive minimums",
        "👑 HBDB Premier": "Exclusive benefits, wealth management",
        "⭐ HBDB Advance": "Preferential rates, dedicated support",
        "💼 Business": "Tailored for entrepreneurs"
    }
    for acc_type, desc in account_types.items():
        st.markdown(f"<p style='color: #e0e0e0; font-size: 12px; margin: 8px 0;'><strong>{acc_type}</strong><br><span style='color: #b0b0b0; font-size: 11px;'>{desc}</span></p>", unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2); margin: 15px 0;'>", unsafe_allow_html=True)
    
    # Quick Info
    st.markdown("<h3 style='color: #f093fb; font-size: 18px;'>📊 Quick Info</h3>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style='background: rgba(255,255,255,0.05); padding: 12px; border-radius: 8px; font-size: 13px; color: #e0e0e0;'>
    <p>✅ <strong>FAQs Available:</strong> <span style='color: #f093fb;'>{len(faq_df)}</span></p>
    <p>🤖 <strong>AI Model:</strong> Mistral Large</p>
    <p>⚡ <strong>Response Time:</strong> Instant</p>
    <p>🔒 <strong>Security:</strong> Bank-Grade Encryption</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2); margin: 15px 0;'>", unsafe_allow_html=True)
    
    # Features
    st.markdown("<h3 style='color: #f093fb; font-size: 18px;'>🎁 Features</h3>", unsafe_allow_html=True)
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
        if st.button("❓ Contact", use_container_width=True, key="btn_contact"):
            st.info("""
            **Get help from our team:**
            📞 1-800-HBDB-101
            📧 support@hbdb.com
            💬 Chat with specialist
            """)
    
    st.markdown("<hr style='border: 1px solid rgba(255,255,255,0.2); margin: 15px 0;'>", unsafe_allow_html=True)
    
    # Actions
    if st.button("🔄 Clear Chat History", use_container_width=True, key="btn_clear"):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("<p style='color: #b0b0b0; font-size: 11px; text-align: center; margin-top: 20px;'>Version 1.0 | Powered by Mistral AI<br>HBDB Banking Assistant</p>", unsafe_allow_html=True)
