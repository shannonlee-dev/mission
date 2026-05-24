
const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');
const { PDFDocument } = require('pdf-lib');

function normalizePdfDimension(value, fallback) {
  const raw = String(value || fallback).trim();
  return raw.endsWith('px') ? raw : `${raw}px`;
}

async function exportSlidesAndMerge() {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  const filePath = path.resolve(__dirname, 'index.html');
  await page.goto('file://' + filePath);

  // 1. 첫 슬라이드 미리보기 PDF 생성
  await page.evaluate((idx) => {
    document.querySelectorAll('.slide').forEach((el, j) => {
      el.classList.toggle('active', j === idx - 1);
    });
  }, 1);
  await page.pdf({
    path: 'slide-preview.pdf',
    printBackground: true,
    width: '1600px',
    height: '900px',
    pageRanges: '1',
  });
  console.log('slide-preview.pdf 미리보기 생성 완료!');

  // 2. CLI 인자 또는 기본값으로 PDF 크기 결정
  const width = normalizePdfDimension(process.argv[2], '1600');
  const height = normalizePdfDimension(process.argv[3], '900');
  console.log(`PDF 크기: ${width} x ${height}`);

  // 3. 입력받은 크기로 모든 슬라이드 PDF 생성
  for (let i = 1; i <= 9; i++) {
    await page.evaluate((idx) => {
      document.querySelectorAll('.slide').forEach((el, j) => {
        el.classList.toggle('active', j === idx - 1);
      });
    }, i);

    await page.pdf({
      path: `slide-${String(i).padStart(2, '0')}.pdf`,
      printBackground: true,
      width,
      height,
      pageRanges: '1',
    });
    console.log(`slide-${i} 저장 완료`);
  }

  await browser.close();

  // PDF 병합
  const mergedPdf = await PDFDocument.create();
  for (let i = 1; i <= 9; i++) {
    const pdfBytes = fs.readFileSync(`slide-${String(i).padStart(2, '0')}.pdf`);
    const pdf = await PDFDocument.load(pdfBytes);
    const copiedPages = await mergedPdf.copyPages(pdf, pdf.getPageIndices());
    copiedPages.forEach((page) => mergedPdf.addPage(page));
  }
  const mergedPdfBytes = await mergedPdf.save();
  fs.writeFileSync('slides-all.pdf', mergedPdfBytes);
  console.log('slides-all.pdf 생성 완료!');
}

exportSlidesAndMerge();
