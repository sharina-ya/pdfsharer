from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Board
from .forms import BoardForm
from django.views.decorators.http import require_POST
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.conf import settings
from .models import Board
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import JsonResponse
import json
def home(request):
    boards = Board.objects.all().order_by('-created_at')
    return render(request, 'boards/home.html', {'boards': boards})


def create_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST, request.FILES)
        if form.is_valid():
            board = form.save()
            return redirect('boards:boards', board_id=board.id)
    else:
        form = BoardForm()
    return render(request, 'boards/create_board.html', {'form': form})


def board_view(request, board_id):
    board = get_object_or_404(Board, id=board_id)

    if request.method == 'POST':
        if 'drawing_data' in request.POST:
            board.drawing_data = request.POST['drawing_data']
            board.save()
            return JsonResponse({'status': 'success'})

    context = {
        'board': board,
        'pdf_url': board.pdf_file.url if board.pdf_file else None,
        'drawing_data': board.drawing_data
    }
    return render(request, 'boards/board.html', context)




def show_pdf(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if not board.pdf_file:
        return HttpResponse(status=404)

    # рисование поверх PDF
    packet = BytesIO()
    can = canvas.Canvas(packet)
    can.save()

    existing_pdf = PdfReader(board.pdf_file.path)
    output = PdfWriter()

    for page in existing_pdf.pages:
        page.merge_page(PdfReader(packet).pages[0])
        output.add_page(page)

    response = HttpResponse(content_type='application/pdf')
    output.write(response)
    return response

@require_POST
def delete_board(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    board.delete()
    return redirect('boards:home')


