"use client";
import React, { useState } from "react";

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [question, setInputMessage] = useState("");
  const [isDarkMode, setIsDarkMode] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("Sem 5"); // Default category
  const [selectedBranch, setSelectedBranch] = useState(null);
  const [selectedSemester, setSelectedSemester] = useState(null);
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [loader, setLoader] = useState(false);
  const baseUrl = "https://d8f2-34-136-84-152.ngrok-free.app";
  const toggleDarkMode = () => {
    setIsDarkMode(!isDarkMode);
  };
  const handleIngest = async () => {
    try {
      setLoader(true);
      const requestOptions = {
        method: "GET",
        headers: {
          "ngrok-skip-browser-warning": "true",
        },
      };

      const url = baseUrl + "/ingest"; // Replace with your API endpoint

      const response = await fetch(url, requestOptions);
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      console.log(data.message);
      setLoader(false);
    } catch (error) {
      setLoader(false);
      console.error("Error:", error);
    }
  };
  const handleSendMessage = async () => {
    if (question.trim() !== "") {
      const newMessages = [...messages, { text: question, isUser: true }];
      setMessages(newMessages);

      setLoader(true);
      try {
        const requestOptions = {
          method: "GET",
          headers: {
            "ngrok-skip-browser-warning": "true",
          },
        };

        const url =
          baseUrl +
          "/rag?" +
          new URLSearchParams({
            query: question,
          }); // Replace with your API endpoint
        console.log(url);
        const response = await fetch(url, requestOptions);
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();
        console.log(data.message);

        const updatedMessages = [
          ...newMessages,
          {
            text: data.answer,
            isUser: false,
            date: new Date().toLocaleString(),
            time: data.time,
          },
        ];
        setMessages(updatedMessages);
        setInputMessage("");
        setLoader(false);
      } catch (error) {
        console.error("Error:", error);
      }
    }
  };

  const handleFileUpload = (e) => {
    if (selectedBranch && selectedSemester && selectedSubject) {
      const files = e.target.files;
      const fileArray = Array.from(files);
      const currentDate = new Date().toLocaleString();
      const filesWithDate = fileArray.map((file) => ({
        file,
        date: currentDate,
        branch: selectedBranch,
        semester: selectedSemester,
        subject: selectedSubject,
      }));
      setUploadedFiles([...uploadedFiles, ...filesWithDate]);
    }
  };

  const changeCategory = (category) => {
    setSelectedCategory(category);
    setSelectedBranch(null);
    setSelectedSemester(null);
    setSelectedSubject(null);
  };

  return (
    <div
      className={`h-screen ${
        isDarkMode
          ? "bg-gradient-to-b from-black to-gray-900 text-white"
          : "bg-gray-100 text-black"
      } flex flex-col`}
    >
      <div className='flex-1 flex'>
        <div
          className={`w-1/4 p-4 ${
            isDarkMode ? "bg-gray-900" : "bg-gray-200"
          } transition-all`}
        >
          {/* Profile Section */}
          <div className='p-4'>
            <h1>Dev Sanghvi</h1>
          </div>
          {/* Document Upload Section */}
          <div className='p-4'>
            <h2 className='text-lg font-semibold mb-2'>Upload Documents</h2>
            {/* Branch selection buttons */}
            <div className='mb-2'></div>
            {selectedCategory === "Sem 5" && (
              <div className='mb-2'>
                <button
                  onClick={() => setSelectedBranch("Computer Science")}
                  className={`${
                    selectedBranch === "Computer Science"
                      ? "bg-blue-500 text-white"
                      : "bg-gray-400 text-black"
                  } px-3 py-2 rounded-full cursor-pointer transition-all hover:bg-blue-400 hover:text-white`}
                >
                  Computer Science
                </button>
              </div>
            )}
            {selectedBranch === "Computer Science" && (
              <div className='mb-2'>
                <button
                  onClick={() => setSelectedSemester("Sem 5")}
                  className={`${
                    selectedSemester === "Sem 5"
                      ? "bg-blue-500 text-white"
                      : "bg-gray-400 text-black"
                  } px-3 py-2 rounded-full cursor-pointer transition-all hover:bg-blue-400 hover:text-white`}
                >
                  5th Sem
                </button>
              </div>
            )}
            {selectedSemester === "Sem 5" && (
              <div className='mb-2 '>
                {/* Add subject buttons for 5th Sem Computer Science */}
                <button
                  onClick={() => setSelectedSubject("Subject 1")}
                  className={`${
                    selectedSubject === "Subject 1"
                      ? "bg-blue-500 text-white"
                      : "bg-gray-400 text-black"
                  } px-3 py-2    rounded-full cursor-pointer transition-all hover-bg-blue-400 hover:text-white`}
                >
                  CYBRSECURITY
                </button>
                <button
                  onClick={() => setSelectedSubject("Subject 2")}
                  className={`${
                    selectedSubject === "Subject 2"
                      ? "bg-blue-500 text-white"
                      : "bg-gray-400 text-black"
                  } px-3 py-2 rounded-full cursor-pointer transition-all hover-bg-blue-400 hover:text-white`}
                >
                  CLOUD COMPUTING
                </button>
                <button
                  onClick={() => setSelectedSubject("Subject 3")}
                  className={`${
                    selectedSubject === "Subject 3"
                      ? "bg-blue-500 text-white"
                      : "bg-gray-400 text-black"
                  } px-3 py-2 rounded-full cursor-pointer transition-all hover-bg-blue-400 hover:text-white`}
                >
                  DATA SCIENCE
                </button>
                <button
                  onClick={() => setSelectedSubject("Subject 4")}
                  className={`${
                    selectedSubject === "Subject 4"
                      ? "bg-blue-500 text-white"
                      : "bg-gray-400 text-black"
                  } px-3 py-2 rounded-full cursor-pointer transition-all hover-bg-blue-400 hover:text-white`}
                >
                  IOT
                </button>
                <button
                  onClick={() => setSelectedSubject("Subject 5")}
                  className={`${
                    selectedSubject === "Subject 5"
                      ? "bg-blue-500 text-white"
                      : "bg-gray-400 text-black"
                  } px-3 py-2 rounded-full cursor-pointer transition-all hover-bg-blue-400 hover:text-white`}
                >
                  DAA
                </button>
                <button
                  onClick={() => setSelectedSubject("Subject 6")}
                  className={`${
                    selectedSubject === "Subject 1"
                      ? "bg-blue-500 text-white"
                      : "bg-gray-400 text-black"
                  } px-3 py-2 rounded-full cursor-pointer transition-all hover-bg-blue-400 hover:text-white`}
                >
                  MERN STACK
                </button>
              </div>
            )}
            {/* File input */}
            {selectedBranch && selectedSemester && selectedSubject && (
              <input
                type='file'
                accept='.pdf, .doc, .docx'
                multiple
                onChange={handleFileUpload}
                className='w-full p-2 border rounded-lg'
              />
            )}
            {/* Uploaded Documents */}
            <div className='mt-4'>
              <h3 className='text-lg font-semibold mb-2'>Uploaded Documents</h3>
              <div className='flex flex-col space-y-3'>
                {uploadedFiles
                  .filter(
                    (item) =>
                      item.branch === selectedBranch &&
                      item.semester === selectedSemester &&
                      item.subject === selectedSubject
                  )
                  .map((item, index) => (
                    <div
                      key={index}
                      className={`${
                        isDarkMode ? "bg-gray-900" : "bg-gray-200"
                      } p-3 rounded-lg flex justify-between items-center transition-all cursor-pointer hover-bg-gray-600`}
                    >
                      <div>
                        <p className='text-base font-semibold'>
                          {item.file.name}
                        </p>
                        <p className='text-sm text-gray-500'>{item.date}</p>
                      </div>
                      <a
                        href={URL.createObjectURL(item.file)}
                        download={item.file.name}
                        className='text-blue-500 hover:text-blue-600'
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
            isDarkMode ? "bg-gradient-to-b from-black to-gray-900" : "bg-white"
          }`}
        >
          {/* logo */}
          <div className='py-4 border-b border-gray-300 flex justify-center items-center'>
            <h2 className='text-2xl font-semibold'>BharatSamikshak</h2>
            <button
              onClick={toggleDarkMode}
              className={`${
                isDarkMode
                  ? "bg-blue-800 hover:bg-blue-700"
                  : "bg-gray-200 hover-bg-gray-300"
              } px-3 py-1 rounded-full ml-2 transition-all`}
            >
              {isDarkMode ? "Light" : "Dark"} Mode
            </button>
          </div>
          {/* Chat History */}
          <div
            className={`flex-1 overflow-y-scroll p-4 ${
              isDarkMode ? "text-white" : "text-black"
            }`}
          >
            {messages.map((message, index) => (
              <div
                key={index}
                className={`mb-4 ${
                  message.isUser ? "text-right" : "text-left"
                }`}
              >
                <div
                  className={`${
                    isDarkMode ? "bg-gray-900" : "bg-gray-200"
                  } p-3 rounded-lg flex justify-between items-center transition-all cursor-pointer hover-bg-gray-600`}
                >
                  <div>
                    <p
                      className={`text-base font-semibold ${
                        message.isUser ? "text-blue-500" : "text-black"
                      }`}
                    >
                      {message.text}
                    </p>
                    {message.isUser ? null : (
                      <div className='flex flex-col'>
                        <p className='text-sm text-black'>
                          Time Taken : {message.time}
                        </p>
                        <p className='text-sm text-gray-500'>{message.date}</p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
            {loader ? (
              <iframe
                src='https://giphy.com/embed/kUTME7ABmhYg5J3psM'
                width='100'
                height='80'
                frameBorder='0'
                className='giphy-embed'
                allowFullScreen
              ></iframe>
            ) : (
              ""
            )}
          </div>
          {/* Message Input Section */}
          <div
            className={`py-4 ${
              isDarkMode
                ? "bg-gradient-to-t from-black to-gray-900"
                : "bg-white"
            } flex justify-between items-center transition-all`}
          >
            <input
              type='text'
              placeholder='Type your message..'
              value={question}
              onChange={(e) => setInputMessage(e.target.value)}
              className={`w-3/4 p-3 m-3 rounded-full border ${
                isDarkMode ? "bg-gray-900" : "bg-gray-100"
              } ${
                isDarkMode ? "text-white" : "text-black"
              } focus:outline-none focus:ring-2 focus:ring-blue-400 transition-all`}
            />
            <button
              onClick={handleIngest}
              className={`px-4 py-2 rounded-full font-semibold transition-all ${
                isDarkMode
                  ? "bg-blue-500 hover:bg-blue-600 text-white"
                  : "bg-blue-400 hover:bg-blue-500 text-black"
              }`}
              // disabled={loader}
            >
              Ingest Document
            </button>
            <button
              onClick={handleSendMessage}
              className={`px-4 py-2 rounded-full font-semibold transition-all ${
                isDarkMode
                  ? "bg-blue-500 hover:bg-blue-600 text-white"
                  : "bg-blue-400 hover:bg-blue-500 text-black"
              }`}
              // disabled={loader}
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
