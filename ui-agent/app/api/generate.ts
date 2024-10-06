import type { NextApiRequest, NextApiResponse } from 'next';
import { spawn } from 'child_process';
import path from 'path';

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    const { prompt } = req.body;
    console.log('Received prompt:', prompt);

    const scriptPath = path.resolve(process.cwd(), 'test_utils.py');
    console.log('Executing Python script:', scriptPath);
    console.log('MISTRAL_API_KEY is set:', !!process.env.MISTRAL_API_KEY);

    const pythonProcess = spawn('python', [scriptPath, prompt], {
      env: { ...process.env, MISTRAL_API_KEY: process.env.MISTRAL_API_KEY }
    });

    let result = '';
    let errorOutput = '';

    pythonProcess.stdout.on('data', (data) => {
      console.log('Python script output:', data.toString());
      result += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      console.error('Python script error:', data.toString());
      errorOutput += data.toString();
    });

    pythonProcess.on('close', (code) => {
      console.log('Python script finished with code:', code);
      if (code !== 0) {
        console.error('Python script execution failed');
        console.error('Error output:', errorOutput);
        res.status(500).json({ error: 'Python script execution failed', details: errorOutput });
      } else {
        try {
          console.log('Raw Python script output:', result);
          let parsedResult;
          try {
            parsedResult = JSON.parse(result);
          } catch (parseError) {
            console.error('Failed to parse Python script output as JSON');
            res.status(500).json({ 
              error: 'Failed to parse Python script output as JSON', 
              details: String(parseError),
              rawOutput: result 
            });
            return;
          }
          console.log('Parsed result:', parsedResult);
          res.status(200).json(parsedResult);
        } catch (error) {
          console.error('Unexpected error while processing Python script output:', error);
          res.status(500).json({ 
            error: 'Unexpected error while processing Python script output', 
            details: error instanceof Error ? error.message : String(error),
            rawOutput: result 
          });
        }
      }
    });

    pythonProcess.on('error', (error) => {
      console.error('Failed to start Python process:', error);
      res.status(500).json({ error: 'Failed to start Python process', details: error.message });
    });

  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}