import { Link } from "react-router-dom";
import type { Plant } from "../types";


export default function PlantCard({ plant }: { plant: Plant }) {
    return (
        <Link to= {'/plants/${plant.id}'} style={styles.card}>
            <div style={styles.imagePlaceholder}>🪴</div>
            <h3>{plant.name}</h3>
            <p style={styles.category}>{plant.category}</p>
            <p style={styles.price}>₹{plant.price}</p>

        </Link>
    );
}

const styles: { [key: string]: React.CSSProperties } = {
    card : {
        display : "block" ,
        border : "1px solid #ddd" ,
        borderRadius : "8px" ,
        padding : "1rem" ,
        textDecoration : "none" ,
        color : "#222" ,
        textAlign : "center" ,
        transition : "transform 0.2s" ,
    },

    imagePlaceholder : {
        fontSize : "3rem",
        marginBottom : "0.5rem"
    },
    category : {
        color : "#666" ,
        fontSize : "0.9rem"
    },
    price : {
        fontWeight : "bold",
        color : "#2f5233"
    },    

};