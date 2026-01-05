import axios from "./axios";

export const login = async (username, password) => {
  const res = await axios.post("/api/auth/login", {
    username: username,
    password: password
  });
  return res.data;
};

export const getCurrentUser = async () => {
  const res = await axios.get("/api/auth/me");
  return res.data;
};

export const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
};