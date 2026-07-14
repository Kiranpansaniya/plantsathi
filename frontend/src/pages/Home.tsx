import { useState, useEffect } from "react";
import api  from "../api/client";
import { Plant } from "../types";
import PlantCard from "../components/PlantCard";

export default function Home() {
    const [ plants, setPlants] = useState<Plant[]>([]);
    const [search, setSearch] = useState(" ");
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api 
            .get("/plants")
            .then((res) => setPlants(res.data))
            .finally(() => setLoading(false));

    },[]);

    const filtered = plants.filter((p) =>
        p.name.toLowerCase().includes(search.toLowerCase())
    );

    if (loading) return <p style={{ padding : "2rem"}}> Loading plants ...</p>;

    return (
        <div style={{ padding : "2rem" }}>
            <h1> Our Plants </h1>
            <input
            type = "text"
            placeholder = "Search plants..."
            value = {search}
            onChange={(e) => setSearch(e.target.value)}
            style={{ padding : "0.5rem", width : "300px", marginBottom : "1.5rem"}}
            />
            <div
            style={{
                display : "grid",
                gridTemplateColumns : "repeat (auto-fill, minmax(200px, 1fr))",
                gap : "1.5rem",
                }}
            >
                {filtered.map((plant) =>(
                    <PlantCard key={plant.id} plant={plant} />
                ))}
            </div>
            {filtered.length === 0 && <p> No plants found .</p>}

        </div>
    );

}