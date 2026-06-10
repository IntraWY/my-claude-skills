# My Claude Skills

Custom skills สำหรับ Claude Code ที่สร้างขึ้นเอง

## วิธีติดตั้ง

ดาวน์โหลดไฟล์ `.skill` แล้วติดตั้งผ่าน Claude Code:
```bash
claude skill install <ชื่อไฟล์>.skill
```

หรือ copy โฟลเดอร์ skill ไปไว้ที่ `~/.claude/skills/`

---

## Skills

### github-init-push

สร้าง GitHub repository ใหม่จากโปรเจกต์ในเครื่อง และ push โค้ดขึ้น GitHub ในขั้นตอนเดียว

**Trigger**: พูดว่า `ส่งขึ้น github`, `สร้าง repo ใหม่`, `push to github` ฯลฯ

**ทำอะไร**:
- ตรวจสอบ GitHub auth
- สำรวจโปรเจกต์และเลือกชื่อ repo ที่เหมาะสม
- Init git และเลือกไฟล์ที่ควร commit (ข้าม binary / secret)
- สร้าง GitHub repo และ push

**ไฟล์**: [`github-init-push.skill`](./github-init-push.skill)

### sync-verify-deploy

ตรวจสอบ/sync GAS monorepo ข้าม local, GitHub/GitLab และ Apps Script — พิสูจน์ว่าโค้ด local ตรงกับที่ deploy จริงไหม (byte-diff), แก้ git ที่ diverged ข้าม 2 remote, และ deploy แบบ URL คงที่

**Trigger**: พูดว่า `ตรวจสอบไฟล์ local เทียบ appscript/github`, `sync ให้ชัวร์`, `เช็คว่า deploy ตรงไหม`, `local ตรงกับที่ deploy หรือยัง`

**ทำอะไร**:
- พิสูจน์ว่า local == LIVE Apps Script ด้วย `clasp pull` ลง temp แล้ว byte-diff (`clasp status` ทำไม่ได้) — รองรับโฟลเดอร์ชื่อไทย (Python `cwd=` + `clasp.cmd`)
- เทียบ git ทั้ง 2 remote (GitLab `origin` + GitHub `github`) แล้ว pull → commit → push ทั้งคู่
- เจอ merge conflict → หยุดถาม user ไม่ auto-resolve
- deploy ด้วย `clasp deploy -i <deploymentId>` (URL ไม่เปลี่ยน) + verify HTTP 200

**ไฟล์**: [`sync-verify-deploy.skill`](./sync-verify-deploy.skill)
