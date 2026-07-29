import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '../api';
import { AuthContext } from './auth-context';

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
          const userData = await api('/users/me');
          const schoolData = await api('/schools/my');
          setUser(userData);
          setSchool(schoolData);
        } catch (error) {
          console.error("Ma'lumotlarni olishda xatolik:", error);
          localStorage.removeItem('token');
          setUser(null);
          setSchool(null);
        }
      }
      setLoading(false);
    };

    fetchUser();
  }, []);

  const login = async (token) => {
    localStorage.setItem('token', token);
    try {
      const userData = await api('/users/me');
      const schoolData = await api('/schools/my');
      setUser(userData);
      setSchool(schoolData);

      const ROLE_HOME = {
        student: '/student-dashboard',
        accountant: '/payments',
        admin: '/dashboard',
        manager: '/dashboard',
        teacher: '/dashboard',
        curator: '/dashboard',
      };

      navigate(ROLE_HOME[userData.role] || '/dashboard');
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

  const refreshUser = async () => {
    if (!localStorage.getItem('token')) return;
    const userData = await api('/users/me');
    setUser(userData);
  };

  return (
    <AuthContext.Provider value={{ user, school, loading, login, logout, refreshUser }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
