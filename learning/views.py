from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import markdown
from django.utils import timezone
from .models import Chat, ChatMessage

from .models import (
    Profile,
    Dosen,
    Mahasiswa,
    Course,
    Materi,
    Tugas,
    PengumpulanTugas,
)

from rest_framework import viewsets
from .serializers import (
    MahasiswaSerializer,
    DosenSerializer,
    CourseSerializer,
    MateriSerializer,
    TugasSerializer,
)

from google import genai
from django.conf import settings

client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)
# =====================================
# HOME
# =====================================

def home(request):
    return render(request, "home.html")


# =====================================
# LOGIN
# =====================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("dashboard")

        return render(
            request,
            "login.html",
            {
                "error": "Username atau Password salah."
            }
        )

    return render(request, "login.html")

# =====================================
# DASHBOARD
# =====================================

@login_required
def dashboard(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user,
        defaults={
            "role": "admin" if request.user.is_superuser else "mahasiswa"
        }
    )

    # ================= ADMIN =================
    if profile.role == "admin":

        context = {
            "jumlah_mahasiswa": Mahasiswa.objects.count(),
            "jumlah_dosen": Dosen.objects.count(),
            "jumlah_course": Course.objects.count(),
            "jumlah_materi": Materi.objects.count(),
            "jumlah_tugas": Tugas.objects.count(),
        }

        return render(
            request,
            "admin_dashboard.html",
            context
        )

    # ================= DOSEN =================
    elif profile.role == "dosen":

        dosen = get_object_or_404(
            Dosen,
            user=request.user
        )

        courses = Course.objects.filter(
            dosen=dosen
        )

        return render(
            request,
            "teacher_dashboard.html",
            {
                "courses": courses,
                "dosen": dosen
            }
        )

    # ================= MAHASISWA =================
    # ================= MAHASISWA =================
    elif profile.role == "mahasiswa":

        mahasiswa = get_object_or_404(
            Mahasiswa,
            user=request.user
        )

        courses = Course.objects.filter(
            kelas=mahasiswa.kelas
        )

        return render(
            request,
            "student_dashboard.html",
            {
                "mahasiswa": mahasiswa,
                "courses": courses,
            }
        )

    return redirect("login")

@login_required
def ai_chat(request, chat_id=None):

    # Semua chat milik user
    chats = Chat.objects.filter(
        user=request.user
    ).order_by("-updated_at")

    # ===============================
    # Pilih chat
    # ===============================

    if chat_id:

        chat = get_object_or_404(
            Chat,
            id=chat_id,
            user=request.user
        )

    else:

        if chats.exists():

            chat = chats.first()

        else:

            chat = Chat.objects.create(
                user=request.user,
                title="Chat Baru"
            )

    # ===============================
    # Kirim Pesan
    # ===============================

    if request.method == "POST":

        pertanyaan = request.POST.get("pertanyaan")

        if pertanyaan:

            # Simpan pesan user
            ChatMessage.objects.create(
                chat=chat,
                role="user",
                message=pertanyaan
            )

            # -------------------------------
            # Ambil seluruh riwayat chat
            # -------------------------------

            riwayat = ChatMessage.objects.filter(
                chat=chat
            ).order_by("created_at")

            contents = []

            # System Prompt
            contents.append({
                "role": "user",
                "parts": [{
                    "text":
                    """
Kamu adalah Smart Learning AI.

Jawablah dalam Bahasa Indonesia.

Berikan jawaban yang jelas,
mudah dipahami mahasiswa.

Jika diminta membuat kode,
gunakan format code block.

Jika pengguna bertanya lanjutan,
ingat percakapan sebelumnya.
                    """
                }]
            })

            # Riwayat Percakapan

            for pesan in riwayat:

                if pesan.role == "user":

                    contents.append({
                        "role": "user",
                        "parts": [
                            {
                                "text": pesan.message
                            }
                        ]
                    })

                else:

                    contents.append({
                        "role": "model",
                        "parts": [
                            {
                                "text": pesan.message
                            }
                        ]
                    })

            # -----------------------------
            # Kirim ke Gemini
            # -----------------------------

            try:

                response = client.models.generate_content(

                    model="gemini-3.5-flash",

                    contents=contents

                )

                jawaban = response.text

            except Exception as e:

                jawaban = f"Terjadi kesalahan : {e}"

            # -----------------------------
            # Simpan jawaban AI
            # -----------------------------

            ChatMessage.objects.create(

                chat=chat,

                role="assistant",

                message=jawaban

            )

            # -----------------------------
            # Update Judul Chat
            # -----------------------------

            if chat.title == "Chat Baru":

                if len(pertanyaan) > 35:

                    chat.title = pertanyaan[:35] + "..."

                else:

                    chat.title = pertanyaan

            chat.save()

            return redirect(
                "chat_detail",
                chat.id
            )

    # ===============================
    # Ambil pesan
    # ===============================

    messages = ChatMessage.objects.filter(
        chat=chat
    ).order_by("created_at")

    return render(
        request,
        "ai_chat.html",
        {
            "chat": chat,
            "messages": messages,
            "chats": chats,
        }
    )

