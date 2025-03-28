const express = require('express');
const path = require('path');
const cors = require('cors');

const app = express();
const port = process.env.PORT || 3000;

// Enable CORS
app.use(cors({
  origin: process.env.API_URL || 'http://localhost:5000',
  credentials: true
}));

// Serve static files
app.use('/static', express.static(path.join(__dirname, '../static')));

// Serve templates
app.use(express.static(path.join(__dirname, '../templates')));

// Default route
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../templates/index.html'));
});

// Start server
app.listen(port, '0.0.0.0', () => {
  console.log(`Frontend server running at http://0.0.0.0:${port}`);
}); 