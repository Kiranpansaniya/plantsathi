import { useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useCart } from "../context/CartContext";

export default function Cart() {
  const { items, fetchCart, updateQuantity, removeItem, total } = useCart();
  const navigate = useNavigate();

  useEffect(() => {
    fetchCart();
  }, []);

  if (items.length === 0) {
    return (
      <div style={{ padding: "2rem" }}>
        <h1>Your Cart</h1>
        <p>Cart is empty. <Link to="/">Go shopping</Link></p>
      </div>
    );
  }

  return (
    <div style={{ padding: "2rem", maxWidth: "600px" }}>
      <h1>Your Cart</h1>
      {items.map((item) => (
        <div key={item.id} style={rowStyle}>
          <div>
            <strong>{item.plant.name}</strong>
            <p>₹{item.plant.price} x {item.quantity}</p>
          </div>
          <div style={{ display: "flex", gap: "0.5rem", alignItems: "center" }}>
            <input
              type="number"
              min={1}
              value={item.quantity}
              onChange={(e) => updateQuantity(item.id, Number(e.target.value))}
              style={{ width: "50px" }}
            />
            <button onClick={() => removeItem(item.id)}>Remove</button>
          </div>
        </div>
      ))}
      <h2>Total: ₹{total}</h2>
      <button onClick={() => navigate("/checkout")} style={buttonStyle}>
        Proceed to Checkout
      </button>
    </div>
  );
}

const rowStyle: React.CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  borderBottom: "1px solid #ddd",
  padding: "1rem 0",
};

const buttonStyle: React.CSSProperties = {
  background: "#2f5233",
  color: "white",
  border: "none",
  padding: "0.6rem 1.2rem",
  borderRadius: "4px",
  cursor: "pointer",
  marginTop: "1rem",
};