import pandas as pd

@login_required
def laporan_pandas(request):

    # ==========================
    # DATA MAHASISWA
    # ==========================
    mahasiswa = pd.DataFrame(
        list(
            Mahasiswa.objects.values(
                "nim",
                "nama",
                "kelas__nama"
            )
        )
    )

    if not mahasiswa.empty:
        mahasiswa.columns = [
            "NIM",
            "Nama Mahasiswa",
            "Kelas"
        ]

    # ==========================
    # DATA DOSEN
    # ==========================
    dosen = pd.DataFrame(
        list(
            Dosen.objects.values(
                "nip",
                "nama"
            )
        )
    )

    if not dosen.empty:
        dosen.columns = [
            "NIP",
            "Nama Dosen"
        ]

    # ==========================
    # DATA COURSE
    # ==========================
    course = pd.DataFrame(
        list(
            Course.objects.values(
                "semester__nama",
                "kelas__nama",
                "mata_kuliah__nama",
                "dosen__nama"
            )
        )
    )

    if not course.empty:
        course.columns = [
            "Semester",
            "Kelas",
            "Mata Kuliah",
            "Dosen"
        ]

    # ==========================
    # DATA MATERI
    # ==========================
    materi = pd.DataFrame(
        list(
            Materi.objects.values(
                "judul",
                "course__mata_kuliah__nama",
                "tanggal_upload"
            )
        )
    )

    if not materi.empty:
        materi.columns = [
            "Judul Materi",
            "Mata Kuliah",
            "Tanggal Upload"
        ]

    # ==========================
    # DATA TUGAS
    # ==========================
    tugas = pd.DataFrame(
        list(
            Tugas.objects.values(
                "judul",
                "course__mata_kuliah__nama",
                "deadline"
            )
        )
    )

    if not tugas.empty:
        tugas.columns = [
            "Judul Tugas",
            "Mata Kuliah",
            "Deadline"
        ]

    context = {

        # Ringkasan
        "total_mahasiswa": len(mahasiswa),
        "total_dosen": len(dosen),
        "total_course": len(course),
        "total_materi": len(materi),
        "total_tugas": len(tugas),

        # Tabel Pandas
        "mahasiswa": mahasiswa.to_html(
            classes="pandas-table",
            index=False,
            border=0
        ),

        "dosen": dosen.to_html(
            classes="pandas-table",
            index=False,
            border=0
        ),

        "course": course.to_html(
            classes="pandas-table",
            index=False,
            border=0
        ),

        "materi": materi.to_html(
            classes="pandas-table",
            index=False,
            border=0
        ),

        "tugas": tugas.to_html(
            classes="pandas-table",
            index=False,
            border=0
        ),
    }

    return render(
        request,
        "laporan_pandas.html",
        context
    )
# =====================================
# DETAIL COURSE
# =====================================

