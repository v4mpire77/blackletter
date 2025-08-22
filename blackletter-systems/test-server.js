const http = require('http');

const server = http.createServer((req, res) => {
  res.writeHead(200, {'Content-Type': 'text/html'});
  res.end(`
    <!DOCTYPE html>
    <html>
    <head><title>Blackletter Test</title></head>
    <body>
      <h1>Frontend Test Server</h1>
      <p>If you can see this, Node.js server is working!</p>
      <p><a href="/upload">Upload would be here</a></p>
      <form action="http://localhost:8000/api/review" method="post" enctype="multipart/form-data">
        <label>Test file upload:</label>
        <input type="file" name="file" accept="application/pdf">
        <button type="submit">Test Upload</button>
      </form>
    </body>
    </html>
  `);
});

const PORT = 3001;
server.listen(PORT, () => {
  console.log(`Test server running on http://localhost:${PORT}`);
});

server.on('error', (err) => {
  console.error('Server error:', err);
});
