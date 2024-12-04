from django.urls import path

from . import views
# URLs for the login, signup, startup pages
# URLs for each of the game screens
app_name = "studdyApp"
urlpatterns = [
    path("", views.index, name="startup"),
    path('home/', views.index, name='startup'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('questions/', views.create_learning_profile, name='create_learning_profile'),
    path('logout/', views.user_logout, name='logout'),

    path('subject/<str:subject_name>/', views.subject_detail, name='subject_detail'),


    path('subject/<str:subject_name>/grade_selection/', views.select_subject_grade, name='select_subject_grade'),
    path('9_physical_science/', views.ninth_physical_science, name='ninth_physical_science'),
    path('9_biology/', views.ninth_biology, name='ninth_biology'),
    path('10_biology/', views.tenth_biology, name='tenth_biology'),
    path('11_biology/', views.eleventh_biology, name='eleventh_biology'),
    path('12_biology/', views.twelfth_biology, name='twelfth_biology'),
    path('10_chemistry/', views.tenth_chemistry, name='tenth_chemistry'),
    path('11_chemistry/', views.eleventh_chemistry, name='eleventh_biology'),
    path('10_earth_science/', views.tenth_earth_science, name='tenth_earth_science'),
    path('9_environmental_science/', views.ninth_environmental_science, name='ninth_environmental_science'),
    path('12_environmental_science/', views.twelfth_environmental_science, name='twelfth_environmental_science'),
    path('12_astronomy/', views.twelfth_astronomy, name='twelfth_astronomy'),
    path('9_anatomy/', views.ninth_anatomy, name='ninth_anatomy'),
    path('10_anatomy/', views.tenth_anatomy, name='tenth_anatomy'),
    path('11_anatomy/', views.eleventh_anatomy, name='eleventh_anatomy'),
    path('12_anatomy/', views.twelfth_anatomy, name='twelfth_anatomy'),
    path('11_physics/', views.eleventh_physics, name='eleventh_physics'),
    path('12_physics/', views.twelfth_physics, name='twelfth_physics'),
]