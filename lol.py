with st.expander("🔍 Advanced Insights: Ad Spend Strategy for Maximizing Profits"):
    st.markdown("""
    Investing in ad spend can be the key to turning your courses into profit-generating powerhouses! Here's how it works with our strategy:

    **Starting Ad Spend**: We begin with a recommended starting ad spend of **$1,500 per month** using targeted Meta Ads (Facebook & Instagram).

    **Goal**: The objective is to optimize your course and sales funnel so that it generates enough profit to **fund its own ad spend**, creating a sustainable growth cycle.

    **Why It Matters**:
    - **Boost Visibility**: Attract more learners with targeted ads tailored to their needs.
    - **Control Your Data**: Build your own audience and customer base, rather than relying solely on platforms like Udemy.
    - **Maximize ROI**: With personalized ad strategies and ongoing optimization, every dollar spent aims to drive the highest possible returns.

    **Example Calculation**:
    If your course makes **$5,000/month** from your own platform, and you spend **$1,500 on ads**, your net revenue would be **$3,500/month**. As your earnings increase, ad spend as a percentage of revenue will decrease, maximizing your profits.

    Ready to take control of your course growth? [Book a free strategy call with NGT Media](https://app.lemcal.com/@sofiadiaz/course-profit-boost-).
    """)
 

# Ad Spend ROI Calculator
st.markdown("---")
st.header("📊 Ad Spend ROI Calculator")
st.write("""
Estimate how quickly your course can become self-sustaining, covering ad spend through generated profits.
""")

# User inputs for the calculator
starting_ad_spend = st.number_input("Enter your starting monthly ad spend ($)", min_value=0.0, value=1500.0, step=100.0)
course_monthly_revenue = st.number_input("Enter your expected monthly revenue from the course ($)", min_value=0.0, value=5000.0, step=100.0)
growth_rate = st.slider("Expected monthly revenue growth rate (%)", min_value=0, max_value=100, value=10)

# Calculate months to break even on ad spend
if st.button("Calculate ROI Timeline"):
    # Initial calculations
    profit = course_monthly_revenue - starting_ad_spend
    months_to_self_sustain = 0

    # Calculate number of months to sustain
    if profit > 0:
        st.write("🎉 Your course is already self-sustaining!")
    else:
        while profit < 0:
            months_to_self_sustain += 1
            course_monthly_revenue *= (1 + growth_rate / 100)
            profit = course_monthly_revenue - starting_ad_spend

        st.write(f"🚀 Your course will be self-sustaining in **{months_to_self_sustain} months**!")
        st.write(f"Projected monthly revenue when self-sustaining: **${course_monthly_revenue:,.2f}**")
        st.write(f"Net profit after covering ad spend: **${profit:,.2f}**")
