const fs = require('fs');
const { PDFDocument } = require('pdf-lib');

async function mergePDFs() {
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

mergePDFs();
