# LUẬT MÀU GRADIENT

## 1. Ba chế độ màu

| Chế độ | Cách làm |
|---|---|
| **bảng** *(mặc định)* | Chỉ lấy màu từ `bang-mau-locket.md`. Tra theo chủ đề (phần 2 của file), chép **nguyên cặp** Nền 1 + Nền 2 + Màu chữ, ghi Mã màu `Mxxx`. **Không** ghép màu của 2 cặp khác nhau, **không** sửa mã HEX. |
| **tự do** | Tự thiết kế màu mới, tuân thủ tuyệt đối mục 2 và 3 bên dưới. Mã màu ghi `mới`. |
| **trộn** | Ưu tiên lấy từ bảng; chỉ tự thiết kế khi không có cặp nào hợp (tối đa ~30% trong 1 mục). Cặp tự thiết kế ghi `mới`. |

Không có file bảng màu → tự chuyển sang **tự do** và báo 1 dòng.

## 2. Luật cơ bản

- Mỗi caption có **Nền 1 → Nền 2** (HEX). Nền 1 ở đầu/trên và sáng hơn; Nền 2 ở cuối/dưới và đậm hơn, tạo cảm giác viên thuốc 3D như Locket.
- **Màu theo vật thể / cảm xúc chính của câu**, không theo mục:

| Chủ thể / cảm xúc | Hướng màu | Mã gợi ý trong bảng |
|---|---|---|
| Cà phê, trà sữa | nâu, caramel | M014, M028, M065, M066, M068 |
| Tiền, ganh tị, rắn | xanh lá | M072, M073 |
| Deadline, cáu, lửa | đỏ, cam | M035, M044, M059 |
| Tình yêu, ngọt | hồng, đào | M001, M011, M024, M061 |
| Buồn, mệt | xanh xám, xám tím | M026, M053, M086, M089 |
| Đêm, ngủ | navy, tím than | M078, M079, M080 |
| Biển, mát | cyan, teal | M007, M043, M075, M076 |
| Nắng, vui | vàng, cam | M016, M032, M048 |
| Mưa | xám xanh | M049, M086, M087 |
| Party, neon | tím, hồng, cyan, chanh neon | M017, M038, M062, M085 |
| Vô tri, meme | màu chói có chủ đích | M017, M035, M032 |

- **Màu chữ chỉ có Đen hoặc Trắng:**
  - Nền sáng, pastel → **Đen**. Kiểu này nhìn "sang" và hợp vibe dễ thương, nên dùng nhiều.
  - Nền đậm, bão hòa cao → **Trắng**.
  - Chữ phải đọc rõ trên **cả hai** nền (tương phản ≥ 4.5:1 với cả Nền 1 lẫn Nền 2).
  - Trong 1 mục nên có cả hai kiểu chữ, mỗi loại khoảng 40–60%.
- **Cấm HEX lười:** #FF0000, #00FF00, #0000FF, #FFFFFF, #000000, #FF69B4.
- **Đa dạng:** trong 1 mục, không quá 3 caption có cặp màu gần giống nhau.

## 3. Luật phối màu nâng cao (cho chế độ tự do / trộn)

Tư duy bằng **OKLCH** (L = độ sáng 0–1, C = độ rực, H = góc màu), rồi mới đổi ra HEX.

1. **Tránh "vùng chết xám":** app vẽ gradient kiểu sRGB, nên 2 màu lệch hue xa sẽ đục, xám ở giữa (xanh → vàng ra xám, đỏ → xanh lá ra nâu). Giữ **2 màu lệch hue ≤ 40°**.
2. **Xoay hue khi tối đi:** Nền 2 không chỉ là Nền 1 tối hơn mà **xoay thêm 10–25°**, như cách họa sĩ tô bóng: vàng → cam, hồng → hồng cánh sen, xanh lá → teal, xanh dương → tím than, cam → đỏ gạch. Đây là bí quyết để gradient có chiều sâu thay vì phẳng lì.
3. **Độ sáng lệch vừa phải:** Nền 1 sáng hơn Nền 2 khoảng **6–15 điểm L** (0.06–0.15). Ít hơn thì phẳng như màu trơn; nhiều hơn thì gãy.
4. **Độ rực đồng đều:** 2 màu có C gần nhau. Một màu rực đi với một màu xỉn → nhìn bẩn.
5. **Hai chế độ sáng/đậm, chọn một cho mỗi caption:**
   - **Sáng** (chữ Đen): cả 2 nền L ≥ 0.66. Pastel kẹo (L 0.82–0.95, C 0.04–0.12: hồng đào, vàng kem, mint, oải hương) hoặc tươi rực (L 0.70–0.85, C 0.12–0.18: vàng chanh, cam neon, cyan).
   - **Đậm** (chữ Trắng): cả 2 nền L ≤ 0.58, C 0.05–0.22. Ví dụ đỏ ớt, xanh rêu, tím than, nâu cafe.
   - Cấm gradient có một nền cần chữ Đen, nền kia cần chữ Trắng.
6. **Không dùng màu bão hòa tối đa:** nhìn rẻ. Rực nhưng phải "có chủ".
7. **Đặt tên cho cặp màu trong đầu** trước khi chọn ("matcha latte", "hoàng hôn Đà Nẵng", "kẹo dâu", "đêm Sài Gòn"). Không đặt được tên gợi cảm giác → cặp màu vô hồn, chọn lại.