@login_required
def detail_course(request, course_id):

    profile = get_object_or_404(
        Profile,
        user=request.user
    )

    # Admin bebas melihat semua course
    if profile.role == "admin":

        course = get_object_or_404(
            Course,
            id=course_id
        )

    # Dosen hanya course miliknya
    elif profile.role == "dosen":

        dosen = get_object_or_404(
            Dosen,
            user=request.user
        )

        course = get_object_or_404(
            Course,
            id=course_id,
            dosen=dosen
        )

    # Mahasiswa hanya course sesuai kelas
    else:

        mahasiswa = get_object_or_404(
            Mahasiswa,
            user=request.user
        )

        course = get_object_or_404(
            Course,
            id=course_id,
            kelas=mahasiswa.kelas
        )

    materi = Materi.objects.filter(
        course=course
    )

    tugas = Tugas.objects.filter(
        course=course
    )

    context = {

        "course": course,

        "materi": materi,

        "tugas": tugas

    }

    return render(
        request,
        "course_detail.html",
        context
    )

# =====================================
# UPLOAD MATERI
# =====================================

@login_required
def upload_materi(request, course_id):

    profile = get_object_or_404(
        Profile,
        user=request.user
    )

    if profile.role != "dosen":
        return redirect("dashboard")

    dosen = get_object_or_404(
        Dosen,
        user=request.user
    )

    course = get_object_or_404(
        Course,
        id=course_id,
        dosen=dosen
    )

    if request.method == "POST":

        file = request.FILES.get("file")

        if not file:
            return render(
                request,
                "upload_materi.html",
                {
                    "course": course,
                    "error": "Silakan pilih file materi."
                }
            )

        Materi.objects.create(
            course=course,
            judul=request.POST.get("judul"),
            deskripsi=request.POST.get("deskripsi"),
            file=file
        )

        return redirect(
            "detail_course",
            course_id=course.id
        )

    return render(
        request,
        "upload_materi.html",
        {
            "course": course
        }
    )


# =====================================
# TAMBAH TUGAS
# =====================================

@login_required
def tambah_tugas(request, course_id):

    profile = get_object_or_404(
        Profile,
        user=request.user
    )

    if profile.role != "dosen":
        return redirect("dashboard")

    dosen = get_object_or_404(
        Dosen,
        user=request.user
    )

    course = get_object_or_404(
        Course,
        id=course_id,
        dosen=dosen
    )

    if request.method == "POST":

        judul = request.POST.get("judul")
        deskripsi = request.POST.get("deskripsi")
        deadline = request.POST.get("deadline")
        file_tugas = request.FILES.get("file_tugas")

        Tugas.objects.create(
            course=course,
            judul=judul,
            deskripsi=deskripsi,
            deadline=deadline,
            file_tugas=file_tugas
        )

        return redirect(
            "detail_course",
            course_id=course.id
        )

    return render(
        request,
        "tambah_tugas.html",
        {
            "course": course
        }
    )


# =====================================
# UPLOAD JAWABAN
# =====================================

@login_required
def upload_jawaban(request, tugas_id):

    profile = get_object_or_404(
        Profile,
        user=request.user
    )

    if profile.role != "mahasiswa":
        return redirect("dashboard")

    mahasiswa = get_object_or_404(
        Mahasiswa,
        user=request.user
    )

    tugas = get_object_or_404(
    Tugas,
    id=tugas_id
    )

    if timezone.now() > tugas.deadline:

        return render(
            request,
            "upload_jawaban.html",
            {
                "tugas": tugas,
                "error": "Maaf, deadline pengumpulan tugas telah berakhir."
            }
        )

    

    if request.method == "POST":

        file_jawaban = request.FILES.get("file_jawaban")

        if not file_jawaban:

            return render(
                request,
                "upload_jawaban.html",
                {
                    "tugas": tugas,
                    "error": "Silakan upload file jawaban."
                }
            )

        PengumpulanTugas.objects.create(
            tugas=tugas,
            mahasiswa=mahasiswa,
            file_jawaban=file_jawaban
        )

        return redirect(
            "detail_course",
            course_id=tugas.course.id
        )

    return render(
        request,
        "upload_jawaban.html",
        {
            "tugas": tugas
        }
    )

# =====================================
# DAFTAR JAWABAN
# =====================================

@login_required
def daftar_jawaban(request, course_id):

    profile = get_object_or_404(
        Profile,
        user=request.user
    )

    if profile.role != "dosen":
        return redirect("dashboard")

    dosen = get_object_or_404(
        Dosen,
        user=request.user
    )

    course = get_object_or_404(
        Course,
        id=course_id,
        dosen=dosen
    )

    jawaban = PengumpulanTugas.objects.filter(
        tugas__course=course
    ).order_by("-tanggal_kumpul")

    return render(
        request,
        "daftar_jawaban.html",
        {
            "course": course,
            "jawaban": jawaban
        }
    )

