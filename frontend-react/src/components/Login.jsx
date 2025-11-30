// src/components/Login.jsx
import { useState } from 'react';

const API_URL = 'http://127.0.0.1:3000';

function Login({ onLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const response = await fetch(`${API_URL}/token`, {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const data = await response.json();
        // Buscar informações do usuário
        const userResponse = await fetch(`${API_URL}/users/me/`, {
          headers: {
            'Authorization': `Bearer ${data.access_token}`
          }
        });
        
        if (userResponse.ok) {
          const user = await userResponse.json();
          onLogin(data.access_token, user);
        } else {
          onLogin(data.access_token, { username, role: 'visualizacao' });
        }
      } else {
        if (response.status === 401) {
          setError('Usuário ou senha incorretos');
        } else {
          setError(`Erro do servidor: ${response.status} ${response.statusText}`);
        }
      }
    } catch (error) {
      console.error('Erro ao fazer login:', error);
      if (error.message === 'Failed to fetch') {
        setError(`Não foi possível conectar ao servidor. Verifique se o backend está rodando em ${API_URL}`);
      } else {
        setError(`Erro ao conectar com o servidor: ${error.message}`);
      }
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-6">
          Login
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          {error && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Username
            </label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Senha
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              required
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 font-semibold"
          >
            Entrar
          </button>
        </form>
        <div className="mt-4 text-sm text-gray-600 text-center space-y-1">
          <p className="font-semibold">Credenciais padrão:</p>
          <p>👑 Admin: admin / admin123</p>
          <p>📊 Gerencial: gerencial / gerencial123</p>
          <p>👁️ Usuário: usuario / usuario123</p>
        </div>
      </div>
    </div>
  );
}

export default Login;
