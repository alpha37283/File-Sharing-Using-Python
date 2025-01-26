import React, { useState, useEffect } from "react";
import Header from "./Header";
import FileList from "./FileList";
import { fetchFiles } from "./utils/apis";

function App() {
  const [files, setFiles] = useState([]);
  const [currentPath, setCurrentPath] = useState("/");

  useEffect(() => {
    loadFiles(currentPath);
  }, [currentPath]);

  const loadFiles = async (path) => {
    try {
      const fetchedFiles = await fetchFiles(path);
      console.log("Files loaded:", fetchedFiles);
      setFiles(fetchedFiles);
    } catch (error) {
      console.error("Failed to load files:", error);
      setFiles([]);
    }
  };

  const handleFolderClick = (folderPath) => {
    setCurrentPath(folderPath);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Header currentPath={currentPath} />
      <main className="container mx-auto px-4 py-8">
        <FileList files={files} onFolderClick={handleFolderClick} currentPath={currentPath} />
      </main>
    </div>
  );
}

export default App;