@login_required
def edit_materi(request, materi_id):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "dosen":
        return redirect("dashboard")

    dosen = get_object_or_404(Dosen, user=request.user)

    materi = get_object_or_404(
        Materi,
        id=materi_id,
        course__dosen=dosen
    )

    if request.method == "POST":

        materi.judul = request.POST.get("judul")
        materi.deskripsi = request.POST.get("deskripsi")

        if request.FILES.get("file"):
            materi.file = request.FILES.get("file")

        materi.save()

        return redirect("detail_course", course_id=materi.course.id)

    return render(
        request,
        "upload_materi.html",
        {
            "course": materi.course,
            "materi": materi,
            "edit": True
        }
    )

@login_required
def hapus_materi(request, materi_id):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "dosen":
        return redirect("dashboard")

    dosen = get_object_or_404(Dosen, user=request.user)

    materi = get_object_or_404(
        Materi,
        id=materi_id,
        course__dosen=dosen
    )

    course_id = materi.course.id

    materi.delete()

    return redirect("detail_course", course_id=course_id)

@login_required
def edit_tugas(request, tugas_id):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "dosen":
        return redirect("dashboard")

    dosen = get_object_or_404(Dosen, user=request.user)

    tugas = get_object_or_404(
        Tugas,
        id=tugas_id,
        course__dosen=dosen
    )

    if request.method == "POST":

        tugas.judul = request.POST.get("judul")
        tugas.deskripsi = request.POST.get("deskripsi")
        tugas.deadline = request.POST.get("deadline")

        if request.FILES.get("file_tugas"):
            tugas.file_tugas = request.FILES.get("file_tugas")

        tugas.save()

        return redirect("detail_course", course_id=tugas.course.id)

    return render(
        request,
        "tambah_tugas.html",
        {
            "course": tugas.course,
            "tugas": tugas,
            "edit": True
        }
    )

@login_required
def hapus_tugas(request, tugas_id):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "dosen":
        return redirect("dashboard")

    dosen = get_object_or_404(Dosen, user=request.user)

    tugas = get_object_or_404(
        Tugas,
        id=tugas_id,
        course__dosen=dosen
    )

    course_id = tugas.course.id

    tugas.delete()

    return redirect("detail_course", course_id=course_id)


# =====================================
# BERI NILAI
# =====================================

@login_required
def beri_nilai(request, jawaban_id):

    profile = get_object_or_404(
        Profile,
        user=request.user
    )

    if profile.role != "dosen":
        return redirect("dashboard")

    dosen = get_object_or_404(
        Dosen,
        user=request.user
    )

    jawaban = get_object_or_404(
        PengumpulanTugas,
        id=jawaban_id,
        tugas__course__dosen=dosen
    )

    if request.method == "POST":

        nilai = request.POST.get("nilai")

        if nilai:
            jawaban.nilai = int(nilai)
            jawaban.save()

        return redirect(
            "daftar_jawaban",
            course_id=jawaban.tugas.course.id
        )

    return render(
        request,
        "beri_nilai.html",
        {
            "jawaban": jawaban
        }
    )


# =====================================
# LOGOUT
# =====================================

def logout_view(request):

    logout(request)

    return redirect("login")

@login_required
def new_chat(request):

    chat = Chat.objects.create(

        user=request.user,

        title="Chat Baru"

    )

    return redirect(
        "chat_detail",
        chat.id
    )

class MahasiswaViewSet(viewsets.ModelViewSet):
    queryset = Mahasiswa.objects.all()
    serializer_class = MahasiswaSerializer


class DosenViewSet(viewsets.ModelViewSet):
    queryset = Dosen.objects.all()
    serializer_class = DosenSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class MateriViewSet(viewsets.ModelViewSet):
    queryset = Materi.objects.all()
    serializer_class = MateriSerializer


class TugasViewSet(viewsets.ModelViewSet):
    queryset = Tugas.objects.all()
    serializer_class = TugasSerializer


