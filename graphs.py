import multi_course_profit_calculator as st
import matplotlib.pyplot as plt

# Function to calculate revenue based on user inputs
def calculate_revenue(course_price, num_students, platform_fee, refund_rate, conversion_rate, subscription_price=None, subscription_months=None):
    # Platform revenue calculation (e.g., Udemy)
    platform_earnings = course_price * num_students * (1 - platform_fee) * (1 - refund_rate)
    
    # Own website revenue calculation
    website_students = num_students * conversion_rate  # Estimated students on own platform
    own_website_earnings = course_price * website_students
    
    # Optional subscription model revenue
    if subscription_price and subscription_months:
        subscription_revenue = subscription_price * website_students * subscription_months
    else:
        subscription_revenue = 0
    
    return platform_earnings, own_website_earnings, subscription_revenue

# Streamlit app setup
st.title("Course Revenue Calculator")
st.write("Compare potential earnings between hosting on Udemy and running your own course website.")

# User inputs
course_price = st.number_input("Course Price ($)", min_value=0, value=100)
num_students = st.number_input("Number of Students on Udemy", min_value=0, value=500)
platform_fee = st.slider("Platform Fee (%)", min_value=0, max_value=100, value=37) / 100
refund_rate = st.slider("Refund Rate (%)", min_value=0, max_value=100, value=5) / 100
conversion_rate = st.slider("Conversion Rate on Your Site (%)", min_value=0, max_value=100, value=15) / 100

# Optional subscription model inputs
use_subscription = st.checkbox("Include Subscription Revenue")
if use_subscription:
    subscription_price = st.number_input("Subscription Price ($)", min_value=0, value=20)
    subscription_months = st.number_input("Subscription Duration (months)", min_value=1, value=6)
else:
    subscription_price, subscription_months = None, None

# Calculate revenues
platform_earnings, own_website_earnings, subscription_revenue = calculate_revenue(
    course_price, num_students, platform_fee, refund_rate, conversion_rate, subscription_price, subscription_months
)

# Display results
st.subheader("Revenue Breakdown")
st.write(f"Earnings on Platform (Udemy): ${platform_earnings:,.2f}")
st.write(f"Earnings on Your Own Website: ${own_website_earnings:,.2f}")
if use_subscription:
    st.write(f"Additional Subscription Revenue: ${subscription_revenue:,.2f}")

# Plotting the revenue comparison
fig, ax = plt.subplots()
labels = ["Udemy Earnings", "Own Website Earnings", "Subscription Revenue"]
values = [platform_earnings, own_website_earnings, subscription_revenue] if use_subscription else [platform_earnings, own_website_earnings]
ax.bar(labels[:len(values)], values, color=["#1f77b4", "#ff7f0e", "#2ca02c"])

# Customize plot
ax.set_ylabel("Revenue ($)")
ax.set_title("Revenue Comparison")
ax.grid(True, axis="y")
x
# Display plot
st.pyplot(fig)

# CTA for more information
st.write("---")
st.write("Ready to take control of your course profits? [Book a call with us!](#)")


