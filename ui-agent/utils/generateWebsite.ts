import axios from 'axios';

export const generateWebsite = async (userPrompt: string) => {
  console.log('Generating website with prompt:', userPrompt);
  try {
    console.log('Sending request to /api/generate');
    const response = await axios.post('/api/generate', { prompt: userPrompt });
    console.log('Received response from /api/generate:', response.data);

    const result = response.data;

    if (typeof result === 'object' && result !== null) {
      if (result.message) {
        console.error('Unexpected response from server:', result.message);
        throw new Error(`Unexpected response from server: ${result.message}`);
      }

      if (result.error) {
        console.error('Error from Python script:', result.error);
        console.error('Error details:', result.details);
        if (result.traceback) console.error('Traceback:', result.traceback);
        throw new Error(`Python script error: ${result.error}. Details: ${result.details}`);
      }

      if (!result.pages || !result.css || !result.output_dir) {
        console.error('Invalid response structure:', result);
        throw new Error(`Invalid response structure from server: ${JSON.stringify(result)}`);
      }

      const website = {
        pages: ['index.html', 'contact.html', 'register.html', 'about.html'],
        files: {
          'index.html': result.pages[0],
          'contact.html': result.pages[1],
          'register.html': result.pages[2],
          'about.html': result.pages[3],
          'styles.css': result.css,
        },
        outputDir: result.output_dir,
      };

      console.log('Generated website structure:', website);
      return website;
    } else {
      console.error('Unexpected response type:', typeof result);
      throw new Error(`Unexpected response type from server: ${typeof result}`);
    }
  } catch (error) {
    console.error('Error generating website:', error);
    if (axios.isAxiosError(error)) {
      console.error('Axios error details:', error.response?.data);
      throw new Error(`Failed to generate website: ${error.message}. Server response: ${JSON.stringify(error.response?.data)}`);
    }
    throw error; // Re-throw the error to be caught by the calling function
  }
};