import { createContext,useContext,useState } from "react";
import type { ReactNode } from "react";
import api from "../api/client";
import type { CartItem } from "../types";
import { useAuth } from "./AuthContext";

interface CartContextType{
    items :CartItem[];
    fetchCart:()=>Promise<void>;
    addToCart:(plantid:number,quantity?:number)=>Promise<void>;
    updateQuantity:(itemid:number,quantity:number)=>Promise<void>;
    removeItem:(itemid:number)=>Promise<void>;
    total:number;
}
const CartContext = createContext<CartContextType|undefined>(undefined);
export function CartProvider({children}:{children:ReactNode}){
    const [items,setitems]=useState<CartItem[]>([]);
    const {user} = useAuth();

    async function fetchCart(){
        if(!user)return;
        const res = await api.get("/cart");
        setitems(res.data);
    }
    async function addToCart(plantid:number,quantity:number=1) {
        await api.post("/cart",{plant_id:plantid,quantity});
        await fetchCart();
    }
    async function updateQuantity(itemid:number,quantity:number) {
        await api.put(`/cart/${itemid}`,{quantity});
        await fetchCart();
    }
    async function removeItem(itemid:number) {
        await api.delete(`/cart/${itemid}`);
        await fetchCart();
    }
    const total = items.reduce((sum,item)=>sum+item.plant.price*item.quantity,0);
    return(
        <CartContext.Provider value={{ items, fetchCart, addToCart, updateQuantity, removeItem, total }}>{children}</CartContext.Provider>
    );
}

export function useCart(){
    const ctx = useContext(CartContext);
    if(!ctx) throw new Error("useCart must be used within CartProvider");
    return ctx;
}