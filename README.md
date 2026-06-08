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
