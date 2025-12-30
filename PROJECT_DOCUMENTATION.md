# Wedding Website Project Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Architecture](#project-architecture)
4. [Directory Structure](#directory-structure)
5. [Application Structure](#application-structure)
6. [Data Models](#data-models)
7. [RSVP Flow](#rsvp-flow)
8. [Static Assets and Styling](#static-assets-and-styling)
9. [Configuration and Settings](#configuration-and-settings)
10. [Database Management](#database-management)
11. [Deployment](#deployment)
12. [Development Workflow](#development-workflow)

---

## Project Overview

This is a **Django 5.2.1-based wedding website** for Kelly & John's 2026 wedding. The project consists of two primary components that work together to provide a complete wedding experience:

1. **Wedding Information Site** - Public-facing informational pages about the wedding
2. **RSVP Management System** - Guest registration and response collection system

The project is deployed on **Railway.app** using **PostgreSQL** as the production database and serves static files through **WhiteNoise**. The site is accessible at the custom domain `foreverandalways.love`.

### Key Features

- **Photo Timeline**: Dynamic "Our Story" page with database-driven photo entries
- **Guest Management**: UUID-based group RSVP system for families and couples
- **Multi-Step RSVP Flow**: Guest lookup, confirmation, attendance selection, and details collection
- **Responsive Design**: Mobile-first design using TailwindCSS and custom CSS
- **Admin Interface**: Customized Django admin for guest management
- **REST API**: Limited API endpoints for dynamic content loading

---

## Technology Stack

### Backend

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.11.9 | Runtime environment |
| **Django** | 5.2.1 | Web framework (MVT pattern) |
| **Django REST Framework** | 3.15.2 | API endpoints for StoryEntry |
| **PostgreSQL** | Latest (Railway) | Production database |
| **SQLite** | Built-in | Development database |
| **Gunicorn** | 21.2.0 | WSGI HTTP server for production |
| **WhiteNoise** | 6.6.0 | Static file serving |
| **Pillow** | 10.4.0 | Image processing for uploads |
| **psycopg2-binary** | 2.9.9 | PostgreSQL adapter |

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| **TailwindCSS** | 3.x | Utility-first CSS framework (wedding app) |
| **Custom CSS** | N/A | Hand-written styles (RSVP app) |
| **AlpineJS** | 3.x (CDN) | Reactive components without build step |
| **Vanilla JavaScript** | ES6+ | Interactive features and DOM manipulation |
| **Vimeo Player API** | Latest (CDN) | Video content integration |

### Build Tools

| Technology | Purpose |
|------------|---------|
| **Node.js & npm** | TailwindCSS build system |
| **PostCSS** | CSS processing pipeline |
| **Tailwind CLI** | CSS compilation and purging |

### Python Dependencies (Complete List)

```python
Django==5.2.1                    # Web framework
djangorestframework==3.15.2      # REST API toolkit
django-widget-tweaks==1.5.0      # Form rendering utilities
Pillow==10.4.0                   # Image processing
psycopg2-binary==2.9.9           # PostgreSQL adapter
python-decouple==3.8             # Environment variable management
whitenoise==6.6.0                # Static file serving
gunicorn==21.2.0                 # Production WSGI server
dj-database-url==2.1.0           # Database URL parsing
```

### Node Dependencies

```json
{
  "tailwindcss": "^3.4.17"
}
```

---

## Project Architecture

### Architectural Pattern: Traditional Django MVT

This project follows Django's **Model-View-Template** (MVT) pattern with server-side rendering:

- **Models**: Define data structures (Guest, StoryEntry)
- **Views**: Handle request logic and render templates
- **Templates**: Django Template Language (DTL) for HTML generation
- **No Single-Page Application**: Traditional multi-page website with progressive enhancement

### Two-App Architecture

The project uses a **dual-app strategy** that separates concerns while sharing infrastructure:

```
┌─────────────────────────────────────────────────────────────┐
│                    wedding_site (Project)                    │
│  ┌───────────────────────┐  ┌───────────────────────────┐  │
│  │   wedding (App)       │  │    rsvp (App)             │  │
│  │                       │  │                           │  │
│  │  • Informational      │  │  • Guest Management       │  │
│  │  • Photo Timeline     │  │  • RSVP Collection        │  │
│  │  • Static Content     │  │  • Group Handling         │  │
│  │  • TailwindCSS        │  │  • Custom CSS             │  │
│  │                       │  │                           │  │
│  │  URLs: /wedding/*     │  │  URLs: /rsvp/*            │  │
│  └───────────────────────┘  └───────────────────────────┘  │
│                                                              │
│            Shared: Static Files, Media, Database             │
└─────────────────────────────────────────────────────────────┘
```

### How the Apps are Separate

**Wedding App (`/wedding/`):**
- **Purpose**: Informational content about the wedding event
- **URL Namespace**: `/wedding/*` (e.g., `/wedding/our-story/`, `/wedding/itinerary/`)
- **Styling**: TailwindCSS with peach/coral/dark-red color palette
- **Templates**: Based on `wedding/templates/wedding/base.html`
- **Data Model**: `StoryEntry` (photo timeline entries)
- **Navigation**: Full navigation bar across all pages
- **User Flow**: Browsing and reading content

**RSVP App (`/rsvp/`):**
- **Purpose**: Guest management and response collection
- **URL Namespace**: `/rsvp/*` (e.g., `/rsvp/lookup/`, `/rsvp/confirm/`)
- **Styling**: Custom CSS with pink/rose color palette (per CLAUDE.md)
- **Templates**: Based on `rsvp/templates/rsvp/base.html`
- **Data Model**: `Guest` (UUID-based groups)
- **Navigation**: Minimal navigation, focused workflow
- **User Flow**: Sequential steps from lookup to completion

### How the Apps are Enmeshed

Despite being separate Django apps, they share common infrastructure:

1. **Shared Static File Collection**:
   ```python
   STATICFILES_DIRS = [
       'wedding/static',  # TailwindCSS styles
       'rsvp/static',     # Custom CSS
   ]
   ```

2. **Shared Database**: Both apps use the same PostgreSQL/SQLite database

3. **Shared URL Configuration**: Both routed through `wedding_site/urls.py`:
   ```python
   urlpatterns = [
       path('', lambda r: redirect('/rsvp/')),  # Root redirects to RSVP
       path('wedding/', include('wedding.urls')),
       path('rsvp/', include('rsvp.urls')),
       path('admin/', admin.site.urls),
   ]
   ```

4. **Shared Settings**: Both apps use `wedding_site/settings.py` configuration

5. **Shared Media Directory**: Both can use `/media/` for uploads (though only wedding app currently does)

6. **Shared Admin Interface**: Both models accessible via `/admin/`

7. **Shared Deployment**: Both apps deploy together as a single Django project

**Key Insight**: The separation is **logical** (different domains of functionality) rather than **physical** (different servers or codebases). They are two apps within one Django project, sharing infrastructure while maintaining independent concerns.

---

## Directory Structure

### Root Level Directory Breakdown

```
wedding-site/
├── wedding_site/          # Django project configuration directory
├── wedding/               # Main wedding website app
├── rsvp/                  # RSVP management app
├── media/                 # User-uploaded media files
├── staticfiles/           # Collected static files for production (generated)
├── node_modules/          # NPM dependencies for TailwindCSS
├── venv/                  # Python virtual environment (not in Git)
├── db.sqlite3             # Development database (not in production)
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── package.json           # Node.js dependencies and scripts
├── package-lock.json      # Locked Node.js dependencies
├── tailwind.config.js     # TailwindCSS configuration
├── Procfile               # Railway deployment configuration
├── railway.json           # Railway service configuration
├── runtime.txt            # Python version specification
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore patterns
├── README.md              # Project documentation
├── CLAUDE.md              # RSVP styling guidelines
└── [migration scripts]    # Various database migration utilities
```

---

### `/wedding_site/` - Django Project Configuration

**Purpose**: Central configuration directory for the entire Django project. This is the "settings hub" that ties everything together.

```
wedding_site/
├── __init__.py            # Python package marker
├── settings.py            # Main Django settings (DATABASE, INSTALLED_APPS, etc.)
├── urls.py                # Root URL configuration
├── wsgi.py                # WSGI entry point for production servers
└── asgi.py                # ASGI entry point (async, not currently used)
```

**Key Files**:

- **`settings.py`** (173 lines):
  - Installed apps: `['wedding', 'rsvp', 'rest_framework', 'widget_tweaks']`
  - Database configuration via `dj_database_url` (auto-detects PostgreSQL URL)
  - Static file settings with WhiteNoise middleware
  - Media file configuration (`MEDIA_ROOT = 'media/'`)
  - Security settings (`SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`)
  - Template configuration with context processors

- **`urls.py`** (Root URL router):
  ```python
  urlpatterns = [
      path('', lambda request: redirect('/rsvp/')),  # Default to RSVP
      path('wedding/', include('wedding.urls')),
      path('rsvp/', include('rsvp.urls')),
      path('admin/', admin.site.urls),
  ]
  ```
  - Redirects root URL to `/rsvp/` (RSVP as primary entry point)
  - Includes URL patterns from both apps
  - Registers Django admin interface

- **`wsgi.py`**:
  - WSGI application callable for Gunicorn
  - Production deployment entry point

---

### `/wedding/` - Main Wedding Website App

**Purpose**: Informational pages about the wedding event, including photo timeline, itinerary, FAQ, and gallery.

```
wedding/
├── __init__.py
├── admin.py               # Admin interface for StoryEntry model
├── apps.py                # App configuration
├── forms.py               # Form definitions (currently empty)
├── models.py              # StoryEntry model (photo timeline)
├── serializers.py         # DRF serializer for StoryEntry API
├── urls.py                # URL routing for wedding pages
├── views.py               # View functions for all pages
├── migrations/            # Database migrations for StoryEntry
│   ├── 0001_initial.py
│   └── __init__.py
├── templates/             # Django templates
│   └── wedding/
│       ├── base.html                    # Base template with navigation
│       ├── downtown_westminster.html    # Downtown guide page
│       ├── faq.html                     # Frequently asked questions
│       ├── gallery.html                 # Photo gallery
│       ├── home.html                    # Landing page
│       ├── honeymoon_fund.html          # Honeymoon fund information
│       ├── itinerary.html               # Wedding day schedule
│       └── our_story.html               # Photo timeline page
└── static/                # Static assets
    ├── css/
    │   ├── tailwind-src.css             # TailwindCSS source (input)
    │   └── tailwind.css                 # Compiled TailwindCSS (output)
    ├── images/
    │   ├── backgrounds/                 # Page background images
    │   │   ├── downtown_westminster_background.png
    │   │   ├── faq_background.png
    │   │   ├── gallery_background.png
    │   │   ├── home_background.png
    │   │   ├── honeymoon_background.png
    │   │   ├── itinerary_background.png
    │   │   ├── ourStory_background.png
    │   │   └── rsvp.png                 # Used by RSVP app
    │   ├── ourStory/                    # Static story photos
    │   │   ├── meetup1.png
    │   │   ├── meetup2.png
    │   │   └── meetup3.png
    │   ├── itinerary/                   # Venue images
    │   │   ├── ceremonySite.png
    │   │   ├── hotel.png
    │   │   └── reception.png
    │   └── header/                      # Logo and branding
    │       ├── blackAndWhiteLogo.png
    │       ├── favicon.ico
    │       └── whiteLogo.png
    └── js/
        ├── scrollLoader.js              # Lazy loading utilities
        └── ourstory-modal.js            # Photo modal interactions
```

**Key Components**:

#### Models (`models.py`)

```python
class StoryEntry(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=225, blank=True, null=True)
    date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='our_story_photos/')
```
- Represents photo timeline entries on "Our Story" page
- Images uploaded to `media/our_story_photos/`
- Exposed via REST API for dynamic loading

#### Views (`views.py`)

All views are **function-based views (FBVs)** that render templates:

- `home_view()` - Landing page
- `our_story_view()` - Photo timeline with StoryEntry data
- `itinerary_view()` - Wedding day schedule
- `gallery_view()` - Photo gallery
- `honeymoon_fund_view()` - Registry/gift information
- `downtown_westminster_view()` - Local area guide
- `faq_view()` - Frequently asked questions

#### API Endpoints (`serializers.py` + DRF ViewSet)

REST API for StoryEntry model:
- `GET /wedding/story-entries/` - List all story entries
- `GET /wedding/story-entries/<id>/` - Get single entry
- Used for AJAX loading on "Our Story" page

#### Static Files

**CSS Architecture**:
- **Input**: `tailwind-src.css` (TailwindCSS directives + custom styles)
- **Processing**: TailwindCSS CLI compiles with `tailwind.config.js`
- **Output**: `tailwind.css` (purged, optimized CSS)
- **Custom Theme**: Peach (#c19e98), Coral (#de8a74), Dark Red (#521714)

**JavaScript**:
- `scrollLoader.js`: Lazy loading and scroll animations
- `ourstory-modal.js`: Photo modal lightbox functionality

**Images**:
- **Backgrounds**: Full-page background images per route
- **Content**: Venue photos, timeline images
- **Branding**: Logo variants (white, black, favicon)

---

### `/rsvp/` - RSVP Management App

**Purpose**: Complete guest RSVP workflow from lookup to confirmation, handling individual and group responses.

```
rsvp/
├── __init__.py
├── admin.py               # Custom Guest admin interface
├── apps.py                # App configuration
├── forms.py               # GuestLookupForm, RSVPDetailsForm
├── models.py              # Guest model with UUID groups
├── urls.py                # RSVP workflow URL patterns
├── views.py               # RSVP flow logic (350+ lines)
├── migrations/            # Database migrations
│   ├── 0001_initial.py
│   ├── 0002_guest_dietary_restrictions_guest_email_and_more.py
│   ├── 0003_alter_guest_email.py
│   ├── 0004_alter_guest_email.py
│   └── __init__.py
├── management/            # Custom Django commands
│   └── commands/
│       ├── __init__.py
│       ├── add_cotton_guests.py        # Add specific guests
│       ├── fix_family_groupings.py     # Fix group assignments
│       ├── load_guests.py              # Bulk import from CSV
│       └── update_guests.py            # Update guest data
├── templates/             # RSVP workflow templates
│   └── rsvp/
│       ├── base.html                   # RSVP base template
│       ├── confirm_guest.html          # Confirm identity
│       ├── group_confirm.html          # Group attendance selection
│       ├── group_declined.html         # All guests declined
│       ├── group_rsvp_questions.html   # Group details form
│       ├── group_thank_you.html        # Completion page
│       ├── lookup.html                 # Name search entry point
│       ├── not_found.html              # No match found
│       ├── rsvp_questions_no.html      # Declining guest message
│       ├── rsvp_questions_yes.html     # Attending guest details
│       └── select_guest.html           # Multiple match selection
└── static/
    └── css/
        └── rsvp_style.css              # 509 lines of custom CSS
```

**Key Components**:

#### Models (`models.py`)

```python
class Guest(models.Model):
    group_id = models.UUIDField(default=uuid.uuid4, editable=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=False)
    dietary_restrictions = models.TextField(blank=True, null=True)
    message_for_couple = models.TextField(blank=True, null=True)
    attending = models.BooleanField(null=True, blank=True)
```

**Critical Design: UUID-Based Grouping**
- `group_id` is a UUID field that groups related guests (families, couples)
- Guests with the same UUID are part of the same RSVP group
- Individual guests have unique UUIDs
- Indexed for fast queries: `Guest.objects.filter(group_id=some_uuid)`
- Editable in admin for manual group management

**Tri-State `attending` Field**:
- `None` - No response yet (initial state)
- `True` - Guest is attending
- `False` - Guest declined

#### Views (`views.py` - 350+ lines)

Complex multi-step RSVP flow with session management:

1. **`lookup_guest()`** - Entry point:
   - Form: Enter first and last name
   - Queries database for matching guests
   - Routes to confirmation or selection page

2. **`confirm_guest()`** - Single match confirmation:
   - Shows guest details for verification
   - Buttons: "That's Me" or "Go Back"
   - Stores `guest_id` in session

3. **`select_guest()`** - Multiple match selection:
   - Lists all matching guests
   - Radio button selection
   - Continues to confirmation

4. **`not_found()`** - No match found:
   - Dead-end page
   - Provides contact information

5. **`group_confirm()`** - Group attendance selection:
   - Loads all guests with same `group_id`
   - Checkboxes: "Who will be attending?"
   - Updates `attending` field for each guest

6. **`rsvp_questions_yes()`** - Individual attending details:
   - Email (required)
   - Dietary restrictions (optional)
   - Message for couple (optional)
   - Saves to Guest model

7. **`rsvp_questions_no()`** - Individual declining message:
   - Optional message for couple
   - Marks `attending=False`

8. **`group_rsvp_questions()`** - Group details collection:
   - Loops through all attending guests in group
   - Collects email, dietary restrictions for each
   - Dynamic form rendering

9. **`group_declined()`** - All guests declined:
   - Shows when entire group declines
   - Optional group message

10. **`group_thank_you()`** - Completion page:
    - Thank you message
    - Different variants for attending/declining

**Session Variables Used**:
- `guest_id` - Primary guest being processed
- `group_id` - UUID of the guest's group
- `attending_guest_ids` - List of attending guest IDs (for group flow)

#### Forms (`forms.py`)

**`GuestLookupForm`**:
```python
class GuestLookupForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
```

**`RSVPDetailsForm`**:
```python
class RSVPDetailsForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['email', 'dietary_restrictions', 'message_for_couple']
```
- Email validation with helpful error messages
- Filters out `@placeholder.com` emails from validation
- Uses `widget_tweaks` for Bootstrap-style rendering

#### Management Commands

**`load_guests.py`** (213 lines):
- Bulk import guests from CSV file
- Predefined family groupings with UUIDs
- Adds test guests (NATO phonetic alphabet names)
- Usage: `python manage.py load_guests --csv-path guests.csv [--clear]`

**Family Groups Hardcoded**:
```python
FAMILY_GROUPS = {
    'Anderson': uuid.UUID('...'),
    'Behrens': uuid.UUID('...'),
    'Brooks': uuid.UUID('...'),
    # ... 15+ families
}
```

**`update_guests.py`** (157 lines):
- Updates existing guests without deleting RSVP data
- Preserves `attending` field values
- Dry-run mode for safety

**`fix_family_groupings.py`** (180 lines):
- Corrects group assignments after data issues
- Reassigns guests to correct families
- Idempotent (safe to re-run)

**`add_cotton_guests.py`** (47 lines):
- Adds specific guests (Will Cotton, J.T. Cotton)
- Checks for duplicates before inserting

#### Static Files

**`rsvp_style.css`** (509 lines):
- Custom CSS following CLAUDE.md guidelines
- Pink/rose color palette:
  - Primary Dark: #b22158 (headings)
  - Primary Medium: #d46b8c (celebration text)
  - Primary Light: #ebb6c2 (buttons)
  - Primary Pale: #eed4e2 (backgrounds)
- Fonts:
  - 'Lora', serif (body text)
  - 'Beth Ellen', cursive (celebration text)
- Responsive design with mobile breakpoints

---

### `/media/` - User-Uploaded Media

**Purpose**: Storage for database-driven uploaded files (Django's `MEDIA_ROOT`).

```
media/
└── our_story_photos/      # StoryEntry model images
    ├── photo1.jpg
    ├── photo2.png
    └── ...
```

**Configuration**:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = 'media/'
```

**Access**:
- Development: Django's development server serves at `/media/`
- Production: Static file serving via WhiteNoise or web server

**Current Usage**:
- Only used by `StoryEntry.image` field
- Images uploaded via Django admin

---

### `/staticfiles/` - Collected Static Files

**Purpose**: Production static file directory created by `python manage.py collectstatic`.

**How It Works**:
1. Development: Django serves from `STATICFILES_DIRS` directly
2. Production:
   - `collectstatic` gathers all static files from apps
   - Copies to `/staticfiles/`
   - WhiteNoise serves from this directory with compression and caching

**Configuration**:
```python
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles/'
STATICFILES_DIRS = ['wedding/static', 'rsvp/static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

**Git Status**: Typically in `.gitignore` (generated file)

---

### `/node_modules/` - NPM Dependencies

**Purpose**: Node.js packages for TailwindCSS build system.

**Installation**: `npm install`

**Contents**:
- `tailwindcss` - TailwindCSS CLI and core
- Dependencies of TailwindCSS (PostCSS, autoprefixer, etc.)

**Git Status**: In `.gitignore` (not committed)

---

### `/venv/` - Python Virtual Environment

**Purpose**: Isolated Python environment with project dependencies.

**Creation**: `python -m venv venv`

**Activation**:
- macOS/Linux: `source venv/bin/activate`
- Windows: `venv\Scripts\activate`

**Git Status**: In `.gitignore` (not committed)

---

### Root-Level Configuration Files

#### `manage.py`

Django's command-line utility for administrative tasks:
```bash
python manage.py runserver       # Start development server
python manage.py migrate         # Apply database migrations
python manage.py createsuperuser # Create admin user
python manage.py collectstatic   # Collect static files
python manage.py load_guests     # Custom command
```

#### `requirements.txt`

Python dependencies for production:
```
Django==5.2.1
djangorestframework==3.15.2
django-widget-tweaks==1.5.0
Pillow==10.4.0
psycopg2-binary==2.9.9
python-decouple==3.8
whitenoise==6.6.0
gunicorn==21.2.0
dj-database-url==2.1.0
```

#### `package.json`

Node.js dependencies and build scripts:
```json
{
  "scripts": {
    "build-css": "tailwindcss -i wedding/static/css/tailwind-src.css -o wedding/static/css/tailwind.css",
    "watch-css": "tailwindcss -i wedding/static/css/tailwind-src.css -o wedding/static/css/tailwind.css --watch"
  },
  "dependencies": {
    "tailwindcss": "^3.4.17"
  }
}
```

**Usage**:
- `npm run build-css` - One-time build for production
- `npm run watch-css` - Watch mode for development

#### `tailwind.config.js`

TailwindCSS configuration with custom wedding theme:
```javascript
module.exports = {
  content: [
    './wedding/templates/**/*.html',
    './rsvp/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        peach: '#c19e98',
        coral: '#de8a74',
        'dark-red': '#521714',
        blush: '#f1ebe9',
      },
      fontFamily: {
        lora: ['Lora', 'serif'],
        script: ['Luxurious Script', 'cursive'],
      },
      backgroundImage: {
        'home': "url('/static/images/backgrounds/home_background.png')",
        // ... more backgrounds
      },
    },
  },
}
```

#### `Procfile`

Railway deployment startup command:
```
web: python run_migration.py && gunicorn wedding_site.wsgi:application
```

**Execution Order**:
1. Run migrations and data loading (`run_migration.py`)
2. Start Gunicorn WSGI server

#### `railway.json`

Railway service configuration:
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

#### `runtime.txt`

Python version specification:
```
python-3.11.9
```

#### `.env.example`

Template for environment variables:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/dbname
ALLOWED_HOSTS=foreverandalways.love,www.foreverandalways.love
CSRF_TRUSTED_ORIGINS=https://foreverandalways.love,https://www.foreverandalways.love
```

**Actual `.env` file**: In `.gitignore` (secrets)

#### `README.md`

Project documentation with setup instructions and deployment guide.

#### `CLAUDE.md`

RSVP styling guidelines document:
- Color palette specifications
- Typography guidelines
- Component styling patterns
- Responsive design breakpoints
- CSS variable definitions

---

### Migration Scripts (Root Level)

#### `run_migration.py` (65 lines)

**Critical for deployment**: One-time PostgreSQL migration script.

**Purpose**: Migrate from SQLite (development) to PostgreSQL (production)

**Process**:
1. Check for marker file (`/tmp/migration_completed`)
2. If not exists:
   - Run `migrate --run-syncdb` (create tables)
   - Apply RSVP migrations (field constraints)
   - Load data from `wedding_data_backup.json`
   - Run `fix_family_groupings` command
   - Create marker file
3. If exists: Skip (already migrated)

**Called In**: `Procfile` before Gunicorn starts

**Safety Mechanism**: Marker file prevents re-execution on every deploy

#### `migrate_to_postgres.py` (52 lines)

Local utility script for manual migration:
1. Export SQLite to JSON (`dumpdata`)
2. Switch DATABASE_URL to PostgreSQL
3. Import JSON to PostgreSQL (`loaddata`)

**Not used in production**: Manual tool for developers

#### `fix_emails.py` (44 lines)

Bulk email update script:
- Converts `@placeholder.com` emails to real emails
- Used during initial data cleanup
- One-off utility

#### `add_cotton_script.py` (47 lines)

Railway-compatible standalone script:
- Sets up Django environment
- Adds specific guests (Will Cotton, J.T. Cotton)
- Can run via `railway run python add_cotton_script.py`
- Duplicate of management command for convenience

---

### Data Backup Files

#### `wedding_data_backup.json`

Full database dump in Django's JSON fixture format:
- All Guest records
- All StoryEntry records
- Used by `run_migration.py` for PostgreSQL migration

**Generation**: `python manage.py dumpdata > wedding_data_backup.json`

**Loading**: `python manage.py loaddata wedding_data_backup.json`

#### `rsvp_app_backup.json`

RSVP app-specific backup:
- Only Guest model data
- Selective backup for RSVP app

#### `wedding_app_backup.json`

Wedding app-specific backup:
- Only StoryEntry model data
- Selective backup for wedding app

---

## Application Structure

### Wedding App - Page-by-Page Breakdown

#### Home Page (`/wedding/home/`)

**Template**: `wedding/templates/wedding/home.html`

**Features**:
- Hero section with video background
- "Save the Date" call-to-action
- Navigation to other sections
- Responsive design

**Static Assets**:
- Background: `wedding/static/images/backgrounds/home_background.png`
- Logo: `wedding/static/images/header/whiteLogo.png`

#### Our Story Page (`/wedding/our-story/`)

**Template**: `wedding/templates/wedding/our_story.html`

**Features**:
- Photo timeline loaded from database
- Modal lightbox for enlarged photos
- REST API integration for dynamic loading
- Celebration text: "Our journey to forever"

**Data Source**:
- Model: `StoryEntry`
- API: `/wedding/story-entries/`
- Images: `/media/our_story_photos/`

**JavaScript**:
- `ourstory-modal.js` - Modal interactions
- `scrollLoader.js` - Lazy loading

#### Itinerary Page (`/wedding/itinerary/`)

**Template**: `wedding/templates/wedding/itinerary.html`

**Features**:
- Wedding day timeline
- Venue information with images
- Directions and parking

**Static Assets**:
- Ceremony: `wedding/static/images/itinerary/ceremonySite.png`
- Reception: `wedding/static/images/itinerary/reception.png`
- Hotel: `wedding/static/images/itinerary/hotel.png`

#### Gallery Page (`/wedding/gallery/`)

**Template**: `wedding/templates/wedding/gallery.html`

**Features**:
- Photo grid layout
- Responsive image gallery
- Lazy loading for performance

#### FAQ Page (`/wedding/faq/`)

**Template**: `wedding/templates/wedding/faq.html`

**Features**:
- Accordion-style Q&A
- Common guest questions
- Contact information

#### Downtown Westminster Page (`/wedding/downtown-westminster/`)

**Template**: `wedding/templates/wedding/downtown_westminster.html`

**Features**:
- Local area guide
- Restaurant recommendations
- Things to do near venue

#### Honeymoon Fund Page (`/wedding/honeymoon-fund/`)

**Template**: `wedding/templates/wedding/honeymoon_fund.html`

**Features**:
- Gift registry information
- Honeymoon fund details
- Alternative gift suggestions

---

### RSVP App - Workflow Breakdown

#### RSVP Flow Architecture

The RSVP system implements a **multi-step state machine** with branching logic:

```
                    ┌─────────────────┐
                    │  lookup_guest   │ (Entry Point)
                    └────────┬────────┘
                             │
                ┌────────────┼────────────┐
                │            │            │
         ┌──────▼─────┐  ┌──▼──────┐  ┌──▼────────┐
         │ not_found  │  │ confirm │  │  select   │
         │  (Dead-end)│  │  guest  │  │  guest    │
         └────────────┘  └────┬────┘  └────┬──────┘
                              │            │
                              └──────┬─────┘
                                     │
                              ┌──────▼────────┐
                              │ group_confirm │
                              └──────┬────────┘
                                     │
                  ┌──────────────────┼──────────────────┐
                  │                  │                  │
         ┌────────▼────────┐  ┌──────▼───────┐  ┌──────▼─────────┐
         │ Group: All Yes  │  │ Group: Mixed │  │ Group: All No  │
         │                 │  │              │  │                │
         │ rsvp_questions  │  │ Individual   │  │ group_declined │
         │     _yes        │  │ branches     │  │                │
         └────────┬────────┘  └──────┬───────┘  └──────┬─────────┘
                  │                  │                  │
                  │           ┌──────┴──────┐           │
                  │           │             │           │
                  │    ┌──────▼─────┐ ┌────▼────────┐  │
                  │    │ questions  │ │  questions  │  │
                  │    │    _yes    │ │    _no      │  │
                  │    └──────┬─────┘ └────┬────────┘  │
                  │           │             │           │
                  │           └──────┬──────┘           │
                  │                  │                  │
                  └──────────────────┼──────────────────┘
                                     │
                              ┌──────▼──────────┐
                              │ group_thank_you │
                              └─────────────────┘
```

#### Step 1: Guest Lookup (`/rsvp/lookup/`)

**View**: `lookup_guest()`

**Template**: `rsvp/templates/rsvp/lookup.html`

**User Action**: Enter first and last name

**Backend Logic**:
```python
def lookup_guest(request):
    if request.method == 'POST':
        form = GuestLookupForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']

            # Query database
            guests = Guest.objects.filter(
                first_name__iexact=first_name,
                last_name__iexact=last_name
            )

            if guests.count() == 0:
                return redirect('rsvp:not_found')
            elif guests.count() == 1:
                return redirect('rsvp:confirm_guest', guest_id=guests.first().id)
            else:
                return redirect('rsvp:select_guest', first_name=first_name, last_name=last_name)
```

**Routing**:
- 0 matches → `not_found`
- 1 match → `confirm_guest`
- 2+ matches → `select_guest`

#### Step 2a: Confirm Guest (`/rsvp/confirm/<guest_id>/`)

**View**: `confirm_guest(guest_id)`

**Template**: `rsvp/templates/rsvp/confirm_guest.html`

**User Action**: Confirm "That's Me" or go back

**Backend Logic**:
```python
def confirm_guest(request, guest_id):
    guest = get_object_or_404(Guest, id=guest_id)

    if request.method == 'POST':
        # Store in session
        request.session['guest_id'] = guest_id
        request.session['group_id'] = str(guest.group_id)

        # Redirect to group confirmation
        return redirect('rsvp:group_confirm')

    return render(request, 'rsvp/confirm_guest.html', {'guest': guest})
```

**Session Storage**:
- `guest_id` - Primary guest being processed
- `group_id` - UUID for loading group members

#### Step 2b: Select Guest (`/rsvp/select/`)

**View**: `select_guest(first_name, last_name)`

**Template**: `rsvp/templates/rsvp/select_guest.html`

**User Action**: Select correct guest from list

**Backend Logic**:
- Lists all guests with matching name
- Radio button selection
- Redirects to `confirm_guest` with selected ID

#### Step 2c: Not Found (`/rsvp/not-found/`)

**View**: `not_found()`

**Template**: `rsvp/templates/rsvp/not_found.html`

**User Action**: Dead-end, contact hosts

**Content**:
- Apologetic message
- Contact information for manual RSVP
- Link to try again

#### Step 3: Group Confirmation (`/rsvp/group-confirm/`)

**View**: `group_confirm()`

**Template**: `rsvp/templates/rsvp/group_confirm.html`

**User Action**: Select which guests in group are attending

**Backend Logic**:
```python
def group_confirm(request):
    group_id = request.session.get('group_id')
    group_guests = Guest.objects.filter(group_id=group_id)

    if request.method == 'POST':
        attending_ids = request.POST.getlist('attending')

        # Update attending status
        for guest in group_guests:
            if str(guest.id) in attending_ids:
                guest.attending = True
            else:
                guest.attending = False
            guest.save()

        if attending_ids:
            request.session['attending_guest_ids'] = attending_ids
            return redirect('rsvp:group_rsvp_questions')
        else:
            return redirect('rsvp:group_declined')
```

**UI**:
- Checkbox for each guest in group
- "Who will be attending?" question
- Submit button

**Routing**:
- All declined → `group_declined`
- Some/all attending → `group_rsvp_questions`

#### Step 4a: Group RSVP Questions (`/rsvp/group-rsvp-questions/`)

**View**: `group_rsvp_questions()`

**Template**: `rsvp/templates/rsvp/group_rsvp_questions.html`

**User Action**: Fill in details for each attending guest

**Backend Logic**:
```python
def group_rsvp_questions(request):
    attending_ids = request.session.get('attending_guest_ids', [])
    attending_guests = Guest.objects.filter(id__in=attending_ids)

    if request.method == 'POST':
        for guest in attending_guests:
            # Extract form data for each guest
            email = request.POST.get(f'email_{guest.id}')
            dietary = request.POST.get(f'dietary_{guest.id}')
            message = request.POST.get(f'message_{guest.id}')

            # Update guest
            guest.email = email
            guest.dietary_restrictions = dietary
            guest.message_for_couple = message
            guest.save()

        return redirect('rsvp:group_thank_you')
```

**UI**:
- Dynamic form with sections for each attending guest
- Email (required)
- Dietary restrictions (optional)
- Message for couple (optional)

#### Step 4b: Group Declined (`/rsvp/group-declined/`)

**View**: `group_declined()`

**Template**: `rsvp/templates/rsvp/group_declined.html`

**User Action**: Optional message for couple

**Backend Logic**:
- Allows group-wide message
- Confirms all guests marked as `attending=False`

#### Step 4c: Individual RSVP Questions - Attending (`/rsvp/rsvp-questions-yes/<guest_id>/`)

**View**: `rsvp_questions_yes(guest_id)`

**Template**: `rsvp/templates/rsvp/rsvp_questions_yes.html`

**User Action**: Fill in details for single attending guest

**Backend Logic**:
- Similar to group questions but for single guest
- Form: `RSVPDetailsForm`
- Saves email, dietary restrictions, message

#### Step 4d: Individual RSVP Questions - Declining (`/rsvp/rsvp-questions-no/<guest_id>/`)

**View**: `rsvp_questions_no(guest_id)`

**Template**: `rsvp/templates/rsvp/rsvp_questions_no.html`

**User Action**: Optional message for couple

**Backend Logic**:
- Marks `attending=False`
- Saves optional message
- No email required for declining guests

#### Step 5: Thank You (`/rsvp/group-thank-you/`)

**View**: `group_thank_you()`

**Template**: `rsvp/templates/rsvp/group_thank_you.html`

**User Action**: Read confirmation message

**Content**:
- Thank you message
- Next steps
- Contact information
- Different messaging for attending vs. declining

---

## Data Models

### Guest Model (RSVP App)

**Location**: `rsvp/models.py`

```python
class Guest(models.Model):
    group_id = models.UUIDField(default=uuid.uuid4, editable=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(blank=False)
    dietary_restrictions = models.TextField(blank=True, null=True)
    message_for_couple = models.TextField(blank=True, null=True)
    attending = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
```

**Field Details**:

| Field | Type | Purpose | Constraints |
|-------|------|---------|-------------|
| `group_id` | UUIDField | Groups related guests (families/couples) | Indexed, editable, default=uuid4 |
| `first_name` | CharField | Guest's first name | Max 100 chars |
| `last_name` | CharField | Guest's last name | Max 100 chars |
| `email` | EmailField | Contact email | Required (`blank=False`) |
| `dietary_restrictions` | TextField | Dietary needs/allergies | Optional |
| `message_for_couple` | TextField | Personal message to couple | Optional |
| `attending` | BooleanField | Attendance status | Nullable (tri-state) |

**Group Management**:

Guests are grouped using `group_id` UUID:
```python
# Get all guests in a group
group_members = Guest.objects.filter(group_id=some_uuid)

# Count attending guests in group
attending_count = Guest.objects.filter(
    group_id=some_uuid,
    attending=True
).count()
```

**Why UUID Instead of ForeignKey?**

Traditional approach (parent-child):
```python
# NOT USED - More rigid structure
class GuestGroup(models.Model):
    name = models.CharField(max_length=100)

class Guest(models.Model):
    group = models.ForeignKey(GuestGroup, on_delete=models.CASCADE)
```

UUID approach (flexible grouping):
- No need for separate GuestGroup table
- Easy to reassign guests between groups (just change UUID)
- No cascading delete concerns
- Simpler admin interface
- Faster queries with indexed UUID

**Tri-State `attending` Field**:

| Value | Meaning | When Set |
|-------|---------|----------|
| `None` | No response yet | Initial state |
| `True` | Guest is attending | After group_confirm or rsvp_questions_yes |
| `False` | Guest declined | After group_confirm or rsvp_questions_no |

**Admin Interface**:

Custom admin configuration in `rsvp/admin.py`:
```python
@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'attending', 'group_id')
    list_filter = ('attending',)
    search_fields = ('first_name', 'last_name', 'email')
```

Allows:
- Viewing all guests with group_id
- Filtering by attendance status
- Searching by name or email
- Editing group_id to reassign guests

---

### StoryEntry Model (Wedding App)

**Location**: `wedding/models.py`

```python
class StoryEntry(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=225, blank=True, null=True)
    date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='our_story_photos/')

    class Meta:
        verbose_name_plural = "Story Entries"
        ordering = ['date']

    def __str__(self):
        return f"{self.title} ({self.date})"
```

**Field Details**:

| Field | Type | Purpose |
|-------|------|---------|
| `title` | CharField | Main heading for timeline entry |
| `subtitle` | CharField | Optional subheading |
| `date` | DateField | Date of the event/milestone |
| `description` | TextField | Full story text |
| `image` | ImageField | Photo for timeline entry |

**Image Upload**:
- Directory: `media/our_story_photos/`
- Accessed via: `/media/our_story_photos/filename.jpg`
- Admin upload interface provided

**Ordering**:
- Default: Chronological by date
- Displayed oldest to newest on timeline

**REST API**:

Serializer in `wedding/serializers.py`:
```python
class StoryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryEntry
        fields = '__all__'
```

ViewSet configured for DRF:
- `GET /wedding/story-entries/` - List all entries
- `GET /wedding/story-entries/<id>/` - Single entry detail

**Usage**:
- AJAX loading on "Our Story" page
- Avoids full page reload
- Allows dynamic timeline updates

---

## RSVP Flow

### Complete User Journey

#### Scenario 1: Single Guest Attending

```
User: Sarah Johnson (individual guest)

1. Navigate to foreverandalways.love → Auto-redirects to /rsvp/
2. lookup_guest: Enter "Sarah" and "Johnson" → Submit
3. confirm_guest: See "Sarah Johnson" → Click "That's Me"
4. group_confirm: Checkbox next to "Sarah Johnson" → Check box → Submit
5. group_rsvp_questions:
   - Email: sarah.johnson@email.com
   - Dietary: "Vegetarian"
   - Message: "So excited!"
   → Submit
6. group_thank_you: See confirmation message → Done

Database State:
- Guest: first_name="Sarah", last_name="Johnson"
- group_id: <unique UUID>
- attending: True
- email: "sarah.johnson@email.com"
- dietary_restrictions: "Vegetarian"
- message_for_couple: "So excited!"
```

#### Scenario 2: Family Group with Mixed Attendance

```
User: John Smith (representing Smith family)
Family Members:
- John Smith (adult)
- Jane Smith (adult)
- Timmy Smith (child)

1. Navigate to foreverandalways.love → Auto-redirects to /rsvp/
2. lookup_guest: Enter "John" and "Smith" → Submit
3. confirm_guest: See "John Smith" → Click "That's Me"
4. group_confirm: See 3 checkboxes:
   ☑ John Smith
   ☑ Jane Smith
   ☐ Timmy Smith (cannot attend)
   → Submit
5. group_rsvp_questions: See 2 forms (John and Jane):
   John Smith:
   - Email: john@email.com
   - Dietary: "None"
   - Message: ""

   Jane Smith:
   - Email: jane@email.com
   - Dietary: "Gluten-free"
   - Message: ""
   → Submit
6. group_thank_you: See confirmation for 2 attending → Done

Database State:
- All 3 guests have same group_id: <shared UUID>
- John: attending=True, email="john@email.com"
- Jane: attending=True, email="jane@email.com", dietary="Gluten-free"
- Timmy: attending=False, email="" (unchanged)
```

#### Scenario 3: Entire Family Declining

```
User: Bob Anderson (representing Anderson family)
Family Members:
- Bob Anderson (adult)
- Alice Anderson (adult)

1. lookup_guest: Enter "Bob" and "Anderson" → Submit
2. confirm_guest: See "Bob Anderson" → Click "That's Me"
3. group_confirm: See 2 checkboxes:
   ☐ Bob Anderson
   ☐ Alice Anderson
   (Leave all unchecked) → Submit
4. group_declined:
   - Message: "Sorry we can't make it. Best wishes!"
   → Submit
5. group_thank_you: See "sorry to miss you" message → Done

Database State:
- Both guests have same group_id: <shared UUID>
- Bob: attending=False, message_for_couple="Sorry we can't make it..."
- Alice: attending=False
```

#### Scenario 4: Multiple Name Matches

```
User: Michael Brown (there are 3 Michael Browns in guest list)

1. lookup_guest: Enter "Michael" and "Brown" → Submit
2. select_guest: See 3 options:
   ○ Michael Brown (email: michael.brown1@email.com)
   ○ Michael Brown (email: michael.brown2@email.com)
   ○ Michael Brown (email: mike.brown@email.com)
   Select first option → Submit
3. confirm_guest: See "Michael Brown" with email hint → "That's Me"
4. [Continue with normal flow...]
```

#### Scenario 5: Guest Not Found

```
User: Unknown Person (not in guest list)

1. lookup_guest: Enter "Unknown" and "Person" → Submit
2. not_found:
   - Message: "We couldn't find your name in our guest list"
   - Contact information: "Please email kelly@email.com"
   - Link: "Try again"
   → Dead end (cannot proceed)
```

### Session Management

**Session Variables**:

```python
# Set in confirm_guest view
request.session['guest_id'] = 123
request.session['group_id'] = 'a1b2c3d4-...'

# Set in group_confirm view
request.session['attending_guest_ids'] = [123, 124]

# Retrieved in subsequent views
guest_id = request.session.get('guest_id')
group_id = request.session.get('group_id')
attending_ids = request.session.get('attending_guest_ids', [])
```

**Security**:
- Django session framework handles cookies
- Session data stored server-side (database or cache)
- Cannot be tampered with by user

**Cleanup**:
- Sessions cleared on browser close (default)
- Can manually clear: `request.session.flush()`

---

## Static Assets and Styling

### Wedding App Styling (TailwindCSS)

#### Build Process

**Source File**: `wedding/static/css/tailwind-src.css`
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom styles */
@layer components {
  .btn-primary {
    @apply bg-coral hover:bg-dark-red text-white font-bold py-2 px-4 rounded;
  }
}
```

**Build Command**:
```bash
npm run watch-css
# or
npm run build-css
```

**Output File**: `wedding/static/css/tailwind.css` (minified, purged)

**Configuration**: `tailwind.config.js`
```javascript
module.exports = {
  content: [
    './wedding/templates/**/*.html',
    './rsvp/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        peach: '#c19e98',
        coral: '#de8a74',
        'dark-red': '#521714',
        blush: '#f1ebe9',
      },
      fontFamily: {
        lora: ['Lora', 'serif'],
        script: ['Luxurious Script', 'cursive'],
      },
    },
  },
}
```

**Usage in Templates**:
```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/tailwind.css' %}">

<div class="bg-peach text-dark-red font-lora">
  <h1 class="text-4xl font-script">Kelly & John</h1>
</div>
```

#### Font Loading

**Google Fonts Import** (in base template):
```html
<link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600&family=Luxurious+Script&display=swap" rel="stylesheet">
```

**Fonts Used**:
- **Lora** (serif) - Body text, headings
- **Luxurious Script** (cursive) - Decorative headings

---

### RSVP App Styling (Custom CSS)

#### CSS File Structure

**File**: `rsvp/static/css/rsvp_style.css` (509 lines)

**Key Sections**:

1. **CSS Custom Properties** (lines 1-20):
   ```css
   :root {
     --primary-dark: #b22158;
     --primary-medium: #d46b8c;
     --primary-light: #ebb6c2;
     --primary-pale: #eed4e2;
     --white: #ffffff;
     --text-dark: #333333;
   }
   ```

2. **Font Imports** (lines 21-25):
   ```css
   @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600&family=Beth+Ellen&display=swap');
   ```

3. **Base Styles** (lines 26-100):
   - Body background: `var(--primary-dark)`
   - Container backgrounds: `var(--primary-pale)` or `var(--white)`
   - Font family: 'Lora', serif

4. **Typography** (lines 101-200):
   - Headings: `color: var(--primary-dark)`
   - Celebration text: `font-family: 'Beth Ellen', cursive; color: var(--primary-medium);`
   - Body text: 1.25rem Lora

5. **Form Styles** (lines 201-350):
   - Input borders: `var(--primary-medium)`
   - Button backgrounds: `var(--primary-light)`
   - Focus states: `var(--primary-dark)`

6. **Component Styles** (lines 351-450):
   - Modal styling
   - Checkbox/radio buttons
   - Error messages

7. **Responsive Design** (lines 451-509):
   ```css
   @media (max-width: 576px) {
     .celebration-text {
       font-size: 1.25rem;
     }
   }

   @media (min-width: 768px) {
     .celebration-text {
       font-size: 3rem;
     }
   }
   ```

#### Color Palette (CLAUDE.md Specification)

| Element | Color | Hex | CSS Variable |
|---------|-------|-----|--------------|
| Main headings | Primary Dark | #b22158 | `var(--primary-dark)` |
| Celebration text | Primary Medium | #d46b8c | `var(--primary-medium)` |
| Buttons | Primary Light | #ebb6c2 | `var(--primary-light)` |
| Backgrounds | Primary Pale | #eed4e2 | `var(--primary-pale)` |
| Body text | Text Dark | #333333 | `var(--text-dark)` |

#### Celebration Text Styling

**Font**: 'Beth Ellen', cursive (playful, hand-written style)

**Usage**:
```html
<p class="celebration-text">We can't wait to celebrate with you!</p>
```

**CSS**:
```css
.celebration-text {
  font-family: 'Beth Ellen', cursive;
  color: var(--primary-medium);
  font-size: 1.25rem; /* Mobile */
}

@media (min-width: 768px) {
  .celebration-text {
    font-size: 3rem; /* Desktop */
  }
}
```

---

### Static File Organization

#### Wedding App Static Files

```
wedding/static/
├── css/
│   ├── tailwind-src.css        # Source (editable)
│   └── tailwind.css             # Compiled (generated)
├── images/
│   ├── backgrounds/             # Full-page backgrounds
│   │   ├── home_background.png
│   │   ├── ourStory_background.png
│   │   ├── itinerary_background.png
│   │   ├── gallery_background.png
│   │   ├── faq_background.png
│   │   ├── downtown_westminster_background.png
│   │   └── honeymoon_background.png
│   ├── ourStory/                # Timeline photos
│   │   ├── meetup1.png
│   │   ├── meetup2.png
│   │   └── meetup3.png
│   ├── itinerary/               # Venue images
│   │   ├── ceremonySite.png
│   │   ├── reception.png
│   │   └── hotel.png
│   └── header/                  # Branding
│       ├── whiteLogo.png
│       ├── blackAndWhiteLogo.png
│       └── favicon.ico
└── js/
    ├── scrollLoader.js          # Lazy loading utilities
    └── ourstory-modal.js        # Photo modal functionality
```

#### RSVP App Static Files

```
rsvp/static/
└── css/
    └── rsvp_style.css           # Custom RSVP styles (509 lines)
```

**Note**: RSVP app reuses background image from wedding app:
```python
# In rsvp_style.css
body {
  background-image: url('/static/images/backgrounds/rsvp.png');
}
```

---

## Configuration and Settings

### Django Settings (`wedding_site/settings.py`)

#### Core Settings

```python
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY', default='fallback-key')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=lambda v: [s.strip() for s in v.split(',')])
```

**Environment Variables**:
- Loaded via `python-decouple`
- `.env` file in development
- Railway environment variables in production

#### Installed Apps

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',      # DRF for StoryEntry API
    'widget_tweaks',       # Form rendering helpers
    'wedding',             # Wedding app
    'rsvp',                # RSVP app
]
```

#### Middleware

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Static file serving
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

**WhiteNoise**:
- Serves static files in production
- Compression and caching
- No need for nginx/Apache

#### Database Configuration

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}
```

**How It Works**:
- Development: `DATABASE_URL` not set → Uses SQLite
- Production: `DATABASE_URL` set by Railway → Uses PostgreSQL

**Railway PostgreSQL URL Format**:
```
postgresql://user:password@host:port/database
```

#### Static Files Configuration

```python
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles/'
STATICFILES_DIRS = [
    'wedding/static',
    'rsvp/static',
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

**Explanation**:
- `STATIC_URL`: URL prefix for accessing static files
- `STATIC_ROOT`: Directory where `collectstatic` copies files
- `STATICFILES_DIRS`: Source directories for static files
- `STATICFILES_STORAGE`: WhiteNoise storage backend with compression

#### Media Files Configuration

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = 'media/'
```

**Usage**:
- User uploads (StoryEntry images)
- Accessed via `/media/our_story_photos/filename.jpg`

**Development**:
```python
# In wedding_site/urls.py (development only)
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

#### Security Settings

```python
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='',
    cast=lambda v: [s.strip() for s in v.split(',')] if v else []
)
```

**Production Values**:
```
CSRF_TRUSTED_ORIGINS=https://foreverandalways.love,https://www.foreverandalways.love
```

**Why Needed**:
- Django's CSRF protection
- Allows form submissions from custom domain
- Required for Railway deployment with custom domain

#### Templates Configuration

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # App-level templates only
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

**Template Discovery**:
- Django looks in `<app>/templates/` directories
- `wedding/templates/wedding/home.html` → `wedding/home.html` in code
- `rsvp/templates/rsvp/lookup.html` → `rsvp/lookup.html` in code

---

### Environment Variables

#### `.env` File Structure (Development)

```bash
# Django Core
SECRET_KEY=your-random-secret-key-here
DEBUG=True

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Allowed Hosts
ALLOWED_HOSTS=localhost,127.0.0.1

# CSRF
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

#### Railway Environment Variables (Production)

Set in Railway dashboard:

| Variable | Value | Source |
|----------|-------|--------|
| `SECRET_KEY` | Random string | Manual |
| `DEBUG` | `False` | Manual |
| `DATABASE_URL` | `postgresql://...` | Auto (Railway PostgreSQL) |
| `ALLOWED_HOSTS` | `foreverandalways.love,www.foreverandalways.love` | Manual |
| `CSRF_TRUSTED_ORIGINS` | `https://foreverandalways.love,https://www.foreverandalways.love` | Manual |

**Railway Auto-Injection**:
- Railway automatically sets `DATABASE_URL` when PostgreSQL is added
- No manual database configuration needed

---

## Database Management

### Development Database (SQLite)

**File**: `db.sqlite3` (in `.gitignore`)

**Advantages**:
- Zero configuration
- File-based (no server needed)
- Fast for development
- Easy to delete and recreate

**Disadvantages**:
- Not suitable for production
- Limited concurrency
- No advanced features (full-text search, JSON operations)

**Common Commands**:
```bash
# Create database and tables
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Load test data
python manage.py load_guests --csv-path guests.csv

# Access database shell
python manage.py dbshell
```

---

### Production Database (PostgreSQL)

**Provider**: Railway (managed PostgreSQL)

**Connection**: Via `DATABASE_URL` environment variable

**Advantages**:
- Production-ready
- High concurrency
- Advanced features
- Automatic backups (Railway)

**Migration Process**: Handled by `run_migration.py` (see below)

---

### Migration Scripts

#### Initial Migration (`run_migration.py`)

**Purpose**: One-time migration from SQLite to PostgreSQL on first deploy

**Process**:
1. Check if already migrated (marker file)
2. Create database tables
3. Load data from JSON backup
4. Fix family groupings
5. Create marker file to prevent re-runs

**Code Breakdown**:
```python
import os
import django
import subprocess
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wedding_site.settings')
django.setup()

MARKER_FILE = '/tmp/migration_completed'

def run_command(command):
    """Execute Django management command"""
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(1)

def main():
    # Check if already migrated
    if os.path.exists(MARKER_FILE):
        print("Migration already completed. Skipping.")
        return

    print("Starting one-time migration...")

    # Step 1: Create tables
    run_command('python manage.py migrate --run-syncdb')

    # Step 2: Apply RSVP migrations (email field constraints)
    run_command('python manage.py migrate rsvp')

    # Step 3: Load data
    run_command('python manage.py loaddata wedding_data_backup.json')

    # Step 4: Fix family groupings
    run_command('python manage.py fix_family_groupings')

    # Step 5: Create marker
    with open(MARKER_FILE, 'w') as f:
        f.write('Migration completed')

    print("Migration completed successfully!")

if __name__ == '__main__':
    main()
```

**Called In**: `Procfile` before Gunicorn starts

**Marker File**: `/tmp/migration_completed`
- Prevents re-execution on every deploy
- Temporary directory (cleared on container restart if needed)

#### Manual Migration (`migrate_to_postgres.py`)

**Purpose**: Local utility for developers to migrate between databases

**Process**:
```bash
# 1. Export SQLite data
python migrate_to_postgres.py export

# 2. Update .env with PostgreSQL DATABASE_URL

# 3. Import to PostgreSQL
python migrate_to_postgres.py import
```

**Code**:
```python
import subprocess
import sys

def export_data():
    """Export SQLite to JSON"""
    subprocess.run([
        'python', 'manage.py', 'dumpdata',
        '--exclude', 'auth.permission',
        '--exclude', 'contenttypes',
        '--indent', '2',
        '--output', 'wedding_data_backup.json'
    ])

def import_data():
    """Import JSON to PostgreSQL"""
    subprocess.run(['python', 'manage.py', 'migrate', '--run-syncdb'])
    subprocess.run(['python', 'manage.py', 'loaddata', 'wedding_data_backup.json'])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python migrate_to_postgres.py [export|import]")
        sys.exit(1)

    action = sys.argv[1]
    if action == 'export':
        export_data()
    elif action == 'import':
        import_data()
    else:
        print("Invalid action. Use 'export' or 'import'")
```

---

### Guest Data Management

#### Loading Guests from CSV

**Command**: `python manage.py load_guests --csv-path guests.csv [--clear]`

**CSV Format**:
```csv
first_name,last_name,email
John,Smith,john@email.com
Jane,Smith,jane@email.com
Sarah,Johnson,sarah@email.com
```

**Family Grouping** (hardcoded in command):
```python
FAMILY_GROUPS = {
    'Smith': uuid.UUID('a1b2c3d4-e5f6-7890-abcd-ef1234567890'),
    'Johnson': uuid.UUID('b2c3d4e5-f6a7-8901-bcde-f01234567891'),
    # ... more families
}

# Assign family UUID
if last_name in FAMILY_GROUPS:
    group_id = FAMILY_GROUPS[last_name]
else:
    group_id = uuid.uuid4()  # Individual guest
```

**Test Guests**:
- Automatically adds NATO phonetic alphabet names (Alpha, Bravo, Charlie...)
- Useful for testing RSVP flow
- Celebrity test families (Clooney, Hanks, Streep)

#### Updating Guest Data

**Command**: `python manage.py update_guests --csv-path updated_guests.csv`

**Features**:
- Updates existing guests without deleting
- Preserves `attending` status
- Preserves responses (dietary restrictions, messages)
- Only updates: email, group assignments

**Process**:
```python
for row in csv_reader:
    guest = Guest.objects.get(first_name=row['first_name'], last_name=row['last_name'])

    # Update email if changed
    if guest.email != row['email']:
        guest.email = row['email']
        guest.save()

    # Preserve attending status (don't overwrite)
    # Preserve dietary_restrictions, message_for_couple
```

#### Fixing Family Groupings

**Command**: `python manage.py fix_family_groupings`

**Purpose**: Correct group assignments after data issues

**Example**:
```python
# Before: John and Jane Smith have different group_ids
john = Guest.objects.get(first_name='John', last_name='Smith')
jane = Guest.objects.get(first_name='Jane', last_name='Smith')
print(john.group_id)  # a1b2c3d4-...
print(jane.group_id)  # e5f6a7b8-... (WRONG)

# Run fix_family_groupings
subprocess.run(['python', 'manage.py', 'fix_family_groupings'])

# After: Both have same group_id
jane.refresh_from_db()
print(jane.group_id)  # a1b2c3d4-... (FIXED)
```

---

## Deployment

### Railway Platform

**Platform**: Railway.app (PaaS - Platform as a Service)

**Why Railway?**
- Free tier available (or low cost)
- Automatic deployments from Git
- Managed PostgreSQL included
- Custom domain support
- Environment variable management
- Zero-config Python/Node.js detection

**Project Structure**:
```
Railway Project: wedding-site
├── Service: web (Django app)
│   └── Environment variables
│   └── Custom domain: foreverandalways.love
└── Database: PostgreSQL
    └── Auto-injected DATABASE_URL
```

---

### Deployment Process

#### 1. Build Phase

Railway uses **Nixpacks** (specified in `railway.json`):

```json
{
  "build": {
    "builder": "NIXPACKS"
  }
}
```

**Nixpacks Auto-Detection**:
- Detects Python (from `requirements.txt`)
- Detects Node.js (from `package.json`)
- Installs both runtimes

**Build Steps**:
1. Install Python 3.11.9 (from `runtime.txt`)
2. Install Python dependencies: `pip install -r requirements.txt`
3. Install Node.js (for TailwindCSS)
4. Install Node dependencies: `npm install`
5. Build CSS: `npm run build-css` (if in package.json scripts)
6. Collect static files: `python manage.py collectstatic --noinput`

#### 2. Migration Phase

Railway runs the `Procfile` command:

```
web: python run_migration.py && gunicorn wedding_site.wsgi:application
```

**Step 1**: `python run_migration.py`
- Checks for marker file
- If first deploy:
  - Creates PostgreSQL tables
  - Loads guest data from JSON
  - Fixes family groupings
  - Creates marker file
- If subsequent deploy:
  - Skips (marker exists)

**Step 2**: `gunicorn wedding_site.wsgi:application`
- Starts WSGI server
- Listens on port from `$PORT` environment variable
- Serves Django application

#### 3. Runtime Phase

**Process**:
- Gunicorn worker processes handle HTTP requests
- Django renders templates and serves responses
- WhiteNoise serves static files (CSS, JS, images)
- PostgreSQL handles database queries

**Scaling**:
```json
{
  "deploy": {
    "numReplicas": 1,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```
- Single replica (sufficient for wedding site traffic)
- Auto-restart on failures (up to 10 retries)

---

### Custom Domain Configuration

**Domain**: `foreverandalways.love`

**DNS Configuration** (at domain registrar):
```
Type    Name    Value
CNAME   www     <railway-provided-url>
ALIAS   @       <railway-provided-url>
```

**Django Settings**:
```python
ALLOWED_HOSTS = ['foreverandalways.love', 'www.foreverandalways.love']

CSRF_TRUSTED_ORIGINS = [
    'https://foreverandalways.love',
    'https://www.foreverandalways.love'
]
```

**Railway SSL**:
- Automatic SSL certificate provisioning
- HTTPS enforced
- Certificate auto-renewal

---

### Environment Variables in Production

**Set in Railway Dashboard**:

```bash
# Core Django
SECRET_KEY=<random-50-char-string>
DEBUG=False

# Database (auto-set by Railway)
DATABASE_URL=postgresql://postgres:password@host:5432/railway

# Domain
ALLOWED_HOSTS=foreverandalways.love,www.foreverandalways.love

# CSRF
CSRF_TRUSTED_ORIGINS=https://foreverandalways.love,https://www.foreverandalways.love
```

**Accessing in Code**:
```python
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
```

---

### Deployment Checklist

**Pre-Deployment**:
- [ ] Update `requirements.txt` with new dependencies
- [ ] Run `npm run build-css` to compile TailwindCSS
- [ ] Test locally with `DEBUG=False`
- [ ] Create `wedding_data_backup.json` with latest guest data
- [ ] Commit all changes to Git

**Railway Configuration**:
- [ ] Set all environment variables
- [ ] Add PostgreSQL database
- [ ] Configure custom domain DNS
- [ ] Set up environment variables

**Post-Deployment**:
- [ ] Verify site loads at custom domain
- [ ] Test RSVP flow end-to-end
- [ ] Check Django admin access
- [ ] Verify static files loading
- [ ] Test media file uploads

**Monitoring**:
- [ ] Check Railway logs for errors
- [ ] Monitor database size
- [ ] Review RSVP submissions in admin

---

## Development Workflow

### Initial Setup

**Prerequisites**:
- Python 3.11.9
- Node.js (for TailwindCSS)
- Git

**Setup Steps**:

```bash
# 1. Clone repository
git clone <repository-url>
cd wedding-site

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# 4. Install Python dependencies
pip install -r requirements.txt

# 5. Install Node.js dependencies
npm install

# 6. Create .env file
cp .env.example .env
# Edit .env with your values

# 7. Create database
python manage.py migrate

# 8. Create superuser
python manage.py createsuperuser

# 9. Load sample data (optional)
python manage.py load_guests --csv-path guests.csv

# 10. Build CSS
npm run build-css
```

---

### Running Development Server

**Terminal 1 - Django Server**:
```bash
source venv/bin/activate
python manage.py runserver
```
- Serves at: `http://127.0.0.1:8000`
- Auto-reloads on Python file changes

**Terminal 2 - CSS Watch**:
```bash
npm run watch-css
```
- Watches `tailwind-src.css` for changes
- Rebuilds `tailwind.css` automatically

**Access Points**:
- Main site: `http://127.0.0.1:8000` → Redirects to `/rsvp/`
- Wedding pages: `http://127.0.0.1:8000/wedding/`
- Admin: `http://127.0.0.1:8000/admin/`

---

### Common Development Tasks

#### Adding a New Guest

**Option 1: Django Admin**
```
1. Navigate to http://127.0.0.1:8000/admin/
2. Log in
3. Click "Guests" → "Add Guest"
4. Fill in details
5. Set group_id (use existing UUID for family, or generate new)
6. Save
```

**Option 2: Management Command**
```bash
# Create guests.csv
echo "first_name,last_name,email" > guests.csv
echo "New,Guest,new@email.com" >> guests.csv

# Load
python manage.py load_guests --csv-path guests.csv
```

#### Adding a Story Entry

**Django Admin**:
```
1. Navigate to http://127.0.0.1:8000/admin/
2. Click "Story Entries" → "Add Story Entry"
3. Fill in:
   - Title: "Our First Date"
   - Subtitle: "Where it all began"
   - Date: 2023-01-15
   - Description: "We met at..."
   - Image: Upload photo
4. Save
```

**Result**: Appears on `/wedding/our-story/` page

#### Modifying TailwindCSS Styles

**Edit Source**:
```css
/* wedding/static/css/tailwind-src.css */

@layer components {
  .custom-button {
    @apply bg-coral hover:bg-dark-red text-white py-2 px-4 rounded;
  }
}
```

**Rebuild** (automatic if watch-css running):
```bash
npm run watch-css  # Already running → Auto-rebuilds
# or
npm run build-css  # Manual rebuild
```

**Use in Template**:
```html
<button class="custom-button">Click Me</button>
```

#### Modifying RSVP Styles

**Edit CSS**:
```css
/* rsvp/static/css/rsvp_style.css */

.custom-class {
  color: var(--primary-dark);
  font-family: 'Lora', serif;
}
```

**No build step needed** - CSS is static, not compiled

**Refresh browser** to see changes

#### Creating a Database Backup

**Full Backup**:
```bash
python manage.py dumpdata > wedding_data_backup.json
```

**App-Specific Backup**:
```bash
# RSVP only
python manage.py dumpdata rsvp > rsvp_app_backup.json

# Wedding only
python manage.py dumpdata wedding > wedding_app_backup.json
```

**Restore**:
```bash
python manage.py loaddata wedding_data_backup.json
```

---

### Testing Workflow

#### Testing RSVP Flow

**Test Guests** (loaded by `load_guests` command):
- Alpha Alphabet
- Bravo Alphabet
- Charlie Alphabet
- ... (NATO phonetic alphabet)

**Celebrity Test Families**:
- George & Amal Clooney (group)
- Tom & Rita Hanks (group)
- Meryl Streep (individual)

**Test Scenarios**:
1. **Individual Guest**:
   - Lookup: "Meryl" "Streep"
   - Confirm identity
   - Mark attending
   - Fill in details

2. **Family Group**:
   - Lookup: "George" "Clooney"
   - Confirm identity
   - Mark George & Amal attending
   - Fill in details for both

3. **Entire Family Declining**:
   - Lookup: "Tom" "Hanks"
   - Confirm identity
   - Leave all unchecked
   - Submit decline message

4. **Multiple Matches**:
   - Add multiple "John Smith" guests
   - Lookup: "John" "Smith"
   - Test selection page

5. **Not Found**:
   - Lookup: "Unknown" "Person"
   - Verify error page

#### Checking RSVP Responses

**Django Admin**:
```
1. Navigate to http://127.0.0.1:8000/admin/
2. Click "Guests"
3. Filter by "Attending: Yes/No/Unknown"
4. View guest details
```

**Database Query** (Django shell):
```bash
python manage.py shell
```

```python
from rsvp.models import Guest

# Count responses
Guest.objects.filter(attending=True).count()
Guest.objects.filter(attending=False).count()
Guest.objects.filter(attending=None).count()

# List attending guests
for guest in Guest.objects.filter(attending=True):
    print(f"{guest.first_name} {guest.last_name}: {guest.email}")

# Check group
group_id = 'a1b2c3d4-...'
Guest.objects.filter(group_id=group_id)
```

---

### Git Workflow

**Branching Strategy**:
```bash
main  # Production branch (deployed to Railway)
```

**Typical Workflow**:
```bash
# 1. Make changes
git add .
git commit -m "Add new feature"

# 2. Push to main
git push origin main

# 3. Railway auto-deploys
# (Monitor deployment in Railway dashboard)
```

**Important Files in `.gitignore`**:
```
venv/
db.sqlite3
.env
node_modules/
staticfiles/
*.pyc
__pycache__/
media/  # Optional - may want to commit some media
```

---

### Troubleshooting

#### Static Files Not Loading

**Symptoms**: CSS/JS/images return 404

**Solutions**:
```bash
# Development
python manage.py collectstatic --noinput

# Production
# Check STATIC_ROOT and STATICFILES_DIRS in settings.py
# Verify WhiteNoise middleware is enabled
```

#### CSS Changes Not Reflecting

**Symptoms**: CSS edits don't appear

**TailwindCSS**:
```bash
# Ensure watch-css is running
npm run watch-css

# Or rebuild manually
npm run build-css

# Hard refresh browser (Cmd+Shift+R / Ctrl+F5)
```

**RSVP CSS**:
```bash
# Clear browser cache
# Or add cache-busting query param in template:
<link rel="stylesheet" href="{% static 'css/rsvp_style.css' %}?v=2">
```

#### Database Locked (SQLite)

**Symptoms**: `database is locked` error

**Solution**:
```bash
# Stop runserver
# Delete db.sqlite3
rm db.sqlite3

# Recreate
python manage.py migrate
python manage.py load_guests --csv-path guests.csv
```

#### Migration Errors

**Symptoms**: `no such table` or migration conflicts

**Solution**:
```bash
# Show migrations
python manage.py showmigrations

# Fake migrations (if needed)
python manage.py migrate --fake

# Or reset
rm db.sqlite3
python manage.py migrate
```

#### RSVP Session Lost

**Symptoms**: User redirected to beginning of flow

**Cause**: Session expired or cleared

**Solution**:
- Ensure session middleware enabled
- Check session timeout settings
- Use `request.session.set_expiry()` if needed

#### Railway Deployment Fails

**Check Logs**:
```bash
railway logs
```

**Common Issues**:
- Missing environment variables
- Database connection errors
- Migration failures
- Missing requirements in `requirements.txt`

**Solution**:
```bash
# Test locally with production settings
DEBUG=False python manage.py runserver

# Verify requirements
pip freeze > requirements.txt
git commit -m "Update requirements"
git push
```

---

## Summary

This wedding website project is a well-architected Django application that demonstrates:

1. **Separation of Concerns**: Two apps (wedding, rsvp) with distinct purposes
2. **Modern Frontend**: TailwindCSS + custom CSS with responsive design
3. **Robust RSVP System**: UUID-based grouping, multi-step workflow, tri-state attendance
4. **Production-Ready**: WhiteNoise static files, PostgreSQL, Gunicorn, Railway deployment
5. **Developer-Friendly**: Management commands, migration scripts, comprehensive documentation

The dual-app architecture allows the informational wedding site and the functional RSVP system to coexist while sharing infrastructure. The RSVP flow is particularly sophisticated, handling individual guests, family groups, mixed attendance, and edge cases like multiple name matches.

The project is configured for seamless deployment on Railway with automatic migrations, environment-based configuration, and custom domain support. The development workflow is streamlined with hot-reloading for both Python and CSS changes.

---

## Quick Reference

### Essential Commands

```bash
# Development
python manage.py runserver          # Start Django server
npm run watch-css                   # Watch TailwindCSS
python manage.py createsuperuser    # Create admin

# Database
python manage.py migrate            # Apply migrations
python manage.py makemigrations     # Create migrations
python manage.py dbshell            # Database CLI

# Data Management
python manage.py load_guests --csv-path guests.csv
python manage.py fix_family_groupings
python manage.py dumpdata > backup.json
python manage.py loaddata backup.json

# Static Files
python manage.py collectstatic      # Collect for production
npm run build-css                   # Build TailwindCSS

# Deployment
git push origin main                # Auto-deploy to Railway
```

### Key Files

- **Settings**: `wedding_site/settings.py`
- **Root URLs**: `wedding_site/urls.py`
- **Guest Model**: `rsvp/models.py`
- **RSVP Flow**: `rsvp/views.py`
- **Wedding Views**: `wedding/views.py`
- **Tailwind Config**: `tailwind.config.js`
- **Deployment**: `Procfile`, `railway.json`

### URLs

- **Development**: `http://127.0.0.1:8000`
- **Production**: `https://foreverandalways.love`
- **Admin**: `/admin/`
- **RSVP Entry**: `/rsvp/`
- **Wedding Info**: `/wedding/`

---

**Last Updated**: 2025-12-30
**Django Version**: 5.2.1
**Python Version**: 3.11.9
**Deployment**: Railway.app with PostgreSQL
