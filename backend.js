import React, { useState } from "react";
import axios from "axios";

const OrderFood = ({ username }) => {
  const [cuisine, setCuisine] = useState("");
  const [item, setItem] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [message, setMessage] = useState("");

  const handleOrder = async () => {
    try {
      const response = await axios.post("http://localhost:3001/place-order", {
        username, cuisine, item, quantity,
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.message || "Order failed");
    }
  };

  return (
    <div>
      <h1>Order Food</h1>
      <select onChange={(e) => setCuisine(e.target.value)}>
        <option value="">Select Cuisine</option>
        <option value="Italian">Italian</option>
        <option value="American">American</option>
        <option value="Asian">Asian</option>
      </select>
      <select onChange={(e) => setItem(e.target.value)}>
        <option value="">Select Item</option>
        <option value="Pizza">Pizza</option>
        <option value="Burger">Burger</option>
      </select>
      <input
        type="number"
        min="1"
        value={quantity}
        onChange={(e) => setQuantity(e.target.value)}
      />
      <button onClick={handleOrder}>Place Order</button>
      <p>{message}</p>
    </div>
  );
};

export default OrderFood;