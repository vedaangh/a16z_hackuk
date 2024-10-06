"use client";

import { useState } from 'react';
import { generateWebsite } from '../utils/generateWebsite';
import WebsitePreview from '../components/WebsitePreview';
import CodeViewer from '../components/CodeViewer';
import { Input, Button, Spinner } from '@nextui-org/react';

export default function Home() {
  const [userPrompt, setUserPrompt] = useState('');
  const [generatedWebsite, setGeneratedWebsite] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [debugInfo, setDebugInfo] = useState<string[]>([]);

  const handleGenerate = async () => {
    setIsLoading(true);
    setError(null);
    setDebugInfo([]);
    try {
      setDebugInfo(prev => [...prev, `Generating website with prompt: ${userPrompt}`]);
      const website = await generateWebsite(userPrompt);
      setDebugInfo(prev => [...prev, `Website generated successfully`]);
      setGeneratedWebsite(website);
    } catch (err) {
      console.error('Error generating website:', err);
      const errorMessage = err instanceof Error ? err.message : String(err);
      setError(errorMessage);
      setDebugInfo(prev => [...prev, `Error: ${errorMessage}`]);
      if (err instanceof Error && err.cause) {
        setDebugInfo(prev => [...prev, `Cause: ${JSON.stringify(err.cause)}`]);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-gray-900 text-white">
      {/* Sidebar */}
      <div className="w-64 bg-gray-800 p-4">
        <h2 className="text-xl font-bold mb-4">Explorer</h2>
        {generatedWebsite && (
          <ul>
            {generatedWebsite.pages.map((page: string) => (
              <li key={page}>{page}</li>
            ))}
            <li>styles.css</li>
          </ul>
        )}
      </div>

      {/* Main content area */}
      <div className="flex-1 flex flex-col">
        {/* Top bar */}
        <div className="bg-gray-800 p-2 flex items-center">
          <Input
            placeholder="Enter your website prompt"
            value={userPrompt}
            onChange={(e) => setUserPrompt(e.target.value)}
            className="flex-grow mr-2"
          />
          <Button
            color="primary"
            onClick={handleGenerate}
            disabled={isLoading}
          >
            {isLoading ? <Spinner size="sm" /> : 'Generate'}
          </Button>
        </div>

        {/* Code editor and preview */}
        <div className="flex-1 flex">
          {/* Code viewer */}
          <div className="flex-1 bg-gray-900 p-4 overflow-auto">
            {generatedWebsite && (
              <CodeViewer files={generatedWebsite.files} />
            )}
          </div>

          {/* Preview */}
          <div className="w-1/2 bg-white p-4">
            {generatedWebsite && (
              <WebsitePreview website={generatedWebsite} />
            )}
          </div>
        </div>

        {/* Bottom bar */}
        <div className="bg-gray-800 p-2 overflow-auto max-h-32">
          {debugInfo.map((info, index) => (
            <div key={index} className="text-green-400">{info}</div>
          ))}
          {error && <div className="text-red-400">{error}</div>}
        </div>
      </div>
    </div>
  );
}