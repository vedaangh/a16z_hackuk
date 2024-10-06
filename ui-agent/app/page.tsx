"use client";

import { useState } from 'react';
import { generateWebsite } from '../utils/generateWebsite';
import WebsitePreview from '../components/WebsitePreview';
import CodeViewer from '../components/CodeViewer';
import { Input, Button, Tabs, Card, Spinner } from '@nextui-org/react';

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
    <div className="min-h-screen bg-gradient-to-br from-gray-900 to-gray-800 text-white p-4">
      <div className="container mx-auto max-w-4xl">
        <h1 className="text-4xl md:text-5xl font-bold mb-8 text-center bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-600">
          AI Website Generator
        </h1>
        <Card className="bg-gray-800 border border-gray-700 p-4 mb-8">
          <div className="flex flex-col md:flex-row items-center gap-4">
            <Input
              size="lg"
              placeholder="Enter your website prompt"
              value={userPrompt}
              onChange={(e) => setUserPrompt(e.target.value)}
              className="w-full md:flex-grow"
            />
            <Button
              color="primary"
              size="lg"
              onClick={handleGenerate}
              disabled={isLoading}
              className="w-full md:w-auto bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700"
            >
              {isLoading ? <Spinner size="sm" /> : 'Generate'}
            </Button>
          </div>
        </Card>

        {isLoading && (
          <div className="text-center py-8">
            <Spinner size="lg" color="primary" />
            <p className="mt-4">Generating your website... This may take a few moments.</p>
          </div>
        )}

        {error && (
          <Card className="bg-red-900 text-red-100 border border-red-700 p-4 mb-4">
            <h3 className="font-bold">Error:</h3>
            <p>{error}</p>
          </Card>
        )}

        {debugInfo.length > 0 && (
          <Card className="bg-gray-800 border border-gray-700 p-4 mb-4">
            <h3 className="font-bold mb-2">Debug Information:</h3>
            <ul className="list-disc pl-5">
              {debugInfo.map((info, index) => (
                <li key={index}>{info}</li>
              ))}
            </ul>
          </Card>
        )}

        {generatedWebsite && (
          <Card className="bg-gray-800 border border-gray-700 p-4">
            <Tabs 
              aria-label="Website view options"
              color="primary"
              variant="bordered"
              className="mt-4"
            >
              <Tabs.Item key="preview" title="Preview">
                <WebsitePreview website={generatedWebsite} />
              </Tabs.Item>
              <Tabs.Item key="code" title="Code">
                <CodeViewer files={generatedWebsite.files} />
              </Tabs.Item>
            </Tabs>
          </Card>
        )}
      </div>
    </div>
  );
}