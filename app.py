"""
Monday.com Business Intelligence Agent
Main Streamlit Application
"""

import streamlit as st
from agent import process_query
from config import DEALS_BOARD_ID, WORK_ORDERS_BOARD_ID

# Page config
st.set_page_config(
    page_title="Monday.com BI Agent",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Monday.com Business Intelligence Agent")
st.markdown("Ask questions about your deals and work orders. The agent queries Monday.com in real-time.")

# Sidebar with info
with st.sidebar:
    st.header("📋 About")
    st.write("This agent connects to your Monday.com boards and answers business questions.")
    
    st.subheader("Connected Boards:")
    st.code(f"Deals: {DEALS_BOARD_ID}")
    st.code(f"Work Orders: {WORK_ORDERS_BOARD_ID}")
    
    st.subheader("Example Questions:")
    st.markdown("""
    - How many deals do we have?
    - What's our total revenue?
    - Show me renewables deals
    - What's our win rate?
    - How are projects being executed?
    - Show me top 5 deals by value
    - What's the mining sector pipeline?
    """)
    
    st.markdown("---")
    st.caption("Built with OpenAI & Monday.com API")

# Main input area
st.markdown("### Ask a Question")

user_question = st.text_input(
    "Your question:",
    placeholder="e.g., How many renewables deals do we have?",
    label_visibility="collapsed"
)

# Process query when user submits
if user_question:
    with st.spinner("🤔 Processing your question..."):
        # Get answer and action log
        answer, action_log = process_query(user_question)
    
    # Display results in two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💡 Answer")
        st.markdown(answer)
    
    with col2:
        st.markdown("### 🔍 Action Log")
        with st.expander("See what the agent did", expanded=True):
            for action in action_log:
                st.text(action)

# Footer
st.markdown("---")
st.caption("💡 Tip: The agent queries Monday.com live for each question - no cached data!")