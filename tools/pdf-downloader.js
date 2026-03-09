#!/usr/bin/env node

/**
 * PDF 下载服务器
 * 提供生成好的 PDF 文件下载
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const PORT = process.env.PDF_PORT || 3456;
const PDF_DIR = path.join(__dirname, '..', 'pdf-output');

// 确保输出目录存在
if (!fs.existsSync(PDF_DIR)) {
    fs.mkdirSync(PDF_DIR, { recursive: true });
    console.log(`📁 创建 PDF 输出目录：${PDF_DIR}`);
}

const server = http.createServer((req, res) => {
    const url = new URL(req.url, `http://localhost:${PORT}`);
    
    // CORS 头
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        res.writeHead(200);
        res.end();
        return;
    }
    
    // 路由：生成 PDF
    if (req.method === 'POST' && url.pathname === '/generate') {
        let body = '';
        req.on('data', chunk => { body += chunk; });
        req.on('end', () => {
            try {
                const { content, filename } = JSON.parse(body);
                const safeFilename = filename.replace(/[^a-zA-Z0-9._-]/g, '_');
                const outputPath = path.join(PDF_DIR, safeFilename);
                
                // 写入临时 Markdown 文件
                const tempMd = path.join(PDF_DIR, '_temp.md');
                fs.writeFileSync(tempMd, content);
                
                // 调用 PDF 生成器
                const converter = path.join(__dirname, 'text-to-pdf.js');
                exec(`node "${converter}" "${tempMd}" "${outputPath}"`, (err, stdout, stderr) => {
                    if (err) {
                        console.error('PDF 生成失败:', stderr);
                        res.writeHead(500);
                        res.end(JSON.stringify({ error: err.message, stderr }));
                        return;
                    }
                    
                    const downloadUrl = `http://localhost:${PORT}/download/${safeFilename}`;
                    res.writeHead(200, { 'Content-Type': 'application/json' });
                    res.end(JSON.stringify({
                        success: true,
                        file: safeFilename,
                        downloadUrl: downloadUrl,
                        path: outputPath
                    }));
                });
            } catch (e) {
                res.writeHead(400);
                res.end(JSON.stringify({ error: e.message }));
            }
        });
        return;
    }
    
    // 路由：下载 PDF
    if (req.method === 'GET' && url.pathname.startsWith('/download/')) {
        const filename = decodeURIComponent(url.pathname.split('/').pop());
        const filepath = path.join(PDF_DIR, filename);
        
        console.log(`下载请求：${filename}`);
        console.log(`文件路径：${filepath}`);
        
        if (!fs.existsSync(filepath)) {
            console.error(`文件不存在：${filepath}`);
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ 
                error: 'File not found',
                filename: filename,
                searchedPath: filepath
            }));
            return;
        }
        
        const stat = fs.statSync(filepath);
        res.writeHead(200, {
            'Content-Type': 'application/pdf',
            'Content-Disposition': `attachment; filename="${filename}"`,
            'Content-Length': stat.size
        });
        
        const stream = fs.createReadStream(filepath);
        stream.pipe(res);
        console.log(`✅ 文件已发送：${filename} (${stat.size} bytes)`);
        return;
    }
    
    // 路由：列出所有 PDF
    if (req.method === 'GET' && url.pathname === '/list') {
        const files = fs.readdirSync(PDF_DIR)
            .filter(f => f.endsWith('.pdf'))
            .map(f => ({
                name: f,
                url: `http://localhost:${PORT}/download/${f}`,
                size: fs.statSync(path.join(PDF_DIR, f)).size
            }));
        
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ files }));
        return;
    }
    
    // 路由：健康检查
    if (req.method === 'GET' && url.pathname === '/health') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ status: 'ok', port: PORT, pdfDir: PDF_DIR }));
        return;
    }
    
    // 路由：首页（HTML 界面）
    if (req.method === 'GET' && url.pathname === '/') {
        const files = fs.readdirSync(PDF_DIR)
            .filter(f => f.endsWith('.pdf'))
            .map(f => ({
                name: f,
                size: fs.statSync(path.join(PDF_DIR, f)).size
            }));
        
        const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF 下载中心</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        .file-list { list-style: none; padding: 0; }
        .file-item { background: #f5f5f5; margin: 10px 0; padding: 15px; border-radius: 5px; display: flex; justify-content: space-between; align-items: center; }
        .file-name { font-weight: bold; color: #2196F3; }
        .file-size { color: #666; font-size: 14px; }
        .download-btn { background: #2196F3; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; }
        .download-btn:hover { background: #1976D2; }
        .status { background: #e8f5e9; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h1>📄 PDF 下载中心</h1>
    <div class="status">
        ✅ 服务器运行正常 | 端口：${PORT} | 文件数：${files.length}
    </div>
    ${files.length === 0 ? '<p>暂无 PDF 文件</p>' : `
    <h2>可用文件</h2>
    <ul class="file-list">
        ${files.map(f => `
            <li class="file-item">
                <div>
                    <div class="file-name">📄 ${f.name}</div>
                    <div class="file-size">${(f.size / 1024).toFixed(2)} KB</div>
                </div>
                <a href="/download/${f.name}" class="download-btn" download>下载</a>
            </li>
        `).join('')}
    </ul>
    `}
    <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
    <p style="color: #666; font-size: 14px;">
        API: <code>POST /generate</code> | <code>GET /list</code> | <code>GET /health</code>
    </p>
</body>
</html>`;
        
        res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
        res.end(html);
        return;
    }
    
    // 默认 404
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: 'Not Found', path: url.pathname }));
});

server.listen(PORT, () => {
    console.log(`📄 PDF 下载服务器已启动`);
    console.log(`   端口：${PORT}`);
    console.log(`   目录：${PDF_DIR}`);
    console.log(`   网页界面：http://localhost:${PORT}/`);
    console.log(`   健康检查：http://localhost:${PORT}/health`);
    console.log(`   列出文件：http://localhost:${PORT}/list`);
    console.log(`\n使用方法:`);
    console.log(`   POST /generate - {"content": "...", "filename": "report.pdf"}`);
    console.log(`   GET  /download/<filename> - 下载 PDF`);
});
