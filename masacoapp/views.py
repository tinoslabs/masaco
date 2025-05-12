from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from .models import AbroadStudies, CoachingProgram, CoachingFAQ, Contact, Testimonial, Partners, TeamMembers, Blog, Service
from .forms import StudyAbroadForm, CoachingForm, CoachingFAQForm, ContactForm, TestimonialForm, PartnersForm, TeamForm, BlogForm, ServiceForm
# Create your views here.
from django.contrib import messages

from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse 
import os


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "There was an error logging in, try again...")
            return redirect('user_login')
    return render(request, 'authenticate/login.html', {'form': True})

def logout_user(request):
    logout(request)
    messages.success(request, "You were logged out")
    return redirect('index')

def index(request):
    abroad = AbroadStudies.objects.all().order_by('-id')
    training = CoachingProgram.objects.all().order_by('-id')
    reviews = Testimonial.objects.all().order_by('-id')
    partners = Partners.objects.all().order_by('-id')
    team = TeamMembers.objects.all().order_by('-id')
    blog = Blog.objects.all().order_by('-id')
    service = Service.objects.all()
    return render(request, 'index.html',{'abroad': abroad, 'training': training,'reviews': reviews,'partners': partners, 'team': team, 'blog': blog,'service': service})
    

@csrf_exempt
def ckeditor_upload(request):
    if request.method == 'POST' and request.FILES.get('upload'):
        upload = request.FILES['upload']
        file_extension = os.path.splitext(upload.name)[1].lower()
        
        # Check if the uploaded file is an image or a PDF
        if file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']:
            folder = 'images'
        elif file_extension == '.pdf':
            folder = 'pdfs'
        else:
            return JsonResponse({'uploaded': False, 'error': 'Unsupported file type.'})

        # Save the file in the appropriate folder
        file_name = default_storage.save(f'{folder}/{upload.name}', ContentFile(upload.read()))
        file_url = default_storage.url(file_name)
        return JsonResponse({
            'uploaded': True,
            'url': file_url
        })
    
    return JsonResponse({'uploaded': False, 'error': 'No file was uploaded.'})


def admin_dashboard(request):
    return render(request,'admin_pages/admin_dashboard.html')


def add_abroad_studies(request):
    if request.method == 'POST':
        form = StudyAbroadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_abroad_studies') 
    else:
        form = StudyAbroadForm()

    return render(request, 'admin_pages/add_abroad_studies.html', {'form': form})


def view_abroad_studies(request):
    studies = AbroadStudies.objects.all().order_by('-id')
    return render(request, 'admin_pages/view_abroad_studies.html', {'studies': studies})


def update_abroad_studeis(request, id):
    abroad = get_object_or_404(AbroadStudies, id=id)
    if request.method == 'POST':
        form = StudyAbroadForm(request.POST, request.FILES, instance=abroad)
        if form.is_valid():
            form.save()
            return redirect('view_abroad_studies')
    else:
        form = StudyAbroadForm(instance=abroad)
    return render(request, 'admin_pages/update_abroad_studeis.html', {'form': form, 'abroad': abroad})


def delete_abroad_studeis(request,id):
    abroad = AbroadStudies.objects.get(id=id)
    abroad.delete()
    return redirect('view_abroad_studies')


def add_coaching(request):
    if request.method == 'POST':
        form = CoachingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_coaching') 
    else:
        form = CoachingForm()

    return render(request, 'admin_pages/add_coaching.html', {'form': form})


def view_coaching(request):
    coaching = CoachingProgram.objects.all().order_by('-id')
    return render(request, 'admin_pages/view_coaching.html', {'coaching': coaching})


def update_coaching(request, id):
    coaching = get_object_or_404(CoachingProgram, id=id)
    if request.method == 'POST':
        form = CoachingForm(request.POST, request.FILES, instance=coaching)
        if form.is_valid():
            form.save()
            return redirect('view_coaching')
    else:
        form = CoachingForm(instance=coaching)
    return render(request, 'admin_pages/update_coaching.html', {'form': form, 'coaching': coaching})


