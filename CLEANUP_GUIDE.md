# Wedding Site Cleanup Guide
## Transitioning from RSVP + Wedding to Wedding-Only Site

**Objective**: Remove RSVP functionality and dependencies to create a clean, informational wedding website.

---

## Table of Contents

1. [Safe to Delete - No Risk](#safe-to-delete---no-risk)
2. [Safe to Delete - Low Risk](#safe-to-delete---low-risk)
3. [Conditional Deletion - Medium Risk](#conditional-deletion---medium-risk)
4. [Risky - Requires Code Changes](#risky---requires-code-changes)
5. [Must Keep - Critical](#must-keep---critical)
6. [Step-by-Step Deletion Plan](#step-by-step-deletion-plan)

---

## Safe to Delete - No Risk

### 🗑️ `/rsvp/` - Entire RSVP App Directory

**Why Not Vital**: You're icing the RSVP app completely

**What It Contains**:
- RSVP models (Guest model with UUID grouping)
- RSVP views (entire multi-step workflow)
- RSVP templates (lookup, confirm, questions, etc.)
- RSVP forms (GuestLookupForm, RSVPDetailsForm)
- RSVP URL patterns
- RSVP static files (rsvp_style.css)
- Management commands (load_guests, fix_family_groupings, etc.)
- RSVP migrations

**Downstream Deletion Risk**: ⚠️ **MEDIUM**
- **Database Impact**: Guest table will remain in database but be unused
- **URL Impact**: All `/rsvp/*` URLs will return 404
- **Settings Impact**: Must remove 'rsvp' from INSTALLED_APPS
- **Root URL Impact**: Currently `/` redirects to `/rsvp/` - will break

**Required Follow-Up Actions**:
1. Remove `'rsvp'` from `INSTALLED_APPS` in `wedding_site/settings.py`
2. Remove `path('rsvp/', include('rsvp.urls'))` from `wedding_site/urls.py`
3. Change root redirect from `/rsvp/` to `/wedding/` or `/wedding/home/`
4. Remove `rsvp/static` from `STATICFILES_DIRS` (if explicitly listed)
5. (Optional) Drop Guest table from database with migration

**Commands to Execute After Deletion**:
```bash
# Remove from Git
git rm -r rsvp/

# Update settings
# (Edit wedding_site/settings.py - remove 'rsvp' from INSTALLED_APPS)

# Update URLs
# (Edit wedding_site/urls.py - remove rsvp include, update root redirect)

# Create migration to drop Guest table (optional)
python manage.py makemigrations
python manage.py migrate
```

---

### 🗑️ `/rsvp/management/commands/` - RSVP Management Commands

**Files**:
- `load_guests.py` (213 lines)
- `update_guests.py` (157 lines)
- `fix_family_groupings.py` (180 lines)
- `add_cotton_guests.py` (47 lines)

**Why Not Vital**: All commands operate on Guest model which is being removed

**Downstream Deletion Risk**: ✅ **NONE** (if deleting entire `/rsvp/` directory)
- These are already inside `/rsvp/` so deleting the parent directory removes them

---

### 🗑️ `add_cotton_script.py` - Root-Level Guest Addition Script

**Why Not Vital**: Standalone script for adding guests to RSVP system

**Downstream Deletion Risk**: ✅ **NONE**
- No dependencies on this file
- Only used for Railway-specific guest additions

**Command**:
```bash
rm add_cotton_script.py
```

---

### 🗑️ `fix_emails.py` - Email Cleanup Script

**Why Not Vital**: One-off utility for fixing placeholder emails in Guest model

**Downstream Deletion Risk**: ✅ **NONE**
- Standalone utility script
- No dependencies

**Command**:
```bash
rm fix_emails.py
```

---

### 🗑️ RSVP Data Backup Files

**Files**:
- `rsvp_app_backup.json`
- Potentially `wedding_data_backup.json` (if includes RSVP data)

**Why Not Vital**: Backups of Guest model data you're removing

**Downstream Deletion Risk**: ✅ **NONE**
- Static data files
- No code dependencies
- **Recommendation**: Archive rather than delete (move to `/archive/` folder)

**Commands**:
```bash
# Archive instead of delete
mkdir archive
mv rsvp_app_backup.json archive/
mv wedding_data_backup.json archive/  # If it contains RSVP data
```

---

### 🗑️ `CLAUDE.md` - RSVP Styling Guidelines

**Why Not Vital**: Document specifically for RSVP pink/rose color palette

**Downstream Deletion Risk**: ✅ **NONE** if using TailwindCSS exclusively for wedding site
- Documentation file only
- No code dependencies
- Wedding app uses TailwindCSS, not these custom CSS guidelines

**Recommendation**: Archive instead of delete (may want color palette reference)

**Command**:
```bash
mv CLAUDE.md archive/CLAUDE.md
```

---

## Safe to Delete - Low Risk

### 🗑️ `run_migration.py` - PostgreSQL Migration Script

**Why Not Vital**: One-time migration script for RSVP data from SQLite to PostgreSQL

**What It Does**:
- Checks marker file (`/tmp/migration_completed`)
- Creates database tables
- Loads guest data from JSON backup
- Runs `fix_family_groupings` command

**Downstream Deletion Risk**: ⚠️ **LOW**
- **Procfile Impact**: Currently called in Procfile
- **Deployment Impact**: If Procfile still references this, deployment will fail

**Required Follow-Up Actions**:
1. Update `Procfile` to remove migration script
2. Ensure database migrations run via standard `migrate` command

**Current Procfile**:
```
web: python run_migration.py && gunicorn wedding_site.wsgi:application
```

**Updated Procfile**:
```
web: python manage.py migrate && gunicorn wedding_site.wsgi:application
```

**Commands**:
```bash
# Update Procfile first
# (Edit Procfile - see above)

# Then delete script
rm run_migration.py
```

---

### 🗑️ `migrate_to_postgres.py` - Manual Migration Utility

**Why Not Vital**: Developer utility for manual database migrations

**Downstream Deletion Risk**: ✅ **NONE**
- Not used in production/deployment
- Developer convenience tool only

**Command**:
```bash
rm migrate_to_postgres.py
```

---

## Conditional Deletion - Medium Risk

### 🤔 `django-widget-tweaks` - Form Rendering Helper

**Current Usage**: Only used in RSVP forms for Bootstrap-style rendering

**Found In**:
- `rsvp/forms.py` - RSVPDetailsForm rendering
- `rsvp/templates/rsvp/` - Form template tags `{% load widget_tweaks %}`

**Why Not Vital**: Wedding app doesn't use forms (no user input needed)

**Downstream Deletion Risk**: ⚠️ **LOW**
- If wedding app has any forms: **MEDIUM RISK**
- If wedding app is purely informational: **LOW RISK**

**Check Before Deleting**:
```bash
# Search for widget_tweaks usage in wedding app
grep -r "widget_tweaks" wedding/
grep -r "render_field" wedding/
```

**If No Results**:
```bash
# Remove from requirements.txt
# (Edit requirements.txt - remove django-widget-tweaks==1.5.0)

# Uninstall locally
pip uninstall django-widget-tweaks

# Remove from INSTALLED_APPS
# (Edit wedding_site/settings.py - remove 'widget_tweaks')
```

**If Results Found**: Keep it, wedding app uses it

---

### 🤔 `djangorestframework` - Django REST Framework

**Current Usage**: StoryEntry API endpoints for photo timeline

**Found In**:
- `wedding/serializers.py` - StoryEntrySerializer
- `wedding_site/settings.py` - INSTALLED_APPS
- `wedding_site/urls.py` - DRF router for StoryEntry ViewSet

**Why It Might Not Be Vital**:
- If "Our Story" page can be simplified to server-side rendering instead of AJAX
- If photo timeline can be rendered directly in template without API

**Downstream Deletion Risk**: ⚠️ **MEDIUM**
- **Our Story Page Impact**: Currently uses AJAX to load StoryEntry data
- **Code Changes Required**: Must refactor `our_story.html` template
- **JavaScript Impact**: `scrollLoader.js` may use API endpoints

**Decision Tree**:

```
Do you want dynamic AJAX loading on "Our Story" page?
│
├─ YES → Keep DRF
│   - Photo timeline loads dynamically
│   - Better UX with lazy loading
│   - More complex
│
└─ NO → Delete DRF
    - Render all photos server-side in template
    - Simpler codebase
    - Faster initial page load
    - Must refactor our_story view
```

**Check Current Usage**:
```bash
# Find DRF usage in wedding app
grep -r "rest_framework" wedding/
grep -r "serializers" wedding/
grep -r "/api/" wedding/

# Check JavaScript API calls
grep -r "fetch\|ajax\|XMLHttpRequest" wedding/static/js/
```

**If Keeping**: No action needed

**If Deleting**:
1. Refactor `wedding/views.py::our_story_view()` to pass StoryEntry queryset to template
2. Update `our_story.html` to loop through entries server-side
3. Remove `wedding/serializers.py`
4. Remove DRF router from `wedding_site/urls.py`
5. Remove `'rest_framework'` from INSTALLED_APPS
6. Remove `djangorestframework==3.15.2` from requirements.txt
7. Update/remove `scrollLoader.js` if it uses API

**Recommendation**: **Keep DRF** unless you want to simplify significantly

---

### 🤔 RSVP Background Image

**File**: `wedding/static/images/backgrounds/rsvp.png`

**Why Not Vital**: Background image for RSVP pages

**Current Usage**: Referenced in `rsvp/static/css/rsvp_style.css`

**Downstream Deletion Risk**: ✅ **NONE** (if deleting entire RSVP app)
- No wedding app dependencies
- Not referenced in wedding templates

**Check Before Deleting**:
```bash
grep -r "rsvp.png" wedding/
```

**If No Results**:
```bash
rm wedding/static/images/backgrounds/rsvp.png
```

---

### 🤔 PostgreSQL Dependencies

**Package**: `psycopg2-binary==2.9.9`

**Why You Might Not Need It**: If switching to SQLite or other database

**Downstream Deletion Risk**: 🔴 **HIGH** if using PostgreSQL in production
- **Railway Production**: Currently uses PostgreSQL (DATABASE_URL)
- **Local Development**: May use SQLite

**Decision Tree**:

```
Are you keeping PostgreSQL in production?
│
├─ YES → Keep psycopg2-binary
│   - Railway PostgreSQL requires it
│   - StoryEntry model needs database
│
└─ NO → Delete psycopg2-binary
    - Must switch DATABASE_URL to SQLite or other
    - Must update Railway configuration
    - Must migrate StoryEntry data
```

**Recommendation**: **Keep it** - PostgreSQL is production-ready and already set up

---

## Risky - Requires Code Changes

### ⚠️ Root URL Redirect

**Current State**: `wedding_site/urls.py`
```python
urlpatterns = [
    path('', lambda request: redirect('/rsvp/')),  # ← This will break
    path('wedding/', include('wedding.urls')),
    path('rsvp/', include('rsvp.urls')),           # ← This will break
    path('admin/', admin.site.urls),
]
```

**Why Risky**: Root URL redirects to non-existent `/rsvp/`

**Downstream Deletion Risk**: 🔴 **HIGH**
- **User Impact**: Homepage (`foreverandalways.love`) will 404
- **SEO Impact**: Search engines will get errors
- **User Experience**: Broken entry point

**Required Changes**:

**Option 1: Redirect to Wedding Home**
```python
urlpatterns = [
    path('', lambda request: redirect('/wedding/home/')),
    path('wedding/', include('wedding.urls')),
    path('admin/', admin.site.urls),
]
```

**Option 2: Wedding App as Root**
```python
# In wedding/urls.py - change from 'wedding/<page>/' to just '<page>/'
urlpatterns = [
    path('home/', views.home_view, name='home'),
    path('our-story/', views.our_story_view, name='our_story'),
    # ...
]

# In wedding_site/urls.py
urlpatterns = [
    path('', include('wedding.urls')),  # Wedding at root
    path('admin/', admin.site.urls),
]
```

**Option 3: Direct Home View at Root**
```python
from wedding import views as wedding_views

urlpatterns = [
    path('', wedding_views.home_view, name='home'),
    path('wedding/', include('wedding.urls')),
    path('admin/', admin.site.urls),
]
```

**Recommendation**: **Option 2** - Clean URLs (`/home/`, `/our-story/` instead of `/wedding/home/`)

---

### ⚠️ `INSTALLED_APPS` in Settings

**Current State**: `wedding_site/settings.py`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',      # ← May be removable
    'widget_tweaks',       # ← Likely removable
    'wedding',
    'rsvp',                # ← MUST REMOVE
]
```

**Why Risky**: Removing apps without migrations can cause Django errors

**Required Changes**:

1. **Remove RSVP App**:
   ```python
   INSTALLED_APPS = [
       'django.contrib.admin',
       'django.contrib.auth',
       'django.contrib.contenttypes',
       'django.contrib.sessions',
       'django.contrib.messages',
       'django.contrib.staticfiles',
       'rest_framework',      # Keep if using DRF for StoryEntry
       # 'widget_tweaks',     # Remove if not used in wedding app
       'wedding',
       # 'rsvp',              # REMOVED
   ]
   ```

2. **Create Migration to Drop RSVP Tables**:
   ```bash
   # Django will detect rsvp app removal
   python manage.py makemigrations
   # Will create migration to drop Guest table

   python manage.py migrate
   ```

**Downstream Deletion Risk**: ⚠️ **MEDIUM**
- **Migration Impact**: Database will have orphaned Guest table until migration runs
- **Production Impact**: Must run migration on Railway after deployment
- **Data Loss**: Guest data will be permanently deleted (archive first!)

**Safe Deletion Process**:
1. Archive RSVP data first: `python manage.py dumpdata rsvp > archive/rsvp_final_backup.json`
2. Remove 'rsvp' from INSTALLED_APPS
3. Run `makemigrations` and `migrate` locally
4. Test locally
5. Commit and deploy to Railway
6. Railway will auto-run migrations

---

### ⚠️ `STATICFILES_DIRS` in Settings

**Current State**: `wedding_site/settings.py`
```python
STATICFILES_DIRS = [
    'wedding/static',
    'rsvp/static',     # ← MUST REMOVE if deleting rsvp
]
```

**Why Risky**: Django will error if directory doesn't exist

**Required Change**:
```python
STATICFILES_DIRS = [
    'wedding/static',
    # 'rsvp/static',  # REMOVED
]
```

**Downstream Deletion Risk**: ⚠️ **LOW**
- **collectstatic Impact**: Will error if rsvp/static referenced but doesn't exist
- **Development Impact**: runserver may warn about missing directory

**Safe Process**:
1. Update `STATICFILES_DIRS` before deleting `/rsvp/`
2. Or delete both simultaneously

---

### ⚠️ TailwindCSS Content Paths

**Current State**: `tailwind.config.js`
```javascript
module.exports = {
  content: [
    './wedding/templates/**/*.html',
    './rsvp/templates/**/*.html',    // ← MUST REMOVE
  ],
  // ...
}
```

**Why Risky**: TailwindCSS will scan non-existent directory (warning but not error)

**Required Change**:
```javascript
module.exports = {
  content: [
    './wedding/templates/**/*.html',
    // './rsvp/templates/**/*.html',  // REMOVED
  ],
  // ...
}
```

**Downstream Deletion Risk**: ⚠️ **LOW**
- **Build Impact**: May show warnings during CSS build
- **Performance**: Faster builds without scanning extra directory

**Command After Change**:
```bash
npm run build-css
```

---

## Must Keep - Critical

### ✅ `/wedding/` - Wedding App Directory

**Why Critical**: This is your entire website now

**Contains**:
- All wedding information pages
- StoryEntry model (photo timeline)
- Templates (home, our_story, itinerary, gallery, FAQ, etc.)
- Static files (TailwindCSS, images, JavaScript)
- Views and URL routing

**Deletion Risk**: 🔴 **CATASTROPHIC** - Deletes entire website

---

### ✅ `/wedding_site/` - Django Project Configuration

**Why Critical**: Core Django settings and configuration

**Contains**:
- `settings.py` - Database, apps, middleware, static files
- `urls.py` - Root URL routing
- `wsgi.py` - Production server entry point

**Deletion Risk**: 🔴 **CATASTROPHIC** - Django won't run

---

### ✅ `requirements.txt` (Core Dependencies)

**Must Keep**:
```python
Django==5.2.1                    # Framework
Pillow==10.4.0                   # Image handling for StoryEntry
psycopg2-binary==2.9.9           # PostgreSQL (if using in production)
python-decouple==3.8             # Environment variables
whitenoise==6.6.0                # Static file serving
gunicorn==21.2.0                 # Production server
dj-database-url==2.1.0           # Database URL parsing
djangorestframework==3.15.2      # If keeping StoryEntry API
```

**Can Remove**:
```python
django-widget-tweaks==1.5.0      # Only if not used in wedding app
```

**Deletion Risk**: 🔴 **HIGH** - Missing dependencies will crash app

---

### ✅ `package.json` & `node_modules/`

**Why Critical**: TailwindCSS build system for wedding app

**Contains**:
- TailwindCSS dependency
- Build scripts (build-css, watch-css)

**Deletion Risk**: 🔴 **HIGH** - Can't build CSS for wedding site

---

### ✅ `tailwind.config.js`

**Why Critical**: TailwindCSS configuration with custom wedding theme

**Contains**:
- Custom color palette (peach, coral, dark-red, blush)
- Custom fonts (Lora, Luxurious Script)
- Background image utilities

**Deletion Risk**: 🔴 **HIGH** - TailwindCSS won't build correctly

---

### ✅ `Procfile` & `railway.json`

**Why Critical**: Railway deployment configuration

**Must Update** (not delete):
```
# Current
web: python run_migration.py && gunicorn wedding_site.wsgi:application

# Updated (after removing run_migration.py)
web: python manage.py migrate && gunicorn wedding_site.wsgi:application
```

**Deletion Risk**: 🔴 **CATASTROPHIC** - Railway won't know how to start app

---

### ✅ `runtime.txt`

**Why Critical**: Specifies Python version for Railway

**Content**: `python-3.11.9`

**Deletion Risk**: 🔴 **HIGH** - May use wrong Python version

---

### ✅ Database Files

**Development**: `db.sqlite3`
**Production**: PostgreSQL (Railway-managed)

**Why Critical**: Stores StoryEntry data (photo timeline)

**Deletion Risk**: 🔴 **CATASTROPHIC** - Lose all wedding content

**Recommendation**: Back up before any changes
```bash
python manage.py dumpdata wedding > archive/wedding_app_final_backup.json
```

---

### ✅ `manage.py`

**Why Critical**: Django's command-line utility

**Deletion Risk**: 🔴 **CATASTROPHIC** - Can't run any Django commands

---

### ✅ `.env` / Environment Variables

**Why Critical**: Secret key, database URL, allowed hosts

**Deletion Risk**: 🔴 **CATASTROPHIC** - App won't start without config

---

## Step-by-Step Deletion Plan

### Phase 1: Backup Everything (Do This First!)

```bash
# Create archive directory
mkdir -p archive

# Backup RSVP data
python manage.py dumpdata rsvp > archive/rsvp_final_backup_$(date +%Y%m%d).json

# Backup wedding data
python manage.py dumpdata wedding > archive/wedding_final_backup_$(date +%Y%m%d).json

# Backup full database
python manage.py dumpdata > archive/full_backup_$(date +%Y%m%d).json

# Copy RSVP directory to archive (for reference)
cp -r rsvp archive/rsvp_backup

# Archive documentation
mv CLAUDE.md archive/
```

---

### Phase 2: Update Configuration Files

**Step 1: Update `wedding_site/urls.py`**
```python
# Before
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('/rsvp/')),
    path('wedding/', include('wedding.urls')),
    path('rsvp/', include('rsvp.urls')),
    path('admin/', admin.site.urls),
]

# After (Option A: Keep /wedding/ prefix)
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('/wedding/home/')),
    path('wedding/', include('wedding.urls')),
    path('admin/', admin.site.urls),
]

# After (Option B: Wedding at root - cleaner URLs)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('wedding.urls')),  # Wedding pages at root
    path('admin/', admin.site.urls),
]
```

**Step 2: Update `wedding_site/settings.py`**

Remove from `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',      # Keep if using StoryEntry API
    # 'widget_tweaks',     # Remove (RSVP only)
    'wedding',
    # 'rsvp',              # REMOVE THIS
]
```

Remove from `STATICFILES_DIRS`:
```python
STATICFILES_DIRS = [
    'wedding/static',
    # 'rsvp/static',  # REMOVE THIS
]
```

**Step 3: Update `tailwind.config.js`**
```javascript
module.exports = {
  content: [
    './wedding/templates/**/*.html',
    // './rsvp/templates/**/*.html',  // REMOVE THIS
  ],
  theme: {
    extend: {
      // ... keep existing config
    },
  },
}
```

**Step 4: Update `Procfile`**
```
# Before
web: python run_migration.py && gunicorn wedding_site.wsgi:application

