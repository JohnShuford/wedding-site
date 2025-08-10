# Kelly & John's Wedding Website 2026

A Django-based wedding website featuring RSVP management, photo galleries, itinerary, and wedding information for Kelly and John's 2026 wedding celebration.

## 🎯 Project Overview

This is a full-stack wedding website that provides:
- **Guest RSVP System**: Group-based RSVP management with dietary restrictions and messaging
- **Photo Gallery**: Interactive story timeline with modal displays
- **Wedding Information**: Itinerary, venue details, FAQ, and downtown Westminster guide
- **Honeymoon Fund**: Integration for wedding gifts
- **Email Notifications**: Automated RSVP confirmations and thank you emails

## 🛠 Technology Stack

### Backend
- **Framework**: Django 5.2.1 (Python web framework)
- **Database**: SQLite3 (development)
- **API**: Django REST Framework for AJAX endpoints
- **Additional Packages**: 
  - `widget_tweaks` for form styling
  - UUID-based guest group management

### Frontend
- **JavaScript**: Vanilla JS with AlpineJS for reactivity
- **CSS Framework**: TailwindCSS 3.4.0
- **Custom Styling**: Wedding-themed color palette and typography
- **Fonts**: Lora (serif), Luxurious Script (cursive)

### Media & Assets
- **Image Storage**: Django media handling with organized photo directories
- **Video Content**: Save-the-date videos and background content

## 📁 Project Structure

```
wedding-site/
├── wedding/                 # Main website app
│   ├── static/             # CSS, JS, images, videos
│   ├── templates/          # HTML templates
│   ├── models.py           # StoryEntry model
│   └── views.py            # Main website views
├── rsvp/                   # RSVP management app
│   ├── models.py           # Guest model with UUID groups
│   ├── forms.py            # RSVP forms
│   ├── templates/          # RSVP-specific templates
│   └── management/         # Custom commands (load_guests)
├── wedding_site/           # Django project settings
├── media/                  # User uploads and photos
├── db.sqlite3              # SQLite database
├── package.json            # Node.js for TailwindCSS
└── tailwind.config.js      # Custom wedding theme
```

## 🚀 Getting Started for Developers

### Prerequisites
- Python 3.8+
- Node.js (for TailwindCSS)
- Git

### Setup Instructions

1. **Clone and Enter Project**
   ```bash
   cd wedding-site
   ```

2. **Python Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt  # You may need to create this
   ```

3. **Install Node Dependencies**
   ```bash
   npm install
   ```

4. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Build CSS (Development)**
   ```bash
   npm run watch-css  # Watches for changes
   # OR
   npm run build-css  # One-time build
   ```

6. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

   Visit: http://127.0.0.1:8000

## 🔧 Key Commands

```bash
# Django Management
python manage.py runserver          # Start development server
python manage.py migrate           # Apply database migrations
python manage.py collectstatic     # Collect static files
python manage.py load_guests        # Custom command to load guest list

# TailwindCSS
npm run watch-css                   # Watch CSS changes during development
npm run build-css                   # Build production CSS

# Database
python manage.py shell              # Django shell for database queries
python manage.py dbshell            # Direct database access
```

## 📋 Core Features

### RSVP System (`rsvp` app)
- **Group Management**: Guests linked by UUID group_id
- **Response Tracking**: Boolean attending field with null for no response
- **Guest Details**: Email (required), dietary restrictions, messages
- **Email Integration**: Automated confirmations and thank you emails

### Wedding Content (`wedding` app)
- **Story Entries**: Timeline photos with modals (StoryEntry model)
- **Static Pages**: Itinerary, gallery, FAQ, venue information
- **API Endpoints**: RESTful endpoints for story data
- **Media Management**: Organized photo storage and serving

### Custom Styling
- **Wedding Theme**: Peach, coral, and dark red color palette
- **Typography**: Elegant serif and script fonts
- **Responsive Design**: Mobile-first with desktop navigation
- **Background Images**: Custom backgrounds for each section

## 🎨 Customization

### Colors (tailwind.config.js)
```javascript
colors: {
  'wedding': {
    peach: '#efcebd',
    'dark-red': '#7b2c44',
    'coral': '#c64e45',
    'light-coral': '#f7918e',
    'blush': '#fce1d6',
    dark: '#2e2e2e',
  }
}
```

### Key Models
- **Guest**: RSVP management with group linking
- **StoryEntry**: Photo timeline with title, date, description

## 🌐 URL Structure

```
/                           # Home page
/our-story/                 # Photo timeline
/itinerary/                 # Wedding day schedule  
/gallery/                   # Photo gallery
/rsvp/                      # RSVP system
/honeymoon-fund/           # Gift information
/downtown_westminster/     # Local venue guide
/faq/                      # Frequently asked questions
/admin/                    # Django admin interface
/api/story-entries/<id>/   # API endpoints
```

## 🔒 Security Notes

- Development settings active (DEBUG=True)
- Default Django secret key (change for production)
- ALLOWED_HOSTS needs configuration for deployment
- Consider environment variables for sensitive settings

## 🚢 Deployment Considerations

1. Set `DEBUG=False`
2. Configure `ALLOWED_HOSTS`
3. Use environment variables for secret keys
4. Set up proper database (PostgreSQL recommended)
5. Configure static file serving
6. Set up email backend for RSVP notifications

## 📧 Current Branch: `thank_you_emails`

The project is currently on a feature branch implementing thank you email functionality for RSVP responses.

---

**For questions or issues**, contact the development team or check the Django admin interface at `/admin/` for content management.
