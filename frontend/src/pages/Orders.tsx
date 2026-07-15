import { useState,useEffect } from "react";
import api from "../api/client";
import type { Order } from "../types";

export default function Orders(){
    const [orders, setOrders] = useState<Order[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api .get("/orders")
            .then((res)=> setOrders(res.data))
            .finally(()=> setLoading(false));
    },[]);

    if (loading) return <p style={{ padding: "2rem"}}>Loading...</p>;
    if (orders.length === 0) {
        return <div style={{ padding: "2rem" }}>
            <h1>Your Orders</h1>
            <p> No orders yet.</p>
        </div>;
    }

    return(
        <div style={{ padding: "2rem", maxWidth: "600px"}}>
            <h1>Your Orders</h1>
            {orders.map((order) =>(
                <div key = {order.id} style={cardStyle}>
                    <h3>Order #{order.id} - {order.status}</h3>
                    {order.items.map((item, idx) =>(
                        <p key = {idx}> {item.plant.name} x {item.quantity} - ₹{item.price_at_purchase * item.quantity} </p>
                    ))}

                    <strong>Total : ₹{order.total}</strong>
                </div>
            ))}
        </div>
    );
}

const cardStyle : React.CSSProperties ={
    border: "1px solid #ddd",
    borderRadius: "8px",
    padding: "1rem",
    marginBottom: "1rem",

};