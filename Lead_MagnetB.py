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

    return {
        "platform_earnings": round(platform_earnings, 2),
        "own_website_earnings": round(own_website_earnings, 2),
        "subscription_revenue": round(subscription_revenue, 2) if subscription_revenue else "N/A"
    }

# Input variables
course_price = 100  # Example price per course
num_students = 500  # Number of students on Udemy
platform_fee = 0.37  # 37% fee for Udemy
refund_rate = 0.05  # 5% refund rate
conversion_rate = 0.15  # 15% of students who would buy on your own site

# Optional variables for subscription model
subscription_price = 20  # Monthly subscription price
subscription_months = 6  # Average subscription duration in months

# Calculate revenue
revenue = calculate_revenue(
    course_price=course_price,
    num_students=num_students,
    platform_fee=platform_fee,
    refund_rate=refund_rate,
    conversion_rate=conversion_rate,
    subscription_price=subscription_price,
    subscription_months=subscription_months
)

# Display results
print("Revenue Breakdown:")
print(f"  Earnings on Platform (Udemy): ${revenue['platform_earnings']}")
print(f"  Earnings on Your Own Website: ${revenue['own_website_earnings']}")
print(f"  Subscription Revenue (Optional): ${revenue['subscription_revenue']}")