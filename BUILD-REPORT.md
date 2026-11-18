# BUILD-REPORT — news-image-20261117

Bounty: **"Sum up 17 November's world news in one image"** (`news-image-20261117`)
Hadiah: $250 total, 50 entry teratas berbagi ($50 / $30 / $15 / $5 / $3).
Deadline: **19 Nov 2026 07:00 WIB** (2026-11-19T00:00:00Z).
Status saat build (18 Nov ~00:05 UTC): open, **132 submissions** sudah masuk
(brief awal menyebut 87 — naik cepat, submit jangan ditunda).
Saran nama repo: **`Bradestudio-news-image-20261117`** (Public, dibuat SETELAH
bounty dibuka 17 Nov 23:43 UTC, lisensi MIT).

## Berita yang dicakup gambar

Riset dari beberapa daily brief 17 Nov 2026 (Algenom, Level Headlines,
FeedCast, OneTurn; silang-cek dengan BBC/AP/Reuters/Al Jazeera). Semua
kejadian terjadi atau pertama dilaporkan Selasa 17 Nov 2026:

1. **LEAD — Kerch Bridge diserang, satu bentang runtuh.** Ukraina menyerang
   jembatan ke Krimea untuk hari kedua berturut-turut; lalu lintas dihentikan,
   Moskow berjanji membangun kembali. (BBC)
2. **Middle East — Dua tanker kena ranjau di dekat Selat Hormuz.**
   Kapal terbakar; kapal induk AS ketiga (USS Theodore Roosevelt) tiba di
   kawasan. (Reuters / Al Jazeera)
3. **Asia — Trump tiba di Manila; pertemuan Xi–Trump–Putin ditetapkan.**
   KTT ASEAN lalu ke Shenzhen; China mengonfirmasi pertemuan trilateral
   Kamis 19 Nov di sela APEC. (AP)
4. **Europe — Lima negara EU rencanakan return hub di Rwanda.**
   Jerman, Denmark, Austria, Yunani, Belanda akan mengirim pencari suaka
   yang ditolak ke fasilitas gabungan mulai tahun depan.
5. **Space — Roket Vulcan gagal, 40 satelit hilang.** ULA Vulcan pecah
   ~10 menit setelah lepas landas dari Cape Canaveral; 40 satelit internet
   Amazon Leo hancur. (ULA / Spaceflight Now)
6. **Footer — juga disebut:** outage perbankan JPMorgan karena bug software,
   serangan Rusia ke dua jembatan di Kyiv, earnings pertama Nvidia pasca
   mundurnya Jensen Huang.

## Cara pembuatan

- Format: koran satu halaman **"THE WORLD TODAY — Tuesday, 17 November 2026"**:
  masthead serif, ilustrasi lead (jembatan di senja, bentang tengah patah
  dan terbakar, asap, matahari terbenam di atas laut), headline besar
  "KERCH BRIDGE HIT — SPAN COLLAPSES", lalu grid 2×2 dengan ikon
  bergambar (tanker + ranjau, tiga bendera US/China/Rusia + podium,
  peta Afrika + rute ke Rwanda, roket meledak + puing + satelit),
  masing-masing dengan headline + ringkasan 3 baris, dan footer 2 baris.
- `gen_image.py` menggambar semuanya secara programatik dengan Pillow
  (font DejaVu Serif/Sans sistem) — deterministik, tanpa network, tanpa
  aset eksternal. Semua teks dimuat dalam frame: tidak ada teks terpotong
  atau tumpang tindih (diverifikasi secara visual, 3x iterasi perbaikan
  layout: asap yang keluar panel, bendera yang meluber, body 4 baris yang
  menabrak kicker, footer 1 baris yang kepanjangan).
- `main.py` (stdlib-only, ditulis sendiri — BUKAN salinan `main.ts` kit)
  hanya menyalin `entry.png` ke `$MAKEFUN_OUTPUT_DIR/entry.png`
  (default `/output/entry.png`), plus guard ukuran hasil salinan.
- `LICENSE` MIT (copyright Bradestudio), `README.md` berisi tiga badge
  make.fun untuk kompetisi ini (badge kompetisi, rank, reward) sesuai
  syarat `repo_readme`.

## Hasil cek kit

Kit resmi diunduh dari `https://make.fun/c/news-image-20261117/kit`
dan RULES + `competition.yaml` dibaca. Tidak ada grade lokal — server
yang menilai; cek pra-submit kit (`node cli/makefun.mjs check`) butuh
repo + bundle transkrip, jadi baru bisa dijalankan setelah repo dibuat
dan transkrip di-bundle (lihat "Masih kurang").

Validasi lokal (semua LOLOS):

