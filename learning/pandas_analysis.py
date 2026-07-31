import pandas as pd

from .models import (
    Mahasiswa,
    Dosen,
    Course,
    Materi,
    Tugas,
)


def statistik_dashboard():

    data = {
        "Kategori": [
            "Mahasiswa",
            "Dosen",
            "Course",
            "Materi",
            "Tugas"
        ],
        "Jumlah": [
            Mahasiswa.objects.count(),
            Dosen.objects.count(),
            Course.objects.count(),
            Materi.objects.count(),
            Tugas.objects.count(),
        ]
    }

    df = pd.DataFrame(data)

    return df