import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import base64
from io import BytesIO
import time

# Google Analytics 4 tag integration
st.markdown(
    """
    <!-- Google Tag Manager -->
    <script>
    (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
    new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
    j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
    'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
    })(window,document,'script','dataLayer','GTM-MLCWPL3X');
    </script>
    <!-- End Google Tag Manager -->
    """,
    unsafe_allow_html=True
)


# Capture lead_id from URL query parameters using the updated Streamlit property
query_params = st.query_params
lead_id = query_params.get('lead_id', [None])[0]
if lead_id:
    st.write(f"Welcome, Lead ID: {lead_id}")

# Page styling with custom CSS
st.markdown(
    """
    <style>
    .stApp { background-color: #001f3f; color: white; }
    h1, h2, h3, h4, h5, h6, p, label { color: #ffffff; }
    .stButton>button { background-color: #00c8c8; color: #ffffff; }
    .stNumberInput input { background-color: #ffffff; color: #001f3f; }
    </style>
    """,
    unsafe_allow_html=True
)

# Load and display the logo
logo = Image.open("images/logo.png")
buffer = BytesIO()
logo.save(buffer, format="PNG")
logo_base64 = base64.b64encode(buffer.getvalue()).decode()

st.markdown(
    f"""
    <style>
    .header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #001f3f;
        padding: 10px 20px;
        color: white;
    }}
    .header .logo {{ width: 130px; }}
    .header .title-container {{ flex-grow: 1; display: flex; justify-content: center; }}
    .header .title {{ font-size: 35px; text-align: center; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    @media (max-width: 768px) {{
        .header {{ flex-direction: column; align-items: center; }}
        .header .title {{ font-size: 24px; text-align: center; }}
        .header .logo {{ margin-bottom: 10px; }}
    }}
    </style>
    <div class="header">
        <img class="logo" src="data:image/png;base64,{logo_base64}" alt="NGT-Media Logo">
        <div class="title-container">
            <h1 class="title">Online Course Profit Calculator</h1>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    '<p style="font-size:25px;">Turn Your Courses into Profit Machines! Stop Losing Profits to Udemy—Discover what you could really be earning by publishing your course on your own website! 📊 🚀</p>',
    unsafe_allow_html=True
)

# Progress bar
progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.01)
    progress_bar.progress(i + 1)
st.markdown("---")
st.header("Input Your Course Details")

# Course input fields
num_courses = st.number_input("How many courses would you like to add?", min_value=1, step=1, value=1)
default_instructor_pct = 30
default_organic_pct = 50
default_affiliate_pct = 20
course_prices = []
course_sales = []
instructor_sales = []
organic_sales = []
affiliate_sales = []

for i in range(num_courses):
    st.write(f"### Course {i+1}")
    price = st.number_input(f"Course {i+1} Price ($)", min_value=0.0, step=0.01, value=50.0, key=f"price_{i}")
    sales = st.number_input(f"Course {i+1} Monthly Sales", min_value=0, step=1, value=100, key=f"sales_{i}")

    st.write("### Course Sales Distribution")
    with st.expander("❓ How to find your Udemy sales data"):
        st.write("""
        1. **Log into your Udemy Instructor Dashboard**.
        2. Go to **Performance** > **Sales**.
        3. View the **Sales Breakdown** section.
        """)

    use_default_pct = st.checkbox(f"I don’t know the exact breakdown – use average values", key=f"default_pct_{i}")
    if use_default_pct:
        instructor_pct = default_instructor_pct
        organic_pct = default_organic_pct
        affiliate_pct = default_affiliate_pct
    else:
        instructor_pct = st.slider(f"Percentage of Instructor-Promoted Sales for Course {i+1} (%)", 0, 100, 30, key=f"instructor_{i}")
        organic_pct = st.slider(f"Percentage of Organic Udemy Sales for Course {i+1} (%)", 0, 100, 50, key=f"organic_{i}")
        affiliate_pct = st.slider(f"Percentage of Affiliate Sales for Course {i+1} (%)", 0, 100, 20, key=f"affiliate_{i}")
        if instructor_pct + organic_pct + affiliate_pct != 100:
            st.warning("Sales percentages must add up to 100%. Please adjust the values.")
            continue

    instructor_sales.append(instructor_pct / 100)
    organic_sales.append(organic_pct / 100)
    affiliate_sales.append(affiliate_pct / 100)
    course_prices.append(price)
    course_sales.append(sales)

# Platform fee configuration
udemy_fees = {"instructor": 0.03, "organic": 0.37, "affiliate": 0.75}
own_platform_fee = 0.10

# Revenue calculation and display
if st.button("Calculate"):
    total_udemy_monthly_revenue = 0
    total_own_platform_monthly_revenue = 0
    udemy_instructor_earnings = []
    udemy_organic_earnings = []
    udemy_affiliate_earnings = []
    own_platform_earnings = []

    for idx, (price, sales, instructor_pct, organic_pct, affiliate_pct) in enumerate(zip(course_prices, course_sales, instructor_sales, organic_sales, affiliate_sales)):
        instructor_revenue = price * sales * instructor_pct * (1 - udemy_fees["instructor"])
        organic_revenue = price * sales * organic_pct * (1 - udemy_fees["organic"])
        affiliate_revenue = price * sales * affiliate_pct * (1 - udemy_fees["affiliate"])
        own_platform_revenue = price * sales * (1 - own_platform_fee)

        udemy_instructor_earnings.append(instructor_revenue)
        udemy_organic_earnings.append(organic_revenue)
        udemy_affiliate_earnings.append(affiliate_revenue)
        own_platform_earnings.append(own_platform_revenue)

        total_udemy_monthly_revenue += instructor_revenue + organic_revenue + affiliate_revenue
        total_own_platform_monthly_revenue += own_platform_revenue

        st.write(f"**Course {idx + 1} Revenue Breakdown**")
        st.write(f"Udemy Monthly Revenue: ${instructor_revenue + organic_revenue + affiliate_revenue:,.2f}")
        st.write(f"Own Platform Monthly Revenue: ${own_platform_revenue:,.2f}")
        st.write("—" * 30)

    st.write("### Total Monthly and Yearly Revenue Comparison")
    st.write(f"Total Udemy Monthly Revenue: ${total_udemy_monthly_revenue:,.2f}")
    st.write(f"Total Own Platform Monthly Revenue: ${total_own_platform_monthly_revenue:,.2f}")
    st.write(f"Total Udemy Yearly Revenue: ${total_udemy_monthly_revenue * 12:,.2f}")
    st.write(f"Total Own Platform Yearly Revenue: ${total_own_platform_monthly_revenue * 12:,.2f}")
    # Chart for revenue comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    bar_width = 0.1  # Width of the bars
    course_indices = np.arange(len(course_prices))

    # Plot the bar chart for Udemy earnings
    ax.barh(course_indices, udemy_instructor_earnings, height=bar_width, label='Udemy Instructor Sales', color='#FF6F61')
    ax.barh(course_indices, udemy_organic_earnings, height=bar_width, label='Udemy Organic Sales', color='#FFA07A', 
            left=np.array(udemy_instructor_earnings))
    ax.barh(course_indices, udemy_affiliate_earnings, height=bar_width, label='Udemy Affiliate Sales', color='#FFD700', 
            left=np.array(udemy_instructor_earnings) + np.array(udemy_organic_earnings))

    # Separate bar for own platform earnings
    ax.barh(course_indices + bar_width + 0.1, own_platform_earnings, height=bar_width, label='Own Platform Earnings', color='#39CCCC')

    # Styling the chart
    ax.set_facecolor('#001f3f')  # Background color
    fig.patch.set_facecolor('#001f3f')  # Figure background color
    ax.tick_params(colors='white')  # Tick color
    ax.yaxis.label.set_color('white')  # Y-axis label color
    ax.xaxis.label.set_color('white')  # X-axis label color
    ax.title.set_color('white')  # Title color
    ax.set_ylabel('Courses', fontsize=14)
    ax.set_xlabel('Monthly Revenue ($)', fontsize=14)
    ax.set_title('Monthly Revenue Comparison: Udemy (by Sales Type) vs. Own Platform', fontsize=16, fontweight='bold')
    ax.set_yticks(course_indices + bar_width / 2)
    ax.set_yticklabels([f'Course {i+1}' for i in range(len(course_prices))], color='white')

    # Gridlines and legend
    ax.grid(True, axis='x', linestyle='--', alpha=0.6)
    legend = ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0., fontsize=10)
    for text in legend.get_texts():
        text.set_color("white")

    # Display the plot in Streamlit
    st.pyplot(fig)

    # Call-to-action button
    st.markdown(
        """
        <style>
        .cta-button {
            background-color: #FF6F61;
            color: white;
            font-size: 18px;
            padding: 15px 30px;
            border-radius: 10px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            margin-top: 30px;
            font-weight: bold;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        .cta-button:hover {
            background-color: #FF3B2D;
            transform: scale(1.05);
            box-shadow: 0px 6px 20px rgba(0, 0, 0, 0.4);
        }
        </style>
        <a href="https://app.lemcal.com/@sofiadiaz/course-profit-boost-" target="_blank" class="cta-button" onclick="trackButtonClick()">
            📈 Want to boost your earnings now? Book a free strategy call with NGT Media 🚀
        </a>
        <script>
            function trackButtonClick() {
                window.dataLayer = window.dataLayer || [];
                window.dataLayer.push({
                    'event': 'cta_button_click',
                    'eventCategory': 'CTA Button',
                    'eventAction': 'click',
                    'eventLabel': 'NGT Media Strategy Call'
                });
            }
        </script>
        """,
        unsafe_allow_html=True
    )