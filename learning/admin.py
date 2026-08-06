from django.contrib import admin
from .models import (
    Profile,
    Semester,
    Kelas,
    Dosen,
    Mahasiswa,
    MataKuliah,
    Course,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("id", "nama")


@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ("id", "nama")


@admin.register(Dosen)
class DosenAdmin(admin.ModelAdmin):
    list_display = ("id", "nama", "nip")


@admin.register(Mahasiswa)
class MahasiswaAdmin(admin.ModelAdmin):
    list_display = ("id", "nama", "nim", "kelas")


@admin.register(MataKuliah)
class MataKuliahAdmin(admin.ModelAdmin):
    list_display = ("kode", "nama", "sks")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "mata_kuliah",
        "kelas",
        "semester",
        "dosen",
    )






