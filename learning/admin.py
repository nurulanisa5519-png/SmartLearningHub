from django.contrib import admin
from .models import (
    Profile,
    Semester,
    Kelas,
    Dosen,
    Mahasiswa,
    MataKuliah,
    Course,
    Materi,
    Tugas,
    PengumpulanTugas,
    Chat, 
    ChatMessage,
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


@admin.register(Materi)
class MateriAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "judul",
        "course",
        "tanggal_upload",
    )


@admin.register(Tugas)
class TugasAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "judul",
        "course",
        "deadline",
    )


@admin.register(PengumpulanTugas)
class PengumpulanTugasAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tugas",
        "mahasiswa",
        "nilai",
        "tanggal_kumpul",
    )

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "updated_at")


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat", "role", "created_at")