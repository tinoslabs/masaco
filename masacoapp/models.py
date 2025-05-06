from django.db import models

# Create your models here.
    
    
class AbroadStudies(models.Model):
    country_name = models.CharField(max_length=100)
    country_logo = models.ImageField(upload_to='images/', null=True, blank=True)
    country_image = models.ImageField(upload_to='images/', null=True, blank=True)
    country_description = models.TextField(null=True, blank=True)   
    main_image = models.ImageField(upload_to='images/', null=True, blank=True)
    video = models.FileField(upload_to='country_videos/', null=True, blank=True)
    study_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.country_name
    
    
    
class CoachingProgram(models.Model): 
    title = models.CharField(max_length=100)
    description = models.TextField()
    duration_months = models.PositiveIntegerField(help_text="Duration in months")
    total_classes = models.PositiveIntegerField()
    image = models.ImageField(upload_to='coaching_images/')   
    coaching_deatils = models.TextField(null=True, blank=True)
    coaching_brochure = models.FileField(upload_to='course_brochures/', null=True, blank=True) 
    coaching_video = models.FileField(upload_to='coaching_videos/', null=True, blank=True)
   
    def __str__(self):
        return self.title
    
    
class CoachingFAQ(models.Model):
    coaching_program = models.ForeignKey(CoachingProgram, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return f"{self.coaching_program.title} - {self.question[:50]}"


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField(default=5)  # 1 to 5 stars
    message = models.TextField()
    image = models.ImageField(upload_to='testimonial_images/')

    def __str__(self):
        return f"{self.name} - {self.designation}"
    
    
class Contact(models.Model):
    name = models.CharField(max_length=100)   
    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class TeamMembers(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team_images/')

    def __str__(self):
        return self.name
    
class Partners(models.Model):
    name = models.CharField(max_length=100,null=True,blank=True)
    logo = models.ImageField(upload_to='team_images/')

    def __str__(self):
        return self.name
    
    
class Blog(models.Model):
    blog_heading = models.CharField(max_length=100)
    blog_details = models.TextField(null=True, blank=True)
    main_image = models.ImageField(upload_to='images/')
    date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.blog_heading
    
    
class Service(models.Model):
    heading = models.CharField(max_length=100)
    details = models.TextField(null=True, blank=True)
    main_image = models.ImageField(upload_to='images/')
    service_pdf = models.FileField(upload_to='service_pdf/', null=True, blank=True)
    
    
    def __str__(self):
        return self.heading
    

    
    
