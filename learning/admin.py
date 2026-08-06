from django.contrib import admin
from django.contrib.auth.models import User, Group

from .models import (
    Profile,
    Semester,
    Kelas,
    Dosen,
    Mahasiswa,
    MataKuliah,
    Course,
    Chat,
    ChatMessage,
)

# =========================
# User & Group
# =========================

admin.site.unregister(User)
admin.site.register(User)

admin.site.unregister(Group)
admin.site.register(Group)

# =========================
# Profile
# =========================

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    search_fields = ("user__username",)

# =========================
# Semester
# =========================

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ("id", "nama")

# =========================
# Kelas
# =========================

@admin.register(Kelas)
class KelasAdmin(admin.ModelAdmin):
    list_display = ("id", "nama")

# =========================
# Dosen
# =========================

@admin.register(Dosen)
class DosenAdmin(admin.ModelAdmin):
    list_display = ("id", "nama", "nip")
    search_fields = ("nama", "nip")

# =========================
# Mahasiswa
# =========================

@admin.register(Mahasiswa)
class MahasiswaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nama",
        "nim",
        "kelas",
    )

    search_fields = (
        "nama",
        "nim",
    )

# =========================
# Mata Kuliah
# =========================

@admin.register(MataKuliah)
class MataKuliahAdmin(admin.ModelAdmin):
    list_display = (
        "kode",
        "nama",
        "sks",
    )

# =========================
# Course
# =========================

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "mata_kuliah",
        "kelas",
        "semester",
        "dosen",
    )

    list_filter = (
        "semester",
        "kelas",
    )

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "updated_at")


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat", "role", "created_at")