import { createContext, useContext, useState, useEffect} from "react";
import type {ReactNode} from "react";
import api from "../api/client";
import type{ User } from "../types";

interface AuthContextType {
  user: User | null;             
  login: (email: string, password: string) => Promise<void>;
  signup: (name: string, email: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;               
}


const AuthContext = createContext<AuthContextType | undefined>(undefined);


export function AuthProvider({ children }: { children: ReactNode }) {
  
  
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true); 

  
  useEffect(() => {
   
    const savedToken = localStorage.getItem("token");

    
    if (!savedToken) {
      setLoading(false);
      return;
    }
    api.get("/auth/me")
      .then((response) => {
        setUser(response.data);
      })
      .catch(() => {
        localStorage.removeItem("token");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  async function login(email: string, password: string) {
    
    const response = await api.post("/auth/login", { email, password });

    localStorage.setItem("token", response.data.access_token);

    setUser(response.data.user);
  }

  async function signup(name: string, email: string, password: string) {
    const response = await api.post("/auth/signup", { name, email, password });
    localStorage.setItem("token", response.data.access_token);
    setUser(response.data.user);
  }

  function logout() {
    localStorage.removeItem("token"); 
    setUser(null);                    
  }

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error("useAuth sirf AuthProvider ke andar use ho sakta hai");
  }

  return context;
}