import React, { createContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [school, setSchool] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const userRes = await fetch('http://localhost:8000/api/v1/users/me', {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          const schoolRes = await fetch('http://localhost:8000/api/v1/schools/my', {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          
          if (userRes.ok && schoolRes.ok) {
            const userData = await userRes.json();
            const schoolData = await schoolRes.json();
            setUser(userData);
            setSchool(schoolData);
          } else {
            localStorage.removeItem('token');
            setUser(null);
            setSchool(null);
          }
        } catch (error) {
          console.error("Ma'lumotlarni olishda xatolik:", error);
        }
      }
      setLoading(false);
    };

    fetchUser();
  }, []);

  const login = async (token) => {
    localStorage.setItem('token', token);
    try {
      const userRes = await fetch('http://localhost:8000/api/v1/users/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const schoolRes = await fetch('http://localhost:8000/api/v1/schools/my', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (userRes.ok && schoolRes.ok) {
        const userData = await userRes.json();
        const schoolData = await schoolRes.json();
        setUser(userData);
        setSchool(schoolData);
        navigate('/');
      }
    } catch (error) {
      console.error("Login vaqtida xatolik:", error);
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setUser(null);
    setSchool(null);
    navigate('/login');
  };

  return (
    <AuthContext.Provider value={{ user, school, loading, login, logout }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
