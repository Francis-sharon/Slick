

import gradio as gr

# Global dictionary to track user orders
user_orders = {}

# Food menu dictionary
food_menu = {
    "Italian": ["Pizza", "Pasta", "Lasagna", "Garlic Bread"],
    "American": ["Burger", "Fries", "Milkshake", "Hotdog"],
    "Asian": ["Sushi", "Ramen", "Spring Rolls", "Dim Sum"],
    "Vegetarian": ["Salad", "Vegetable Stir Fry", "Vegetarian Pizza", "Falafel"],
}

def update_food_items(cuisine_choice):
    """Update food items based on cuisine selection"""
    choices = food_menu.get(cuisine_choice, [])
    if not choices:
        choices = ["Select Item"]
    return gr.update(choices=choices, value=choices[0] if choices else None)

def recommend_items(selected_item, order_history):
    """Recommends items based on selected item and user's order history"""
    recommendations = {
        "Burger": ["Fries", "Milkshake", "Pizza"],
        "Pizza": ["Garlic Bread", "Salad", "Pasta"],
        "Pasta": ["Garlic Bread", "Pizza", "Salad"],
        "Salad": ["Soup", "Pasta", "Bread"],
        "Sushi": ["Ramen", "Spring Rolls", "Dim Sum"],
        "Ramen": ["Spring Rolls", "Dim Sum", "Fried Rice"],
        "Lasagna": ["Garlic Bread", "Salad", "Pasta"],
        "Fries": ["Burger", "Milkshake", "Pizza"],
    }

    recommended = recommendations.get(selected_item, ["Water", "Fries", "Salad"])
    additional = [item for item in recommendations if item not in order_history]
    return recommended[:3]

def place_order(name, cuisine, item, quantity):
    """Process the food order with recommendations"""
    if not name:
        return "Please enter your name in the profile tab before ordering."
    if not cuisine or not item or item == "Select Item":
        return "Please select both cuisine and food item."
    if quantity <= 0:
        return "Please select a valid quantity."

    # Track the order
    if name not in user_orders:
        user_orders[name] = []
    user_orders[name].append(item)

    # Generate recommendations
    recommendations = recommend_items(item, user_orders[name])

    order_message = f"Order placed: {quantity} {item}(s) from {cuisine} cuisine for {name}"
    recommender_message = f"\n\nBased on your order, you might also like: {', '.join(recommendations)}"

    return order_message + recommender_message

def get_popular_items():
    """Return popular items with personalized recommendations"""
    base_recommendations = [
        "Pizza (Italian)",
        "Burger (American)",
        "Sushi (Asian)",
        "Salad (Vegetarian)"
    ]
    return "Our most popular items:\n" + "\n".join(base_recommendations)

# Create the Gradio app
with gr.Blocks(css=".gradio-container {background: #eaf4fb;}") as app:
    gr.Markdown("<h1 style='color: #1f4e79;'>SLICK FOOD ORDERS</h1>")

    with gr.Tabs():
        # Profile Tab
        with gr.TabItem("Profile"):
            name = gr.Textbox(label="Name", placeholder="Enter your name")
            email = gr.Textbox(label="Email", placeholder="Enter your email")
            contact = gr.Textbox(label="Contact", placeholder="Enter your contact number")

            profile_output = gr.Textbox(label="Profile Status")
            gr.Button("Save Profile").click(
                lambda n, e, c: f"Profile saved for {n}" if n else "Please enter name",
                inputs=[name, email, contact],
                outputs=profile_output
            )

        # Order Food Tab
        with gr.TabItem("Order Food"):
            gr.Markdown("Select a cuisine and food item below:")

            with gr.Row():
                cuisine = gr.Dropdown(
                    choices=list(food_menu.keys()),
                    label="Cuisine"
                )
                food_item = gr.Dropdown(
                    choices=["Select Item"],
                    label="Food Item"
                )
                quantity = gr.Number(label="Quantity", value=1, minimum=1)

            order_output = gr.Textbox(label="Order Confirmation")

            # Connect the update function for food items
            cuisine.change(
                fn=update_food_items,
                inputs=cuisine,
                outputs=food_item
            )

            # Connect the order button with recommendations
            gr.Button("Place Order").click(
                fn=place_order,
                inputs=[name, cuisine, food_item, quantity],
                outputs=order_output
            )

        # Recommendations Tab
        with gr.TabItem("Recommendations"):
            gr.Markdown("<h3>Popular Items:</h3>")
            recommended_items = gr.Textbox(
                label="Recommended Items",
                value="Click 'Show Popular Items' to see recommendations",
                interactive=False
            )

            # Use a proper function for recommendations
            gr.Button("Show Popular Items").click(
                fn=get_popular_items,
                inputs=None,
                outputs=recommended_items
            )

# Launch the app
app.launch()

import gradio as gr

# URL of the food ordering app
FOOD_ORDERING_APP_URL = "https://f06e99de90b71a9679.gradio.live/"  # Replace with the actual app's URL

# Simulated user database for login
user_database = {
    "user1": "password123",
    "admin": "adminpass"
}

def login(username, password):
    """
    Verifies the username and password.
    Args:
        username: Entered username.
        password: Entered password.
    Returns:
        A message and visibility state for the Next button.
    """
    if username in user_database and user_database[username] == password:
        return (
            "Login successful! Click the link below to proceed.",
            f'<a href="{FOOD_ORDERING_APP_URL}" target="_blank" style="color:blue; text-decoration: underline;">Next</a>',
        )
    return "Invalid username or password. Please try again.", ""

# Create login interface
with gr.Blocks() as login_app:
    gr.Markdown("<h1 style='color: #1f4e79;'>Login to Access the Food Ordering App</h1>")

    with gr.Row():
        username = gr.Textbox(label="Username", placeholder="Enter your username")
        password = gr.Textbox(label="Password", placeholder="Enter your password", type="password")

    login_output = gr.Textbox(label="Login Status", interactive=False)
    next_link = gr.HTML(value="", visible=True)  # Dynamic HTML link

    # Handle login process
    login_button = gr.Button("Login")
    login_button.click(
        fn=login,
        inputs=[username, password],
        outputs=[login_output, next_link]
    )

    gr.Markdown("""
    <style>
        body {background-color: #dceefc;}
        .gradio-container {background: #ffffff; border-radius: 12px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);}
        h1 {color: #2a6bbf; font-family: Arial, sans-serif;}
    </style>
    """)

login_app.launch()
