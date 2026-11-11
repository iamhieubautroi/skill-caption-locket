# -*- coding: utf-8 -*-
"""
Sinh bảng màu gradient cho caption Locket.

Mỗi cặp màu được thiết kế trong OKLCH (L, C, H) rồi đổi ra HEX:
  Nền 1 = (L, C, H)
  Nền 2 = (L - dL, C + dC, H + dH)   -> tối hơn + xoay hue (hue shift)
Script tự:
  - ép màu vào gam sRGB (giảm C, giữ L và H),
  - chọn Màu chữ Đen/Trắng theo tương phản WCAG,
  - nếu chưa đạt >= 4.5:1 trên CẢ HAI nền thì đẩy độ sáng (tối đa 0.08),
  - cảnh báo cặp trùng nhau và cặp lệch hue quá 40 độ.

Chạy:  python tao_bang_mau.py
Ra:    references/bang-mau-locket.md, references/bang-mau-locket.json,
       assets/xem-truoc-bang-mau.html
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "references")
ASSETS = os.path.join(HERE, "..", "assets")
MIN_CONTRAST = 4.5
MAX_HUE_GAP = 40

# (tên, L, C, H, dL, dH, dC, [chủ đề], ghi chú vibe)
SPECS = [
    # ---------- PASTEL / SÁNG (chữ Đen) ----------
    ("Kẹo dâu",            0.87, 0.11,  12, 0.08, -12, 0.01, ["tình yêu", "ngọt", "crush"], "ngọt, dễ thương"),
    ("Đào chín",           0.90, 0.07,  45, 0.07, -15, 0.01, ["ăn uống", "ngọt", "sáng sớm"], "ấm, mềm"),
    ("Vani kem",           0.94, 0.06,  95, 0.06, -20, 0.01, ["ăn uống", "chill", "sáng sớm"], "sạch, nhẹ"),
    ("Bơ sáp",             0.92, 0.08, 125, 0.07,  15, 0.01, ["ăn uống", "thiên nhiên"], "tươi, healthy"),
    ("Bạc hà",             0.92, 0.06, 170, 0.07,  20, 0.01, ["ốm", "chill", "lạnh"], "mát, sạch"),
    ("Matcha latte",       0.88, 0.08, 135, 0.08,  12, 0.01, ["trà sữa", "cafe", "ăn uống", "hà nội", "mùa thu"], "trà xanh sữa"),
    ("Nước biển nông",     0.91, 0.06, 205, 0.07,  20, 0.01, ["biển", "du lịch", "chill"], "trong veo"),
    ("Trời trong",         0.90, 0.06, 240, 0.07,  15, 0.01, ["sáng sớm", "học", "chill"], "sáng, thoáng"),
    ("Oải hương",          0.88, 0.07, 300, 0.07,  15, 0.01, ["ngủ", "chill", "đà lạt"], "mơ màng"),
    ("Khoai môn",          0.85, 0.08, 310, 0.08, -12, 0.01, ["trà sữa", "ăn uống", "ngọt"], "tím sữa"),
    ("Hồng phấn",          0.91, 0.06, 350, 0.07, -12, 0.01, ["tình yêu", "phụ nữ", "makeup", "cưới"], "nữ tính"),
    ("Sen hồng",           0.88, 0.08, 355, 0.08, -15, 0.01, ["tâm linh", "phụ nữ", "gia đình", "tết"], "thanh, hiền"),
    ("Kem dừa",            0.95, 0.03,  85, 0.06, -10, 0.00, ["tối giản", "flex", "20/11", "cưới", "sang chảnh"], "trắng ngà"),
    ("Trà sữa trân châu",  0.84, 0.07,  65, 0.10, -10, 0.01, ["trà sữa", "ăn uống"], "caramel sữa"),
    ("Bánh flan",          0.90, 0.10,  85, 0.08, -25, 0.02, ["ăn uống", "vô tri", "ngọt"], "vàng trứng"),
    ("Xoài non",           0.92, 0.12, 105, 0.06, -25, 0.02, ["nắng", "mùa hè", "ăn uống"], "vàng tươi"),
    ("Chanh neon",         0.92, 0.18, 120, 0.08, -15, 0.00, ["meme", "vô tri", "party"], "lime chói"),
    ("Cam sữa",            0.86, 0.12,  60, 0.08, -15, 0.01, ["thú cưng", "vô tri", "ăn uống"], "mèo cam"),
    ("Táo xanh",           0.88, 0.14, 135, 0.08,  15, 0.00, ["gym", "healthy", "du lịch"], "giòn, tươi"),
    ("Ngọc mint",          0.86, 0.11, 175, 0.08,  20, 0.00, ["chill", "biển", "mùa hè"], "mint đậm"),
    ("Xanh baby",          0.86, 0.08, 240, 0.08,  15, 0.01, ["crush", "học", "ngọt"], "xanh em bé"),
    ("Tím mộng",           0.82, 0.10, 295, 0.08,  15, 0.01, ["đà lạt", "ngủ", "tâm linh"], "tím mơ"),
    ("Kẹo bông",           0.88, 0.08, 350, 0.07, -40, 0.02, ["ngọt", "vô tri", "sinh nhật"], "hồng sang tím"),
    ("Bubblegum",          0.80, 0.14, 355, 0.08, -15, 0.01, ["crush", "vô tri", "valentine"], "hồng kẹo cao su"),
    ("Hồng đất",           0.80, 0.06,  20, 0.08, -10, 0.01, ["vintage", "buồn nhẹ", "ootd"], "hồng xỉn"),
    ("Xám mây",            0.88, 0.015,250, 0.08,  10, 0.00, ["mệt", "không cảm xúc", "mưa"], "xám lạnh"),
    ("Tro hồng",           0.85, 0.02, 350, 0.08,  -5, 0.00, ["mệt", "buồn nhẹ"], "xám ấm"),
    ("Latte",              0.85, 0.04,  70, 0.08, -10, 0.01, ["cafe", "vintage", "ootd", "makeup"], "be cafe sữa"),
    ("Nắng sớm",           0.93, 0.10,  95, 0.06, -35, 0.02, ["sáng sớm", "nắng", "mới ngủ dậy"], "vàng sang đào"),
    ("Cát biển",           0.88, 0.07,  75, 0.06, -10, 0.00, ["biển", "du lịch", "ăn uống", "sáng sớm"], "cát ấm"),
    ("Bánh nướng",         0.84, 0.12,  75, 0.10, -15, 0.01, ["trung thu", "ăn uống", "tâm linh"], "vàng nướng"),
    ("Mai vàng",           0.88, 0.16,  95, 0.10, -20, 0.00, ["tết", "20/11", "nắng", "vô tri"], "vàng hoa mai"),
    ("Tuyết",              0.95, 0.02, 230, 0.06,  10, 0.01, ["noel", "lạnh", "tối giản"], "trắng xanh"),
    ("Bí ngô",             0.78, 0.15,  55, 0.08, -15, 0.00, ["halloween", "trung thu"], "cam bí"),
    ("Cam neon",           0.76, 0.18,  48, 0.07, -15, 0.00, ["deadline", "vô tri", "gym"], "cam báo động"),
    ("Lá thu",             0.82, 0.12,  65, 0.10, -25, 0.01, ["mùa thu", "hà nội", "chill"], "vàng sang cam"),
    ("Soda xanh",          0.84, 0.12, 200, 0.08,  20, 0.00, ["party", "mùa hè", "biển"], "aqua sủi"),
    ("Cyan neon",          0.82, 0.14, 220, 0.08,  20, 0.00, ["game", "party", "công nghệ"], "cyan điện"),
    ("Hoàng hôn Đà Nẵng",  0.74, 0.16,  55, 0.10, -40, 0.01, ["hoàng hôn", "biển", "du lịch"], "cam sang hồng"),
    ("Bình minh",          0.88, 0.08,  70, 0.07, -40, 0.01, ["sáng sớm", "chill"], "đào sang hồng"),
    ("Cực quang",          0.80, 0.12, 170, 0.08,  40, 0.00, ["đêm", "du lịch", "chill"], "mint sang xanh"),
    ("Trà đá",             0.78, 0.12,  70, 0.10, -15, 0.01, ["ăn uống", "nhậu", "vỉa hè"], "hổ phách"),
    ("Vịnh ngọc",          0.70, 0.11, 190, 0.10,  15, 0.00, ["du lịch", "biển"], "ngọc bích"),
    ("Lửa trại",           0.70, 0.19,  55, 0.10, -25, 0.00, ["lửa", "deadline", "party"], "cam lửa"),
    ("Kaki",               0.80, 0.05,  95, 0.08, -10, 0.00, ["ootd", "vintage"], "kaki"),
    ("Vàng kim",           0.80, 0.11,  90, 0.12, -15, 0.01, ["flex", "tết", "tốt nghiệp"], "gold"),
    ("Bạc",                0.86, 0.01, 260, 0.12,   0, 0.00, ["flex", "sang chảnh", "công nghệ"], "silver"),
    ("Nắng gắt",           0.80, 0.17,  70, 0.08, -25, 0.00, ["nắng", "mùa hè", "nóng", "deadline", "cảnh báo"], "nắng 40 độ"),
    ("Mưa phùn",           0.80, 0.02, 230, 0.08,  10, 0.00, ["mưa", "hà nội", "lạnh"], "xám mưa phùn"),
    ("Gió mùa",            0.86, 0.04, 220, 0.08,  15, 0.01, ["lạnh", "mùa đông"], "xanh lạnh"),
    ("Ốm vặt",             0.90, 0.05, 150, 0.06,  10, 0.00, ["ốm", "mệt"], "xanh nhợt"),
    ("San hô",             0.82, 0.11,  30, 0.08, -10, 0.01, ["biển", "mùa hè", "ootd"], "coral"),
    ("Mộng mị",            0.75, 0.05, 290, 0.08,  10, 0.00, ["overthinking", "buồn nhẹ", "ngủ"], "lavender xám"),
    ("Xi măng",            0.72, 0.01, 250, 0.08,   0, 0.00, ["vô tri", "mệt", "công sở"], "xám bê tông"),
    ("Lá non",             0.78, 0.17, 140, 0.08,  12, 0.00, ["thiên nhiên", "mùa xuân", "healthy"], "xanh lộc"),
    ("Bầu trời",           0.74, 0.12, 235, 0.08,  15, 0.00, ["du lịch", "máy bay", "nắng"], "xanh trời trưa"),
    ("Lightstick",         0.74, 0.12, 300, 0.08,  12, 0.00, ["kpop", "concert", "party"], "tím pastel đậm"),

    # ---------- ĐẬM / BÓNG (chữ Trắng) ----------
    ("Đỏ cờ",              0.56, 0.21,  29, 0.08,  -4, 0.00, ["bóng đá", "2/9", "tết", "cưới"], "đỏ thắm"),
    ("Đỏ ớt",              0.60, 0.20,  38, 0.12, -12, 0.00, ["deadline", "cáu", "lửa", "gym"], "cam đỏ cay"),
    ("Rượu vang",          0.40, 0.13,  15, 0.10, -10, 0.00, ["sang chảnh", "valentine", "noel"], "đỏ vang"),
    ("Hồng cánh sen",      0.60, 0.22, 355, 0.08, -15, 0.00, ["crush", "valentine", "party"], "hồng rực"),
    ("Hồng neon",          0.62, 0.25, 340, 0.08, -15, 0.00, ["party", "kpop", "vô tri"], "hồng điện"),
    ("Mận chín",           0.45, 0.13, 345, 0.10, -15, 0.00, ["tình yêu", "đêm", "sang chảnh"], "mận đậm"),
    ("Đất nung",           0.58, 0.13,  40, 0.10,  -8, 0.00, ["vintage", "du lịch", "ootd"], "terracotta"),
    ("Cafe sữa đá",        0.55, 0.07,  60, 0.12,  -8, 0.00, ["cafe", "sáng sớm"], "nâu sữa"),
    ("Cafe đen",           0.40, 0.05,  55, 0.12,  -5, 0.00, ["cafe", "đêm", "deadline"], "nâu đen"),
    ("Socola",             0.45, 0.08,  45, 0.10,  -8, 0.00, ["ăn uống", "valentine", "ngọt"], "socola"),
    ("Caramel cháy",       0.58, 0.10,  65, 0.12, -12, 0.00, ["trà sữa", "cafe"], "caramel"),
    ("Vàng mù tạt",        0.56, 0.11,  85, 0.10, -15, 0.00, ["vintage", "tâm linh", "ootd"], "mustard"),
    ("Xanh rêu",           0.50, 0.08, 130, 0.10,  10, 0.00, ["thiên nhiên", "chill", "vintage"], "rêu"),
    ("Rừng thông",         0.45, 0.08, 160, 0.10,  15, 0.00, ["đà lạt", "núi", "noel"], "thông xanh"),
    ("Rắn độc",            0.58, 0.17, 145, 0.10,  10, 0.00, ["meme", "toxic", "cà khịa"], "xanh rắn"),
    ("Tiền về",            0.52, 0.12, 155, 0.10,  10, 0.00, ["tiền", "lương", "flex"], "xanh đô la"),
    ("Ngọc lục bảo",       0.52, 0.11, 172, 0.10,  15, 0.00, ["sang chảnh", "flex"], "emerald"),
    ("Biển sâu",           0.52, 0.10, 200, 0.10,  15, 0.00, ["biển", "chill", "buồn nhẹ"], "teal sâu"),
    ("Đại dương",          0.52, 0.14, 240, 0.10,  15, 0.00, ["biển", "du lịch", "học"], "xanh biển"),
    ("Xanh điện",          0.55, 0.20, 262, 0.08,  12, 0.00, ["game", "công nghệ", "học"], "electric blue"),
    ("Navy",               0.35, 0.10, 260, 0.10,  10, 0.00, ["tốt nghiệp", "công sở", "đêm"], "xanh hải quân"),
    ("Đêm Sài Gòn",        0.38, 0.13, 280, 0.10,  15, 0.00, ["đêm", "sài gòn", "party"], "tím xanh đêm"),
    ("Nửa đêm",            0.30, 0.08, 285, 0.10,  10, 0.00, ["ngủ", "2AM", "overthinking"], "tím than"),
    ("Thạch anh tím",      0.50, 0.17, 300, 0.10,  12, 0.00, ["tâm linh", "tarot", "party"], "amethyst"),
    ("Galaxy",             0.45, 0.20, 290, 0.10,  15, 0.00, ["đêm", "game", "kpop"], "tím vũ trụ"),
    ("Phù thủy",           0.35, 0.13, 300, 0.10,  10, 0.00, ["halloween", "đêm"], "tím đen"),
    ("Tím Huế",            0.52, 0.12, 315, 0.10,  10, 0.00, ["vintage", "buồn nhẹ", "phụ nữ"], "tím mộng mơ"),
    ("Magenta",            0.55, 0.22, 330, 0.08, -10, 0.00, ["party", "kpop", "ootd"], "magenta"),
    ("Bão",                0.50, 0.025,250, 0.12,  10, 0.00, ["mưa", "buồn", "bão", "công sở", "họp"], "xám bão"),
    ("Chiều mưa",          0.58, 0.04, 235, 0.12,  15, 0.00, ["mưa", "buồn nhẹ", "chill"], "xám xanh"),
    ("Than chì",           0.35, 0.01, 260, 0.10,   0, 0.00, ["không cảm xúc", "ngầu", "mệt"], "graphite"),
    ("Buồn xanh",          0.52, 0.05, 255, 0.10,  15, 0.01, ["buồn", "thất tình", "đêm"], "blue mood"),
    ("Đen bóng",           0.28, 0.01, 280, 0.08,  20, 0.00, ["flex", "sang chảnh", "ngầu"], "obsidian"),
    ("Đỏ gạch",            0.52, 0.14,  35, 0.10,  -5, 0.00, ["vintage", "gym"], "gạch nung"),
    ("Cyberpunk",          0.52, 0.18, 280, 0.08, -40, 0.00, ["game", "đêm", "party"], "tím sang xanh"),
    ("Dưa hấu",            0.62, 0.20,  15, 0.08, -10, 0.00, ["mùa hè", "ăn uống", "vô tri"], "đỏ hồng dưa"),
    ("Sân cỏ",             0.58, 0.16, 140, 0.10,   5, 0.00, ["bóng đá", "gym", "thể thao"], "xanh sân cỏ"),
    ("Hồng nhung",         0.52, 0.15,   5, 0.10, -10, 0.00, ["phụ nữ", "gia đình", "tình yêu"], "hồng đậm"),
    ("Denim",              0.48, 0.08, 255, 0.08,   5, 0.00, ["ootd", "học"], "jean"),
    ("Cổ vịt",             0.45, 0.09, 215, 0.10,  15, 0.00, ["đêm", "chill", "sang chảnh"], "teal xanh cổ vịt"),
    ("Ô liu",              0.52, 0.09, 115, 0.08,  10, 0.00, ["ootd", "vintage", "thiên nhiên"], "olive"),
]


# ---------------- màu học ----------------
def oklch_to_oklab(L, C, H):
    h = math.radians(H)
    return L, C * math.cos(h), C * math.sin(h)


def oklab_to_linear_srgb(L, a, b):
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    return (
        +4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )


def linear_to_srgb(x):
    return 12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055


def in_gamut(rgb, eps=1e-4):
    return all(-eps <= c <= 1 + eps for c in rgb)


def oklch_to_hex(L, C, H):
    """Đổi OKLCH -> HEX, giảm C (giữ L, H) nếu ngoài gam sRGB. Trả (hex, C thực tế)."""
    lo, hi = 0.0, C
    if in_gamut(oklab_to_linear_srgb(*oklch_to_oklab(L, C, H))):
        lo = C
    else:
        for _ in range(30):
            mid = (lo + hi) / 2
            if in_gamut(oklab_to_linear_srgb(*oklch_to_oklab(L, mid, H))):
                lo = mid
            else:
                hi = mid
    rgb = oklab_to_linear_srgb(*oklch_to_oklab(L, lo, H))
    srgb = [min(1, max(0, linear_to_srgb(min(1, max(0, c))))) for c in rgb]
    return "#" + "".join(f"{round(c * 255):02X}" for c in srgb), lo


def rel_lum(hexcode):
    vals = [int(hexcode[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    lin = [v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in vals]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast(y1, y2):
    hi, lo = max(y1, y2), min(y1, y2)
    return (hi + 0.05) / (lo + 0.05)


def build(spec):
    name, L, C, H, dL, dH, dC, tags, vibe = spec
    H2 = (H + dH) % 360

    def make(shift):
        h1, c1 = oklch_to_hex(L + shift, C, H)
        h2, c2 = oklch_to_hex(L - dL + shift, C + dC, H2)
        y1, y2 = rel_lum(h1), rel_lum(h2)
        black = min(contrast(y1, 0), contrast(y2, 0))
        white = min(contrast(y1, 1), contrast(y2, 1))
        return h1, h2, c1, c2, black, white

    h1, h2, c1, c2, black, white = make(0)
    text = "Đen" if black >= white else "Trắng"
    shift, nudged = 0.0, False
    step = 0.01 if text == "Đen" else -0.01
    while (black if text == "Đen" else white) < MIN_CONTRAST:
        shift += step
        nudged = True
        if abs(shift) > 0.08 + 1e-9:
            break
        h1, h2, c1, c2, black, white = make(shift)
    best = black if text == "Đen" else white
    return {
        "name": name,
        "bg1": h1,
        "bg2": h2,
        "textColor": text,
        "tags": tags,
        "vibe": vibe,
        "contrast": round(best, 2),
        "_nudged": round(shift, 2) if nudged else 0,
        "_ok": best >= MIN_CONTRAST,
        "_hue_gap": abs(((dH + 180) % 360) - 180),
        "_lab": [oklch_to_oklab(L + shift, c1, H), oklch_to_oklab(L - dL + shift, c2, H2)],
    }


def lab_dist(a, b):
    return math.dist(a, b)


def main():
    items = [build(s) for s in SPECS]
    for i, it in enumerate(items, 1):
        it["id"] = f"M{i:03d}"

    problems = []
    for it in items:
        if not it["_ok"]:
            problems.append(f"{it['id']} {it['name']}: tương phản chỉ {it['contrast']}")
        if it["_hue_gap"] > MAX_HUE_GAP:
            problems.append(f"{it['id']} {it['name']}: lệch hue {it['_hue_gap']}°")
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            d = max(lab_dist(a["_lab"][0], b["_lab"][0]), lab_dist(a["_lab"][1], b["_lab"][1]))
            if d < 0.035:
                problems.append(f"Gần trùng: {a['id']} {a['name']} ~ {b['id']} {b['name']} (Δ={d:.3f})")

    nudged = [f"{it['id']} {it['name']} ({it['_nudged']:+.2f})" for it in items if it["_nudged"]]

    public = [{k: v for k, v in it.items() if not k.startswith("_")} for it in items]
    for p in public:
        p.pop("contrast", None)
    ordered = [{"id": p["id"], **{k: v for k, v in p.items() if k != "id"}} for p in public]

    with open(os.path.join(REF, "bang-mau-locket.json"), "w", encoding="utf-8") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=2)

    write_md(items)
    write_html(items)

    print(f"Tổng: {len(items)} cặp màu "
          f"({sum(i['textColor'] == 'Đen' for i in items)} chữ Đen, "
          f"{sum(i['textColor'] == 'Trắng' for i in items)} chữ Trắng)")
    print("Đã chỉnh độ sáng:", ", ".join(nudged) if nudged else "không")
    print("Vấn đề:" if problems else "Không có vấn đề.")
    for p in problems:
        print("  -", p)
    return 1 if any("tương phản" in p or "lệch hue" in p for p in problems) else 0


def write_md(items):
    tags = {}
    for it in items:
        for t in it["tags"]:
            tags.setdefault(t, []).append(it)
    lines = [
        "# BẢNG MÀU CAPTION LOCKET",
        "",
        f"{len(items)} cặp gradient đã kiểm tra: chữ đọc rõ (tương phản ≥ {MIN_CONTRAST}:1 trên cả 2 nền), "
        f"2 màu lệch hue ≤ {MAX_HUE_GAP}° nên không bị xám đục ở giữa.",
        "",
        "**Cách dùng:** tìm chủ đề ở phần 2 → lấy mã ID → tra phần 1 để lấy Nền 1, Nền 2, Màu chữ. "
        "Luôn chép NGUYÊN cặp (Nền 1 + Nền 2 + Màu chữ), không ghép màu của 2 cặp khác nhau.",
        "",
        "## 1. Danh sách cặp màu",
        "",
        "| ID | Tên | Nền 1 | Nền 2 | Màu chữ | Vibe | Chủ đề |",
        "|---|---|---|---|---|---|---|",
    ]
    for it in items:
        lines.append(f"| {it['id']} | {it['name']} | {it['bg1']} | {it['bg2']} | {it['textColor']} | "
                     f"{it['vibe']} | {', '.join(it['tags'])} |")
    lines += ["", "## 2. Tra theo chủ đề", ""]
    for t in sorted(tags):
        refs = ", ".join(f"{i['id']} {i['name']}" for i in tags[t])
        lines.append(f"- **{t}:** {refs}")
    lines.append("")
    with open(os.path.join(REF, "bang-mau-locket.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def write_html(items):
    def esc(s):
        return s.replace("&", "&amp;").replace("<", "&lt;")

    pills = []
    for it in items:
        fg = "#111111" if it["textColor"] == "Đen" else "#FFFFFF"
        pills.append(
            f'<div class="cell"><div class="pill" style="background:linear-gradient(180deg,{it["bg1"]},{it["bg2"]});'
            f'color:{fg}">{esc(it["name"])}</div>'
            f'<div class="meta">{it["id"]} · {it["bg1"]} → {it["bg2"]} · {it["textColor"]}</div>'
            f'<div class="tags">{esc(", ".join(it["tags"]))}</div></div>'
        )
    html = f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bảng màu Locket</title>
<style>
:root {{ --bg:#141414; --sheet:#1f1f21; --muted:#8e8e93; --text:#f2f2f7; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--text); font-family:-apple-system,"SF Pro Rounded","Segoe UI",system-ui,sans-serif; }}
main {{ max-width:1100px; margin:0 auto; padding:24px 16px 48px; }}
h1 {{ font-size:20px; margin:0 0 4px; }}
p {{ color:var(--muted); margin:0 0 20px; font-size:14px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:18px 14px; background:var(--sheet); padding:20px; border-radius:24px; }}
.pill {{ display:inline-block; padding:11px 20px; border-radius:999px; font-weight:700; font-size:17px; line-height:1.2;
  box-shadow: inset 0 1px 0 rgba(255,255,255,.25), 0 2px 6px rgba(0,0,0,.35); }}
.meta {{ font:12px ui-monospace,Consolas,monospace; color:var(--muted); margin-top:6px; }}
.tags {{ font-size:12px; color:#636366; margin-top:2px; }}
</style></head><body><main>
<h1>Bảng màu caption Locket ({len(items)} cặp)</h1>
<p>Nền tối giống bảng Chú thích trong app. Gradient chạy từ trên xuống.</p>
<div class="grid">{''.join(pills)}</div>
</main></body></html>"""
    with open(os.path.join(ASSETS, "xem-truoc-bang-mau.html"), "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
