# My Claude Skills

Custom skills สำหรับ Claude Code ที่สร้างขึ้นเอง — เก็บเป็นไฟล์ `.skill` (zip) พร้อมโฟลเดอร์ต้นฉบับ เพื่อติดตั้งข้ามเครื่องได้ — พร้อม global rules ที่โหลดอัตโนมัติทุก session

**ตอนนี้มี 2 skills + 1 global rule** · ปรับปรุงล่าสุด: 2026-06-18

## รายการ skills

| # | Skill | ใช้ตอนไหน | Trigger หลัก | ไฟล์ |
|---|-------|-----------|--------------|------|
| 1 | **github-init-push** | สร้าง repo ใหม่จากโปรเจกต์ในเครื่องแล้ว push ขึ้น GitHub ในขั้นตอนเดียว | `ส่งขึ้น github`, `สร้าง repo ใหม่` | [`.skill`](./github-init-push.skill) |
| 2 | **sync-verify-deploy** | ตรวจสอบ/sync GAS monorepo ข้าม local ↔ GitHub/GitLab ↔ Apps Script แล้ว deploy | `sync ให้ชัวร์`, `เช็คว่า deploy ตรงไหน` | [`.skill`](./sync-verify-deploy.skill) |

## วิธีติดตั้ง (skills)

ดาวน์โหลดไฟล์ `.skill` แล้วติดตั้งผ่าน Claude Code:
```bash
claude skill install <ชื่อไฟล์>.skill
```

หรือ copy โฟลเดอร์ skill ไปไว้ที่ `~/.claude/skills/` (เช่น `sync-verify-deploy/`)

## Global rules (always-on)

กฎที่โหลดอัตโนมัติทุก session ผ่าน `~/.claude/CLAUDE.md` — **ไม่ใช่ skill** จึงติดตั้งด้วยมือ (ไม่ใช้ `claude skill install`)

| # | Rule | ใช้ตอนไหน | ไฟล์ |
|---|------|-----------|------|
| 1 | **visual-mockup** | ทุกครั้งที่วางแผน/แก้ไข จะเสนอทำ mockup HTML รันบน local URL เพิ่มจาก markdown (สร้างเมื่อตอบตกลง) | [`rules/visual-mockup.md`](./rules/visual-mockup.md) |

**ติดตั้งแบบเร็ว (คำสั่งเดียว — แนะนำ):**
```powershell
git clone https://github.com/IntraWY/my-claude-skills.git
powershell -ExecutionPolicy Bypass -File my-claude-skills/install-rule.ps1
```
สคริปต์จะ copy ไฟล์ rule และเติมบรรทัด import ให้เอง (รันซ้ำได้ ไม่พัง) — เสร็จแล้วเปิด session ใหม่

**หรือติดตั้งด้วยมือ (PowerShell / Windows):**
```powershell
# 1. ดึง repo (clone ครั้งแรก หรือ git pull ถ้ามีแล้ว)
git clone https://github.com/IntraWY/my-claude-skills.git
# 2. copy ไฟล์ rule เข้า config กลาง
New-Item -ItemType Directory -Force ~/.claude/rules
Copy-Item my-claude-skills/rules/visual-mockup.md ~/.claude/rules/visual-mockup.md
# 3. เพิ่มบรรทัด import ใน ~/.claude/CLAUDE.md (สร้างไฟล์ถ้ายังไม่มี):
#       @rules/visual-mockup.md
# 4. รีสตาร์ท Claude Code (เปิด session ใหม่) ให้ import โหลด
```

> ตอนสร้าง mockup จริง ใช้ superpowers visual companion ถ้าติดตั้งไว้ ไม่งั้น fallback เป็น `python -m http.server` (ต้องมี Python ใน PATH)

## โครงสร้าง repo

```
my-claude-skills/
├── github-init-push/            # โฟลเดอร์ต้นฉบับ
│   └── SKILL.md
├── github-init-push.skill       # แพ็กเกจ zip สำหรับ install
├── sync-verify-deploy/
│   ├── SKILL.md
│   └── verify_live.py           # helper script
├── sync-verify-deploy.skill
├── rules/
│   └── visual-mockup.md         # global rule (always-on)
└── install-rule.ps1             # ตัวติดตั้ง rule คำสั่งเดียว
```