# After
web: python manage.py migrate && gunicorn wedding_site.wsgi:application
```

**Step 5: Update `requirements.txt`**

Remove:
```
django-widget-tweaks==1.5.0
```

Keep everything else (unless you decide to remove DRF).

---

### Phase 3: Delete RSVP Files

```bash
# Delete RSVP app
git rm -rf rsvp/

# Delete RSVP scripts
git rm add_cotton_script.py
git rm fix_emails.py
git rm run_migration.py
git rm migrate_to_postgres.py

# Delete RSVP backups (optional - already archived)
git rm rsvp_app_backup.json
git rm wedding_data_backup.json  # If contains RSVP data

# Delete RSVP background image
git rm wedding/static/images/backgrounds/rsvp.png
```

---

### Phase 4: Update Dependencies

```bash
# Uninstall removed packages
pip uninstall django-widget-tweaks

# Rebuild requirements.txt
pip freeze > requirements.txt

# Rebuild CSS
npm run build-css
```

---

### Phase 5: Database Cleanup

```bash
# Create migration to drop RSVP tables
python manage.py makemigrations

# You should see something like:
# Migrations for 'rsvp':
#   rsvp/migrations/0005_auto_YYYYMMDD_HHMM.py
#     - Delete model Guest

# Apply migration locally
python manage.py migrate

