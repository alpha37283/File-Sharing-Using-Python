import React from "react";

function Header({ currentPath }) {
  return (
    <header className="bg-blue-600 text-white p-4">
      <h1 className="text-2xl font-bold">File Sharing System By</h1>
      <p className="text-sm mt-2">Muneeb Hussain Shah</p>
      <p className="text-sm mt-2">Muhammad Atif</p>
      <p className="text-sm mt-2">Kamran Wahab</p>
      <p className="text-sm mt-2">Current path: {currentPath}</p>
    </header>
  );
}

export default Header;
