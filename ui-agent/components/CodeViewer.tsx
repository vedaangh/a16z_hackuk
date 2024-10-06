import { useState } from 'react';

const CodeViewer = ({ files }) => {
  const [currentFile, setCurrentFile] = useState(Object.keys(files)[0]);

  return (
    <div>
      <div>
        {Object.keys(files).map((file) => (
          <button key={file} onClick={() => setCurrentFile(file)}>
            {file}
          </button>
        ))}
      </div>
      <pre>
        <code>{files[currentFile]}</code>
      </pre>
    </div>
  );
};

export default CodeViewer;