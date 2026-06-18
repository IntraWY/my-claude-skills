# Rule: Offer a runnable HTML mockup when planning or editing

Whenever I present a plan or propose a change (plan mode, design proposals, or describing
an edit before/while making it):

1. **Markdown is always the primary deliverable.** Write the plan/explanation in markdown
   exactly as normal — never replace it with a mockup.
2. **Then add ONE line offering a visual mockup**, e.g.:
   `> 💡 อยากให้ทำ mockup HTML รันบน local URL เพื่อดูภาพไหม? (ตอบ "ทำ mockup" ได้เลย)`
   - Just the offer. Do **not** build the mockup until the user agrees — keeps token cost ~0.
   - For trivial / non-visual edits (rename, pure logic) the offer may note it adds little,
     but still offer per the user's preference.
3. **When the user accepts**, build and serve it:
   - Resolve the visual companion server dynamically (do NOT hardcode a version): glob
     `~/.claude/plugins/cache/**/superpowers/*/skills/brainstorming/scripts/start-server.sh`
     and pick the newest version dir.
   - Start it with `--project-dir <cwd>` and `run_in_background: true` (Windows). Read
     `$STATE_DIR/server-info` on the next turn for the URL/port. Write the mockup as an
     HTML fragment (or full doc) into `screen_dir`; follow `visual-companion.md` in that
     skill for the loop and CSS classes.
   - **Fallback** if the server can't be found/started: write `mockup.html` to a temp /
     working dir and run `python -m http.server <port>` in the background, then give the
     URL. (Python is available; `PYTHONIOENCODING=utf-8` is already set.)
   - Tell the user the exact `http://localhost:<port>` URL and a one-line summary of
     what's on screen.
4. **Cleanup**: when the mockup is no longer needed, stop the server
   (`stop-server.sh $SESSION_DIR`, or kill the python process) and mention it.
