# music/views.py
import boto3
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import Http404, FileResponse, HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from .forms import SheetMusicForm, FileFieldForm
from django.views.generic.edit import FormView
from .models import SheetMusic
import os


def index(request):
    try:
        items = SheetMusic.objects.all().order_by('-id')[:5]
    except items.DoesNotExist:
        raise Http404("No musics exist")
    return render(request, 'music/index.html', {'items': items})


@login_required()
def download_music(request, sheetID):
    # sheet_music = get_object_or_404(SheetMusic, id=sheetID)
    #
    # if sheet_music.pdf:
    #     file_path = sheet_music.pdf.path
    #     if os.path.exists(file_path):
    #         response = FileResponse(open(file_path, 'rb'))
    #         response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    #         return response
    #     else:
    #         raise Http404("File not found")
    # else:
    #     raise Http404("File not found")
    sheet_music = get_object_or_404(SheetMusic, id=sheetID)

    if sheet_music.pdf:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        file_key = sheet_music.pdf.name

        try:
            # Download the file from S3
            s3_object = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            file_stream = s3_object['Body'].read()

            # Stream the file as an HTTP response
            response = StreamingHttpResponse(file_stream, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{sheet_music.pdf.name}"'
            return response
        except s3_client.exceptions.NoSuchKey:
            raise Http404("File not found")
    else:
        raise Http404("File not found")


@login_required()
def upload_sheet_music(request):
    if request.method == 'POST':
        form = SheetMusicForm(request.POST, request.FILES)
        if form.is_valid():
            sheet_music = form.save(commit=False)
            sheet_music.save()
            return render(request, 'music/index.html', {'form': form})
    else:
        form = SheetMusicForm()
    return render(request, 'music/upload_sheet_music.html', {'form': form})


@login_required()
def music_page(request, sheetID):
    sheet = get_object_or_404(SheetMusic, id=sheetID)
    return render(request, 'music/music_page.html', {'sheet': sheet})


@login_required
def display_pdf(request, sheetID):
    sheet = get_object_or_404(SheetMusic, id=sheetID)
    #

    sheet = get_object_or_404(SheetMusic, id=sheetID)

    if sheet.pdf:
        file_url = sheet.pdf.url
        return HttpResponseRedirect(file_url)
    else:
        raise Http404("PDF file not found")
    # # Check if the sheet music has a PDF file
    # if sheet.pdf:
    #     file_path = sheet.pdf.path
    #     if os.path.exists(file_path):
    #         # Open the file in binary mode
    #         with open(file_path, 'rb') as f:
    #             response = HttpResponse(f.read(), content_type='application/pdf')
    #             # Set Content-Disposition to inline
    #             response['Content-Disposition'] = 'inline; filename="{0}"'.format(os.path.basename(file_path))
    #         return response
    #
    # # If no PDF file or file not found, return a 404 response
    # raise Http404("PDF file not found")


@login_required()
def music_list(request):
    try:
        items = SheetMusic.objects.all()
    except items.DoesNotExist:
        raise Http404("No musics exist")
    return render(request, 'music/music_list.html', {'items': items})


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('index.html')
    else:
        return redirect('music/registration/login.html')


class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "music/upload_multiple_pdfs.html"  # Replace with your template.
    success_url = "/"  # Replace with your URL or reverse().

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        for f in files:
            sheet_music = SheetMusic(
                title=f.name.split('.')[0],
                pdf=f,
            )
            sheet_music.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
