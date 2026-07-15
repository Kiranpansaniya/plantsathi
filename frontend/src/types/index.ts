export interface Plant{
    id : number;
    name : string;
    category : string;
    price : number;
    stock : number;
    description : string;
    image_url : string;

}
export interface User{
    id : number;
    name : string;
    email : string;
    is_admin : boolean;
}
export interface CartItem{
    id : number;
    plant_id : number;
    quantity : number;
    plant : Plant
}
export interface OrderItem{
    plant_id : number;
    quantity : number;
    price_at_purchase : number;
    plant : Plant;
}
export interface Order{
        id : number;
        total : number;
        status : string;
        items : OrderItem[];
}