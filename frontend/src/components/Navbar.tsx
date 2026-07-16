import { Link,useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import {useCart} from "../context/CartContext";

export default function Navbar(){
    const {user,logout}=useAuth();
    const {items}=useCart();
    const navigate = useNavigate();

    function handleLogout(){
        logout();
        navigate("/");
    }
    return(
        <nav style={styles.nav}>
            <Link to="/" style={styles.logo}>🪴PlantSaathi</Link>
            <div style={styles.link}>
                <Link to ="/" style={styles.link}>Home</Link>
                {user?(
                    <>
                    <Link to="/cart" style={styles.link}>Cart ({items.length})</Link>
                    <Link to="/orders" style={styles.link}>Orders</Link>
                    <span style={styles.link}>Hi,{user.name}</span>
                    <button onClick={handleLogout} style={styles.button}>  Logout   </button>
                    </>
                ):(<>
                <Link to="/login" style={styles.link}>   Login   </Link>
                <Link to="/signup" style={styles.link}>  Signup   </Link>
                </>
            )}
            </div>
        </nav>  
    );
}
const styles : {[key:string]:React.CSSProperties}={
    nav:{
        display:"flex",
        justifyContent:"space-between",
        alignItems:"center",
        padding:"1rem 2rem",
        backgroundColor:"#2f5233",
        color:"white",
    },
    logo:{fontSize:"1.4rem",fontWeight:"bold",color:"white",textDecoration:"none"},
    links:{display:"flex",gap:"2rem",alignItems:"center"},
    link:{color:"white",textDecoration:"none"},
    button : {
        background:"white",
        color:"#2f5233",
        border:"none",
        padding:"0.4rem 0.8rem",
        borderRadius:"4px",
        cursor:"pointer",
    },
};
