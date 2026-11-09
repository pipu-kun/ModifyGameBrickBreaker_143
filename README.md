class Striker (Papan Pemukul)

    init: Menyiapkan posisi awal, ukuran, kecepatan, dan warna papan pemukul.

    display: Menggambar papan pemukul di layar dengan sudut melengkung dan garis aksen.

    update: Menggerakkan papan ke kiri atau kanan berdasarkan input tombol panah dan membatasi agar tidak keluar dari batas layar.

    getRect: Mengembalikan objek kotak pemukul untuk keperluan deteksi tabrakan.

class Block (Bata)

    init: Mengatur posisi, ukuran, warna, serta menentukan status khusus seperti bata peledak warna merah dan tingkat kesehatan bata di mana warna putih memerlukan dua kali pukul.

    display: Menggambar bata di layar jika kesehatannya masih di atas nol dan mengubah warna bata putih yang mulai rusak.

    hit: Mengurangi nilai kesehatan bata saat tertabrak bola.

    getRect dan getHealth: Mengembalikan posisi kotak bata serta sisa nilai kesehatannya.

Class Ball (Bola)

    init: Menyiapkan posisi, ukuran jari-jari, kecepatan, dan arah vektor gerak bola.

    display: Menggambar bola ke layar lengkap dengan efek bayangan agar terlihat hidup.

    update: Memperbarui posisi bola setiap bingkai, memantulkannya saat mengenai dinding samping atau atas, serta mendeteksi jika bola jatuh melewati batas bawah layar.

    reset: Mengembalikan posisi bola ke tengah layar saat pemain kehilangan nyawa.

    hit: Membalikkan arah gerak vertikal bola saat memantul.

    getRect: Mengembalikan area lingkaran bola untuk deteksi tabrakan.

Fungsi Pendukung

    drawBackground: Menggambar warna latar belakang dan garis grid tipis bergaya futuristik.

    collisionChecker: Memeriksa apakah terjadi tabrakan antara dua objek berbentuk kotak.

    explodeBlock: Menangani mekanisme ledakan area ketika bata merah hancur sehingga ikut menghapus bata lain di dalam radius tertentu.

    populateBlocks: Mengisi area permainan dengan sebaran bata secara acak berdasarkan konfigurasi jarak.

Pengelola game

    gameOver: Menampilkan layar kalah atau menang, mencetak skor, serta mendengarkan tombol Spasi untuk memulai ulang permainan atau keluar.

    main: Fungsi utama yang menjalankan perulangan permainan, menangani masukan papan ketik, memeriksa tabrakan bola dengan pemukul dan bata, memperbarui skor serta sisa nyawa, dan merender seluruh elemen permainan ke layar.
