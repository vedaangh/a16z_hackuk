import { useState } from 'react';

const WebsitePreview = ({ website }) => {
  const [currentPage, setCurrentPage] = useState('index.html');

  return (
    <div>
      <div className="mb-4">
        {website.pages.map((page) => (
          <button
            key={page}
            onClick={() => setCurrentPage(page)}
            className={`mr-2 px-3 py-1 rounded ${
              currentPage === page ? 'bg-blue-500 text-white' : 'bg-gray-200'
            }`}
          >
            {page}
          </button>
        ))}
      </div>
      <iframe
        src={`/generated_website/${currentPage}`}
        className="w-full h-[600px] border-none"
      />
    </div>
  );
};

export default WebsitePreview;