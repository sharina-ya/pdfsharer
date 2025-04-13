async function renderPDF(url) {
    const pdfViewer = document.getElementById('pdf-viewer');
    pdfViewer.innerHTML = '';


    const loadingTask = pdfjsLib.getDocument(url);
    const pdf = await loadingTask.promise;


    for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
        const page = await pdf.getPage(pageNum);
        const viewport = page.getViewport({ scale: 1.5 });


        const pageDiv = document.createElement('div');
        pageDiv.className = 'pdf-page';
        pageDiv.style.marginBottom = '20px';


        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        await page.render({
            canvasContext: context,
            viewport: viewport
        }).promise;

        pageDiv.appendChild(canvas);
        pdfViewer.appendChild(pageDiv);
    }

    document.getElementById('pdf-scroll-container').scrollTo(0, 0);
}
