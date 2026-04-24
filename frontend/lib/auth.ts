const TOKEN_KEY = "token";

// 💾 SAVE TOKEN
export const setToken = (token: string) => {
  localStorage.setItem(TOKEN_KEY, token);
};

// 📥 GET TOKEN
export const getToken = () => {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
};

// ❌ REMOVE TOKEN
export const removeToken = () => {
  localStorage.removeItem(TOKEN_KEY);
};