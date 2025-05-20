from PIL import Image, ImageDraw, ImageFont
import random, textwrap, qrcode

def draw_centered_table(draw, text, font, cell_x, cell_y, cell_width, cell_height, fill="black"):
    """
    Fungsi untuk menggambar teks di dalam sel tabel dengan posisi center.

    :param draw: Objek ImageDraw
    :param text: Teks yang akan digambar
    :param font: Font yang digunakan
    :param cell_x: Koordinat X kiri sel
    :param cell_y: Koordinat Y atas sel
    :param cell_width: Lebar sel
    :param cell_height: Tinggi sel
    :param fill: Warna teks
    """
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]  # Dapatkan ukuran teks
    text_x = cell_x + (cell_width - text_width) // 2  # Center secara horizontal
    text_y = cell_y + (cell_height - text_height) // 2  # Center secara vertikal
    draw.text((text_x, text_y), text, fill=fill, font=font)

def draw_centered_text(draw, text, font, center_x, center_y, fill="black"):
    """
    Fungsi untuk menggambar teks dengan posisi terpusat (center) berdasarkan koordinat x, y.

    :param draw: Objek ImageDraw
    :param text: Teks yang akan digambar
    :param font: Font yang digunakan
    :param center_x: Koordinat X tengah
    :param center_y: Koordinat Y tengah
    :param fill: Warna teks
    """
    if not text:
        return  # Hindari error jika text = None atau kosong
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]  # Ambil ukuran teks
    text_x = center_x - (text_width // 2)  # Hitung posisi X agar center
    text_y = center_y - (text_height // 2)  # Hitung posisi Y agar center
    draw.text((text_x, text_y), text, fill=fill, font=font)

def create_certificate(train_id, name, certificate_code, train_name, school, listOfSection, date)->str:
    img = Image.open('media/template/template.png')
    d = ImageDraw.Draw(img)
    center_x = img.width // 2
    
    loc_noseri = 438
    loc_name = 600
    loc_school = 690
    loc_desc = 938

    font1 = ImageFont.truetype(
        "apps/utils/bebas.ttf", 50
    )
    font2 = ImageFont.truetype(
        "apps/utils/roboto_medium.ttf", 24
    )
    font2_40 = ImageFont.truetype(
        'apps/utils/roboto_medium.ttf', 40
    )
    font3 = ImageFont.truetype(
        "apps/utils/roboto_regular.ttf", 20
    )
    font3_30 = ImageFont.truetype(
        "apps/utils/roboto_regular.ttf", 24
    )
    
    draw_centered_text(d, certificate_code, font2_40, center_x, loc_noseri)
    draw_centered_text(d, name, font1, center_x, loc_name)
    draw_centered_text(d, school, font1, center_x, loc_school)
    
    description = f'Diklat dengan tema : {train_name}'
    line_spacing = 10 
    
    wrapped_text = textwrap.wrap(description, width=70)

    for line in wrapped_text:
        draw_centered_text(d, line, font3_30, center_x, loc_desc)
        text_height = d.textbbox((0, 0), line, font=font3_30)[3] - d.textbbox((0, 0), line, font=font3_30)[1]
        loc_desc += text_height + line_spacing
    

    # Posisi tabel
    y_start = loc_desc + 30
    row_height = 60
    col_widths = [50, 800, 120]
    table_width = sum(col_widths)
    x_start = (img.width - table_width) // 2
    
    # Data
    header = ["No", "Materi", "JP"]
    # listOfSection = [
    #     ["Pengantar Akun Belajar.id: Fitur, Manfaat, dan Potensi", "10JP"],
    #     ["Praktik Integrasi Akun Belajar.id Dengan Canva", "11JP"],
    #     ["Praktik Integrasi Akun Belajar.id Dengan Quizziz", "11JP"]
    # ]

    # Warna Header
    d.rectangle([x_start, y_start, x_start + table_width, y_start + row_height], outline="black", fill="gray")
    x_pos = x_start
    for i, col_name in enumerate(header):
        d.text((x_pos + 10, y_start + 10), col_name, fill="white", font=font2)
        x_pos += col_widths[i]

    y_start += row_height
    total_jp = 0

    # Fungsi membagi teks panjang menjadi beberapa baris
    def wrap_text(text, font, max_width):
        lines = []
        words = text.split()
        while words:
            line = ''
            while words and font.getlength(line + words[0]) < max_width:
                line += (words.pop(0) + " ")
            lines.append(line.strip())
        return lines

    # Menggambar isi tabel
    for idx, row in enumerate(listOfSection, start=1):
        x_pos = x_start
        total_row_jp = int(row[1].replace("JP", ""))  # Ambil angka JP
        total_jp += total_row_jp
        
        # Bungkus teks jika terlalu panjang
        wrapped_text = wrap_text(row[0], font3_30, col_widths[1] - 20)

        # Tentukan tinggi baris berdasarkan jumlah baris teks
        row_h = row_height * len(wrapped_text)

        # Nomor
        d.rectangle([x_pos, y_start, x_pos + col_widths[0], y_start + row_h], outline="black", fill="white")
        d.text((x_pos + 15, y_start + 10), str(idx), fill="black", font=font3_30)
        x_pos += col_widths[0]

        # Materi
        d.rectangle([x_pos, y_start, x_pos + col_widths[1], y_start + row_h], outline="black", fill="white")
        for i, line in enumerate(wrapped_text):
            d.text((x_pos + 10, y_start + 10 + (i * 25)), line, fill="black", font=font3_30)
        x_pos += col_widths[1]

        # Total JP
        d.rectangle([x_pos, y_start, x_pos + col_widths[2], y_start + row_h], outline="black", fill="white")
        d.text((x_pos + 15, y_start + 10), f"{total_row_jp}JP", fill="black", font=font3_30)

        y_start += row_h

    # Baris total JP
    d.rectangle([x_start, y_start, x_start + table_width, y_start + row_height], outline="black", fill="lightgray")
    d.text((x_start + 10, y_start + 10), "Total JP", fill="black", font=font2)
    d.text((x_start + col_widths[0] + col_widths[1] + 10, y_start + 10), f"{total_jp}JP", fill="black", font=font2)

    loc_kehadiran = y_start + 100
    draw_centered_text(d, "Kehadiran", font2_40, center_x, loc_kehadiran)
    
    loc_hadir = loc_kehadiran + 50
    draw_centered_text(d, f'{date} : HADIR', font3_30, center_x, loc_hadir)

    file_name = "media/file/certificate/" + name + " - " + train_name +' - '+ str(random.randint(0, 255)) + ".pdf"
    
    qr = qrcode.QRCode(version = 1, box_size= 10, border=3)
    qr.add_data(certificate_code)
    qr.make(fit=True)
    
    img_qr = qr.make_image(fill_color = 'black', back_color = 'white')
    img_qr.save(f'media/file/qr/{name} - {train_id}.jpg')
    
    img_qr_load = Image.open(f'media/file/qr/{name} - {train_id}.jpg')
    qr_size = (200,200)
    img_qr_resize = img_qr_load.resize(qr_size)
    
    q_post = (132,1600)
    
    img.paste(img_qr_resize, q_post)
    
    img.save(file_name)
    return file_name


    