---

## รายละเอียด

### 1. github-init-push

สร้าง GitHub repository ใหม่จากโปรเจกต์ในเครื่อง และ push โค้ดขึ้น GitHub ในขั้นตอนเดียว

- **Trigger**: พูดว่า `ส่งขึ้น github`, `สร้าง repo ใหม่`, `push to github` ฯลฯ
- **เหมาะกับ**: โปรเจกต์ในเครื่องที่ยังไม่มี git remote / ยังไม่ได้ขึ้น GitHub
- **ทำอะไร**:
  - ตรวจสอบ GitHub auth
  - สำรวจโปรเจกต์และเลือกชื่อ repo ที่เหมาะสม
  - Init git และเลือกไฟล์ที่ควร commit (ข้าม binary / secret)
  - สร้าง GitHub repo และ push
- **ไฟล์ในแพ็กเกจ**: `github-init-push/SKILL.md`
- **ดาวน์โหลด**: [`github-init-push.skill`](./github-init-push.skill)

### 2. sync-verify-deploy

ตรวจสอบ/sync GAS monorepo ข้าม local, GitHub/GitLab และ Apps Script — พิสูจน์ว่าโค้ด local ตรงกับที่ deploy จริงไหม (byte-diff), แก้ git ที่ diverged ข้าม 2 remote, และ deploy แบบ URL คงที่

- **Trigger**: พูดว่า `ตรวจสอบไฟล์ local เทียบ appscript/github`, `sync ให้ชัวร์`, `เช็คว่า deploy ตรงไหน`, `local ตรงกับที่ deploy หรือยัง`
- **เหมาะกับ**: monorepo Google Apps Script (clasp 3.x) บน Windows ที่มีหลาย sub-project + 2 git remote
- **ทำอะไร**:
  - พิสูจน์ว่า local == LIVE Apps Script ด้วย `clasp pull` ลง temp แล้ว byte-diff (`clasp status` ทำไม่ได้) — รองรับโฟลเดอร์ชื่อไทย (Python `cwd=` + `clasp.cmd`)
  - เทียบ git ทั้ง 2 remote (GitLab `origin` + GitHub `github`) แล้ว pull → commit → push ทั้งคู่
  - เจอ merge conflict → หยุดถาม user ไม่ auto-resolve
  - deploy ด้วย `clasp deploy -i <deploymentId>` (URL ไม่เปลี่ยน) + verify HTTP 200
- **ไฟล์ในแพ็กเกจ**: `sync-verify-deploy/SKILL.md`, `sync-verify-deploy/verify_live.py`
- **helper**: `verify_live.py` — รันได้ตรง: `python verify_live.py <dir1> <dir2> ...` แสดงผล `SAME`/`DIFF` พร้อมขนาดไฟล์
- **ดาวน์โหลด**: [`sync-verify-deploy.skill`](./sync-verify-deploy.skill)

### 3. visual-mockup (global rule)

เวลาวางแผนหรือเสนอการแก้ไข จะยังคงใช้ markdown เป็นหลัก แล้วเสนอเพิ่ม 1 บรรทัดว่าอยากได้ mockup HTML รันบน local URL ไหม — สร้างจริงเฉพาะเมื่อตอบตกลง (ประหยัด token)

- **ประเภท**: global rule (always-on) — ไม่ใช่ skill
- **โหลดยังไง**: import ใน `~/.claude/CLAUDE.md` ด้วยบรรทัด `@rules/visual-mockup.md`
- **ติดตั้ง**: รัน `install-rule.ps1` (คำสั่งเดียว) หรือดูขั้นตอนที่หัวข้อ "Global rules (always-on)"
- **ตอนสร้าง mockup**: ใช้ superpowers visual companion (ถ้ามี) หรือ fallback `python -m http.server`
- **ไฟล์**: [`rules/visual-mockup.md`](./rules/visual-mockup.md)
