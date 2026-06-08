---
name: github-init-push
description: >
  สร้าง GitHub repository ใหม่จากโปรเจกต์ในเครื่อง และ push โค้ดขึ้น GitHub
  ครอบคลุมทั้ง init git, เลือกไฟล์ที่ควร commit, ตั้งชื่อ repo ให้เข้าใจง่าย,
  และ push ขึ้น GitHub ในขั้นตอนเดียว

  ใช้สกิลนี้เมื่อผู้ใช้พูดว่า: "ส่งขึ้น github", "สร้าง repo ใหม่", "push to github",
  "create new repo", "อัปโหลดขึ้น github", "เอาขึ้น github", "init git แล้ว push",
  หรือมีโปรเจกต์ local ที่ยังไม่มี git/remote และต้องการเผยแพร่
---

# GitHub Init & Push

เปลี่ยนโปรเจกต์ local ที่ยังไม่มี git ให้กลายเป็น GitHub repository ที่พร้อมใช้งาน

## ขั้นตอนทั้งหมด

### 1. ตรวจสอบ GitHub auth

```bash
gh auth status
```

ถ้ายัง login ไม่อยู่ แนะนำให้รัน `gh auth login` ก่อน

### 2. สำรวจโปรเจกต์

อ่านไฟล์สำคัญเพื่อเข้าใจว่าโปรเจกต์นี้คืออะไร:
- `README.md` หรือ `README.*`
- `package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod` (ถ้ามี)
- ไฟล์หลักของโปรเจกต์

สิ่งที่ต้องรู้ก่อนดำเนินการต่อ:
- โปรเจกต์นี้ทำอะไร (สรุปสั้นๆ)
- ภาษา/เทคโนโลยีที่ใช้
- ชื่อ repo ที่เหมาะสม

### 3. เลือกชื่อ repo ที่ดี

ชื่อ repo ที่ดีควร:
- เป็น **kebab-case** (ตัวพิมพ์เล็กทั้งหมด คั่นด้วย `-`)
- **สั้นและสื่อความหมาย** (2-4 คำ)
- บอกว่า "ทำอะไร" หรือ "คืออะไร" ได้ทันที
- หลีกเลี่ยงคำทั่วไปที่ไม่บอกอะไร เช่น `my-project`, `test`, `code`

ตัวอย่าง:
- `claude-apple-watch-notify` ✅
- `nextjs-auth-boilerplate` ✅  
- `my-project-v2` ❌

ถ้าไม่แน่ใจ ให้เสนอชื่อ 2-3 ตัวเลือกให้ผู้ใช้เลือก

### 4. ตรวจสอบสถานะ git

```bash
git status 2>&1 || echo "NOT_GIT_REPO"
```

- **ยังไม่มี git repo** → รัน `git init`
- **มี git repo อยู่แล้ว** → ตรวจสอบ branch และ remote ที่มีอยู่

### 5. เลือกไฟล์ที่ควร commit

**ควร include:**
- ซอร์สโค้ดทั้งหมด
- `README.md`, `LICENSE`, config files
- Script และ skill files

**ไม่ควร include (exclude):**
- ไฟล์ binary ที่ไม่ใช่ asset จริงๆ (zip, exe, dll, obj)
- Build artifacts (`dist/`, `build/`, `target/`, `__pycache__/`)
- Dependencies (`node_modules/`, `.venv/`, `vendor/`)
- ไฟล์ temp / session / cache
- `.env` หรือไฟล์ที่มี secret

สร้าง `.gitignore` ถ้าจำเป็น ก่อน stage ไฟล์

```bash
# stage เฉพาะไฟล์ที่ต้องการ (ไม่ใช้ git add -A แบบมั่วๆ)
git add <ไฟล์/โฟลเดอร์ที่ต้องการ>
```

### 6. สร้าง commit

Commit message ควรสะท้อนว่าโปรเจกต์คืออะไร:

```bash
git commit -m "feat: <สรุปสั้นๆ ว่าโปรเจกต์นี้คืออะไร>"
```

ตัวอย่าง:
- `feat: Claude Code Apple Watch notifications via ntfy.sh`
- `feat: Next.js authentication boilerplate with JWT`

### 7. สร้าง GitHub repo และ push

```bash
gh repo create <repo-name> \
  --public \
  --description "<คำอธิบายสั้นๆ ภาษาที่ผู้ใช้ใช้>" \
  --source . \
  --remote origin \
  --push
```

ใช้ `--private` แทน `--public` ถ้าผู้ใช้บอกว่าต้องการ private repo

### 8. แจ้งผลลัพธ์

บอกผู้ใช้:
- URL ของ repo ที่สร้าง
- ไฟล์ที่ถูก commit (และไฟล์ที่ถูก exclude พร้อมเหตุผล)

## ข้อควรระวัง

- **อย่า commit `.env`** หรือไฟล์ที่มี API key / secret โดยเด็ดขาด
- **อย่าใช้ `git add -A` หรือ `git add .`** โดยไม่ตรวจสอบก่อน — อาจ commit ไฟล์ที่ไม่ต้องการ
- ถ้า repo ชื่อซ้ำกับที่มีอยู่แล้วใน GitHub → แนะนำชื่อใหม่หรือให้ผู้ใช้เลือก