# Verify Guest table is gone
python manage.py dbshell
# In SQLite: .tables
# In PostgreSQL: \dt
# Should NOT see rsvp_guest table
```

---

### Phase 6: Test Locally

```bash
# Start development server
python manage.py runserver

# Test all pages:
# - Home: http://127.0.0.1:8000 (or http://127.0.0.1:8000/wedding/home/)
# - Our Story: http://127.0.0.1:8000/wedding/our-story/
# - Itinerary: http://127.0.0.1:8000/wedding/itinerary/
# - Gallery: http://127.0.0.1:8000/wedding/gallery/
# - FAQ: http://127.0.0.1:8000/wedding/faq/
# - Admin: http://127.0.0.1:8000/admin/

# Verify:
# ✅ No 404 errors
# ✅ Static files load (CSS, images, JS)
# ✅ StoryEntry data displays on "Our Story" page
# ✅ All navigation links work
# ✅ No console errors in browser dev tools
```

---

### Phase 7: Commit and Deploy

```bash
# Stage all changes
git add .

# Commit
git commit -m "Remove RSVP app - transition to wedding info site only

- Deleted /rsvp/ app directory and all RSVP-related files
- Removed RSVP from INSTALLED_APPS and URL configuration
- Updated root URL to redirect to wedding site
- Removed django-widget-tweaks dependency
- Created database migration to drop Guest table
- Archived RSVP data and code for reference
- Updated Procfile to use standard migrate command"

