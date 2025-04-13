from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BoardForm
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, FileResponse
from .models import Board
import json
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
def home(request):
    boards = Board.objects.all().order_by('-created_at')
    return render(request, 'boards/home.html', {'boards': boards})

def hellopage(request):
    return render(request, 'hellopage.html')

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

    if board.pdf_file:
        # Для PDF используем специальный шаблон
        return render(request, 'boards/pdf2.html', {
            'board': board,
            'pdf_url': board.pdf_file.url,
            'saved_drawing': board.drawing_data
        })
    else:
        if request.method == 'POST':
            if 'drawing_data' in request.POST:
                board.drawing_data = request.POST['drawing_data']
                board.save()
                return JsonResponse({'status': 'success'})

        return render(request, 'boards/board.html', {
            'board': board,
            'drawing_data': board.drawing_data
        })


def show_pdf(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    if not board.pdf_file:
        return HttpResponse(status=404)

    #file_path = board.pdf_file.path
    #return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    return render(request, 'boards/pdf2.html', {
        'board': board,
        'pdf_url': board.pdf_file.url
    })
@require_POST
def delete_board(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    board.delete()
    return redirect('boards:home')


@csrf_exempt
def save_drawing(request, board_id):
    if request.method == 'POST':
        board = get_object_or_404(Board, id=board_id)
        try:
            data = json.loads(request.body)
            board.drawing_data = data.get('drawing_data')
            board.save()
            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
    return JsonResponse({'status': 'error'}, status=400)

def broadcast_drawing(board_id, data):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'board_{board_id}',
        {
            'type': 'annotation_message',
            'message': data
        }
    )


from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем пользователя
            messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
            return redirect('boards:home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('boards:home')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})



@login_required  # Только для авторизованных пользователей
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('boards:home')