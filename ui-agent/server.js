const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');

const app = express();
app.use(cors());
app.use(express.json());

app.post('/generate', (req, res) => {
  const { prompt } = req.body;
  const pythonProcess = spawn('python', ['test_utils.py', prompt]);

  let result = '';
  pythonProcess.stdout.on('data', (data) => {
    result += data.toString();
  });

  pythonProcess.on('close', (code) => {
    res.json(JSON.parse(result));
  });
});

app.listen(3001, () => console.log('Server running on port 3001'));