# Push to main (triggers Railway deployment)
git push origin main
```

---

### Phase 8: Verify Production Deployment

**Check Railway Logs**:
```bash
railway logs
```

**Look for**:
- ✅ Migration successful
- ✅ Gunicorn started
- ✅ No import errors
- ✅ Static files collected

**Test Production Site**:
- Visit `https://foreverandalways.love`
- Should redirect to wedding home page
- Test all pages
- Verify images and CSS load
- Check admin panel works

---

## Summary: What's Getting Deleted

### 🗑️ **Definitely Delete** (No Risk)
- [x] `/rsvp/` directory (entire RSVP app)
- [x] `add_cotton_script.py`
- [x] `fix_emails.py`
- [x] `run_migration.py`
- [x] `migrate_to_postgres.py`
- [x] `rsvp_app_backup.json` (archive first)
- [x] `CLAUDE.md` (archive first)
- [x] `wedding/static/images/backgrounds/rsvp.png`

### 🤔 **Probably Delete** (Low Risk)
- [ ] `django-widget-tweaks` from requirements.txt (check wedding app first)
- [ ] `wedding_data_backup.json` (archive first)

### ⚠️ **Maybe Delete** (Medium Risk - Requires Decision)
- [ ] `djangorestframework` (if simplifying StoryEntry to server-side rendering)

