document.addEventListener('DOMContentLoaded', function() {
    const pdfViewer = document.getElementById('pdf-viewer');
    const canvas = document.getElementById('annotation-layer');
    const ctx = canvas.getContext('2d');

    // Загрузка PDF
    pdfjsLib.getDocument(pdfUrl).promise.then(function(pdf) {
        pdf.getPage(1).then(function(page) {
            const viewport = page.getViewport({ scale: 1.5 });


            canvas.width = viewport.width;
            canvas.height = viewport.height;

            page.render({
                canvasContext: ctx,
                viewport: viewport
            });
        });
    });
});