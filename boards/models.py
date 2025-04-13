from django.db import models
import uuid

class Board(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)
    drawing_data = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