### ✅ **Never Delete** (Critical)
- [x] `/wedding/` directory
- [x] `/wedding_site/` directory
- [x] `requirements.txt` (core dependencies)
- [x] `package.json` & TailwindCSS setup
- [x] `Procfile` (update, don't delete)
- [x] `railway.json`
- [x] `runtime.txt`
- [x] `manage.py`
- [x] Database files
- [x] `.env` / environment variables

---

## Final Checklist Before Going Live

- [ ] RSVP data backed up to `/archive/`
- [ ] Wedding data backed up to `/archive/`
- [ ] All configuration files updated (settings.py, urls.py, tailwind.config.js)
- [ ] RSVP files deleted from Git
- [ ] Dependencies updated (requirements.txt)
- [ ] CSS rebuilt (`npm run build-css`)
- [ ] Migrations created and applied locally
- [ ] Local testing passed (all pages work)
- [ ] Changes committed to Git
- [ ] Deployed to Railway
- [ ] Production testing passed
- [ ] Admin panel accessible
- [ ] StoryEntry data intact
- [ ] No 404 errors on production

---

## Estimated Impact

**Lines of Code Removed**: ~2,500+ lines
- `/rsvp/` app: ~1,500 lines
- Management commands: ~600 lines
- Migration scripts: ~200 lines
- Utilities: ~100 lines
- Documentation: ~100 lines

**Files Removed**: ~50+ files
- RSVP app files: ~40
- Scripts: ~5
- Backups/docs: ~5

**Database Tables Dropped**: 1 (Guest table)

**Dependencies Removed**: 1-2 packages
- `django-widget-tweaks` (confirmed)
- `djangorestframework` (optional)

**Result**: Cleaner, simpler codebase focused solely on wedding information

---

**Good luck with the cleanup! The wedding site will be much cleaner afterward.** 🧹✨
