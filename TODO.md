# Wedding Site - TODO List

**Last Updated**: 2026-01-06
**Current Goal**: Content & functionality completion before deployment

---

## 🔴 High Priority - Content & Functionality

### Home Page
- [ ] **Replace video with correct wedding video**
  - Current video needs to be swapped out
  - Location: `wedding/templates/wedding/home.html` or `wedding/static/videos/`

### Our Story Page
- [x] **Add StoryEntry content via Django admin** ✅ (2026-01-06)
  - All 16 story entries added with photos/content/dates/descriptions
  - Admin user: delta / kellyandjohn@foreverandalways.com
  - Template now uses dynamic DB-driven content
  - Responsive grid with vertically centered images
  - Modals working perfectly!

- [ ] **Create backup of StoryEntry database**
  - Dump all 16 story entries to a JSON fixture file
  - Store in `wedding/fixtures/story_entries.json`
  - Easily recoverable if database gets wiped
  - Commands:
    ```bash
    # Create backup
    python manage.py dumpdata wedding.StoryEntry --indent 2 > wedding/fixtures/story_entries.json

    # Restore from backup
    python manage.py loaddata wedding/fixtures/story_entries.json
    ```

- [ ] **Rework modal layout and formatting**
  - Photo on the left (40% width)
  - Title centered at the top of the modal
  - Content on the right (60% width) - subtitle, date, description
  - Move close 'x' button to top right corner of modal (currently misaligned)
  - Location: `wedding/templates/wedding/our_story.html:126-161`

### Itinerary Page
- [ ] **Confirm/finalize layout**
  - Review current itinerary page design
  - Verify timeline, schedule, venue info displays correctly
  - Make any necessary layout adjustments

### Gallery Page
- [ ] **Add engagement photos**
  - Upload engagement photos to media folder
  - Add to gallery template or via admin

- [ ] **Add Telluride photos**
  - Upload Telluride photos to media folder
  - Add to gallery template or via admin

### New Pages
- [ ] **Create Honeymoon Fund page**
  - Add content/copy for honeymoon fund information
  - Include payment/contribution links if applicable
  - Ensure page matches site design

- [ ] **Create FAQ page**
  - Write FAQ content (accommodations, dress code, etc.)
  - Design Q&A layout with site styling
  - Ensure mobile-friendly accordion or list format

---

## ✅ Completed - Our Story Database Migration (Session 2026-01-06)

- [x] **Created Django admin superuser**
  - Username: delta
  - Email: kellyandjohn@foreverandalways.com
  - Access: http://127.0.0.1:8000/admin/

- [x] **Added all 16 StoryEntry records via admin**
  - Blue Moon, RMNP, Colorado Springs, Leaf Peeping
  - Broncos, One Year Anniversary, First 14er, Mexico
  - Skiing, Red Rocks, Two Year Anniversary, New Zealand
  - Three Year Anniversary, NYE, Four Year Anniversary, Engagement

- [x] **Updated Our Story template to use database**
  - Switched from static hardcoded images to dynamic DB-driven content
  - Responsive grid: 1→2→3→4 columns with `items-center` for vertical alignment
  - Images flow left-to-right, varying heights handled gracefully
  - Static images commented out as backup
  - `wedding/templates/wedding/our_story.html:8-19`

- [x] **Added chronological ordering to view**
  - Stories display in date order
  - `wedding/views.py:13`

- [x] **Modals fully functional**
  - Click any image to open modal with full story details
  - JavaScript working properly with API
  - Smooth hover transitions on thumbnails

---

## ✅ Completed - RSVP Cleanup (Session 2026-01-04)

- [x] **Removed 'rsvp' from INSTALLED_APPS**
- [x] **Removed 'widget_tweaks' from INSTALLED_APPS**
- [x] **Removed 'rsvp/static' from STATICFILES_DIRS**
- [x] **Removed RSVP templates from tailwind.config.js**
- [x] **Fixed outdated comment in wedding_site/urls.py**
- [x] **Converted "Our Story" page to TailwindCSS grid**
  - Responsive grid: 1→2→3→4 columns
  - Images flow left-to-right across rows
- [x] **Fixed JavaScript API URL** - `wedding/static/js/ourstory-modal.js:7`
- [x] **All local testing passed**
  - All pages load without errors
  - Navigation working (desktop + mobile)
  - Browser console clean
  - Responsive design verified