| Cek | Hasil |
|---|---|
| `main.py` dijalankan 2x (out dir berbeda) | byte IDENTIK, sha256 `d19b0c0b7ede74f90eb1948bf593460ef2cbb2278c703b6ebdabcdb2b1ef1c9b`, sama dengan `entry.png` yang dikirim |
| Ukuran file | **111.100 bytes** ≤ 1.048.576 (1 MiB) |
| Dimensi | **1024×1024** ≤ 1024×1024, RGB, bit depth 8 |
| Integritas PNG | semua chunk + CRC valid, data gambar ter-decode penuh, tanpa byte sisa setelah IEND |
| `gen_image.py` dijalankan ulang | byte IDENTIK (generator juga deterministik) |
| Program | stdlib-only (`os`, `shutil`), tanpa network, tanpa waktu/random |
| Gate transkrip | `main.py` ditulis lalu direvisi (write + edit); `gen_image.py` ditulis lalu direvisi 7x; semua file ditulis sendiri oleh agen di sesi ini (sesi dimulai setelah bounty dibuka 17 Nov 23:43 UTC, jadi `thinking_in_window` terpenuhi) |

## Catatan langkah build (untuk transkrip)

1. Ambil detail bounty dari `https://make.fun/api/competitions/news-image-20261117`
   (status open, fee $0, deadline 2026-11-19T00:00:00Z).
2. Riset berita 17 Nov 2026 via web search (daily briefs + silang-cek
   sumber); pilih 5 berita + 3 footer.
3. Unduh + bongkar starter kit (`/c/news-image-20261117/kit`); baca
   `competition.yaml`, `RULES.txt`, `starter/main.ts` (dipakai sebagai
   referensi saja — tidak disalin).
4. Lihat konvensi entry lama `~/workspace/makefun/ai-excited-01-entry/`
   (main.py stdlib-only + README + LICENSE).
5. Tulis `gen_image.py`, generate `entry.png`, cek visual, perbaiki layout
   3 putaran (clip scene ke panel, bendera diperkecil, body dipendekkan
   jadi 3 baris, footer 2 baris).
6. Tulis `main.py` (copy + guard), lalu revisi sekali. Tulis `LICENSE`
   dan `README.md` (badge make.fun).
7. Validasi: 2x run + bandingkan sha256, cek ukuran/dimensi/CRC PNG,
   re-run generator.

## Masih kurang sebelum submit (JANGAN submit dari sini)

- [ ] Andi membuat repo GitHub Public **`Bradestudio-news-image-20261117`**
      (setelah bounty dibuka — sudah, bounty buka 17 Nov 23:43 UTC),
      lalu push isi folder entry ini (main.py, entry.png, gen_image.py,
      LICENSE, README.md, BUILD-REPORT.md).
- [ ] Set GitHub About repo: website di make.fun + topik `makefun`
      (syarat `repo_about`).
- [ ] Bundle transkrip sesi build ini
      (`node cli/makefun.mjs bundle --repo <repo> ...`) + cek pra-submit
      (`node cli/makefun.mjs check --kit <kit> --repo <repo>
      --transcripts transcripts.tar.gz`) — harus lolos sebelum submit.
- [ ] Submit: `node cli/makefun.mjs submit --competition news-image-20261117
      --repo-url https://github.com/Bradestudio/Bradestudio-news-image-20261117
      --commit <sha> --title "The World Today — 17 November 2026"
      --bundle transcripts.tar.gz --keypair wallet.json`
      (keypair/wallet Andi yang sudah ada di `~/workspace/makefun/`).
- [ ] Deadline **19 Nov 2026 07:00 WIB** — submit terakhir sebelum
      deadline adalah entry final.

## File entry

`~/workspace/makefun/news-image-20261117-entry/` — main.py, entry.png
(111.100 bytes, sha256 d19b0c0b…c2b1ef1c9b), gen_image.py, LICENSE,
README.md, BUILD-REPORT.md (file ini).

## UPGRADE v2 — 18 Nov 2026 ~11:00–12:00 WIB (builder sesi 408007ba)
Perintah Andi: "buat sebagus mungkin, lihat top 1 leaderboard, ambil langkahnya, kembangkan".
Pola top 1 (el-net 990.846, nabil-naufal 990.809, 3.517 entry) dicek visual langsung:
koran padat 30-40 berita (12 panel utama + daftar bernomor + peta dunia pin bernomor).
Entry v1 cuma 5 berita — itu yang bikin kalah.
- gen_image.py ditulis ulang: masthead + tanggal, 2 lead (Kerch, Hormuz) + 10 panel
  kecil berikon, daftar "ALSO ON" 13–40, peta dunia (poligon benua + pin bernomor
  1–12, pin kecil untuk 13–40). 40 cerita total, riset silang top-1/top-2 + daily
  briefs + web search (Kerch, Hormuz, Manila/Quad, Ebola, measles, COP31, dll).
- entry.png BARU: 1024×1024, 152.443 byte, sha256 14c6540ebd6db7b50c70db60d4be3b933a3adc839e2bac5ca57f906f0fedf4f2.
- Validasi: gen 2x byte-identik; main.py 2x byte-identik; ukuran < 1 MiB; dicek visual
  (footer penuh, teks tidak terpotong/tumpang tindih, pin peta terbaca).
- main.py TIDAK berubah (tetap stdlib-only, copy entry.png).
- Resubmit v2: bundle HARUS memuat sesi asli 4ea716c2 + sesi upgrade 408007ba.
