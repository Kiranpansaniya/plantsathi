import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/client";
import { useCart } from "../context/CartContext";

export default function Checkout(){
    const { items, total, fetchCart } = useCart();
    const[loading, setLoading ] = useState(false);
    const [error, setError ] = useState("");
    const navigate = useNavigate();

    async function handlePlaceOrder() {
        setLoading(true);
        setError("");
        try {
            const res = await api.post("/checkout");
            await fetchCart();
            navigate('/orders',{ state : {newOrderId : res.data.id}});
            
        } catch(err: any){
            setError(err.response?.data?.detail || " Checkout Failed");
        } finally{
            setLoading(false);
        }
        
    }

    return (
        <div style={{ padding : "2rem", maxWidth : "500px"}}>
            <h1>Checkout</h1>
            {items.map((item) => (
                <div key={item.id} style={{ display: "flex", justifyContent : "space-between"}}>
                    <span>{item.plant.name} x {item.quantity}</span>
                    <span>₹{item.plant.price * item.quantity}</span>
                </div> 
            ))}

            <hr/>
            <h2>Total : ₹{total}</h2>
            {error && <p style={{ color: "red"}}>{error}</p>}
            <button onClick={handlePlaceOrder} disabled ={loading} style={buttonStyle}>
                {loading ? "Placing order...": "Confirm Order"}
            </button>
        </div>
    );
}

const buttonStyle : React.CSSProperties = {
    background : "#2f5233",
    color : "white",
    border : "none",
    padding : "0.6rem 1.2rem",
    borderRadius : "4px",
    cursor : "pointer",
    marginTop :"1rem",

};