---

## 🟡 Medium Priority - Optional Cleanup

### Dependency Cleanup
- [ ] **Remove django-widget-tweaks from requirements.txt**
  - Optional: Can remove to reduce dependencies
  ```bash
  pip uninstall django-widget-tweaks
  pip freeze > requirements.txt
  ```

### Database Cleanup
- [ ] **Drop Guest table (optional)**
  ```bash
  python manage.py makemigrations
  # May detect rsvp app removal and prompt to drop table
  ```
  - Guest table is harmless if left unused

### Production Testing (After Deploy)

- [ ] **Railway deployment succeeds**

  - Check Railway logs for errors
  - Verify migrations ran successfully

- [ ] **Ugly URL works**: http://wedding-site-production-8735.up.railway.app

  - Test all pages
  - Verify static files load

- [ ] **When ready: Re-add custom domain**

  - Add `foreverandalways.love` back in Railway
  - Wait 5-10 mins for DNS propagation
  - Test production site

- [ ] **Production site fully functional**
  - All pages load
  - No errors in Railway logs
  - Static files and media files work
  - Admin panel accessible

---

## 🚀 Deployment Steps

- [ ] **Pre-deployment checks**

  - [ ] All local tests passing
  - [ ] CSS rebuilt: `npm run build-css`
  - [ ] No uncommitted changes (or commit them)

- [ ] **Commit cleanup changes**

  ```bash
  git add .
  git commit -m "Remove RSVP app and clean up codebase

  - Deleted /rsvp/ directory and related scripts
  - Updated URL routing to wedding-only
  - Fixed navigation links (desktop + mobile)
  - Removed RSVP from settings and dependencies
  - Updated Procfile for standard migrations
  - Created migration to drop Guest table"
  ```

- [ ] **Push to Railway**

  ```bash
  git push origin main
  ```

- [ ] **Monitor deployment**

  - Watch Railway dashboard
  - Check build logs
  - Verify deployment succeeds

- [ ] **Post-deployment verification**
  - Test ugly URL
  - Check Railway logs for errors
  - Verify database migration ran

---

## 📝 Optional Improvements (Future)

- [ ] **Consider removing `/wedding/` prefix entirely**

  - Change `wedding_site/urls.py` to: `path('', include('wedding.urls'))`
  - URLs become: `/`, `/our-story/`, `/itinerary/` (cleaner)
  - Update all template links to remove `/wedding/` prefix

- [ ] **Evaluate if DRF is still needed**

  - If StoryEntry API is only used for "Our Story" page
  - Consider simplifying to server-side rendering
  - Would remove djangorestframework dependency

- [ ] **Add "Coming Soon" or "Under Construction" page**

  - If you want to hide work-in-progress from family

- [ ] **SEO improvements**

  - Add meta descriptions
  - Add Open Graph tags for social sharing
  - Add structured data for wedding event

- [ ] **Performance optimizations**
  - Image compression
  - Lazy loading for images
  - CSS minification

---

## 🐛 Known Issues / Bugs

_None currently - add any issues you discover here_

---

## 💡 Ideas / Future Features

_Add any ideas for the site here_

---

## Notes

- **Domain Status**: Custom domain removed from Railway
- **Ugly URL**: wedding-site-production-8735.up.railway.app
- **Local Dev**: Two terminals (Django + TailwindCSS watcher)
- **RSVP Files**: KEEPING in codebase, just removing from settings/config
- **Hard Refresh**: Always use Cmd+Shift+R after CSS/HTML changes! (See LOCAL_DEV_SETUP.md)
- **Admin Credentials**: delta / kandj / kellyandjohn@foreverandalways.com
- **StoryEntry Database**: ✅ All 16 entries added and working!

---

**Progress Tracker**:

- ✅ URL rewiring complete
- ✅ JavaScript API fix complete
- ✅ Navigation links fixed (desktop + mobile)
- ✅ Settings/config cleanup complete
- ✅ "Our Story" grid layout complete (responsive TailwindCSS grid)
- ✅ RSVP removed from settings (files kept in codebase)
- ✅ Local testing complete
- ✅ Admin user created (delta)
- ✅ All 16 StoryEntry records added via admin
- ✅ Our Story page fully functional with working modals
- 🔄 Content & functionality work in progress (FAQ, Honeymoon Fund, Gallery)
- ⏳ Deployment pending (after remaining content complete)
