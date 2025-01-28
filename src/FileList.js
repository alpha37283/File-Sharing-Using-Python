import React from "react";
import { FaFolder, FaFile, FaArrowLeft } from "react-icons/fa";

function FileList({ files, onFolderClick, currentPath }) {
  const handleDownload = (fileName) => {
    const downloadUrl = `/download${currentPath}${fileName}`;
    window.open(downloadUrl, "_blank");
  };

  const handleGoBack = () => {
    const parentPath = currentPath.slice(0, currentPath.lastIndexOf("/", currentPath.length - 2) + 1);
    onFolderClick(parentPath || "/");
  };

  return (
    <div className="bg-white shadow-md rounded-lg overflow-hidden">
      <table className="w-full">
        <thead className="bg-gray-50">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Name
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Size
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Last Modified
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {currentPath !== "/" && (
            <tr className="hover:bg-gray-50">
              <td
                className="px-6 py-4 whitespace-nowrap text-blue-600 hover:underline cursor-pointer"
                colSpan="4"
                onClick={handleGoBack}
              >
                <FaArrowLeft className="inline mr-2" />
                Back
              </td>
            </tr>
          )}
          {files.map((file, index) => (
            <tr key={index} className="hover:bg-gray-50">
              <td className="px-6 py-4 whitespace-nowrap">
                <div className="flex items-center">
                  {file.isDirectory ? (
                    <FaFolder className="h-5 w-5 text-yellow-500 mr-2" />
                  ) : (
                    <FaFile className="h-5 w-5 text-gray-400 mr-2" />
                  )}
                  <span
                    className={`${
                      file.isDirectory ? "cursor-pointer text-blue-600 hover:underline" : ""
                    }`}
                    onClick={() => file.isDirectory && onFolderClick(`${currentPath}${file.name}/`)}
                  >
                    {file.name}
                  </span>
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {file.size ? `${file.size} bytes` : "-"}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {new Date(file.lastModified * 1000).toLocaleString()}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {!file.isDirectory && (
                  <button
                    onClick={() => handleDownload(file.name)}
                    className="text-blue-600 hover:text-blue-800"
                  >
                    Download
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default FileList;