import { create } from "zustand";
import { login as loginApi } from "@/lib/api";

type User = {
  id: number;
  token: string;
};

type AuthState = {
  user: User | null;
  login: (email: string, password: string) => Promise<boolean>;
  logout: () => void;
  hydrate: () => void;
};

export const useAuth = create<AuthState>((set) => ({
  user: null,

  login: async (email, password) => {
    try {
      const data = await loginApi(email, password);

      const user = {
        id: data.user_id,
        token: data.access_token,
      };

      localStorage.setItem("user", JSON.stringify(user));
      set({ user });

      return true;
    } catch (err) {
      console.error(err);
      return false;
    }
  },

  logout: () => {
    localStorage.removeItem("user");
    set({ user: null });
  },

  hydrate: () => {
    const userStr = localStorage.getItem("user");
    if (userStr) {
      set({ user: JSON.parse(userStr) });
    }
  },
}));