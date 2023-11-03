import React, { useState } from 'react';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('Sem 5'); // Default category

  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };

  const handleSendMessage = () => {
    if (inputMessage.trim() !== '') {
      const newMessages = [...messages, { text: inputMessage, isUser: true }];
      setMessages(newMessages);
      setInputMessage('');

    // idhar chatbot / model response ka logic 
      setTimeout(() => {
        const chatbotResponse = 'This is a chatbot response.';
        const updatedMessages = [...newMessages, { text: chatbotResponse, isUser: false }];
        setMessages(updatedMessages);
      }, 1000);
    }
  };

  const handleFileUpload = (e) => {
    const files = e.target.files;
    const fileArray = Array.from(files);
    const currentDate = new Date().toLocaleString();
    const filesWithDate = fileArray.map((file) => ({
      file,
      date: currentDate,
      category: selectedCategory,
    }));
    setUploadedFiles([...uploadedFiles, ...filesWithDate]);
  };

  const changeCategory = (category) => {
    setSelectedCategory(category);
  };

  return (
    <div
      className={`h-screen ${
        isDarkMode
          ? 'bg-gradient-to-b from-gray-900 to-gray-800 text-white'
          : 'bg-gray-100 text-black'
      } flex flex-col`}
    >
      <div className="flex-1 flex">
        <div
          className={`w-1/4 p-4 ${
            isDarkMode ? 'bg-gray-700' : 'bg-gray-200'
          } transition-all`}
        >
          {/* Profile Section */}
          <div className="p-4">
            {/* ... Profile section content ... */}
            <h1>Dev Sanghvi</h1>
          </div>
          {/* Document Upload Section */}
          <div className="p-4">
            <h2 className="text-lg font-semibold mb-2">Upload Documents</h2>
            <input
              type="file"
              accept=".pdf, .doc, .docx"
              multiple
              onChange={handleFileUpload}
              className="w-full p-2 border rounded-lg"
            />
            <div className="mt-4">
              <h3 className="text-lg font-semibold mb-2">Uploaded Documents</h3>
              {/* Category selection buttons */}
              <div className="mb-2">
                <button
                  onClick={() => changeCategory('Sem 5')}
                  className={`${
                    selectedCategory === 'Sem 5'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-400 text-black'
                  } px-3 py-2 rounded-full mr-2 cursor-pointer transition-all hover:bg-blue-400 hover:text-white`}
                >
                  Sem 5
                </button>
                <button
                  onClick={() => changeCategory('Sem 6')}
                  className={`${
                    selectedCategory === 'Sem 6'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-400 text-black'
                  } px-3 py-2 rounded-full cursor-pointer transition-all hover:bg-blue-400 hover:text-white`}
                >
                  Sem 6
                </button>
               
              </div>
              <div className="flex flex-col space-y-3">
                {uploadedFiles
                  .filter((item) => item.category === selectedCategory)
                  .map((item, index) => (
                    <div
                      key={index}
                      className={`${
                        isDarkMode ? 'bg-gray-700' : 'bg-gray-200'
                      } p-3 rounded-lg flex justify-between items-center transition-all cursor-pointer hover:bg-gray-600`}
                    >
                      <div>
                        <p className="text-base font-semibold">
                          {item.file.name}
                        </p>
                        <p className="text-sm text-gray-500">{item.date}</p>
                      </div>
                      <a
                        href={URL.createObjectURL(item.file)}
                        download={item.file.name}
                        className="text-blue-500 hover:text-blue-600"
                      >
                        Download
                      </a>
                    </div>
                  ))}
              </div>
            </div>
          </div>
        </div>
        <div
          className={`w-3/4 p-4 ${
            isDarkMode
              ? 'bg-gradient-to-b from-gray-800 to-gray-700'
              : 'bg-white'
          }`}
        >
          {/* logo */}
          <div className="py-4 border-b border-gray-300 flex justify-center items-center">
            <h2 className="text-2xl font-semibold">
              BharatSamikshak
            </h2>
            <button
              onClick={toggleDarkMode}
              className={`${
                isDarkMode
                  ? 'bg-gray-700 hover:bg-gray-600'
                  : 'bg-gray-200 hover-bg-gray-300'
              } px-3 py-1 rounded-full ml-2 transition-all`}
            >
              {isDarkMode ? 'Light' : 'Dark'} Mode
            </button>
          </div>
          {/* Chat History */}
          <div
            className={`flex-1 overflow-y-scroll p-4 ${
              isDarkMode ? 'text-gray-300' : 'text-black'
            }`}
          >
            {messages.map((message, index) => (
              <div key={index} className={`mb-4 ${message.isUser ? 'text-right' : 'text-left'}`}>
                <div
                  className={`${
                    isDarkMode ? 'bg-gray-700' : 'bg-gray-200'
                  } p-3 rounded-lg flex justify-between items-center transition-all cursor-pointer hover-bg-gray-600`}
                >
                  <div>
                    <p className={`text-base font-semibold ${message.isUser ? 'text-blue-500' : 'text-black'}`}>
                      {message.text}
                    </p>
                    {message.isUser ? null : (
                      <p className="text-sm text-gray-500">{new Date().toLocaleString()}</p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
          {/* Message Input Section */}
          <div
            className={`py-4 ${
              isDarkMode ? 'bg-gradient-to-t from-gray-800 to-gray-700' : 'bg-white'
            } flex justify-between items-center transition-all`}
          >
            <input
              type="text"
              placeholder="Type your message.."
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              className={`w-3/4 p-3 m-3 rounded-full border ${
                isDarkMode ? 'bg-gray-700' : 'bg-gray-100'
              } ${
                isDarkMode ? 'text-white' : 'text-black'
              } focus:outline-none focus:ring-2 focus:ring-blue-400 transition-all`}
            />
            <button
              onClick={handleSendMessage}
              className={`px-4 py-2 rounded-full font-semibold transition-all ${
                isDarkMode
                  ? 'bg-blue-500 hover:bg-blue-600 text-white'
                  : 'bg-blue-400 hover:bg-blue-500 text-black'
              }`}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;
