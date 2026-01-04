# Local Development Setup

Quick reference for running the wedding site locally with real-time changes.

---

## ⚠️ IMPORTANT: Browser Caching (Read This First!)

**CSS/HTML changes not showing up?**

### YOU MUST DO A HARD REFRESH!

- **Mac**: `Cmd + Shift + R`
- **Windows**: `Ctrl + F5`

**Regular refresh (Cmd+R) will use CACHED CSS and you won't see your changes!**

This is the #1 reason changes "don't work" - it's just your browser showing you old cached files.

**When to Hard Refresh:**
- ✅ After ANY CSS/TailwindCSS change
- ✅ After ANY HTML template change
- ✅ When text sizing doesn't update (text-9xl → text-8xl)
- ✅ When colors don't change
- ✅ When layout doesn't shift
- ✅ **Basically: ALWAYS hard refresh when testing visual changes!**

**When Regular Refresh is OK:**
- Python code changes (views, models) - Django auto-reloads the server
- Content changes that don't affect styling

---

## Starting Local Development (Every Time)

You need **TWO terminal windows** running simultaneously:

### Terminal 1: Django Development Server

```bash
# Navigate to project
cd /Users/airforce/wedding-site

# Activate virtual environment
source venv/bin/activate

# Run Django dev server
python manage.py runserver
```

**Access at:** http://127.0.0.1:8000

**What it does:**
- Serves your Django app locally
- Auto-reloads on Python file changes (views, models, settings)
- Hot reloads templates
- Shows errors in terminal

---

### Terminal 2: TailwindCSS Watch Mode

```bash
# Navigate to project
cd /Users/airforce/wedding-site

# Run Tailwind watcher
npm run watch-css
```

**What it does:**
- Watches `wedding/static/css/tailwind-src.css`
- Auto-compiles to `wedding/static/css/tailwind.css`
- Rebuilds CSS instantly when you change Tailwind classes in templates
- Shows build output in terminal

---

## Workflow for Real-Time Changes

### HTML/TailwindCSS Changes

1. Edit template: `wedding/templates/wedding/home.html`
2. Change classes: `class="mt-20"` → `class="mt-8"`
3. Save file
4. Terminal 2 shows: "Rebuilding..."
5. Hard refresh browser: **Cmd+Shift+R** (Mac) or **Ctrl+F5** (Windows)
6. See changes instantly ✨

### Python Changes (Views, Models, Settings)

1. Edit file: `wedding/views.py`
2. Save file
3. Terminal 1 shows: "...code changed, reloading."
4. Regular refresh browser: **Cmd+R** or **F5**
5. See changes instantly ✨

### Custom CSS Changes

1. Edit: `wedding/static/css/tailwind-src.css` (custom styles)
2. Save file
3. Terminal 2 rebuilds automatically
4. Hard refresh browser: **Cmd+Shift+R**
5. See changes instantly ✨

---

## Common Commands

### Stop Servers

- **In each terminal:** Press `Ctrl+C`

### Restart Django Server

```bash
# In Terminal 1 (after stopping with Ctrl+C)
python manage.py runserver
```

### Restart Tailwind Watcher

```bash
# In Terminal 2 (after stopping with Ctrl+C)
npm run watch-css
```

### Check What's Running

```bash
# See if Django is running
lsof -i :8000

# Kill Django if stuck
pkill -f runserver
```

---

## Troubleshooting

### "Port already in use" Error

```bash
# Kill whatever's on port 8000
lsof -ti:8000 | xargs kill -9

# Then restart
python manage.py runserver
```

### CSS Changes Not Showing

```bash
# Hard refresh browser: Cmd+Shift+R
# Or clear browser cache

# Check Terminal 2 - is Tailwind watcher running?
# Restart watcher if needed:
npm run watch-css
```

### Python Changes Not Showing

```bash
# Check Terminal 1 - did Django auto-reload?
# Look for: "...code changed, reloading."

# If not, restart server:
Ctrl+C
python manage.py runserver
```

### Virtual Environment Not Activated

```bash
# You'll see error: "command not found: python"
# Activate venv:
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

---

## Quick Start Checklist

- [ ] Open Terminal 1
- [ ] `cd /Users/airforce/wedding-site`
- [ ] `source venv/bin/activate`
- [ ] `python manage.py runserver`
- [ ] Open Terminal 2 (new tab/window)
- [ ] `cd /Users/airforce/wedding-site`
- [ ] `npm run watch-css`
- [ ] Visit http://127.0.0.1:8000 in browser
- [ ] Make changes and see them live!

---

## When You're Done

1. **Terminal 1:** Press `Ctrl+C` to stop Django
2. **Terminal 2:** Press `Ctrl+C` to stop Tailwind watcher
3. Close terminals or type `deactivate` to exit venv

---

**Pro Tip:** Keep both terminals visible side-by-side so you can see rebuild output and errors in real-time!