def delete_coaching(request,id):
    coaching = CoachingProgram.objects.get(id=id)
    coaching.delete()
    return redirect('view_coaching')


def add_faq(request):
    coaching_programs = CoachingProgram.objects.all()
    if request.method == 'POST':
        program_id = request.POST.get('coaching_program')
        question = request.POST.get('question')
        answer = request.POST.get('answer')

        coaching_program = get_object_or_404(CoachingProgram, id=program_id)

        CoachingFAQ.objects.create(
            coaching_program=coaching_program,
            question=question,
            answer=answer
        )
        return redirect('list_faq')

    return render(request, 'admin_pages/add_faq.html', {'coaching_programs': coaching_programs})


def update_faq(request, id):
    faq = get_object_or_404(CoachingFAQ, id=id)
    coaching_programs = CoachingProgram.objects.all()

    if request.method == 'POST':
        program_id = request.POST.get('coaching_program')
        question = request.POST.get('question')
        answer = request.POST.get('answer')

        coaching_program = get_object_or_404(CoachingProgram, id=program_id)

        faq.coaching_program = coaching_program
        faq.question = question
        faq.answer = answer
        faq.save()

        return redirect('list_faq')

    return render(request, 'admin_pages/update_faq.html', {
        'faq': faq,
        'coaching_programs': coaching_programs
    })


def delete_faq(request,id):
    faq = CoachingFAQ.objects.get(id=id)
    faq.delete()
    return redirect('list_faq')

# List all FAQs
def list_faq(request):
    faqs = CoachingFAQ.objects.select_related('coaching_program').all()
    return render(request, 'admin_pages/list_faq.html', {'faqs': faqs})

def add_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('list_testimonials')
    else:
        form = TestimonialForm()
    return render(request, 'admin_pages/add_testimonial.html', {'form': form})

def list_testimonials(request):
    testimonials = Testimonial.objects.all()
    return render(request, 'admin_pages/list_testimonials.html', {'testimonials': testimonials})

def update_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    if request.method == 'POST':
        form = TestimonialForm(request.POST, request.FILES, instance=testimonial)
        if form.is_valid():
            form.save()
            return redirect('list_testimonials')
    else:
        form = TestimonialForm(instance=testimonial)
    return render(request, 'admin_pages/update_testimonial.html', {'form': form})

def delete_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    return redirect('list_testimonials')



def add_partners(request):
    if request.method == 'POST':
        form = PartnersForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_partners') 
    else:
        form = PartnersForm()

    return render(request, 'admin_pages/add_partners.html', {'form': form})


def view_partners(request):
    logo = Partners.objects.all().order_by('-id')
    return render(request,'admin_pages/view_partners.html',{'logo':logo})


def update_partners(request,id):
    logos = get_object_or_404(Partners, id=id)
    if request.method == 'POST':
        form = PartnersForm(request.POST, request.FILES, instance=logos)
        if form.is_valid():
            form.save()
            return redirect('view_partners')
    else:
        form = PartnersForm(instance=logos)
    return render(request, 'admin_pages/update_partners.html', {'form': form, 'logos': logos})


def delete_partners(request,id):
    logos = Partners.objects.get(id=id)
    logos.delete()
    return redirect('view_partners')



def add_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_team') 
    else:
        form = TeamForm()

    return render(request, 'admin_pages/add_team.html', {'form': form})


def view_team(request):
    team = TeamMembers.objects.all().order_by('-id')
    return render(request,'admin_pages/view_team.html',{'team':team})


def update_team(request,id):
    team = get_object_or_404(TeamMembers, id=id)
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES, instance=team)
        if form.is_valid():
            form.save()
            return redirect('view_team')
    else:
        form = TeamForm(instance=team)
    return render(request, 'admin_pages/update_team.html', {'form': form, 'team': team})



