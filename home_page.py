import streamlit as st

def introduction_page():
    st.markdown(
        """
        <h1 style="text-align: center;">
            Welcome to Retire<span style="color: #538786;">Wise</span>
        </h1>
        """,
        unsafe_allow_html=True
    )
    st.header("Your Personalized Path to a Secure Future")

    st.markdown(
        """
        <span style="color: #538786; font-weight: bold;">
        RetireWise</span> is here to empower you with personalized, AI-driven investment plans tailored to your retirement goals, financial situation, and ethical values. Our mission is to make retirement planning accessible, transparent, and effective for everyone. 

        <h2>Why Choose Retire<span style="color: #538786;">Wise</span>?</h2>
        <ul>
            <li><span style="color: #538786; font-weight: bold;">AI-Driven Personalization:</span> Our advanced AI technology delivers highly personalized investment recommendations based on your unique profile.</li>
            <li><span style="color: #538786; font-weight: bold;">Ethical Investment Options:</span> Align your investments with your ethical values through our carefully curated options.</li>
            <li><span style="color: #538786; font-weight: bold;">Continuous Portfolio Optimization:</span> Stay on track with real-time updates and continuous portfolio adjustments.</li>
            <li><span style="color: #538786; font-weight: bold;">Comprehensive Financial Planning Tools:</span> Access a wide range of tools for scenario analysis, performance monitoring, and more.</li>
        </ul>

        <h2>How It Works:</h2>
        <ol>
            <li><span style="color: #538786; font-weight: bold;">Create Your Profile:</span> Share your financial details, retirement goals, and ethical preferences.</li>
            <li><span style="color: #538786; font-weight: bold;">Get Personalized Recommendations:</span> Our AI generates a detailed, diversified investment plan tailored to your needs.</li>
            <li><span style="color: #538786; font-weight: bold;">Implement and Monitor:</span> Use our platform to implement your portfolio with your existing brokerage accounts, and monitor your progress with real-time updates and insights.</li>
        </ol>

        <h2>Ready to Start?</h2>
        Create your personalized retirement plan today and take the first step towards a secure and prosperous future.
        """,
        unsafe_allow_html=True
    )

    st.markdown("<span style='color: #538786; font-weight: bold;'>To create your portfolio, please click on 🛠️ Portfolio Creation in the sidebar.</span>", unsafe_allow_html=True)
