# Wedding Site - TODO List

**Last Updated**: 2026-01-04
**Current Goal**: Content & functionality completion before deployment

---

## 🔴 High Priority - Content & Functionality

### Home Page
- [ ] **Replace video with correct wedding video**
  - Current video needs to be swapped out
  - Location: `wedding/templates/wedding/home.html` or `wedding/static/videos/`

### Our Story Page
- [ ] **Add StoryEntry content via Django admin**
  - Database has 0 story entries currently
  - Need to add photos/content/dates/descriptions for each story
  - Access: http://127.0.0.1:8000/admin/
  - Required for modals to work properly

- [ ] **Fix modal scroll functionality**
  - Modal should scroll properly when content exceeds viewport
  - Check: `wedding/templates/wedding/our_story.html` modal styles
  - May need to add overflow scrolling to modal container

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
- **Our Story Issue**: Currently using Bootstrap grid classes but no Bootstrap CSS loaded
- **StoryEntry Database**: 0 entries currently - need to add via admin

---

**Progress Tracker**:

- ✅ URL rewiring complete
- ✅ JavaScript API fix complete
- ✅ Navigation links fixed (desktop + mobile)
- ✅ Settings/config cleanup complete
- ✅ "Our Story" grid layout complete (responsive TailwindCSS grid)
- ✅ RSVP removed from settings (files kept in codebase)
- ✅ Local testing complete
- 🔄 Content & functionality work in progress
- ⏳ Deployment pending (after content complete)