def delete_team(request,id):
    team = TeamMembers.objects.get(id=id)
    team.delete()
    return redirect('view_team')

def add_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_blog') 
    else:
        form = BlogForm()

    return render(request, 'admin_pages/add_blog.html', {'form': form})


def view_blog(request):
    blog = Blog.objects.all().order_by('-id')
    return render(request,'admin_pages/view_blog.html',{'blog':blog})


def update_blog(request, id):
    blog = get_object_or_404(Blog, id=id)  # <-- Was TeamMembers
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('view_blog')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'admin_pages/update_blog.html', {'form': form, 'blog': blog})


def delete_blog(request,id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    return redirect('view_blog')


def add_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_service') 
    else:
        form = ServiceForm()

    return render(request, 'admin_pages/add_service.html', {'form': form})


def view_service(request):
    service = Service.objects.all().order_by('-id')
    return render(request,'admin_pages/view_service.html',{'service':service})


def update_service(request, id):
    service = get_object_or_404(Service, id=id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('view_service')
    else:
        form = ServiceForm(instance=service)  # <-- fixed from instance=blog

    return render(request, 'admin_pages/update_service.html', {'form': form, 'service': service})



def delete_service(request,id):
    service = Service.objects.get(id=id)
    service.delete()
    return redirect('view_service')

def about(request):
    team = TeamMembers.objects.all().order_by('-id')
    reviews = Testimonial.objects.all().order_by('-id')
    partners = Partners.objects.all().order_by('-id')
    return render(request, 'about.html',{'team':team,'reviews':reviews,'partners':partners})

def service(request):
    return render(request, 'service.html')

def service_details(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    all_services = Service.objects.all().order_by('id')
    return render(request, 'service-details.html', {
        'service': service,
        'all_services': all_services,
    })


def country(request):
    abroad = AbroadStudies.objects.all().order_by('-id')
    return render(request, 'country.html',{'abroad':abroad})

def country_details(request, id):
    country = get_object_or_404(AbroadStudies, id=id)
    all_countries = AbroadStudies.objects.all()
    return render(request, 'country-details.html', {
        'country': country,
        'all_countries': all_countries
    })

# def country_details(request, id):
#     country = get_object_or_404(AbroadStudies, id=id)
#     return render(request, 'country-details.html', {'country': country})

def coaching(request):
    training = CoachingProgram.objects.all().order_by('-id')
    return render(request, 'coaching.html',{'training':training})

def coaching_details(request, pk):
    coaching = get_object_or_404(CoachingProgram, pk=pk)
    return render(request, 'coaching-details.html',{'coaching': coaching})

def coaching_details(request, pk):
    coaching = get_object_or_404(CoachingProgram, pk=pk)
    all_coaching = CoachingProgram.objects.all()
    return render(request, 'coaching-details.html', {
        'coaching': coaching,
        'all_coaching': all_coaching
    })

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        comment = request.POST.get("comment")

        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            comment=comment
        )
        return render(request, 'contact.html', {'success': True})
    return render(request, 'contact.html')

def contact_list(request):
    contact = Contact.objects.all().order_by('-id')
    return render(request, 'admin_pages/contact_list.html', {'contact': contact})

def delete_contact(request,id):
    contact = Contact.objects.get(id=id)
    contact.delete()
    return redirect('contact_list')

def blog(request):
    blog = Blog.objects.all().order_by('-id')
    return render(request, 'blog.html', {'blog': blog})



def blog_details(request, id):
    blog = get_object_or_404(Blog, id=id)
    recent_posts = Blog.objects.exclude(id=blog.id).order_by('-date')[:3]  # Latest 3 posts, excluding current
    return render(request, 'blog-details.html', {'blog': blog, 'recent_posts': recent_posts})

def testimonials(request):
    return render(request, 'testimonial.html')