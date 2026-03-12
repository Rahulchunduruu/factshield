import streamlit as st
from crew import run_factcheck

st.header('🔍 FactMind')
st.subheader('AI-Powered Fact Checker')

claim = st.text_input("Enter a claim to fact-check:", placeholder="e.g., The moon landing was fake")

if st.button("🔍 Analyze Claim", type="primary"):
    if claim:
        with st.spinner("🤖 Analyzing claim..."):
            result = run_factcheck(claim, "text")
        
        # Display results with better formatting
        verdict = result.get('verdict', 'Unknown')
        
        # Color-coded verdict with confidence
        if verdict.lower() == 'genuine':
            st.success(f"✅ **Verdict: {verdict}**")
        elif verdict.lower() == 'fake':
            st.error(f"❌ **Verdict: {verdict}**")
        else:
            st.warning(f"⚠️ **Verdict: {verdict}**")
        
        # Show confidence score if available
        if result.get('confidence_score') != 'N/A':
            st.metric("Confidence Score", result['confidence_score'])
        
        # Claims analyzed
        if result.get('claims_analyzed') != 'N/A':
            st.subheader("🎯 Claims Analyzed")
            st.info(result['claims_analyzed'])
        
        # Explanation
        st.subheader("📝 Analysis")
        st.write(result.get('explanation', 'No explanation provided'))
       

        #source
        if 'sources' in result and result['sources'] and result['sources'] != 'N/A':
            st.subheader("🔗 Sources")
            if isinstance(result['sources'], list):
                for i, source in enumerate(result['sources'], 1):
                    with st.container():
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            st.markdown(f"**{i}.** {source}")
                        with col2:
                            if source.startswith('http'):
                                st.link_button("🔗", source, help=f"Visit Source {i}")
                        st.divider()
            else:
                with st.container():
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"**1.** {result['sources']}")
                    with col2:
                        if str(result['sources']).startswith('http'):
                            st.link_button("🔗", result['sources'], help="Visit Source")
        
    else:
        st.warning("Please enter a claim first!")
