# LOCKET CAPTION STUDIO

Skill giúp AI (ChatGPT, Gemini, Claude) viết thư viện caption Locket giọng Gen Z Việt: emoji iPhone + chữ + gradient 2 màu + màu chữ, chia 109 mục, chọn theo STT rồi xuất Excel / Google Sheets.

> File này là **hướng dẫn cho bạn**, không cần tải lên AI.

> 🤖 **Nếu bạn là AI được gửi link repo này:** đọc [`SKILL.md`](SKILL.md) trước, rồi đọc các file trong [`references/`](references/): `giong-van-genz.md`, `so-tay-giong.md`, `trend.md`, `danh-muc.md`, `mau-sac.md`, `bang-mau-locket.md`. Làm theo đúng `SKILL.md` suốt cuộc trò chuyện. Lượt đầu chỉ chào 1 dòng và in menu khởi động (mục 6.1).
> Bản thô của từng file để đọc trực tiếp: `https://raw.githubusercontent.com/iamhieubautroi/skill-caption-locket/main/<đường dẫn file>` (vd `.../main/SKILL.md`, `.../main/references/trend.md`).

## Trong thư mục có gì

| File | Dùng để | Tải lên AI? |
|---|---|---|
| `SKILL.md` | Luật, quy trình, menu, định dạng | ✅ |
| `CHI-DAN-NGAN.txt` | Đoạn chỉ dẫn ngắn để dán vào ô Instructions | dán, không tải |
| `references/giong-van-genz.md` | Cách Gen Z nói chuyện, slang, danh sách cấm | ✅ |
| `references/trend.md` | Kho trend (**bạn cập nhật**) | ✅ |
| `references/so-tay-giong.md` | Câu bạn khen/chê (**bạn cập nhật**) | ✅ |
| `references/danh-muc.md` | 16 nhóm, 109 mục | ✅ |
| `references/mau-sac.md` | Luật màu + 3 chế độ màu | ✅ |
| `references/bang-mau-locket.md` | 98 cặp gradient | ✅ |
| `references/bang-mau-locket.json` | Bảng màu dạng dữ liệu (cho AI chạy code khi xuất Excel) | tùy chọn |
| `assets/xem-truoc-bang-mau.html` | Mở bằng trình duyệt để xem 98 viên màu | ❌ |
| `scripts/tao_bang_mau.py` | Sinh lại bảng màu khi bạn thêm/sửa màu | ❌ |

---

## Cài đặt

### ChatGPT (khuyên dùng Project)
1. Bấm **Projects → New project**, đặt tên "Locket Caption".
2. Vào phần cài đặt **Instructions** của project, dán nội dung `CHI-DAN-NGAN.txt`.
3. Phần **Files**: tải lên `SKILL.md` + 6 file trong `references/` (`.json` tùy chọn).
4. Mở chat mới trong project, gõ `bắt đầu`.

*Cách khác:* **Custom GPT** (Explore GPTs → Create → Configure). Dán `CHI-DAN-NGAN.txt` vào Instructions, tải các file vào Knowledge, bật **Web Search** (để tra trend) và **Code Interpreter & Data Analysis** (để xuất Excel).

### Gemini (Gem)
1. Vào **Gems → New Gem**, đặt tên "Locket Caption".
2. Ô **Instructions**: dán nội dung `CHI-DAN-NGAN.txt`.
3. Phần **Knowledge**: thêm `SKILL.md` + các file `references/`. Nếu Gemini không nhận đuôi `.md`, đổi đuôi thành `.txt` (nội dung giữ nguyên).
4. Gemini thường không tạo file Excel trong Gem. Khi xuất, nó sẽ đưa **bảng + khối CSV**: bấm nút **Xuất sang Google Sheets** dưới bảng, hoặc copy khối CSV dán vào Sheets.

### Claude
- **Claude.ai:** nén cả thư mục `locket-caption-skill` thành `.zip`, rồi vào **Settings → Capabilities → Skills** để tải lên.
- **Claude Code:** chép thư mục vào `~/.claude/skills/locket-caption-studio/`.
- Claude đọc `SKILL.md` trực tiếp, không cần `CHI-DAN-NGAN.txt`.

---

## Cách dùng (không cần nhớ lệnh)

- Gõ **số** để chọn caption: `3` · `1,4,7` · `5-12` · `hết` · `hết trừ 4,9` · `15.3` (câu 3 của mục 15).
- Gõ **chữ cái** để chọn hành động trong menu cuối mỗi câu trả lời.
- **Nói tự nhiên** cũng hiểu: "mặn lên", "thêm đi", "qua mục tết", "câu 5 hay", "câu 7 nghe AI quá", "xuất excel".
- Gõ `?` để xem hướng dẫn. Thấy AI làm ẩu thì gõ `luật` để nó nạp lại luật.

---

## Dạy trend mới & giọng văn

AI không tự nhớ giữa các cuộc trò chuyện. **Bộ nhớ thật là 2 file bạn cập nhật:**

1. Khi AI đề xuất trend (menu Trend) hoặc bạn khen/chê một câu, nó in sẵn dòng **`📌 Dán vào …`**.
2. Copy dòng đó, dán vào `references/trend.md` hoặc `references/so-tay-giong.md` (chỗ có ghi chú `<!-- Dán … -->`).
3. **Tải lại file đó lên** Project / Gem (xóa bản cũ, thêm bản mới).

Mẹo:
- Thấy trend nào trên TikTok thì dán thẳng vào chat: "giờ đang trend câu …". AI sẽ phân tích và soạn dòng cho bạn.
- Mỗi 1–2 tháng chọn menu **Trend → Đánh dấu trend hết hạn** để dọn kho.
- Trend cũ thì đổi trạng thái thành 🧊, đừng xóa, để AI biết mà tránh.

---

## Thêm hoặc sửa màu

1. Mở `scripts/tao_bang_mau.py`, thêm một dòng vào danh sách `SPECS` (có ghi chú cách khai báo ở đầu file).
2. Chạy: `python scripts/tao_bang_mau.py`. Script tự kiểm độ tương phản, cảnh báo cặp trùng, rồi ghi đè `references/bang-mau-locket.md` / `.json` và trang xem trước.
3. Tải lại `bang-mau-locket.md` lên AI.

Lưu ý: thêm màu vào giữa danh sách sẽ đổi mã `Mxxx` của các màu phía sau. Nên thêm vào **cuối danh sách** để giữ mã cũ.
