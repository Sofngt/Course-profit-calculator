import streamlit as st
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.patches as patches
from PIL import Image
import base64
from io import BytesIO

# Set up custom styling for the background, text color, and button color

# Setting page style with custom CSS
st.markdown(
    """
    <style>
    /* Background color for the entire page */
    .stApp {
        background-color: #001f3f;
        color: white;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        color: #ffffff;
    }
    .stButton>button {
        background-color: #00c8c8;
        color: #ffffff;
    }
    .stNumberInput input {
        background-color: #ffffff;
        color: #001f3f;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Load the logo image
logo = Image.open("images/logo.png")

# Convert the PIL image to a base64 string
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
        background-color: #001f3f;  /* Header background color */
        padding: 10px 20px;
        color: white;
    }}
    .header .logo {{
        width: 130px;  /* Adjust this value to resize the logo */
    }}
    .header .title-container {{
        flex-grow: 1;  /* Allows the title container to take available space */
        display: flex;
        justify-content: center;  /* Centers the title within the container */
    }}
    .header .title {{
        margin: 0;
        padding: 0;
        font-size: 35px;
        text-align: center;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}

    /* Responsive styling for smaller screens */
    @media (max-width: 768px) {{
        .header .title {{
            font-size: 18px; /* Adjust font size for smaller screens */
        }}
        .header .title-container {{
            padding: 5px; /* Adjust padding for smaller screens */
        }}
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
import time

progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.01)
    progress_bar.progress(i + 1)
st.markdown("---")  # Horizontal line separator
st.header("Input Your Course Details")
# Lists to store course details
course_prices = []
course_sales = []
instructor_sales = []
organic_sales = []
affiliate_sales = []

# Input fields to add courses
num_courses = st.number_input("How many courses would you like to add?", min_value=1, step=1, value=1)

# Default percentages if unknown
default_instructor_pct = 30
default_organic_pct = 50
default_affiliate_pct = 20

# Add course inputs dynamically based on the number of courses
for i in range(num_courses):
    st.write(f"### Course {i+1}")
    price = st.number_input(f"Course {i+1} Price ($)", min_value=0.0, step=0.01, value=50.0, key=f"price_{i}")
    sales = st.number_input(f"Course {i+1} Monthly Sales", min_value=0, step=1, value=100, key=f"sales_{i}")
    
    #explenation
    st.write("### Course Sales Distribution")
    st.write("Let’s break down your sales!")
    with st.expander("❓ How to find your Udemy sales data"):
        st.write("""
        1. **Log into your Udemy Instructor Dashboard**.
        2. Go to **Performance** > **Sales**.
        3. View the **Sales Breakdown** section, where you'll see categories like:
            - Instructor-Promoted Sales: Sales generated directly through your promotions (e.g., coupon links).
            - Organic Udemy Sales: Sales generated organically through Udemy’s platform (e.g., searches, recommendations).
            - Affiliate Sales: Sales made via Udemy's affiliate marketing network.
        4. If you don't have exact values, feel free to use our default estimates.
        """)

    # Checkbox for unknown sales percentages
    # Checkbox for unknown sales percentages with a unique key for each course
    use_default_pct = st.checkbox(f"I don’t know the exact breakdown – use average values", key=f"default_pct_{i}")
    
    if use_default_pct:
        instructor_pct = default_instructor_pct
        organic_pct = default_organic_pct
        affiliate_pct = default_affiliate_pct
    else:
        instructor_pct = st.slider(f"Percentage of Instructor-Promoted Sales for Course {i+1} (%)", 0, 100, 30, key=f"instructor_{i}")
        organic_pct = st.slider(f"Percentage of Organic Udemy Sales for Course {i+1} (%)", 0, 100, 50, key=f"organic_{i}")
        affiliate_pct = st.slider(f"Percentage of Affiliate Sales for Course {i+1} (%)", 0, 100, 20, key=f"affiliate_{i}")

        # Ensure total percentage adds up to 100%
        if instructor_pct + organic_pct + affiliate_pct != 100:
            st.warning("Sales percentages must add up to 100%. Please adjust the values.")
            continue

    # Convert percentages to decimal for calculation
    instructor_sales.append(instructor_pct / 100)
    organic_sales.append(organic_pct / 100)
    affiliate_sales.append(affiliate_pct / 100)

    # Add values to lists
    course_prices.append(price)
    course_sales.append(sales)

# Platform fees by sales type
udemy_fees = {
    "instructor": 0.03,  # 3% fee for instructor-promoted sales
    "organic": 0.37,     # 37% fee for organic sales
    "affiliate": 0.75    # 75% fee for affiliate sales
}
own_platform_fee = 0.10  # Hypothetical 10% fee for the user's own platform


import numpy as np

# Button to calculate revenue
if st.button("Calculate"):

    # Initialize variables for total monthly and yearly revenue
    total_udemy_monthly_revenue = 0
    total_own_platform_monthly_revenue = 0
    
    # Initialize lists for earnings by sales type for each course
    udemy_instructor_earnings = []
    udemy_organic_earnings = []
    udemy_affiliate_earnings = []
    own_platform_earnings = []

    # Calculate revenue for each course and populate earnings lists for chart
    for idx, (price, sales, instructor_pct, organic_pct, affiliate_pct) in enumerate(zip(course_prices, course_sales, instructor_sales, organic_sales, affiliate_sales)):
        # Calculate Udemy revenue based on each type of sale
        instructor_revenue = price * sales * instructor_pct * (1 - udemy_fees["instructor"])
        organic_revenue = price * sales * organic_pct * (1 - udemy_fees["organic"])
        affiliate_revenue = price * sales * affiliate_pct * (1 - udemy_fees["affiliate"])
        
        # Calculate own platform revenue
        own_platform_revenue = price * sales * (1 - own_platform_fee)

        # Append calculated revenues to respective lists
        udemy_instructor_earnings.append(instructor_revenue)
        udemy_organic_earnings.append(organic_revenue)
        udemy_affiliate_earnings.append(affiliate_revenue)
        own_platform_earnings.append(own_platform_revenue)

        # Update total monthly revenue
        course_udemy_monthly_revenue = instructor_revenue + organic_revenue + affiliate_revenue
        total_udemy_monthly_revenue += course_udemy_monthly_revenue
        total_own_platform_monthly_revenue += own_platform_revenue

        # Display per-course revenue breakdown
        st.write(f"**Course {idx + 1} Revenue Breakdown**")
        st.write(f"Udemy Monthly Revenue: ${course_udemy_monthly_revenue:,.2f}")
        st.write(f"Own Platform Monthly Revenue: ${own_platform_revenue:,.2f}")
        st.write("—" * 30)  # Separator line

    # Calculate total yearly revenue
    total_udemy_yearly_revenue = total_udemy_monthly_revenue * 12
    total_own_platform_yearly_revenue = total_own_platform_monthly_revenue * 12

    # Calculate losses with Udemy
    monthly_loss_with_udemy = total_own_platform_monthly_revenue - total_udemy_monthly_revenue
    yearly_loss_with_udemy = total_own_platform_yearly_revenue - total_udemy_yearly_revenue

    # Example for displaying values with styling in Streamlit
    def styled_text(label, value):
        return f'<span style="color:#FFD700; font-weight:bold;">${value:,.2f}</span>'

    # Display per-course revenue breakdown
    st.write(f"**Course {idx + 1} Revenue Breakdown**")
    st.markdown(f"Udemy Monthly Revenue: {styled_text('Udemy Monthly Revenue', course_udemy_monthly_revenue)}", unsafe_allow_html=True)
    st.markdown(f"Own Platform Monthly Revenue: {styled_text('Own Platform Monthly Revenue', own_platform_revenue)}", unsafe_allow_html=True)
    st.write("—" * 30)  # Separator line

    # Display total revenue comparison
    st.write("### Total Monthly and Yearly Revenue Comparison")
    st.markdown(f"**Total Udemy Monthly Revenue:** {styled_text('Total Udemy Monthly Revenue', total_udemy_monthly_revenue)}", unsafe_allow_html=True)
    st.markdown(f"**Total Own Platform Monthly Revenue:** {styled_text('Total Own Platform Monthly Revenue', total_own_platform_monthly_revenue)}", unsafe_allow_html=True)
    st.markdown(f"**Total Udemy Yearly Revenue:** {styled_text('Total Udemy Yearly Revenue', total_udemy_yearly_revenue)}", unsafe_allow_html=True)
    st.markdown(f"**Total Own Platform Yearly Revenue:** {styled_text('Total Own Platform Yearly Revenue', total_own_platform_yearly_revenue)}", unsafe_allow_html=True)

    # Display loss with Udemy
    st.write("### Potential Loss by Using Udemy")
    st.markdown(f"**Monthly Loss with Udemy:** {styled_text('Monthly Loss with Udemy', monthly_loss_with_udemy)}", unsafe_allow_html=True)
    st.markdown(f"**Yearly Loss with Udemy:** {styled_text('Yearly Loss with Udemy', yearly_loss_with_udemy)}", unsafe_allow_html=True)

    

    # Create the stacked horizontal bar chart with enhanced styling
    fig, ax = plt.subplots(figsize=(12, 6))

    bar_width = 0.1  # Reduced width for narrower bars
    course_indices = np.arange(len(course_prices))  # Positions for the courses

    # Set custom font
    plt.rcParams['font.family'] = 'DejaVu Sans'  # or any other sans-serif font

    # Plot bars with rounded edges
    ax.barh(course_indices, udemy_instructor_earnings, height=bar_width, label='Udemy Instructor Sales', color='#FF6F61', edgecolor='none')
    ax.barh(course_indices, udemy_organic_earnings, height=bar_width, label='Udemy Organic Sales', color='#FFA07A', 
            left=udemy_instructor_earnings, edgecolor='none')
    ax.barh(course_indices, udemy_affiliate_earnings, height=bar_width, label='Udemy Affiliate Sales', color='#FFD700', 
            left=np.array(udemy_instructor_earnings) + np.array(udemy_organic_earnings), edgecolor='none')

    # Separate bar for Own Platform Earnings with spacing and rounded edges
    ax.barh(course_indices + bar_width + 0.1, own_platform_earnings, height=bar_width, label='Own Platform Earnings', color='#39CCCC', edgecolor='none')

    # Customize the appearance to match the Streamlit theme
    ax.set_facecolor('#001f3f')  # Set background color to match Streamlit theme
    fig.patch.set_facecolor('#001f3f')  # Set figure background color
    ax.tick_params(colors='white')  # Set tick color to white
    ax.yaxis.label.set_color('white')  # Set y-axis label color
    ax.xaxis.label.set_color('white')  # Set x-axis label color
    ax.title.set_color('white')  # Set title color

    # Labels
    ax.set_ylabel('Courses', fontsize=14)
    ax.set_xlabel('Monthly Revenue ($)', fontsize=14)
    ax.set_title('Monthly Revenue Comparison: Udemy (by Sales Type) vs. Own Platform', fontsize=16, fontweight='bold')
    ax.set_yticks(course_indices + bar_width / 2)
    ax.set_yticklabels([f'Course {i+1}' for i in range(len(course_prices))], color='white')
    
    # Add subtle gridlines
    ax.grid(True, axis='x', linestyle='--', alpha=0.6)
    
    # Set legend outside of plot area with white text
    legend = ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0., fontsize=10)
    for text in legend.get_texts():
        text.set_color("white")
    st.markdown("---")
    # Show chart
    st.pyplot(fig)

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
    """,
    unsafe_allow_html=True
)

# Add the call-to-action button
st.markdown(
    """
    <a href="https://app.lemcal.com/@sofiadiaz/course-profit-boost-" target="_blank" class="cta-button">
        📈 Want to boost your earnings? Book a free strategy call with NGT Media 🚀
    </a>
    """,
    unsafe_allow_html=True
)


