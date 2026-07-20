from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import json
import uvicorn
import os

app = FastAPI()

# Barcha kubiklar ro'yxati
TOVARLAR = [
    {
        "id": 1,
        "nomi": "Monster Go 3x3 Magnetic",
        "narxi": 160000,
        "brend": "GAN",
        "tavsif": "Magnitli professional kubik. Juda yengil, baraka topasan! Burilishlari silliq va tez.",
        "rasmlar": "https://images.unsplash.com/photo-1591808051642-881a7a402322?w=500,https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=500,https://images.unsplash.com/photo-1546776310-eef45dd6d63c?w=500",
        "sharhlar": ["Daxshat kubik ekan, srazi 40 sekunda terdim!", "Gan baribir zo'r, tavsiya qilaman."]
    },
    {
        "id": 2,
        "nomi": "MoYu WeiLong WR M V9",
        "narxi": 380000,
        "brend": "MoYu",
        "tavsif": "Eng yuqori darajadagi flagman model. Magnitlari kuchli, sozlamalari juda ko'p.",
        "rasmlar": "https://images.unsplash.com/photo-1591808051642-881a7a402322?w=500,https://images.unsplash.com/photo-1546776310-eef45dd6d63c?w=500,https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=500",
        "sharhlar": ["Narxiga arziydi, juda tez.", "Menga magnitlari juda yoqdi."]
    }
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <title>Alpha Cube - Geymerlar Ekotizimi</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #080c14; color: #fff; margin: 0; padding: 20px; }
        .header { background: linear-gradient(135deg, #111827, #311042); padding: 40px; text-align: center; border-radius: 12px; margin-bottom: 30px; border-bottom: 3px solid #a855f7; }
        .header h1 { color: #38bdf8; font-size: 3rem; margin: 0; letter-spacing: 3px; text-shadow: 0 0 10px #38bdf8; }
        .container { display: flex; gap: 20px; max-width: 1300px; margin: 0 auto; align-items: flex-start; }
        .products-grid { display: flex; flex-wrap: wrap; gap: 20px; flex: 3; }
        .card { background-color: #0f172a; border: 2px solid #1e293b; border-radius: 16px; padding: 20px; width: 280px; cursor: pointer; transition: all 0.3s; position: relative; overflow: hidden; }
        .card:hover { transform: scale(1.03); border-color: #a855f7; box-shadow: 0 0 15px rgba(168, 85, 247, 0.4); }
        .card img { width: 100%; height: 200px; object-fit: cover; border-radius: 10px; margin-bottom: 15px; }
        .badge { background-color: #1e293b; color: #38bdf8; padding: 4px 10px; border-radius: 20px; font-size: 0.8rem; display: inline-block; margin-bottom: 10px; border: 1px solid #38bdf8; }
        .card h3 { margin: 10px 0; font-size: 1.4rem; color: #f3f4f6; }
        .card p { color: #94a3b8; font-size: 0.9rem; min-height: 40px; }
        .price { color: #4ade80; font-size: 1.5rem; font-weight: bold; margin: 15px 0; text-shadow: 0 0 5px rgba(74, 222, 128, 0.3); }
        .btn { background: linear-gradient(90deg, #38bdf8, #a855f7); color: #fff; border: none; padding: 12px; width: 100%; border-radius: 8px; font-weight: bold; cursor: pointer; font-size: 1rem; text-transform: uppercase; transition: 0.2s; }
        .btn:hover { filter: brightness(1.2); box-shadow: 0 0 10px #a855f7; }
        .form-container { background-color: #111827; border: 2px solid #38bdf8; border-radius: 16px; padding: 25px; flex: 1; min-width: 320px; box-shadow: 0 0 15px rgba(56, 189, 248, 0.2); }
        .form-container h2 { color: #38bdf8; margin-top: 0; }
        input, textarea { width: 100%; padding: 12px; margin-bottom: 15px; border-radius: 8px; border: 1px solid #334155; background-color: #070a12; color: #fff; box-sizing: border-box; }
        input:focus, textarea:focus { border-color: #a855f7; outline: none; }
        .btn-submit { background: linear-gradient(90deg, #a855f7, #6366f1); }
        .modal { display: none; position: fixed; z-index: 999; left: 0; top: 0; width: 100%; height: 100%; background-color: rgba(5, 7, 12, 0.9); justify-content: center; align-items: center; backdrop-filter: blur(5px); }
        .modal-content { background-color: #0f172a; border: 3px solid #a855f7; border-radius: 24px; width: 85%; max-width: 950px; display: flex; overflow: hidden; box-shadow: 0 0 30px #a855f7; position: relative; animation: openModal 0.3s ease-out; }
        @keyframes openModal { from { transform: scale(0.8); opacity: 0; } to { transform: scale(1); opacity: 1; } }
        .close-btn { position: absolute; top: 15px; right: 20px; color: #94a3b8; font-size: 30px; font-weight: bold; cursor: pointer; z-index: 10; transition: 0.2s; }
        .close-btn:hover { color: #ff0055; }
        .modal-left { flex: 1.2; padding: 25px; background-color: #070b12; display: flex; flex-direction: column; gap: 15px; border-right: 2px solid #1e293b; }
        .main-img-container { width: 100%; height: 320px; border-radius: 12px; overflow: hidden; border: 2px solid #334155; }
        .main-img-container img { width: 100%; height: 100%; object-fit: cover; }
        .thumbnails-grid { display: flex; gap: 10px; flex-wrap: wrap; }
        .thumb-img { width: 65px; height: 65px; object-fit: cover; border-radius: 6px; cursor: pointer; border: 2px solid #1e293b; opacity: 0.6; transition: 0.2s; }
        .thumb-img:hover, .thumb-img.active { opacity: 1; border-color: #38bdf8; }
        .modal-right { flex: 1; padding: 25px; display: flex; flex-direction: column; overflow-y: auto; max-height: 500px; }
        .modal-right h2 { margin-top: 0; font-size: 2rem; color: #fff; border-bottom: 2px solid #1e293b; padding-bottom: 10px; }
        .modal-shop-name { color: #a855f7; font-weight: bold; font-size: 1.1rem; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 1px; }
        .modal-desc { color: #cbd5e1; line-height: 1.6; font-size: 0.95rem; margin-bottom: 20px; }
        .promo-section { background-color: #1e1b4b; border: 1px dashed #6366f1; padding: 15px; border-radius: 12px; margin-bottom: 20px; }
        .promo-section input { margin-bottom: 8px; padding: 8px; font-size: 0.9rem; text-align: center; letter-spacing: 2px; }
        .promo-btn { width: 100%; padding: 8px; font-size: 0.9rem; background-color: #6366f1; border: none; border-radius: 6px; color: #fff; font-weight: bold; cursor: pointer; }
        .reviews-section { margin-top: 15px; border-top: 2px solid #1e293b; padding-top: 15px; }
        .reviews-section h4 { margin: 0 0 10px 0; color: #38bdf8; font-size: 1.1rem; }
        .review-item { background-color: #1e293b; padding: 10px; border-radius: 8px; margin-bottom: 8px; font-size: 0.85rem; border-left: 3px solid #a855f7; color: #e2e8f0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>ALPHA CUBE</h1>
        <p>Geymerlar va professionallar uchun maxsus kubiklar do'koni</p>
    </div>
    <div class="container">
        <div class="products-grid"> REPLACE_PRODUCTS_HERE </div>
        <div class="form-container">
            <h2>Yangi Kubik Qo'shish</h2>
            <form action="/qoshish" method="post">
                <input type="text" name="nomi" placeholder="Kubik nomi (Masalan: GAN 14 MagLev)" required>
                <input type="text" name="brend" placeholder="Brendi (Masalan: GAN, MoYu)" required>
                <input type="number" name="narxi" placeholder="Narxi (so'mda)" required>
                <textarea name="rasmlar" placeholder="Rasmlar URL manzillari (Kamida 3 ta, har birini vergul (,) bilan ajratib yozing!)" rows="4" required></textarea>
                <textarea name="tavsif" placeholder="Tovar haqida geymercha batafsil ma'lumot..." rows="3"></textarea>
                <button type="submit" class="btn btn-submit">Do'konga Joylash</button>
            </form>
        </div>
    </div>
    <div id="gamerModal" class="modal" onclick="closeModalOutside(event)">
        <div class="modal-content">
            <span class="close-btn" onclick="toggleModal(false)">&times;</span>
            <div class="modal-left">
                <div class="main-img-container"> <img id="modalMainImg" src="" alt="Asosiy Rasm"> </div>
                <div id="modalThumbnails" class="thumbnails-grid"></div>
            </div>
            <div class="modal-right">
                <div class="modal-shop-name">🏪 Do'kon: Alpha Cube Store</div>
                <h2 id="modalTitle">Kubik Nomi</h2>
                <div class="modal-desc" id="modalDesc">Batafsil tavsif shu yerda bo'ladi...</div>
                <div class="price" id="modalPrice">0 so'm</div>
                <div class="promo-section">
                    <input type="text" id="promoInput" placeholder="PROMO KOD">
                    <button class="promo-btn" onclick="applyPromo()">Kodni tekshirish</button>
                    <div id="promoMsg" style="font-size: 0.85rem; margin-top: 5px; text-align: center;"></div>
                </div>
                <button class="btn" style="font-size: 1.2rem; padding: 15px;">Hozir sotib olish</button>
                <div class="reviews-section">
                    <h4>💬 Xaridorlar sharhlari:</h4>
                    <div id="modalReviews"></div>
                </div>
            </div>
        </div>
    </div>
    <script>
        const productsData = REPLACE_JS_DATA;
        let activeBasePrice = 0;
        function openProduct(id) {
            const product = productsData.find(p => p.id === id);
            if(!product) return;
            activeBasePrice = product.narxi;
            document.getElementById('modalTitle').innerText = product.nomi;
            document.getElementById('modalDesc').innerText = product.tavsif;
            document.getElementById('modalPrice').innerText = product.narxi.toLocaleString('ru-RU') + " so'm";
            document.getElementById('promoInput').value = "";
            document.getElementById('promoMsg').innerText = "";
            const imgList = product.rasmlar.split(',').map(url => url.trim()).filter(url => url.length > 0);
            const mainImg = document.getElementById('modalMainImg');
            mainImg.src = imgList[0] || 'https://images.unsplash.com/photo-1591808051642-881a7a402322?w=500';
            const thumbGrid = document.getElementById('modalThumbnails');
            thumbGrid.innerHTML = "";
            imgList.forEach((url, index) => {
                if(index < 10) {
                    const imgEl = document.createElement('img');
                    imgEl.src = url;
                    imgEl.className = 'thumb-img' + (index === 0 ? ' active' : '');
                    imgEl.onclick = function() {
                        mainImg.src = url;
                        document.querySelectorAll('.thumb-img').forEach(el => el.classList.remove('active'));
                        imgEl.classList.add('active');
                    };
                    thumbGrid.appendChild(imgEl);
                }
            });
            const reviewsDiv = document.getElementById('modalReviews');
            reviewsDiv.innerHTML = "";
            if(product.sharhlar && product.sharhlar.length > 0) {
                product.sharhlar.forEach(sh => {
                    const shEl = document.createElement('div');
                    shEl.className = 'review-item';
                    shEl.innerText = sh;
                    reviewsDiv.appendChild(shEl);
                });
            } else {
                reviewsDiv.innerHTML = "<div style='color:#64748b; font-size:0.85rem;'>Hozircha sharhlar yo'q. Birinchi bo'lib qoldiring!</div>";
            }
            toggleModal(true);
        }
        function toggleModal(show) { document.getElementById('gamerModal').style.display = show ? 'flex' : 'none'; }
        function closeModalOutside(e) { if(e.target.id === 'gamerModal') toggleModal(false); }
        function applyPromo() {
            const code = document.getElementById('promoInput').value.trim().toUpperCase();
            const msg = document.getElementById('promoMsg');
            const priceEl = document.getElementById('modalPrice');
            if(code === 'ALPHA40' || code === 'BARAKA') {
                const newPrice = activeBasePrice * 0.9;
                priceEl.innerText = newPrice.toLocaleString('ru-RU') + " so'm (Promokod faol!)";
                priceEl.style.color = "#22c55e";
                msg.innerText = "✅ 10% chegirma qo'llanildi!";
                msg.style.color = "#4ade80";
            } else {
                msg.innerText = "❌ Bunday promokod mavjud emas!";
                msg.style.color = "#f87171";
            }
        }
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def bosh_sahifa(request: Request):
    tovarlar_html = ""
    for tovar in TOVARLAR:
        rasm_top = tovar['rasmlar'].split(',')[0].strip()
        if not rasm_top:
            rasm_top = "https://images.unsplash.com/photo-1591808051642-881a7a402322?w=500"
        tovarlar_html += f"""
        <div class="card" onclick="openProduct({tovar['id']})">
            <img src="{rasm_top}" alt="{tovar['nomi']}">
            <span class="badge">{tovar['brend']}</span>
            <h3>{tovar['nomi']}</h3>
            <p>{tovar['tavsif'][:60]}...</p>
            <div class="price">{tovar['narxi']:,} so'm</div>
            <button class="btn">Sotib olish</button>
        </div>
        """
    js_data = json.dumps(TOVARLAR)
    yakuniy_kod = HTML_TEMPLATE.replace("REPLACE_PRODUCTS_HERE", tovarlar_html).replace("REPLACE_JS_DATA", js_data)
    return yakuniy_kod

@app.post("/qoshish")
async def yangi_tovar(nomi: str = Form(...), narxi: int = Form(...), brend: str = Form(...), tavsif: str = Form(...), rasmlar: str = Form(...)):
    yangi_id = len(TOVARLAR) + 1
    TOVARLAR.append({
        "id": yangi_id,
        "nomi": nomi,
        "narxi": narxi,
        "brend": brend,
        "tavsif": tavsif,
        "rasmlar": rasmlar,
        "sharhlar": ["Yangi kelgan tovar! Birinchilardan bo'lib sharh qoldiring."]
    })
    return RedirectResponse(url="/", status_code=303)

# RENDER UCHUN ISHGA TUSHIRISH QISMI
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
