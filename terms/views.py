from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactFormSubmission
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.utils import timezone
import zipfile
import io
from .models import DataDownload
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@require_http_methods(["GET", "POST"])
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Validate fields (basic validation)
        if not name or not email or not subject or not message:
            messages.error(request, 'All required fields must be filled.')
            return render(request, 'terms/contact_us.html')

        # Save submission to the database
        submission = ContactFormSubmission(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message
        )
        submission.save()

        messages.success(request, 'Your message has been sent successfully!')
        return redirect('terms:contact_us')

    return render(request, 'terms/contact_us.html')


def terms_of_service(request):
    return render(request, 'terms/terms.html')


def data_collection_info(request):
    return render(request, 'Terms/data_collection.html')


def privacy_policy(request):
    return render(request, 'terms/privacy_policy.html')


def user_data_download(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Save email and timestamp in the model
        DataDownload.objects.create(email=email, timestamp=timezone.now())
        return render(request, 'terms/user_data_download.html')

@csrf_exempt
def download_data(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Create a zip file with dummy data
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr('user_data.txt', f'This is some dummy data.\nEmail: {email}\nDate: {timezone.now().strftime("%Y-%m-%d %H:%M:%S")}')

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=user_data.zip'
        return response

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def about(request):
    return render(request, 'Terms/about.html')