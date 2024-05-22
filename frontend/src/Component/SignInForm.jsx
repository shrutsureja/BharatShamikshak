import React, { useState } from 'react';

const SignInForm = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [department, setDepartment] = useState('Select Department');
  const [semester, setSemester] = useState('Select Semester');
  const [error, setError] = useState('');

  const departments = ['Computer Science', 'Electrical Engineering', 'Mechanical Engineering', 'Civil Engineering'];
  const semesters = ['Semester 1', 'Semester 2', 'Semester 3', 'Semester 4', 'Semester 5', 'Semester 6', 'Semester 7', 'Semester 8'];

  const handleSignIn = (e) => {
    e.preventDefault();

    // Validation section
    if (!username || !password || department === 'Select Department' || semester === 'Select Semester') {
      setError('Please fill in all fields.');
      return;
    }


    console.log('Username:', username);
    console.log('Password:', password);
    console.log('Department:', department);
    console.log('Semester:', semester);

    // Reset form and clear any error
    setUsername('');
    setPassword('');
    setDepartment('Select Department');
    setSemester('Select Semester');
    setError('');
  };

  return (
    <div className="w-96 mx-auto mt-8">
      <h1 className="text-2xl font-bold mb-4">Sign In</h1>
      {error && <div className="text-red-500 mb-4">{error}</div>}
      <form onSubmit={handleSignIn}>
        <div className="mb-4">
          <label htmlFor="username" className="block text-sm font-medium text-gray-700">Username</label>
          <input
            type="text"
            id="username"
            className="w-full px-4 py-2 border rounded-lg"
            placeholder="Enter your username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
        </div>
        <div className="mb-4">
          <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
          <input
            type="password"
            id="password"
            className="w-full px-4 py-2 border rounded-lg"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <div className="mb-4">
          <label htmlFor="department" className="block text-sm font-medium text-gray-700">Department</label>
          <select
            id="department"
            className="w-full px-4 py-2 border rounded-lg"
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
          >
            <option value="Select Department" disabled>Select Department</option>
            {departments.map((dept) => (
              <option key={dept} value={dept}>
                {dept}
              </option>
            ))}
          </select>
        </div>
        <div className="mb-4">
          <label htmlFor="semester" className="block text-sm font-medium text-gray-700">Semester</label>
          <select
            id="semester"
            className="w-full px-4 py-2 border rounded-lg"
            value={semester}
            onChange={(e) => setSemester(e.target.value)}
          >
            <option value="Select Semester" disabled>Select Semester</option>
            {semesters.map((sem) => (
              <option key={sem} value={sem}>
                {sem}
              </option>
            ))}
          </select>
        </div>
        <button
          type="submit"
          className="w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
        >
          Sign In
        </button>
      </form>
    </div>
  );
};

export default SignInForm;
