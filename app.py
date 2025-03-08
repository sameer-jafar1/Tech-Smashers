from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample menu items
menu = [
    {"id": 1, "name": "Pizza", "price": 10},
    {"id": 2, "name": "Burger", "price": 5},
    {"id": 3, "name": "Pasta", "price": 8}
]

cart = []
selected_item = 0

@app.route("/menu", methods=["GET"])
def get_menu():
    return jsonify(menu)

@app.route("/gesture", methods=["POST"])
def gesture_action():
    global selected_item, cart
    data = request.json
    action = data.get("action")

    if action == "next_item":
        selected_item = (selected_item + 1) % len(menu)
    elif action == "previous_item":
        selected_item = (selected_item - 1) % len(menu)
    elif action == "select_item":
        cart.append(menu[selected_item])
    elif action == "confirm_order":
        return jsonify({"status": "Order Confirmed", "cart": cart})

    return jsonify({"selected_item": selected_item, "cart": cart})

if __name__ == "__main__":
    app.run(debug=True)
