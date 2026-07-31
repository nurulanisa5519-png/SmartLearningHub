from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# ==================================
# API ROUTER
# ==================================

router = DefaultRouter()

router.register(r'mahasiswa', views.MahasiswaViewSet, basename='mahasiswa')
router.register(r'dosen', views.DosenViewSet, basename='dosen')
router.register(r'course', views.CourseViewSet, basename='course')
router.register(r'materi', views.MateriViewSet, basename='materi')
router.register(r'tugas', views.TugasViewSet, basename='tugas')

urlpatterns = [

    # ======================
    # HOME
    # ======================

    path('', views.home, name='home'),

    # ======================
    # AUTH
    # ======================

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ======================
    # DASHBOARD
    # ======================

    path('dashboard/', views.dashboard, name='dashboard'),

    # ======================
    # COURSE
    # ======================

    path(
        'course/<int:course_id>/',
        views.detail_course,
        name='detail_course'
    ),

    # ======================
    # MATERI
    # ======================

    path(
        'course/<int:course_id>/upload-materi/',
        views.upload_materi,
        name='upload_materi'
    ),

    path(
        'materi/<int:materi_id>/edit/',
        views.edit_materi,
        name='edit_materi'
    ),

    path(
        'materi/<int:materi_id>/hapus/',
        views.hapus_materi,
        name='hapus_materi'
    ),

    # ======================
    # TUGAS
    # ======================

    path(
        'course/<int:course_id>/tambah-tugas/',
        views.tambah_tugas,
        name='tambah_tugas'
    ),

    path(
        'tugas/<int:tugas_id>/edit/',
        views.edit_tugas,
        name='edit_tugas'
    ),

    path(
        'tugas/<int:tugas_id>/hapus/',
        views.hapus_tugas,
        name='hapus_tugas'
    ),

    # ======================
    # JAWABAN
    # ======================

    path(
        'upload-jawaban/<int:tugas_id>/',
        views.upload_jawaban,
        name='upload_jawaban'
    ),

    # ======================
    # NILAI
    # ======================

    path(
        'course/<int:course_id>/jawaban/',
        views.daftar_jawaban,
        name='daftar_jawaban'
    ),

    path(
        'beri-nilai/<int:jawaban_id>/',
        views.beri_nilai,
        name='beri_nilai'
    ),

    path(
        "laporan/",
        views.laporan_pandas,
        name="laporan_pandas"
    ),

    # ======================
    # API
    # ======================

    path('api/', include(router.urls)),

]