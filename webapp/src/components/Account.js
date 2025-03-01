// // src/components/Account.js
// import React, { useEffect, useState } from 'react';
// import axios from 'axios';

// const API_BASE_URL = 'http://localhost:80'; // Adjust based on your API Gateway

// const Account = () => {
//     const [accounts, setAccounts] = useState([]);
//     const [username, setUsername] = useState('');
//     const [password, setPassword] = useState('');
//     const [name, setName] = useState(''); // New state for account name
//     const [error, setError] = useState('');
//     const [successMessage, setSuccessMessage] = useState(''); // New state for success messages

//     const fetchAccounts = async () => {
//         try {
//             const response = await axios.get(`${API_BASE_URL}/accounts`);
//             setAccounts(response.data.data); // Adjust based on your API response structure
//         } catch (err) {
//             console.error(err);
//         }
//     };

//     const handleLogin = async (e) => {
//         e.preventDefault();
//         try {
//             const response = await axios.post(`${API_BASE_URL}/token`, { username, password });
//             console.log('Login successful:', response.data);
//             setSuccessMessage('Account successfully logged in!'); // Success message for login
//             fetchAccounts(); // Fetch accounts after successful login
//         } catch (err) {
//             setError('Login failed. Please check your credentials.');
//             console.error(err);
//         }
//     };

//     const handleCreateAccount = async (e) => {
//         e.preventDefault();
//         try {
//             const response = await axios.post(`${API_BASE_URL}/accounts/create`, { name, username, password });
//             console.log('Account created:', response.data);
//             setSuccessMessage('Account successfully created!'); // Success message for account creation
//             setName(''); // Clear the name input
//             setUsername(''); // Clear the username input
//             setPassword(''); // Clear the password input
//         } catch (err) {
//             setError('Account creation failed. Please try again.');
//             console.error(err);
//         }
//     };

//     useEffect(() => {
//         fetchAccounts();
//     }, []);

//     return (
//         <div>
//             <h1>Login</h1>
//             <form onSubmit={handleLogin}>
//                 <input
//                     type="text"
//                     placeholder="Username"
//                     value={username}
//                     onChange={(e) => setUsername(e.target.value)}
//                     required
//                 />
//                 <input
//                     type="password"
//                     placeholder="Password"
//                     value={password}
//                     onChange={(e) => setPassword(e.target.value)}
//                     required
//                 />
//                 <button type="submit">Login</button>
//             </form>
//             {error && <p>{error}</p>}
//             {successMessage && <p>{successMessage}</p>} {/* Display success message */}

//             <h1>Create Account</h1>
//             <form onSubmit={handleCreateAccount}>
//                 <input
//                     type="text"
//                     placeholder="Name"
//                     value={name}
//                     onChange={(e) => setName(e.target.value)}
//                     required
//                 />
//                 <input
//                     type="text"
//                     placeholder="Username"
//                     value={username}
//                     onChange={(e) => setUsername(e.target.value)}
//                     required
//                 />
//                 <input
//                     type="password"
//                     placeholder="Password"
//                     value={password}
//                     onChange={(e) => setPassword(e.target.value)}
//                     required
//                 />
//                 <button type="submit">Create Account</button>
//             </form>

//             <h2>Accounts</h2>
//             <ul>
//                 {accounts.map(account => (
//                     <li key={account.userId}>{account.name} - {account.username}</li>
//                 ))}
//             </ul>
//         </div>
//     );
// };

// export default Account;