
import { useState , useEffect } from "react";
import { useParams,useNavigate } from "react-router-dom";
import api from "../api/client";
import type { Plant } from "../types";
import { useAuth } from "../context/AuthContext";
import { useCart } from "../context/CartContext";

export default function PlantDetail(){
    const { id } = useParams();
    const [Plant , setPlant] = useState<Plant | null>(null);
    const [quantity , setQuantity ]= useState(1);
    const { user } = useAuth();
    const { addToCart } = useCart();
    const navigate = useNavigate();

    useEffect(() => {
        api.get(`/plants/${id}`). then((res) => setPlant(res.data));
    },[id]);

    async function handleAddToCart() {
        if (!user){
            navigate("/login")
            return;
        }
        
        await addToCart(Plant!.id,quantity);
        alert("Added To Cart!");
    }

    if (!Plant) return <p style={{ padding : "2rem"}}>Loading...</p>;

    return (
        <div style={{ padding : "2rem",maxWidth : "600px"}}>
            <div style={{ fontSize : "5rem", textAlign : "center"}}>🪴</div>
            <h1> {Plant.name}</h1>
            <p style={{ color : "#666"}}>{Plant.category}</p>
            <p style={{ fontSize : "1.5rem", fontWeight : "bold", color : "#2f5233"}}>
                ₹{Plant.price}
            </p>
            <p>{Plant.description}</p>
            <p>Stock : {Plant.stock > 0 ? Plant.stock : "Out Of Stock"}</p>
            {Plant.stock > 0 && (
                <div style={{ display : "flex", gap : "1rem",alignItems : "center", marginTop : "1rem"}}>
                    
                    <input type="number" min={Plant.stock} value={quantity}
                    onChange={(e) => setQuantity(Number(e.target.value))}
                    style={{ width : "60px", padding : "0.4rem"}}/>

                    <button onClick={handleAddToCart} style={buttonStyle}>
                        Add To Cart
                    </button>
                </div>
            )}

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
};