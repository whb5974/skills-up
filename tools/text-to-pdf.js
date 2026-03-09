#!/usr/bin/env node

/**
 * Text/Markdown to PDF Converter
 * 将文字或 Markdown 内容转换为 PDF 文件
 */

const PDFDocument = require('pdfkit');
const fs = require('fs');
const path = require('path');

// 简单的 Markdown 解析器
function parseMarkdown(text) {
    const lines = text.split('\n');
    const blocks = [];
    let currentList = null;
    
    for (const line of lines) {
        // 标题
        if (line.startsWith('# ')) {
            blocks.push({ type: 'h1', text: line.slice(2) });
        } else if (line.startsWith('## ')) {
            blocks.push({ type: 'h2', text: line.slice(3) });
        } else if (line.startsWith('### ')) {
            blocks.push({ type: 'h3', text: line.slice(4) });
        }
        // 列表
        else if (line.startsWith('- ') || line.startsWith('* ')) {
            if (!currentList) {
                currentList = { type: 'list', items: [] };
                blocks.push(currentList);
            }
            currentList.items.push(line.slice(2));
        }
        // 代码块
        else if (line.startsWith('```')) {
            if (currentList) currentList = null;
            blocks.push({ type: 'code', text: line.slice(3) });
        }
        // 空行
        else if (line.trim() === '') {
            if (currentList) currentList = null;
            blocks.push({ type: 'space' });
        }
        // 普通文本
        else {
            if (currentList) currentList = null;
            blocks.push({ type: 'text', text: line });
        }
    }
    
    return blocks;
}

function generatePDF(inputFile, outputFile, options = {}) {
    return new Promise((resolve, reject) => {
        // 读取输入内容
        let content;
        if (inputFile === '-') {
            // 从 stdin 读取
            content = fs.readFileSync(0, 'utf-8');
        } else {
            content = fs.readFileSync(inputFile, 'utf-8');
        }
        
        // 创建 PDF 文档
        const doc = new PDFDocument({
            size: options.size || 'A4',
            margins: {
                top: 50,
                bottom: 50,
                left: 50,
                right: 50
            }
        });
        
        // 输出流
        const stream = fs.createWriteStream(outputFile);
        doc.pipe(stream);
        
        // 解析 Markdown
        const blocks = parseMarkdown(content);
        
        // 渲染到 PDF
        for (const block of blocks) {
            switch (block.type) {
                case 'h1':
                    doc.fontSize(24).font('Helvetica-Bold').text(block.text, { align: 'left' });
                    doc.moveDown(0.5);
                    break;
                case 'h2':
                    doc.fontSize(18).font('Helvetica-Bold').text(block.text, { align: 'left' });
                    doc.moveDown(0.3);
                    break;
                case 'h3':
                    doc.fontSize(14).font('Helvetica-Bold').text(block.text, { align: 'left' });
                    doc.moveDown(0.2);
                    break;
                case 'list':
                    doc.fontSize(11).font('Helvetica');
                    for (const item of block.items) {
                        doc.text(`• ${item}`, { indent: 20 });
                    }
                    doc.moveDown(0.3);
                    break;
                case 'code':
                    doc.fontSize(10).font('Courier').text(block.text, {
                        align: 'left',
                        continued: false
                    });
                    doc.moveDown(0.2);
                    break;
                case 'space':
                    doc.moveDown(0.5);
                    break;
                case 'text':
                default:
                    doc.fontSize(11).font('Helvetica').text(block.text, { align: 'left' });
                    break;
            }
        }
        
        // 完成
        doc.end();
        
        stream.on('finish', () => {
            resolve(outputFile);
        });
        
        stream.on('error', reject);
    });
}

// CLI 接口
async function main() {
    const args = process.argv.slice(2);
    
    if (args.includes('--help') || args.includes('-h')) {
        console.log(`
Text to PDF Converter

用法:
  node text-to-pdf.js <input.md> <output.pdf> [options]
  cat input.md | node text-to-pdf.js - output.pdf

选项:
  --size <A4|Letter>  页面大小 (默认：A4)
  --help, -h          显示帮助

示例:
  node text-to-pdf.js report.md report.pdf
  cat notes.md | node text-to-pdf.js - notes.pdf
`);
        process.exit(0);
    }
    
    if (args.length < 2) {
        console.error('错误：请指定输入和输出文件');
        console.error('用法：node text-to-pdf.js <input> <output>');
        process.exit(1);
    }
    
    const inputFile = args[0];
    const outputFile = args[1];
    const options = {};
    
    const sizeIdx = args.indexOf('--size');
    if (sizeIdx !== -1 && args[sizeIdx + 1]) {
        options.size = args[sizeIdx + 1];
    }
    
    try {
        await generatePDF(inputFile, outputFile, options);
        console.log(`✅ PDF 已生成：${outputFile}`);
    } catch (err) {
        console.error('生成 PDF 失败:', err.message);
        process.exit(1);
    }
}

main();

module.exports = { generatePDF, parseMarkdown };
