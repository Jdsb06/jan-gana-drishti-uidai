"""
Jan-Gana-Drishti: Predictive Governance Dashboard
Government of India - UIDAI Hackathon 2026

A Streamlit-based analytics platform for Aadhaar data analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from modules.etl_pipeline import load_and_clean_data
from modules.fraud_detection import GhostHunterEngine
from modules.migration_tracker import MigrationPulseTracker
from modules.child_welfare import ChildWelfareAnalyzer
from modules.policy_impact import PolicyImpactEngine
from modules.forecasting import PredictiveForecastingEngine
from modules.benchmarking import BenchmarkingEngine

# Page configuration
st.set_page_config(
    page_title="Jan-Gana-Drishti | UIDAI Analytics",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Government styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #FF9933 0%, #FFFFFF 50%, #138808 100%);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
    }
    .main-title {
        color: #000080;
        font-size: 42px;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .subtitle {
        color: #2C3E50;
        font-size: 18px;
        font-style: italic;
    }
    .metric-card {
        background-color: #F8F9FA;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #138808;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        color: #000000 !important;
    }
    .alert-critical {
        background-color: #FFF3CD;
        padding: 15px;
        border-left: 5px solid #DC3545;
        border-radius: 5px;
        margin: 10px 0;
        color: #000000 !important;
    }
    .alert-critical h4 {
        color: #DC3545 !important;
        margin-top: 0;
    }
    .alert-critical p {
        color: #000000 !important;
        margin: 8px 0;
    }
    .info-box {
        background-color: #E7F3FF;
        padding: 15px;
        border-left: 5px solid #0066CC;
        border-radius: 5px;
        margin: 10px 0;
        color: #000000 !important;
    }
    .info-box h4 {
        color: #0066CC !important;
        margin-top: 0;
    }
    .info-box p, .info-box ul, .info-box li {
        color: #000000 !important;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    /* Fix metric card text visibility */
    [data-testid="stMetricValue"] {
        color: #1f77b4 !important;
        font-size: 2rem !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #31333F !important;
        font-size: 1rem !important;
    }
    [data-testid="stMetricDelta"] {
        color: #808495 !important;
    }
    /* Ensure all text in main content is visible */
    .stMarkdown, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, 
    .stMarkdown h3, .stMarkdown h4 {
        color: inherit !important;
    }
    /* Fix warning text */
    .stAlert {
        background-color: #FFF3CD !important;
        color: #000000 !important;
    }
    .stAlert p, .stAlert div, .stAlert span {
        color: #000000 !important;
    }
    /* Fix warning box styling */
    [data-testid="stAlert"] {
        background-color: #FFF3CD !important;
        color: #000000 !important;
    }
    [data-testid="stAlert"] p, [data-testid="stAlert"] div {
        color: #000000 !important;
    }
    /* Fix sidebar expander content visibility */
    .sidebar .stMarkdown {
        color: #FAFAFA !important;
    }
    .sidebar .stMarkdown p, .sidebar .stMarkdown div, .sidebar .stMarkdown span {
        color: #FAFAFA !important;
    }
    section[data-testid="stSidebar"] .stMarkdown {
        color: #FAFAFA !important;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown div,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stMarkdown strong,
    section[data-testid="stSidebar"] .stMarkdown span {
        color: #FAFAFA !important;
    }
    section[data-testid="stSidebar"] [data-testid="stExpander"] .stMarkdown {
        color: #FAFAFA !important;
    }
    /* Ensure main content expanders are visible */
    .main .stExpander .stMarkdown {
        color: #000000 !important;
    }
    .main .stExpander .stMarkdown p,
    .main .stExpander .stMarkdown li,
    .main .stExpander .stMarkdown strong {
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_data():
    """Load and process all data with caching"""
    with st.spinner("🔄 Loading Aadhaar datasets... Please wait (this may take 1-2 minutes)"):
        merged_data, pipeline = load_and_clean_data()
    return merged_data, pipeline


@st.cache_data(show_spinner=False)
def run_fraud_detection(_data):
    """Run fraud detection analysis"""
    with st.spinner("🕵️ Running fraud detection algorithms..."):
        fraud_engine = GhostHunterEngine(_data)
        results = fraud_engine.run_full_analysis()
    return results


@st.cache_data(show_spinner=False)
def run_migration_analysis(_data):
    """Run migration analysis"""
    with st.spinner("🌍 Analyzing migration patterns..."):
        migration_tracker = MigrationPulseTracker(_data)
        results = migration_tracker.run_full_analysis()
    return results


@st.cache_data(show_spinner=False)
def run_child_welfare_analysis(_data):
    """Run child welfare analysis"""
    with st.spinner("👶 Analyzing child welfare patterns..."):
        child_analyzer = ChildWelfareAnalyzer(_data)
        results = child_analyzer.run_full_analysis()
    return results


@st.cache_data(show_spinner=False)
def run_policy_impact_analysis(_data, _fraud_results, _migration_results, _welfare_results):
    """Run policy impact prediction analysis"""
    with st.spinner("🎯 Simulating policy interventions..."):
        policy_engine = PolicyImpactEngine(_data, _fraud_results, _migration_results, _welfare_results)
        results = policy_engine.run_full_analysis()
    return results


@st.cache_data(show_spinner=False)
def run_forecasting_analysis(_data):
    """Run predictive forecasting analysis"""
    with st.spinner("📈 Generating forecasts and trend analysis..."):
        forecasting_engine = PredictiveForecastingEngine(_data)
        results = forecasting_engine.run_full_analysis()
    return results


@st.cache_data(show_spinner=False)
def run_benchmarking_analysis(_data, _fraud_results, _migration_results, _welfare_results):
    """Run comparative benchmarking analysis"""
    with st.spinner("🏆 Generating performance benchmarks..."):
        benchmarking_engine = BenchmarkingEngine(_data, _fraud_results, _migration_results, _welfare_results)
        results = benchmarking_engine.run_full_analysis()
    return results


def render_header():
    """Render the main header"""
    st.markdown("""
    <div class="main-header">
        <div class="main-title">🇮🇳 Jan-Gana-Drishti</div>
        <div class="subtitle">People-Data-Vision | Predictive Governance Dashboard</div>
        <div style="color: #555; margin-top: 10px;">Government of India · UIDAI Analytics · March-December 2025</div>
    </div>
    """, unsafe_allow_html=True)


def render_help_guide():
    """Render Help & User Guide page for government employees"""
    st.header("📚 Help & User Guide")
    st.markdown("### Welcome to Jan-Gana-Drishti Dashboard!")
    st.markdown("This guide will help you understand and use all features effectively.")
    st.markdown("---")
    
    # Quick Start Section
    st.subheader("🚀 Quick Start Guide")
    st.markdown("""
    <div class="info-box">
        <h4>👋 Getting Started in 3 Easy Steps:</h4>
        <ol>
            <li><strong>Select a Module</strong> from the left sidebar navigation menu</li>
            <li><strong>View the Dashboard</strong> - Charts and metrics will load automatically</li>
            <li><strong>Take Action</strong> - Use the insights to make informed decisions</li>
        </ol>
        <p><strong>💡 Tip:</strong> Start with the <strong>"Executive Summary"</strong> page to get an overview of all key metrics!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Module Explanations
    st.subheader("🎯 Understanding Each Module")
    
    # Executive Summary
    with st.expander("📊 Executive Summary - What is it?", expanded=False):
        st.markdown("""
        **Purpose:** Get a quick overview of all important statistics and alerts.
        
        **What you'll see:**
        - Total number of districts and states covered
        - Total Aadhaar enrolments in the period
        - Critical fraud alerts that need immediate attention
        - Districts requiring urgent welfare intervention
        - Top 10 districts with highest fraud risk
        - Geographic distribution maps
        
        **Who should use it:** 
        - Senior officers for daily briefings
        - Decision makers for quick status checks
        - Anyone who wants a quick overview
        
        **Action Items:**
        - Check the critical alerts every day
        - Review districts flagged in red
        - Share the summary in morning meetings
        """)
    
    # Fraud Detection
    with st.expander("🕵️ Fraud Detection (Ghost Hunter) - How does it work?", expanded=False):
        st.markdown("""
        **Purpose:** Identify suspicious patterns and potential fraud in Aadhaar transactions.
        
        **What you'll see:**
        - **Benford's Law Analysis:** A mathematical test that finds unusual number patterns
        - **Anomaly Scores:** Higher scores = More suspicious activity
        - **Risk Categories:** LOW, MEDIUM, HIGH, CRITICAL
        - **Duplicate Detection:** Same biometric data appearing multiple times
        
        **Simple Explanation:**
        Think of this like a smart security guard that notices when numbers don't look natural. 
        For example, if a district suddenly has too many enrolments starting with "9", 
        it might indicate data manipulation.
        
        **Who should use it:**
        - Fraud investigation officers
        - District monitoring teams
        - Audit departments
        
        **What to do when you see fraud alerts:**
        1. ✅ Note down the district name and risk level
        2. ✅ Check the detailed metrics for that district
        3. ✅ Initiate field verification in high-risk areas
        4. ✅ Share report with your supervisor
        5. ✅ Follow up with local Aadhaar centers
        """)
    
    # Migration Heatmap
    with st.expander("🌍 Migration Heatmap (Migration Pulse) - Understanding population movement", expanded=False):
        st.markdown("""
        **Purpose:** Track where people are moving and why.
        
        **What you'll see:**
        - **Inflow Districts:** Areas receiving more people (shown in blue/green)
        - **Outflow Districts:** Areas losing population (shown in red/orange)
        - **Migration Rate:** How fast people are moving
        - **Interactive Map:** Visual representation of population movement
        
        **Simple Explanation:**
        This is like a population movement tracker. When people move to new places for work or 
        other reasons, they update their Aadhaar address. This tool tracks those changes and 
        shows you the trends.
        
        **Real-world uses:**
        - Planning new schools/hospitals in growing areas
        - Reducing services in areas losing population
        - Understanding employment patterns
        - Disaster preparedness
        
        **Who should use it:**
        - Urban planning departments
        - Public health officials
        - Education department officers
        - Resource allocation teams
        
        **Action Items:**
        - High Inflow? Plan for more infrastructure
        - High Outflow? Investigate reasons (employment, drought, etc.)
        """)
    
    # Child Welfare
    with st.expander("👶 Child Welfare (Missing Middle) - Protecting our children", expanded=False):
        st.markdown("""
        **Purpose:** Identify districts where children might be at risk or missing from records.
        
        **What you'll see:**
        - **Welfare Risk Levels:** CRITICAL, HIGH, MEDIUM, LOW
        - **Under-Enrollment Rate:** % of children not enrolled in Aadhaar
        - **Geographic Vulnerability Map:** Visual display of risk areas
        - **District Rankings:** Which areas need immediate help
        
        **Simple Explanation:**
        Every child should be registered in Aadhaar for their safety and to access benefits. 
        This tool finds districts where many children are missing from records, which could mean:
        - Children not getting school meals or scholarships
        - Potential child trafficking risk
        - Remote areas lacking enrollment camps
        
        **Who should use it:**
        - Women & Child Development officers
        - District Collectors
        - Child Protection Units
        - NGO coordinators
        
        **Immediate Actions for CRITICAL districts:**
        1. 🚨 Organize mobile Aadhaar enrollment camps
        2. 🚨 Coordinate with local schools and Anganwadis
        3. 🚨 Conduct door-to-door surveys
        4. 🚨 Create awareness about Aadhaar benefits
        5. 🚨 Report to State Child Welfare Committee
        """)
    
    # Policy Impact
    with st.expander("🎯 Policy Impact & ROI - Planning interventions", expanded=False):
        st.markdown("""
        **Purpose:** Simulate different government interventions and see their expected results.
        
        **What you'll see:**
        - **Fraud Reduction Scenario:** What if we increase verification?
        - **Migration Management:** Impact of creating local jobs
        - **Child Welfare Campaigns:** Results of enrollment drives
        - **ROI Calculations:** Money spent vs. benefits gained
        
        **Simple Explanation:**
        Before spending crores on a program, use this tool to see:
        - How much fraud will be reduced?
        - How many children will be helped?
        - Is the program cost-effective?
        - Which districts to target first?
        
        **Who should use it:**
        - Planning Commission officers
        - Budget allocation teams
        - Chief Ministers' offices
        - Program implementation units
        
        **Example Use Case:**
        "If we spend ₹50 lakhs on biometric verification in District X, 
        we can potentially prevent ₹2 crore in fraudulent transactions."
        """)
    
    # Forecasting
    with st.expander("📈 Forecasting & Trends - Predicting the future", expanded=False):
        st.markdown("""
        **Purpose:** Predict future trends based on current and past data.
        
        **What you'll see:**
        - **Enrollment Forecasts:** Expected registrations for next 6-12 months
        - **Seasonal Patterns:** When registrations increase/decrease
        - **Trend Lines:** Whether things are improving or worsening
        - **Confidence Intervals:** How sure we are about predictions
        
        **Simple Explanation:**
        This is like weather forecasting, but for Aadhaar registrations. Based on past patterns,
        we predict what will happen in the coming months.
        
        **Practical Applications:**
        - **Staff Planning:** Know when to hire temporary enrollment staff
        - **Resource Allocation:** When to stock more Aadhaar kits
        - **Budget Requests:** Justify next year's budget with data
        - **Capacity Planning:** Prepare for peak seasons
        
        **Who should use it:**
        - UIDAI regional officers
        - HR and recruitment teams
        - Logistics and supply chain managers
        - Financial planning departments
        """)
    
    # Benchmarking
    with st.expander("🏆 Benchmarking & Best Practices - Learning from the best", expanded=False):
        st.markdown("""
        **Purpose:** Compare district/state performance and learn from top performers.
        
        **What you'll see:**
        - **Performance Rankings:** Which districts are doing best?
        - **Efficiency Scores:** Comparison against national average
        - **Best Practices:** What are top districts doing differently?
        - **Gap Analysis:** How far behind are low performers?
        
        **Simple Explanation:**
        If District A has 95% child enrollment and District B has only 60%, what is District A 
        doing right? This tool helps you learn and replicate successful strategies.
        
        **Real Success Story Example:**
        "District Thrissur reduced fraud by 80% using mobile biometric verification. 
        Other districts can follow their model."
        
        **Who should use it:**
        - District Collectors comparing their performance
        - State coordinators identifying top performers
        - Training departments creating best practice manuals
        - Award committees recognizing excellence
        
        **Action Steps:**
        1. Check your district's ranking
        2. Identify top 3 performing districts
        3. Contact them to understand their methods
        4. Implement similar strategies
        5. Track improvement over time
        """)
    
    st.markdown("---")
    
    # Common Questions
    st.subheader("❓ Frequently Asked Questions (FAQ)")
    
    with st.expander("Q1: How often is the data updated?"):
        st.markdown("""
        **Answer:** The current dashboard shows data from **March to December 2025**. 
        In production deployment, data would be updated:
        - Daily for real-time monitoring
        - Weekly for trend analysis
        - Monthly for official reports
        """)
    
    with st.expander("Q2: Can I download reports and charts?"):
        st.markdown("""
        **Answer:** Yes! 
        - For charts: Click the camera icon (📷) in the top-right of any chart to save as image
        - For data: You can copy metrics and numbers for your reports
        - For screenshots: Use your computer's screenshot tool (Windows: Win+Shift+S)
        """)
    
    with st.expander("Q3: What should I do if I find a critical fraud alert?"):
        st.markdown("""
        **Answer:** Follow these steps immediately:
        1. ✅ Take a screenshot of the fraud details
        2. ✅ Note down: District name, Risk score, Date
        3. ✅ Inform your immediate supervisor
        4. ✅ Send alert to district fraud investigation team
        5. ✅ Initiate field verification within 48 hours
        6. ✅ Document all findings
        7. ✅ Update the central fraud database
        """)
    
    with st.expander("Q4: I'm not a technical person. Can I still use this?"):
        st.markdown("""
        **Answer:** Absolutely! This dashboard is designed for all government employees, 
        regardless of technical background. 
        
        **Key Points:**
        - No coding knowledge required
        - Just click and view
        - All charts have clear explanations
        - Colors show what's good (green) and bad (red)
        - If stuck, refer to this help guide
        
        **Remember:** If you can use a smartphone, you can use this dashboard!
        """)
    
    with st.expander("Q5: Which districts should I focus on first?"):
        st.markdown("""
        **Answer:** Priority order based on risk:
        
        **Immediate Attention (Today):**
        - Districts marked "CRITICAL RISK" in any module
        - Fraud scores above 8.0
        - Child welfare risk marked as "CRITICAL"
        
        **This Week:**
        - Districts marked "HIGH RISK"
        - Top 10 in fraud detection list
        - High outflow migration areas
        
        **This Month:**
        - Medium risk districts
        - Implement best practices from benchmarking
        - Plan long-term interventions
        """)
    
    with st.expander("Q6: Can I access this dashboard from my phone/tablet?"):
        st.markdown("""
        **Answer:** Yes! This dashboard works on:
        - 💻 Desktop computers
        - 📱 Smartphones (Android/iPhone)
        - 📱 Tablets (iPad/Android tablets)
        - 🖥️ Any device with a web browser
        
        **Tip:** For best experience, use landscape mode on mobile devices.
        """)
    
    with st.expander("Q7: Who do I contact for technical support?"):
        st.markdown("""
        **Answer:** For technical issues or questions:
        
        **Email:** uidai-support@nic.in (Example)
        **Phone:** 1800-XXX-XXXX (Example - Toll Free)
        **Portal:** https://support.uidai.gov.in (Example)
        
        **Before contacting support:**
        - Note down the error message
        - Take a screenshot if possible
        - Mention which module you were using
        - Provide your district/state name
        """)
    
    with st.expander("Q8: How do I interpret the color codes?"):
        st.markdown("""
        **Answer:** Universal color system used across all modules:
        
        🔴 **Red/Critical:** Immediate action required (within 24-48 hours)
        🟠 **Orange/High:** Urgent attention needed (within 1 week)
        🟡 **Yellow/Medium:** Monitor closely (within 2-4 weeks)
        🟢 **Green/Low:** Good performance, maintain current efforts
        🔵 **Blue:** Information/neutral data
        
        **Rule of Thumb:** If you see red, take action today!
        """)
    
    st.markdown("---")
    
    # Glossary
    st.subheader("📖 Important Terms Explained (Glossary)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Benford's Law:** A mathematical pattern that detects fraud by checking if numbers look natural
        
        **Anomaly Score:** A number (0-10) showing how suspicious something is. Higher = More suspicious
        
        **Biometric Duplication:** When same fingerprints/iris appear in multiple Aadhaar numbers
        
        **Demographic Data:** Basic information like name, address, date of birth
        
        **Enrollment Rate:** Percentage of population registered in Aadhaar
        
        **Inflow/Outflow:** People coming into or leaving from a district
        """)
    
    with col2:
        st.markdown("""
        **ROI (Return on Investment):** Money saved or gained compared to money spent
        
        **Risk Score:** A number showing danger level (0-10 scale)
        
        **Trend Analysis:** Looking at patterns over time to predict future
        
        **Welfare Risk:** Chance of children missing from social benefit programs
        
        **Benchmark:** Standard to compare performance against
        
        **Confidence Interval:** How sure we are about a prediction (e.g., 95% confident)
        """)
    
    st.markdown("---")
    
    # Training Resources
    st.subheader("🎓 Training & Resources")
    
    st.markdown("""
    <div class="info-box">
        <h4>📚 Additional Learning Materials:</h4>
        <ul>
            <li><strong>Quick Reference Card:</strong> Print the one-page guide (available in sidebar)</li>
            <li><strong>Video Tutorials:</strong> Coming soon - Step-by-step walkthrough videos</li>
            <li><strong>Webinars:</strong> Monthly training sessions for government officials</li>
            <li><strong>User Manual:</strong> Detailed PDF guide available for download</li>
            <li><strong>Best Practices:</strong> Monthly newsletter with success stories</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Footer
    st.info("""
    💡 **Pro Tip:** Bookmark this help page and refer to it whenever you have questions. 
    The more you use the dashboard, the easier it becomes!
    
    🙏 **Feedback Welcome:** If you have suggestions to improve this guide, please contact your 
    system administrator.
    """)
    
    st.success("""
    ✅ **Remember:** This dashboard is a powerful tool to help you serve citizens better. 
    Every alert you act on, every trend you identify, makes a real difference in people's lives.
    """)


def render_executive_summary(data, fraud_results, migration_results, welfare_results):
    """Render Executive Summary page"""
    st.header("📊 Executive Summary Dashboard")
    st.markdown("---")
    
    # Key Performance Indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_districts = data['district'].nunique()
        st.metric(
            label="📍 Total Districts",
            value=f"{total_districts:,}",
            delta=f"{data['state'].nunique()} States"
        )
    
    with col2:
        total_enrolments = data['total_enrolment'].sum()
        st.metric(
            label="👥 Total Enrolments",
            value=f"{total_enrolments/1e6:.2f}M",
            delta="March-Dec 2025"
        )
    
    with col3:
        # Safely get fraud count
        fraud_count = 0
        if fraud_results['combined'] is not None and len(fraud_results['combined']) > 0:
            fraud_count = len(fraud_results['combined'][fraud_results['combined']['dual_detection'] == True])
        st.metric(
            label="🚨 Critical Fraud Alerts",
            value=fraud_count,
            delta="Dual Detection",
            delta_color="inverse"
        )
    
    with col4:
        critical_welfare = len(welfare_results['district_scores'][
            welfare_results['district_scores']['welfare_risk'] == 'CRITICAL RISK'
        ])
        st.metric(
            label="🚨 Child Welfare Risks",
            value=critical_welfare,
            delta="Critical Districts",
            delta_color="inverse"
        )
    
    st.markdown("---")
    
    # National Trends Overview
    st.subheader("📈 National Trends Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly enrolment trends
        monthly_trends = data.groupby('month_year')['total_enrolment'].sum().reset_index()
        monthly_trends['month_year'] = monthly_trends['month_year'].astype(str)
        
        fig_monthly = px.line(
            monthly_trends,
            x='month_year',
            y='total_enrolment',
            title="📅 Monthly Enrolment Trends",
            labels={'month_year': 'Month', 'total_enrolment': 'Total Enrolments'},
            markers=True
        )
        fig_monthly.update_layout(height=400)
        st.plotly_chart(fig_monthly, width='stretch')
    
    with col2:
        # State-wise distribution
        state_summary = data.groupby('state')['total_enrolment'].sum().reset_index()
        state_summary = state_summary.nlargest(10, 'total_enrolment')
        
        fig_states = px.bar(
            state_summary,
            x='total_enrolment',
            y='state',
            orientation='h',
            title="🏛️ Top 10 States by Enrolment",
            labels={'total_enrolment': 'Total Enrolments', 'state': 'State'}
        )
        fig_states.update_layout(height=400)
        st.plotly_chart(fig_states, width='stretch')
    
    # Key Insights
    st.markdown("---")
    st.subheader("💡 Key Insights & Policy Implications")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="alert-critical">
        <h4>🚨 Fraud Detection</h4>
        <p><strong>{}</strong> districts show suspicious patterns violating Benford's Law.</p>
        <p><strong>Implication:</strong> Potential ghost enrolments leading to subsidy leakage. 
        Immediate audit required.</p>
        </div>
        """.format(
            len(fraud_results['benford'][fraud_results['benford']['risk_level'] == 'HIGH RISK']) 
            if len(fraud_results['benford']) > 0 else 0
        ), unsafe_allow_html=True)
    
    with col2:
        high_migration = len(migration_results['district_scores'][
            migration_results['district_scores']['migration_type'] == 'HIGH IN-MIGRATION'
        ])
        st.markdown("""
        <div class="info-box">
        <h4>🌍 Migration Hotspots</h4>
        <p><strong>{}</strong> districts experiencing high in-migration.</p>
        <p><strong>Implication:</strong> Need for infrastructure scaling, healthcare expansion, 
        and PDS capacity increase.</p>
        </div>
        """.format(high_migration), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="alert-critical">
        <h4>👶 Child Welfare Risk</h4>
        <p><strong>{}</strong> districts have critically low child MBU rates.</p>
        <p><strong>Implication:</strong> Children at risk of losing scholarship benefits, 
        MDM, and PDS access. Mobile biometric camps needed.</p>
        </div>
        """.format(critical_welfare), unsafe_allow_html=True)


def render_fraud_detection(fraud_results):
    """Render Fraud Detection page"""
    st.header("🕵️ Ghost Hunter: Fraud Detection Analysis")
    st.markdown("---")
    
    st.markdown("""
    <div class="info-box">
    <h4>📋 Methodology</h4>
    <p><strong>Benford's Law:</strong> Natural datasets follow a logarithmic distribution for first digits. 
    Deviations indicate artificial/manipulated data.</p>
    <p><strong>Isolation Forest:</strong> Machine learning algorithm detecting anomalous adult enrolment patterns 
    (should be rare due to 99%+ saturation).</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs for different analyses
    tab1, tab2, tab3 = st.tabs(["🎯 Combined Risk Score", "📊 Benford's Law Analysis", "🤖 ML Anomaly Detection"])
    
    with tab1:
        st.subheader("Top Fraud Suspects (Combined Analysis)")
        
        combined_df = fraud_results['combined']
        
        # Check if we have results
        if combined_df is None or len(combined_df) == 0:
            st.warning("⚠️ No fraud suspects found. This could mean:\n"
                      "- Insufficient data for analysis\n"
                      "- All districts are compliant\n"
                      "- Data quality issues")
            return
        
        top_suspects = combined_df.head(20)
        
        # Risk score distribution
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig_risk = px.scatter(
                top_suspects,
                x='deviation_factor',
                y='anomaly_score',
                size='total_enrolment',
                color='risk_level',
                hover_data=['district', 'state'],
                title="🎯 Risk Matrix: Benford Deviation vs ML Anomaly Score",
                labels={
                    'deviation_factor': 'Benford Deviation Factor',
                    'anomaly_score': 'Isolation Forest Score',
                    'risk_level': 'Risk Level'
                },
                color_discrete_map={
                    'HIGH RISK': '#DC3545',
                    'MODERATE RISK': '#FFC107',
                    'COMPLIANT': '#28A745'
                }
            )
            fig_risk.update_layout(height=500)
            st.plotly_chart(fig_risk, width='stretch')
        
        with col2:
            st.markdown("### 🚨 Critical Findings")
            critical_count = len(combined_df[combined_df['dual_detection'] == True])
            st.metric("Dual Detection (Critical)", critical_count)
            
            high_risk = len(combined_df[combined_df['risk_level'] == 'HIGH RISK'])
            st.metric("High Risk (Benford)", high_risk)
            
            anomalies = len(combined_df[combined_df['is_anomaly'] == True])
            st.metric("Anomalies (ML)", anomalies)
        
        # Detailed table
        st.markdown("---")
        st.subheader("📋 Detailed Fraud Suspect List")
        
        display_df = top_suspects[['state', 'district', 'total_enrolment', 
                                   'risk_level', 'deviation_factor', 
                                   'is_anomaly', 'dual_detection']].copy()
        display_df.columns = ['State', 'District', 'Total Enrolments', 
                             'Benford Risk', 'Deviation Factor', 
                             'ML Anomaly', 'Critical Alert']
        
        # Style function for the fraud table
        def highlight_row(row):
            if row['Critical Alert'] == True:
                return ['background-color: #DC3545; color: white; font-weight: 600'] * len(row)
            elif row['Benford Risk'] == 'HIGH RISK':
                return ['background-color: #FD7E14; color: white; font-weight: 600'] * len(row)
            elif row['Benford Risk'] == 'MODERATE RISK':
                return ['background-color: #FFC107; color: #212529; font-weight: 600'] * len(row)
            else:
                return [''] * len(row)
        
        st.dataframe(
            display_df.style.apply(highlight_row, axis=1),
            width='stretch'
        )
    
    with tab2:
        st.subheader("📊 Benford's Law Compliance Analysis")
        
        benford_df = fraud_results['benford']
        
        # Check if we have results
        if len(benford_df) == 0:
            st.warning("⚠️ No Benford's Law analysis results available. "
                      "Ensure districts have sufficient transaction data (≥5 months of data).")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Risk distribution pie chart
            risk_counts = benford_df['risk_level'].value_counts()
            fig_pie = px.pie(
                values=risk_counts.values,
                names=risk_counts.index,
                title="Risk Level Distribution",
                color=risk_counts.index,
                color_discrete_map={
                    'HIGH RISK': '#DC3545',
                    'MODERATE RISK': '#FFC107',
                    'COMPLIANT': '#28A745'
                }
            )
            st.plotly_chart(fig_pie, width='stretch')
        
        with col2:
            # Top violators
            top_violators = benford_df[benford_df['risk_level'] == 'HIGH RISK'].head(10)
            fig_bar = px.bar(
                top_violators,
                x='chi_square_stat',
                y='district',
                orientation='h',
                title="Top 10 Benford Violators",
                labels={'chi_square_stat': 'Chi-Square Statistic', 'district': 'District'}
            )
            st.plotly_chart(fig_bar, width='stretch')
        
        # State-wise summary
        st.markdown("---")
        st.subheader("🏛️ State-wise Fraud Risk Summary")
        
        state_summary = benford_df.groupby('state')['risk_level'].value_counts().unstack(fill_value=0)
        state_summary['total'] = state_summary.sum(axis=1)
        state_summary = state_summary.sort_values('HIGH RISK', ascending=False).head(15)
        
        fig_state = px.bar(
            state_summary.reset_index(),
            x='state',
            y=['HIGH RISK', 'MODERATE RISK', 'COMPLIANT'],
            title="State-wise Risk Distribution (Top 15 States)",
            labels={'value': 'Number of Districts', 'state': 'State'},
            barmode='stack',
            color_discrete_map={
                'HIGH RISK': '#DC3545',
                'MODERATE RISK': '#FFC107',
                'COMPLIANT': '#28A745'
            }
        )
        st.plotly_chart(fig_state, width='stretch')
    
    with tab3:
        st.subheader("🤖 Machine Learning Anomaly Detection (Isolation Forest)")
        
        isolation_df = fraud_results['isolation']
        
        # Check if we have results
        if len(isolation_df) == 0:
            st.warning("⚠️ No Isolation Forest analysis results available.")
            return
        
        anomalies = isolation_df[isolation_df['is_anomaly'] == True]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig_anomaly = px.scatter(
                isolation_df,
                x='adult_enrol_ratio',
                y='enrol_age_18_plus',
                color='is_anomaly',
                size='total_enrol',
                hover_data=['district', 'state'],
                title="Adult Enrolment Patterns (Anomalies in Red)",
                labels={
                    'adult_enrol_ratio': 'Adult Enrolment Ratio',
                    'enrol_age_18_plus': 'Total Adult Enrolments',
                    'is_anomaly': 'Anomaly'
                },
                color_discrete_map={True: '#DC3545', False: '#28A745'}
            )
            fig_anomaly.update_layout(height=500)
            st.plotly_chart(fig_anomaly, width='stretch')
        
        with col2:
            st.markdown("### 📊 Anomaly Statistics")
            st.metric("Total Anomalies", len(anomalies))
            st.metric("Anomaly Rate", f"{len(anomalies)/len(isolation_df)*100:.1f}%")
            
            st.markdown("""
            <div class="info-box">
            <h4>⚠️ Why This Matters</h4>
            <p>Adult saturation is >99%. High adult enrolments suggest:</p>
            <ul>
            <li>Ghost enrolments for subsidy fraud</li>
            <li>Data entry errors</li>
            <li>Duplicate registrations</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Top anomalies table
        st.markdown("---")
        st.subheader("Top 20 Anomalous Districts")
        
        top_anomalies = anomalies.head(20)[['state', 'district', 'enrol_age_18_plus', 
                                            'adult_enrol_ratio', 'anomaly_score']]
        top_anomalies.columns = ['State', 'District', 'Adult Enrolments', 
                                 'Adult Ratio', 'Anomaly Score']
        
        # Style function for anomalies - highlight rows based on anomaly score
        def highlight_anomalies(row):
            # More negative scores = more anomalous
            score = row['Anomaly Score']
            if score < -0.3:
                return ['background-color: #DC3545; color: white; font-weight: 600'] * len(row)
            elif score < -0.2:
                return ['background-color: #FD7E14; color: white; font-weight: 600'] * len(row)
            elif score < -0.1:
                return ['background-color: #FFC107; color: #212529; font-weight: 600'] * len(row)
            else:
                return [''] * len(row)
        
        st.dataframe(
            top_anomalies.style.apply(highlight_anomalies, axis=1),
            width='stretch'
        )


def render_migration_heatmap(migration_results):
    """Render Migration Analysis page"""
    st.header("🌍 Migration Pulse: Population Movement Tracker")
    st.markdown("---")
    
    st.markdown("""
    <div class="info-box">
    <h4>📋 Methodology</h4>
    <p><strong>In-Migration Signal:</strong> High demographic updates (address changes) indicate people arriving.</p>
    <p><strong>Out-Migration Signal:</strong> High biometric authentications + low address changes indicate people leaving.</p>
    <p><strong>Migration Score:</strong> Composite metric combining both signals for net migration intensity.</p>
    </div>
    """, unsafe_allow_html=True)
    
    district_scores = migration_results['district_scores']
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🗺️ Migration Heatmap", "📊 Migration Analytics", "📅 Temporal Trends"])
    
    with tab1:
        st.subheader("India Migration Intensity Map")
        
        # Create choropleth map
        fig_map = px.choropleth(
            district_scores,
            geojson=None,  # Would need India GeoJSON for actual map
            locations='state',
            locationmode='geojson-id',
            color='migration_intensity',
            hover_data=['district', 'migration_type', 'in_migration_score', 'out_migration_score'],
            title="Migration Intensity Heatmap (By State)",
            color_continuous_scale='RdYlGn',
            labels={'migration_intensity': 'Migration Intensity'}
        )
        
        # Fallback: Use scatter plot on map
        # Group by state for visualization
        state_migration = district_scores.groupby('state').agg({
            'migration_intensity': 'mean',
            'in_migration_score': 'mean',
            'out_migration_score': 'mean'
        }).reset_index()
        
        fig_bar = px.bar(
            state_migration.sort_values('migration_intensity', ascending=False).head(20),
            x='migration_intensity',
            y='state',
            orientation='h',
            title="Top 20 States by Migration Intensity",
            labels={'migration_intensity': 'Average Migration Intensity', 'state': 'State'},
            color='migration_intensity',
            color_continuous_scale='Reds'
        )
        fig_bar.update_layout(height=600)
        st.plotly_chart(fig_bar, width='stretch')
        
        # District-level details
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Top In-Migration Districts")
            top_in = district_scores.nlargest(10, 'in_migration_score')[
                ['district', 'state', 'in_migration_score', 'migration_type']
            ]
            # Style function for migration tables
            def style_migration(val, col_name):
                if col_name == 'Migration Type':
                    if val == 'HIGH IN-MIGRATION':
                        return 'background-color: #28A745; color: white; font-weight: 600'
                    elif val == 'HIGH OUT-MIGRATION':
                        return 'background-color: #DC3545; color: white; font-weight: 600'
                    elif val == 'HIGH MOBILITY':
                        return 'background-color: #FFC107; color: #212529; font-weight: 600'
                return ''
            
            styled_df = top_in.style.applymap(lambda x: style_migration(x, 'Migration Type'), subset=['migration_type'] if 'migration_type' in top_in.columns else [])
            st.dataframe(styled_df, width='stretch')
        
        with col2:
            st.markdown("### 📉 Top Out-Migration Districts")
            top_out = district_scores.nlargest(10, 'out_migration_score')[
                ['district', 'state', 'out_migration_score', 'migration_type']
            ]
            styled_df = top_out.style.applymap(lambda x: style_migration(x, 'Migration Type'), subset=['migration_type'] if 'migration_type' in top_out.columns else [])
            st.dataframe(styled_df, width='stretch')
    
    with tab2:
        st.subheader("📊 Migration Analytics Dashboard")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            in_migration_count = len(district_scores[
                district_scores['migration_type'] == 'HIGH IN-MIGRATION'
            ])
            st.metric("📈 High In-Migration", in_migration_count)
        
        with col2:
            out_migration_count = len(district_scores[
                district_scores['migration_type'] == 'HIGH OUT-MIGRATION'
            ])
            st.metric("📉 High Out-Migration", out_migration_count)
        
        with col3:
            high_mobility = len(district_scores[
                district_scores['migration_type'] == 'HIGH MOBILITY (Both)'
            ])
            st.metric("🔄 High Mobility", high_mobility)
        
        # Scatter plot: In-Migration vs Out-Migration
        st.markdown("---")
        fig_scatter = px.scatter(
            district_scores,
            x='in_migration_score',
            y='out_migration_score',
            color='migration_type',
            size='total_demo_updates',
            hover_data=['district', 'state'],
            title="Migration Matrix: In-Migration vs Out-Migration",
            labels={
                'in_migration_score': 'In-Migration Score',
                'out_migration_score': 'Out-Migration Score',
                'migration_type': 'Migration Type'
            },
            color_discrete_map={
                'HIGH IN-MIGRATION': '#28A745',
                'HIGH OUT-MIGRATION': '#DC3545',
                'HIGH MOBILITY (Both)': '#FFC107',
                'STABLE': '#6C757D'
            }
        )
        fig_scatter.update_layout(height=600)
        st.plotly_chart(fig_scatter, width='stretch')
        
        # Migration type distribution
        col1, col2 = st.columns(2)
        
        with col1:
            migration_counts = district_scores['migration_type'].value_counts()
            fig_pie = px.pie(
                values=migration_counts.values,
                names=migration_counts.index,
                title="Migration Type Distribution",
                color=migration_counts.index,
                color_discrete_map={
                    'HIGH IN-MIGRATION': '#28A745',
                    'HIGH OUT-MIGRATION': '#DC3545',
                    'HIGH MOBILITY (Both)': '#FFC107',
                    'STABLE': '#6C757D'
                }
            )
            st.plotly_chart(fig_pie, width='stretch')
        
        with col2:
            # Top mobility districts
            top_mobility = district_scores.nlargest(15, 'migration_intensity')
            fig_mobility = px.bar(
                top_mobility,
                x='migration_intensity',
                y='district',
                orientation='h',
                title="Top 15 High Mobility Districts",
                labels={'migration_intensity': 'Migration Intensity', 'district': 'District'},
                color='migration_intensity',
                color_continuous_scale='Oranges'
            )
            st.plotly_chart(fig_mobility, width='stretch')
    
    with tab3:
        st.subheader("📅 Temporal Migration Trends")
        
        temporal_df = migration_results['temporal_trends']
        temporal_df['month_year'] = temporal_df['month_year'].astype(str)
        
        # Line chart for temporal trends
        fig_temporal = go.Figure()
        
        fig_temporal.add_trace(go.Scatter(
            x=temporal_df['month_year'],
            y=temporal_df['total_address_changes'],
            mode='lines+markers',
            name='Address Changes (In-Migration)',
            line=dict(color='#28A745', width=3)
        ))
        
        fig_temporal.add_trace(go.Scatter(
            x=temporal_df['month_year'],
            y=temporal_df['total_bio_auth'],
            mode='lines+markers',
            name='Biometric Auth (Out-Migration)',
            line=dict(color='#DC3545', width=3)
        ))
        
        fig_temporal.update_layout(
            title="Monthly Migration Activity Trends",
            xaxis_title="Month",
            yaxis_title="Transaction Count",
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_temporal, width='stretch')
        
        # Mobility ratio over time
        fig_ratio = px.line(
            temporal_df,
            x='month_year',
            y='mobility_ratio',
            title="Monthly Mobility Ratio (Address Changes per 100 Biometric Auth)",
            labels={'month_year': 'Month', 'mobility_ratio': 'Mobility Ratio (%)'},
            markers=True
        )
        fig_ratio.update_layout(height=400)
        st.plotly_chart(fig_ratio, width='stretch')
        
        # Policy Implications
        st.markdown("---")
        st.markdown("""
        <div class="info-box">
        <h4>💡 Policy Implications</h4>
        <ul>
        <li><strong>High In-Migration Districts:</strong> Need infrastructure scaling (schools, hospitals, PDS outlets)</li>
        <li><strong>High Out-Migration Districts:</strong> Economic distress indicators - need employment schemes</li>
        <li><strong>Seasonal Patterns:</strong> Plan resource allocation based on migration cycles</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)


def render_child_welfare(welfare_results):
    """Render Child Welfare Analysis page"""
    st.header("👶 Missing Middle: Child Welfare Risk Dashboard")
    st.markdown("---")
    
    st.markdown("""
    <div class="alert-critical">
    <h4>⚠️ Critical Issue: Missing Child Biometric Updates (MBU)</h4>
    <p>Children (5-17 years) require mandatory biometric updates for:</p>
    <ul>
    <li><strong>School Services:</strong> Mid-Day Meals (MDM), Scholarships</li>
    <li><strong>Healthcare:</strong> Immunization tracking, health insurance</li>
    <li><strong>PDS Benefits:</strong> Subsidized rations</li>
    </ul>
    <p><strong>Risk:</strong> Children without updated biometrics may lose access to these welfare schemes.</p>
    </div>
    """, unsafe_allow_html=True)
    
    district_scores = welfare_results['district_scores']
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["🚨 Red Districts", "📊 Analytics Dashboard", "🎯 Intervention Priorities"])
    
    with tab1:
        st.subheader("🚨 Red Districts: Lowest Child MBU Rates")
        
        red_districts = welfare_results['red_districts']
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            critical_count = len(district_scores[district_scores['welfare_risk'] == 'CRITICAL RISK'])
            st.metric("🔴 Critical Risk", critical_count)
        
        with col2:
            high_count = len(district_scores[district_scores['welfare_risk'] == 'HIGH RISK'])
            st.metric("🟠 High Risk", high_count)
        
        with col3:
            total_affected = district_scores[
                district_scores['welfare_risk'].isin(['CRITICAL RISK', 'HIGH RISK'])
            ]['mbu_shortfall'].sum()
            st.metric("👶 Children Affected", f"{total_affected/1000:.1f}K")
        
        with col4:
            avg_mbu_rate = district_scores['child_mbu_rate'].mean()
            st.metric("📊 Avg Child MBU Rate", f"{avg_mbu_rate:.1f}%")
        
        # Red districts bar chart
        st.markdown("---")
        
        # Create a visualization that works even with low/zero rates
        red_districts_viz = red_districts.head(20).copy()
        
        # Create a composite score for visualization
        # Use percentile (inverted so lower = worse) + shortfall
        red_districts_viz['viz_score'] = red_districts_viz['child_mbu_percentile']
        
        fig_red = px.bar(
            red_districts_viz,
            x='viz_score',
            y='district',
            orientation='h',
            color='welfare_risk',
            title="Top 20 Red Districts (Child Welfare Risk - Lower Percentile = Higher Risk)",
            labels={'viz_score': 'Child MBU Percentile Rank', 'district': 'District'},
            color_discrete_map={
                'CRITICAL RISK': '#DC3545',
                'HIGH RISK': '#FD7E14',
                'MODERATE RISK': '#FFC107'
            },
            hover_data=['child_mbu_rate', 'mbu_shortfall']
        )
        fig_red.update_layout(
            height=600,
            xaxis_title="Percentile Rank (0=Worst, 100=Best)",
            showlegend=True
        )
        st.plotly_chart(fig_red, width='stretch')
        
        # Detailed table
        st.markdown("---")
        st.subheader("📋 Detailed Red District Analysis")
        
        display_df = red_districts[['state', 'district', 'child_mbu_rate', 
                                   'child_mbu_percentile', 'mbu_shortfall', 
                                   'welfare_risk']].copy()
        display_df.columns = ['State', 'District', 'Child MBU Rate (%)', 
                             'Percentile Rank', 'Missing Updates', 'Risk Level']
        display_df['Child MBU Rate (%)'] = display_df['Child MBU Rate (%)'].round(1)
        display_df['Percentile Rank'] = display_df['Percentile Rank'].round(0)
        display_df['Missing Updates'] = display_df['Missing Updates'].astype(int)
        
        # Style function for risk levels with improved colors
        def highlight_risk(row):
            if row['Risk Level'] == 'CRITICAL RISK':
                return ['background-color: #DC3545; color: white; font-weight: 600'] * len(row)
            elif row['Risk Level'] == 'HIGH RISK':
                return ['background-color: #FD7E14; color: white; font-weight: 600'] * len(row)
            elif row['Risk Level'] == 'MODERATE RISK':
                return ['background-color: #FFC107; color: #212529; font-weight: 600'] * len(row)
            else:
                return ['background-color: #28A745; color: white; font-weight: 600'] * len(row)
        
        st.dataframe(
            display_df.style.apply(highlight_risk, axis=1),
            width='stretch',
            height=600
        )
    
    with tab2:
        st.subheader("📊 Child Welfare Analytics")
        
        # Child vs Adult comparison
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribution of child MBU rates
            fig_dist = px.histogram(
                district_scores,
                x='child_mbu_rate',
                nbins=30,
                title="Distribution of Child MBU Rates",
                labels={'child_mbu_rate': 'Child MBU Rate (%)', 'count': 'Number of Districts'},
                color_discrete_sequence=['#138808']
            )
            fig_dist.update_layout(height=400)
            st.plotly_chart(fig_dist, width='stretch')
        
        with col2:
            # Risk level pie chart
            risk_counts = district_scores['welfare_risk'].value_counts()
            fig_pie = px.pie(
                values=risk_counts.values,
                names=risk_counts.index,
                title="Child Welfare Risk Distribution",
                color=risk_counts.index,
                color_discrete_map={
                    'CRITICAL RISK': '#DC3545',
                    'HIGH RISK': '#FD7E14',
                    'MODERATE RISK': '#FFC107',
                    'LOW RISK': '#28A745'
                }
            )
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, width='stretch')
        
        # Child vs Adult MBU comparison
        st.markdown("---")
        st.subheader("👶 vs 👨 Child-Adult MBU Comparison")
        
        # Prepare size column (ensure non-negative values for Plotly)
        district_scores['size_for_plot'] = district_scores['mbu_shortfall'].clip(lower=0) + 1
        
        # Scatter plot
        fig_compare = px.scatter(
            district_scores,
            x='adult_mbu_rate',
            y='child_mbu_rate',
            color='welfare_risk',
            size='size_for_plot',
            hover_data=['district', 'state', 'mbu_shortfall'],
            title="Child vs Adult MBU Rates (Size = Missing Updates)",
            labels={
                'adult_mbu_rate': 'Adult MBU Rate (%)',
                'child_mbu_rate': 'Child MBU Rate (%)',
                'welfare_risk': 'Risk Level'
            },
            color_discrete_map={
                'CRITICAL RISK': '#DC3545',
                'HIGH RISK': '#FD7E14',
                'MODERATE RISK': '#FFC107',
                'LOW RISK': '#28A745'
            }
        )
        # Add diagonal line (equal rates)
        fig_compare.add_trace(go.Scatter(
            x=[0, 100],
            y=[0, 100],
            mode='lines',
            name='Equal Rate Line',
            line=dict(color='gray', dash='dash')
        ))
        fig_compare.update_layout(height=600)
        st.plotly_chart(fig_compare, width='stretch')
        
        # Gap analysis
        col1, col2 = st.columns(2)
        
        with col1:
            large_gap = district_scores.nlargest(15, 'mbu_gap')
            fig_gap = px.bar(
                large_gap,
                x='mbu_gap',
                y='district',
                orientation='h',
                title="Top 15 Districts: Largest Child-Adult MBU Gap",
                labels={'mbu_gap': 'MBU Gap (Adult - Child %)', 'district': 'District'},
                color='mbu_gap',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig_gap, width='stretch')
        
        with col2:
            # State-wise summary
            state_summary = district_scores.groupby('state').agg({
                'child_mbu_rate': 'mean',
                'adult_mbu_rate': 'mean',
                'mbu_gap': 'mean'
            }).reset_index()
            state_summary = state_summary.nlargest(15, 'mbu_gap')
            
            fig_state = px.bar(
                state_summary,
                x='mbu_gap',
                y='state',
                orientation='h',
                title="Top 15 States: Average Child-Adult MBU Gap",
                labels={'mbu_gap': 'Average MBU Gap (%)', 'state': 'State'},
                color='mbu_gap',
                color_continuous_scale='Oranges'
            )
            st.plotly_chart(fig_state, width='stretch')
    
    with tab3:
        st.subheader("🎯 Intervention Priority Matrix")
        
        priorities = welfare_results['priorities']
        
        st.markdown("""
        <div class="info-box">
        <h4>📋 Priority Scoring Methodology</h4>
        <p>Districts prioritized based on:</p>
        <ul>
        <li><strong>Risk Severity (50%):</strong> How far below national average</li>
        <li><strong>Scale of Impact (50%):</strong> Number of children affected</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Priority bar chart
        fig_priority = px.bar(
            priorities.head(20),
            x='intervention_priority',
            y='district',
            orientation='h',
            color='welfare_risk',
            title="Top 20 Districts Requiring Immediate Intervention",
            labels={'intervention_priority': 'Priority Score', 'district': 'District'},
            color_discrete_map={
                'CRITICAL RISK': '#DC3545',
                'HIGH RISK': '#FD7E14',
                'MODERATE RISK': '#FFC107'
            }
        )
        fig_priority.update_layout(height=700)
        st.plotly_chart(fig_priority, width='stretch')
        
        # Action plan table
        st.markdown("---")
        st.subheader("📋 Recommended Action Plan")
        
        action_df = priorities.head(15)[['state', 'district', 'mbu_shortfall', 
                                        'child_mbu_rate', 'welfare_risk']].copy()
        
        def generate_action(row):
            if row['welfare_risk'] == 'CRITICAL RISK':
                return "🚨 URGENT: Mobile Biometric Camp + School Awareness Drive"
            elif row['welfare_risk'] == 'HIGH RISK':
                return "⚠️ HIGH PRIORITY: District-level Campaign + CSC Activation"
            else:
                return "⚡ MODERATE: Awareness through Anganwadi Centers"
        
        action_df['Recommended Action'] = action_df.apply(generate_action, axis=1)
        action_df['Children Affected'] = action_df['mbu_shortfall'].astype(int)
        action_df['Current MBU Rate (%)'] = action_df['child_mbu_rate'].round(1)
        
        # Create display DataFrame with proper column selection
        display_df = action_df[['state', 'district', 'Children Affected', 
                               'Current MBU Rate (%)', 'welfare_risk', 'Recommended Action']].copy()
        display_df.columns = ['State', 'District', 'Children Affected', 
                             'Current MBU Rate (%)', 'Risk Level', 'Recommended Action']
        
        # Style function for action plan table
        def highlight_action_plan(row):
            if row['Risk Level'] == 'CRITICAL RISK':
                return ['background-color: #DC3545; color: white; font-weight: 600'] * len(row)
            elif row['Risk Level'] == 'HIGH RISK':
                return ['background-color: #FD7E14; color: white; font-weight: 600'] * len(row)
            elif row['Risk Level'] == 'MODERATE RISK':
                return ['background-color: #FFC107; color: #212529; font-weight: 600'] * len(row)
            else:
                return [''] * len(row)
        
        st.dataframe(
            display_df.style.apply(highlight_action_plan, axis=1),
            width='stretch'
        )
        
        # Temporal trends
        st.markdown("---")
        st.subheader("📅 Child MBU Temporal Trends")
        
        temporal_df = welfare_results['temporal']
        temporal_df['month_year'] = temporal_df['month_year'].astype(str)
        
        fig_temporal = go.Figure()
        
        fig_temporal.add_trace(go.Scatter(
            x=temporal_df['month_year'],
            y=temporal_df['bio_age_5_17'],
            mode='lines+markers',
            name='Child MBU Count',
            line=dict(color='#138808', width=3),
            yaxis='y1'
        ))
        
        fig_temporal.add_trace(go.Scatter(
            x=temporal_df['month_year'],
            y=temporal_df['child_mbu_rate'],
            mode='lines+markers',
            name='Child MBU Rate (%)',
            line=dict(color='#FF9933', width=3),
            yaxis='y2'
        ))
        
        fig_temporal.update_layout(
            title="Monthly Child MBU Trends",
            xaxis_title="Month",
            yaxis=dict(title="MBU Count", side='left'),
            yaxis2=dict(title="MBU Rate (%)", overlaying='y', side='right'),
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_temporal, width='stretch')
         

def render_policy_impact(policy_results):
    """Render Policy Impact & ROI Analysis page"""
    st.header("🎯 Policy Impact Prediction & ROI Analysis")
    st.markdown("""
    **Simulate policy interventions and estimate return on investment for evidence-based decision-making**
    """)
    st.markdown("---")
    
    # Policy Recommendations Dashboard
    st.subheader("📋 National Policy Recommendations")
    
    recommendations = policy_results['policy_recommendations']
    
    # Priority filter
    priority_filter = st.multiselect(
        "Filter by Priority",
        ["CRITICAL", "HIGH", "MEDIUM"],
        default=["CRITICAL", "HIGH"]
    )
    
    filtered_recs = recommendations[recommendations['priority'].isin(priority_filter)]
    
    for _, rec in filtered_recs.iterrows():
        priority_color = {'CRITICAL': '#DC3545', 'HIGH': '#FD7E14', 'MEDIUM': '#FFC107'}
        st.markdown(f"""
        <div class="info-box" style="border-left-color: {priority_color[rec['priority']]};">
        <h4>{rec['category']} [{rec['priority']}]</h4>
        <p><strong>Recommendation:</strong> {rec['recommendation']}</p>
        <p><strong>Expected Impact:</strong> {rec['expected_impact']}</p>
        <p><strong>Timeline:</strong> {rec['implementation_timeline']}</p>
        <p><strong>Responsible:</strong> {rec['responsible_ministry']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Fraud Intervention ROI
    st.subheader("🕵️ Fraud Audit Intervention ROI")
    
    fraud_roi = policy_results['fraud_interventions']
    
    if len(fraud_roi) > 0:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_savings = fraud_roi['projected_annual_savings_inr'].sum()
            st.metric("Total Potential Savings", f"₹{total_savings/1e7:.2f} Cr")
        
        with col2:
            total_audit_cost = fraud_roi['audit_cost_inr'].sum()
            st.metric("Total Audit Cost", f"₹{total_audit_cost/1e7:.2f} Cr")
        
        with col3:
            total_roi = ((total_savings - total_audit_cost) / total_audit_cost * 100)
            st.metric("Combined ROI", f"{total_roi:.0f}%", delta="High Return")
        
        st.markdown("#### 📊 District-wise Fraud Intervention ROI")
        
        fig_fraud_roi = px.bar(
            fraud_roi.head(10),
            x='projected_annual_savings_inr',
            y='district',
            orientation='h',
            title="Top 10 Districts by Projected Savings (Annual)",
            labels={'projected_annual_savings_inr': 'Annual Savings (₹)', 'district': 'District'},
            color='roi_percentage',
            color_continuous_scale='RdYlGn',
            text='roi_percentage'
        )
        fig_fraud_roi.update_traces(texttemplate='ROI: %{text:.0f}%', textposition='outside')
        fig_fraud_roi.update_layout(height=500)
        st.plotly_chart(fig_fraud_roi, use_container_width=True)
        
        st.dataframe(
            fraud_roi[['state', 'district', 'estimated_fraud_enrolments', 
                      'projected_annual_savings_inr', 'audit_cost_inr', 'roi_percentage', 
                      'intervention_priority']],
            use_container_width=True
        )
    else:
        st.info("No high-risk fraud districts detected for intervention")
    
    st.markdown("---")
    
    # Child Welfare Intervention ROI
    st.subheader("👶 Child Welfare Outreach ROI")
    
    welfare_roi = policy_results['welfare_interventions']
    
    if len(welfare_roi) > 0:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_children_risk = welfare_roi['children_at_risk'].sum()
            st.metric("Children at Risk", f"{total_children_risk:,}")
        
        with col2:
            total_children_helped = welfare_roi['children_helped'].sum()
            st.metric("Children Helped (Projected)", f"{total_children_helped:,.0f}")
        
        with col3:
            total_welfare_value = welfare_roi['welfare_access_value_inr'].sum()
            st.metric("Welfare Access Value", f"₹{total_welfare_value/1e7:.2f} Cr")
        
        st.markdown("#### 📊 District-wise Child Welfare Intervention ROI")
        
        fig_welfare_roi = px.scatter(
            welfare_roi,
            x='children_at_risk',
            y='roi_percentage',
            size='welfare_access_value_inr',
            color='intervention_priority',
            hover_data=['state', 'district'],
            title="Child Welfare Intervention ROI Analysis",
            labels={'children_at_risk': 'Children at Risk', 'roi_percentage': 'ROI (%)'},
            color_discrete_map={'HIGH': '#DC3545', 'MEDIUM': '#FFC107'}
        )
        fig_welfare_roi.update_layout(height=500)
        st.plotly_chart(fig_welfare_roi, use_container_width=True)
        
        st.dataframe(
            welfare_roi[['state', 'district', 'children_at_risk', 'children_helped',
                        'welfare_access_value_inr', 'program_cost_inr', 'roi_percentage']],
            use_container_width=True
        )
    else:
        st.info("No critical welfare risk districts detected for intervention")
    
    st.markdown("---")
    
    # Infrastructure Needs
    st.subheader("🏗️ Migration Infrastructure Planning")
    
    infra_needs = policy_results['infrastructure_needs']
    
    if len(infra_needs) > 0:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_residents = infra_needs['estimated_new_residents'].sum()
            st.metric("Estimated New Residents", f"{total_residents:,}")
        
        with col2:
            total_ration_shops = infra_needs['ration_shops_needed'].sum()
            st.metric("Ration Shops Needed", f"{total_ration_shops}")
        
        with col3:
            total_cost = infra_needs['total_infrastructure_cost_inr'].sum()
            st.metric("Total Infrastructure Cost", f"₹{total_cost/1e7:.2f} Cr")
        
        st.markdown("#### 📊 Infrastructure Investment Requirements")
        
        # Stacked bar chart for infrastructure components
        infra_plot = infra_needs.head(10).copy()
        infra_plot['ration_cost'] = infra_plot['ration_shops_needed'] * 500000
        infra_plot['healthcare_cost'] = infra_plot['healthcare_centers_needed'] * 2000000
        infra_plot['school_cost'] = infra_plot['school_capacity_needed'] * 1000
        
        fig_infra = go.Figure()
        fig_infra.add_trace(go.Bar(name='Ration Shops', x=infra_plot['district'], 
                                   y=infra_plot['ration_cost']/1e6))
        fig_infra.add_trace(go.Bar(name='Healthcare', x=infra_plot['district'], 
                                   y=infra_plot['healthcare_cost']/1e6))
        fig_infra.add_trace(go.Bar(name='Schools', x=infra_plot['district'], 
                                   y=infra_plot['school_cost']/1e6))
        
        fig_infra.update_layout(
            barmode='stack',
            title='Infrastructure Cost Breakdown by District (₹ Crore)',
            xaxis_title='District',
            yaxis_title='Cost (₹ Crore)',
            height=500
        )
        st.plotly_chart(fig_infra, use_container_width=True)
        
        st.dataframe(
            infra_needs[['state', 'district', 'estimated_new_residents', 'ration_shops_needed',
                        'healthcare_centers_needed', 'school_capacity_needed', 
                        'total_infrastructure_cost_inr', 'urgency']],
            use_container_width=True
        )
    else:
        st.info("No high in-migration districts detected for infrastructure planning")


def render_forecasting(forecasting_results, data):
    """Render Forecasting & Trends Analysis page"""
    st.header("📈 Predictive Forecasting & Trend Analysis")
    st.markdown("""
    **Anticipate future patterns and trends for proactive governance**
    """)
    st.markdown("---")
    
    # State Enrolment Forecasts
    st.subheader("🔮 State Enrolment Forecasts (Next 6 Months)")
    
    state_forecasts = forecasting_results['state_forecasts']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        rapid_growth = len(state_forecasts[state_forecasts['trend_direction'] == 'RAPID GROWTH'])
        st.metric("States in Rapid Growth", rapid_growth, delta="Need capacity expansion")
    
    with col2:
        declining = len(state_forecasts[state_forecasts['trend_direction'].isin(['DECLINING', 'RAPID DECLINE'])])
        st.metric("States Declining", declining, delta="Investigate causes", delta_color="inverse")
    
    with col3:
        avg_confidence = state_forecasts['confidence_score'].mean()
        st.metric("Avg Forecast Confidence", f"{avg_confidence:.1f}%")
    
    st.markdown("#### 📊 State Growth Rate Comparison")
    
    fig_growth = px.bar(
        state_forecasts.head(15),
        x='state',
        y='growth_rate_pct_per_month',
        color='trend_direction',
        title='Monthly Growth Rate by State (%)',
        labels={'growth_rate_pct_per_month': 'Growth Rate (% per month)', 'state': 'State'},
        color_discrete_map={
            'RAPID GROWTH': '#28A745',
            'STEADY GROWTH': '#138808',
            'STABLE': '#6C757D',
            'DECLINING': '#FD7E14',
            'RAPID DECLINE': '#DC3545'
        }
    )
    fig_growth.update_layout(height=500)
    st.plotly_chart(fig_growth, use_container_width=True)
    
    st.dataframe(
        state_forecasts[['state', 'current_monthly_avg', 'growth_rate_pct_per_month',
                        'trend_direction', 'forecast_6m_total', 'confidence_score', 
                        'policy_implication']],
        use_container_width=True
    )
    
    st.markdown("---")
    
    # Seasonal Patterns
    st.subheader("📅 Seasonal Pattern Analysis")
    
    seasonal = forecasting_results['seasonal_patterns']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Peak Biometric Month", seasonal['peak_bio_month'])
    
    with col2:
        st.metric("Peak Biometric Value", f"{seasonal['peak_bio_value']/1e6:.2f}M")
    
    with col3:
        st.metric("Peak Enrolment Month", seasonal['peak_enrolment_month'])
    
    with col4:
        st.metric("Enrolment Volatility", f"{seasonal['enrolment_volatility_pct']:.1f}%")
    
    st.markdown("#### 📊 Monthly Trends Analysis")
    
    monthly_data = seasonal['monthly_data']
    monthly_data['month_year'] = monthly_data['month_year'].astype(str)
    
    fig_seasonal = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Biometric Authentication Trends', 'Enrolment Trends'),
        vertical_spacing=0.15
    )
    
    fig_seasonal.add_trace(
        go.Scatter(x=monthly_data['month_year'], y=monthly_data['bio_age_17_plus'],
                  mode='lines+markers', name='Adult Bio', line=dict(color='#138808')),
        row=1, col=1
    )
    fig_seasonal.add_trace(
        go.Scatter(x=monthly_data['month_year'], y=monthly_data['bio_age_5_17'],
                  mode='lines+markers', name='Child Bio', line=dict(color='#FF9933')),
        row=1, col=1
    )
    
    fig_seasonal.add_trace(
        go.Scatter(x=monthly_data['month_year'], y=monthly_data['total_enrolment'],
                  mode='lines+markers', name='Total Enrolment', line=dict(color='#000080')),
        row=2, col=1
    )
    
    fig_seasonal.update_layout(height=700, showlegend=True, hovermode='x unified')
    st.plotly_chart(fig_seasonal, use_container_width=True)
    
    st.markdown("---")
    
    # Emerging Hotspots
    st.subheader("🚀 Emerging Hotspot Districts")
    
    hotspots = forecasting_results['emerging_hotspots']
    
    st.info(f"**{len(hotspots)} districts identified with rapid activity growth** - These districts require proactive capacity planning")
    
    fig_hotspots = px.scatter(
        hotspots,
        x='growth_rate_pct',
        y='acceleration_pct',
        size='avg_monthly_activity',
        color='emerging_status',
        hover_data=['state', 'district'],
        title='Emerging Hotspot Analysis (Growth vs Acceleration)',
        labels={'growth_rate_pct': 'Growth Rate (%)', 'acceleration_pct': 'Acceleration (%)'},
        color_discrete_map={
            'RAPID EMERGENCE': '#DC3545',
            'STEADY GROWTH': '#FD7E14',
            'STABLE': '#6C757D'
        }
    )
    fig_hotspots.update_layout(height=500)
    st.plotly_chart(fig_hotspots, use_container_width=True)
    
    st.dataframe(
        hotspots[['state', 'district', 'avg_monthly_activity', 'growth_rate_pct',
                 'acceleration_pct', 'emerging_status']],
        use_container_width=True
    )
    
    st.markdown("---")
    
    # Future Fraud Risks
    st.subheader("⚠️ Predictive Fraud Risk Analysis")
    
    future_fraud = forecasting_results['future_fraud_risks']
    
    if len(future_fraud) > 0:
        st.warning(f"**{len(future_fraud)} districts flagged as HIGH RISK for future fraud** based on behavioral patterns")
        
        fig_fraud_risk = px.scatter(
            future_fraud,
            x='adult_enrol_ratio',
            y='bio_to_enrol_ratio',
            size='total_enrolment',
            color='fraud_risk_score',
            hover_data=['state', 'district'],
            title='Future Fraud Risk Indicators',
            labels={'adult_enrol_ratio': 'Adult Enrolment Ratio', 
                   'bio_to_enrol_ratio': 'Bio-to-Enrol Ratio'},
            color_continuous_scale='Reds'
        )
        fig_fraud_risk.update_layout(height=500)
        st.plotly_chart(fig_fraud_risk, use_container_width=True)
        
        st.dataframe(
            future_fraud[['state', 'district', 'fraud_risk_score', 'predicted_risk',
                         'adult_enrol_ratio', 'bio_to_enrol_ratio', 'demo_to_bio_ratio']],
            use_container_width=True
        )
    else:
        st.success("No districts flagged for elevated future fraud risk")


def render_benchmarking(benchmarking_results):
    """Render Benchmarking & Best Practices page"""
    st.header("🏆 Comparative Benchmarking & Best Practices")
    st.markdown("""
    **Compare performance across states/districts and identify exemplary practices for replication**
    """)
    st.markdown("---")
    
    # State Performance Index
    st.subheader("📊 State Performance Index")
    
    state_perf = benchmarking_results['state_performance']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        excellent = len(state_perf[state_perf['performance_tier'] == 'EXCELLENT'])
        st.metric("Excellent Performers", excellent)
    
    with col2:
        good = len(state_perf[state_perf['performance_tier'] == 'GOOD'])
        st.metric("Good Performers", good)
    
    with col3:
        avg = len(state_perf[state_perf['performance_tier'] == 'AVERAGE'])
        st.metric("Average Performers", avg)
    
    with col4:
        needs_imp = len(state_perf[state_perf['performance_tier'] == 'NEEDS IMPROVEMENT'])
        st.metric("Needs Improvement", needs_imp, delta_color="inverse")
    
    st.markdown("#### 📊 State Performance Ranking")
    
    fig_perf = px.bar(
        state_perf.head(20),
        x='composite_index',
        y='state',
        orientation='h',
        color='performance_tier',
        title='Top 20 States by Composite Performance Index',
        labels={'composite_index': 'Composite Index (0-100)', 'state': 'State'},
        color_discrete_map={
            'EXCELLENT': '#28A745',
            'GOOD': '#138808',
            'AVERAGE': '#FFC107',
            'NEEDS IMPROVEMENT': '#DC3545'
        }
    )
    fig_perf.update_layout(height=600)
    st.plotly_chart(fig_perf, use_container_width=True)
    
    st.dataframe(
        state_perf[['state', 'composite_index', 'national_rank', 'performance_tier',
                   'bio_update_rate', 'child_bio_compliance', 'demo_activity_score',
                   'vs_national_avg']],
        use_container_width=True
    )
    
    st.markdown("---")
    
    # Best Practices
    st.subheader("✨ Best Practices & Exemplary Cases")
    
    best_practices = benchmarking_results['best_practices']
    
    # Group by category
    categories = best_practices['category'].unique()
    
    for category in categories:
        st.markdown(f"#### {category}")
        category_practices = best_practices[best_practices['category'] == category]
        
        for _, practice in category_practices.iterrows():
            st.markdown(f"""
            <div class="info-box">
            <h4>{practice['state']} - {practice['district']}</h4>
            <p><strong>Metric:</strong> {practice['metric_name']} = {practice['metric_value']}</p>
            <p><strong>Why Exemplary:</strong> {practice['why_exemplary']}</p>
            <p><strong>Replicable Action:</strong> {practice['replicable_action']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Laggards & Intervention Needs
    st.subheader("🎯 Priority Areas for Intervention")
    
    laggards = benchmarking_results['laggards']
    
    st.warning(f"**{len(laggards)} areas identified needing urgent intervention**")
    
    # Group by issue type
    col1, col2 = st.columns(2)
    
    with col1:
        state_issues = len(laggards[laggards['level'] == 'State'])
        st.metric("State-level Issues", state_issues)
    
    with col2:
        district_issues = len(laggards[laggards['level'] == 'District'])
        st.metric("District-level Issues", district_issues)
    
    # Issue breakdown
    issue_counts = laggards.groupby('issue').size().reset_index(name='count')
    
    fig_issues = px.pie(
        issue_counts,
        values='count',
        names='issue',
        title='Issue Type Distribution',
        color_discrete_sequence=px.colors.sequential.Reds
    )
    fig_issues.update_layout(height=400)
    st.plotly_chart(fig_issues, use_container_width=True)
    
    st.markdown("#### 📋 Detailed Intervention Priority List")
    
    # Color-code by issue severity
    display_laggards = laggards.copy()
    
    st.dataframe(
        display_laggards[['level', 'state', 'district', 'issue', 'metric', 'value',
                         'national_avg', 'gap', 'recommended_action']],
        use_container_width=True
    )
    
    st.markdown("---")
    
    # State Peer Comparison Tool
    st.subheader("🔍 State Peer Comparison Tool")
    
    selected_state = st.selectbox(
        "Select a state to compare with peers",
        state_perf['state'].sort_values().unique()
    )
    
    if selected_state:
        from modules.benchmarking import BenchmarkingEngine
        
        # Need to re-instantiate for method call
        st.info(f"Comparing {selected_state} with peer states of similar size...")
        
        # Show selected state metrics
        selected_metrics = state_perf[state_perf['state'] == selected_state].iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Composite Index", f"{selected_metrics['composite_index']:.1f}")
        
        with col2:
            st.metric("National Rank", f"#{int(selected_metrics['national_rank'])}")
        
        with col3:
            st.metric("Performance Tier", selected_metrics['performance_tier'])
        
        with col4:
            st.metric("vs National Avg", f"{selected_metrics['vs_national_avg']:+.1f}")


def main():
    """Main application"""
    
    # Render header
    render_header()
    
    # Initialize session state for tracking
    if 'viewed_pages' not in st.session_state:
        st.session_state.viewed_pages = set()
    if 'quick_filters' not in st.session_state:
        st.session_state.quick_filters = {'state': None, 'risk_level': None, 'date_range': None}
    
    # Sidebar navigation with enhanced utility
    st.sidebar.title("📱 Control Center")
    
    # Help Section - MOVED TO TOP
    st.sidebar.info("💡 **Tip:** Use Quick Actions below for instant access to critical features!")
    
    st.sidebar.markdown("---")
    
    # Quick Action Panel - Top Priority
    with st.sidebar.expander("⚡ Quick Actions", expanded=True):
        st.text("🎯 Fast Track to Results")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🚨 Critical Alerts", use_container_width=True):
                st.session_state.quick_nav = "🏠 Executive Summary"
                st.rerun()
            if st.button("📊 Full Report", use_container_width=True):
                st.session_state.export_mode = True
        with col2:
            if st.button("🔍 Find Issues", use_container_width=True):
                st.session_state.quick_nav = "🕵️ Fraud Detection"
                st.rerun()
            if st.button("📥 Export Data", use_container_width=True):
                st.session_state.show_export = True
    
    st.sidebar.markdown("---")
    
    # Smart Filters Section
    with st.sidebar.expander("🎛️ Smart Filters", expanded=False):
        st.text("Filter data across all modules:")
        
        # State filter
        filter_state = st.selectbox(
            "📍 Select State",
            ["All States"] + ["Maharashtra", "Karnataka", "Tamil Nadu", "Gujarat", "Rajasthan"],
            key="filter_state_select"
        )
        st.session_state.quick_filters['state'] = None if filter_state == "All States" else filter_state
        
        # Risk level filter
        filter_risk = st.selectbox(
            "⚠️ Risk Level",
            ["All Levels", "CRITICAL", "HIGH", "MEDIUM", "LOW"],
            key="filter_risk_select"
        )
        st.session_state.quick_filters['risk_level'] = None if filter_risk == "All Levels" else filter_risk
        
        # Date range (simplified)
        filter_month = st.select_slider(
            "📅 Time Period",
            options=["Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Full Year"],
            value="Full Year",
            key="filter_month_select"
        )
        st.session_state.quick_filters['date_range'] = filter_month
        
        if st.button("🔄 Reset All Filters", use_container_width=True):
            st.session_state.quick_filters = {'state': None, 'risk_level': None, 'date_range': None}
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # Main Navigation
    page = st.sidebar.radio(
        "📑 Main Modules",
        ["🏠 Executive Summary",
         "📚 Help & User Guide",
         "🕵️ Fraud Detection", 
         "🌍 Migration Heatmap", 
         "👶 Child Welfare",
         "🎯 Policy Impact & ROI",
         "📈 Forecasting & Trends",
         "🏆 Benchmarking & Best Practices"],
        key="main_page_selector"
    )
    
    # Check if quick nav was triggered
    if 'quick_nav' in st.session_state:
        page = st.session_state.quick_nav
        del st.session_state.quick_nav
    
    # Track viewed pages
    st.session_state.viewed_pages.add(page)
    
    st.sidebar.markdown("---")
    
    # Contextual Page Guide
    with st.sidebar.expander("📖 Current Page Guide", expanded=False):
        guides = {
            "🏠 Executive Summary": [
                "Goal: Get complete overview",
                "• View all critical alerts",
                "• Check district rankings",
                "• Identify urgent issues"
            ],
            "📚 Help & User Guide": [
                "Goal: Learn the system",
                "• Understand each module",
                "• Follow step-by-step guides",
                "• Get quick reference"
            ],
            "🕵️ Fraud Detection": [
                "Goal: Find suspicious activity",
                "• Check Benford's Law scores",
                "• Review high-risk districts",
                "• Export fraud reports"
            ],
            "🌍 Migration Heatmap": [
                "Goal: Track population movement",
                "• View inflow/outflow patterns",
                "• Plan infrastructure needs",
                "• Identify migration hotspots"
            ],
            "👶 Child Welfare": [
                "Goal: Protect children",
                "• Find under-enrolled districts",
                "• Prioritize interventions",
                "• Plan enrollment camps"
            ],
            "🎯 Policy Impact & ROI": [
                "Goal: Simulate interventions",
                "• Calculate ROI of policies",
                "• Compare strategies",
                "• Optimize resource allocation"
            ],
            "📈 Forecasting & Trends": [
                "Goal: Predict future needs",
                "• View trend projections",
                "• Plan ahead for demand",
                "• Identify growth areas"
            ],
            "🏆 Benchmarking & Best Practices": [
                "Goal: Learn from best performers",
                "• Compare district performance",
                "• Identify success stories",
                "• Replicate best practices"
            ]
        }
        guide_text = guides.get(page, ["Select a module to begin"])
        for line in guide_text:
            st.text(line)
    
    # Progress Tracker
    with st.sidebar.expander("📈 Your Progress", expanded=False):
        total_modules = 8
        viewed = len(st.session_state.viewed_pages)
        progress = viewed / total_modules
        st.progress(progress)
        st.text(f"Explored: {viewed}/{total_modules} modules")
        st.write("")  # spacing
        
        if viewed == total_modules:
            st.success("🎉 You've explored all modules!")
        elif viewed >= 4:
            st.info("🌟 Great progress! Keep exploring.")
        else:
            st.warning("💪 More modules to discover!")
    
    # Quick Stats Dashboard
    st.sidebar.markdown("---")
    with st.sidebar.expander("📊 Live Dashboard Stats", expanded=False):
        st.text("System Status: 🟢 Online")
        st.text("Last Updated: Real-time")
        st.text("Data Period: Mar-Dec 2025")
        st.write("")  # spacing
        st.text("Coverage:")
        st.text("• 🗺️ 36 States/UTs")
        st.text("• 🏛️ 600+ Districts")
        st.text("• 👥 5M+ Transactions")
    
    # Export & Download Options
    st.sidebar.markdown("---")
    with st.sidebar.expander("💾 Export & Reports", expanded=False):
        st.text("📥 Download Options:")
        st.write("")  # spacing
        
        if st.button("📄 Generate PDF Report", use_container_width=True):
            st.info("📊 PDF generation feature coming soon!")
        
        if st.button("📊 Export to Excel", use_container_width=True):
            st.info("📈 Excel export feature coming soon!")
        
        if st.button("📸 Save Dashboard", use_container_width=True):
            st.info("💾 Dashboard snapshot feature coming soon!")
        
        st.markdown("---")
        st.text("🖨️ Quick Print:")
        st.caption("Use Ctrl+P (Win) or Cmd+P (Mac)")
    
    # About Section (Collapsed by default)
    st.sidebar.markdown("---")
    with st.sidebar.expander("ℹ️ About System", expanded=False):
        st.subheader("Jan-Gana-Drishti")
        st.caption("People-Data-Vision")
        st.write("")  # spacing
        st.text("Mission: Transform Aadhaar logs")
        st.text("into actionable insights")
        st.write("")  # spacing
        st.text("Powered by:")
        st.text("• 🤖 AI/ML Analytics")
        st.text("• 📊 Real-time Processing")
        st.text("• 🔒 Secure Infrastructure")
        st.write("")  # spacing
        st.text("Developed by:")
        st.text("National Informatics Centre")
        st.text("Government of India 🇮🇳")
        st.write("")  # spacing
        st.caption("Version: 2.0 | Jan 2026")
    
    st.sidebar.markdown("---")
    st.sidebar.caption("📞 Need Help? Visit Help & User Guide")
    st.sidebar.caption("Or contact NIC Support")
    
    # Load data (cached)
    try:
        data, pipeline = load_data()
        st.sidebar.success("✅ Data loaded successfully")
        
        # Run analyses (cached)
        if 'fraud_results' not in st.session_state:
            st.session_state.fraud_results = run_fraud_detection(data)
        
        if 'migration_results' not in st.session_state:
            st.session_state.migration_results = run_migration_analysis(data)
        
        if 'welfare_results' not in st.session_state:
            st.session_state.welfare_results = run_child_welfare_analysis(data)
        
        if 'policy_results' not in st.session_state:
            st.session_state.policy_results = run_policy_impact_analysis(
                data,
                st.session_state.fraud_results,
                st.session_state.migration_results,
                st.session_state.welfare_results
            )
        
        if 'forecasting_results' not in st.session_state:
            st.session_state.forecasting_results = run_forecasting_analysis(data)
        
        if 'benchmarking_results' not in st.session_state:
            st.session_state.benchmarking_results = run_benchmarking_analysis(
                data,
                st.session_state.fraud_results,
                st.session_state.migration_results,
                st.session_state.welfare_results
            )
        
        # Page routing
        if page == "🏠 Executive Summary":
            render_executive_summary(
                data, 
                st.session_state.fraud_results,
                st.session_state.migration_results,
                st.session_state.welfare_results
            )
        
        elif page == "📚 Help & User Guide":
            render_help_guide()
        
        elif page == "🕵️ Fraud Detection":
            render_fraud_detection(st.session_state.fraud_results)
        
        elif page == "🌍 Migration Heatmap":
            render_migration_heatmap(st.session_state.migration_results)
        
        elif page == "👶 Child Welfare":
            render_child_welfare(st.session_state.welfare_results)
        
        elif page == "🎯 Policy Impact & ROI":
            render_policy_impact(st.session_state.policy_results)
        
        elif page == "📈 Forecasting & Trends":
            render_forecasting(st.session_state.forecasting_results, data)
        
        elif page == "🏆 Benchmarking & Best Practices":
            render_benchmarking(st.session_state.benchmarking_results)
    
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        st.info("Please ensure the data files are in the correct location (data/ directory)")
        st.exception(e)


if __name__ == "__main__":
    main()
