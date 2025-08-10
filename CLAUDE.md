# RSVP Flow Styling Guidelines

This document provides comprehensive styling guidelines for the wedding RSVP application to ensure visual consistency across all pages and components.

## Color Palette

The RSVP flow uses a cohesive pink/rose color scheme with these specific hex values:

### CSS Custom Properties
```css
:root {
  /* Primary Colors */
  --primary-dark: #b22158;      /* Main headings, search text */
  --primary-medium: #d46b8c;    /* Secondary headings, celebration text */
  --primary-light: #ebb6c2;     /* Buttons, accents */
  --primary-pale: #eed4e2;      /* Background boxes, containers */
  
  /* Neutral Colors */
  --white: #ffffff;             /* Alternative background */
  --text-dark: #333333;         /* Body text */
  --text-muted: #666666;        /* Helper text */
}
```

### Color Usage Guidelines

| Element | Color | Hex Code | CSS Variable |
|---------|--------|----------|--------------|
| **Save the Date Modal** |
| "Save the Date!" title | Primary Dark | #b22158 | `var(--primary-dark)` |
| "Watch Kelly & John's..." subtitle | Primary Medium | #d46b8c | `var(--primary-medium)` |
| "Close this window..." text | Primary Medium | #d46b8c | `var(--primary-medium)` |
| X close button | Primary Light | #ebb6c2 | `var(--primary-light)` |
| Modal background | Primary Pale or White | #eed4e2 / #ffffff | `var(--primary-pale)` or `var(--white)` |
| **RSVP Pages** |
| "We can't wait to celebrate..." | Primary Medium | #d46b8c | `var(--primary-medium)` |
| "Who's RSVPing?" headers | Primary Dark | #b22158 | `var(--primary-dark)` |
| Text box outlines | Primary Medium | #d46b8c | `var(--primary-medium)` |
| Search text | Primary Dark | #b22158 | `var(--primary-dark)` |
| Search button background | Primary Light | #ebb6c2 | `var(--primary-light)` |
| Page background containers | Primary Pale or White | #eed4e2 / #ffffff | `var(--primary-pale)` or `var(--white)` |
| Overall page background | Primary Dark | #b22158 | `var(--primary-dark)` |

## Typography

### Font Families
- **Primary Font**: 'Lora', serif - Used for all body text, forms, and general content
- **Celebration Font**: 'Beth Ellen', cursive - Used specifically for celebration text "We can't wait to celebrate with you!"

### Font Imports
```css
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600&family=Beth+Ellen&display=swap');
```

### Typography Scale
```css
/* Celebration Text - Beth Ellen */
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

/* Primary Headings - Lora */
h1, .modal-title {
  font-family: 'Lora', serif;
  color: var(--primary-dark);
  font-size: 1.75rem;
  font-weight: normal;
  margin-bottom: 2rem;
}

/* Secondary Headings - Lora */
h2 {
  font-family: 'Lora', serif;
  color: var(--primary-dark);
  font-size: 1.75rem;
  font-weight: normal;
  margin-bottom: 2rem;
}

/* Subtitle Text - Lora */
.modal-subtitle, .subtitle {
  font-family: 'Lora', serif;
  color: var(--primary-medium);
  font-size: 1.125rem;
  margin-bottom: 2rem;
}

/* Body Text - Lora */
p, .body-text {
  font-family: 'Lora', serif;
  color: var(--text-dark);
  font-size: 1.25rem;
  margin-bottom: 1rem;
}
```

## Component Styling Guidelines

### Save the Date Modal
```css
/* Modal container with primary pale background */
.modal-container {
  background-color: var(--primary-pale); /* or var(--white) */
  border-radius: 1rem;
  padding: 2rem;
}

/* Title styling */
.modal-title {
  color: var(--primary-dark);
  font-family: 'Lora', serif;
  font-size: 2rem;
}

/* Subtitle styling */
.modal-subtitle {
  color: var(--primary-medium);
  font-family: 'Lora', serif;
  font-size: 1.125rem;
}

/* Close button */
.modal-close-btn {
  background-color: var(--primary-light);
  color: white;
  border: none;
  border-radius: 50%;
  width: 3rem;
  height: 3rem;
}

/* Instructional text */
.modal-instruction {
  color: var(--primary-medium);
  font-family: 'Lora', serif;
}
```

### RSVP Page Elements
```css
/* Celebration text - Beth Ellen font */
.celebration-text {
  color: var(--primary-medium);
  font-family: 'Beth Ellen', cursive;
  font-size: 1.25rem;
  margin-bottom: 1.5rem;
}

/* Main headings */
.rsvp-heading {
  color: var(--primary-dark);
  font-family: 'Lora', serif;
  font-size: 1.75rem;
  font-weight: normal;
}

/* Form containers */
.form-container {
  background-color: var(--white);
  border-radius: 1.5rem;
  padding: 3rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Input fields */
.form-input {
  border: 2px solid var(--primary-medium);
  background-color: var(--white);
  font-family: 'Lora', serif;
  border-radius: 0.375rem;
  padding: 0.75rem 1rem;
}

.form-input:focus {
  border-color: var(--primary-dark);
  box-shadow: 0 0 0 3px rgba(212, 107, 140, 0.2);
}

/* Search/Submit buttons */
.btn-search {
  background-color: var(--primary-light);
  color: var(--text-dark);
  font-family: 'Lora', serif;
  border: none;
  border-radius: 1.5rem;
  padding: 0.75rem 2rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
```

### Background Treatments
```css
/* Page background */
body.rsvp-page {
  background-color: var(--primary-dark);
  background-image: url('/static/images/backgrounds/rsvp.png');
  font-family: 'Lora', serif;
}

/* Container backgrounds */
.content-container {
  background-color: var(--primary-pale); /* or var(--white) */
  border-radius: 1.5rem;
  padding: 3rem;
}
```

## Responsive Design

### Breakpoints
- Mobile: up to 576px
- Tablet: 577px - 768px  
- Desktop: 768px and above

### Mobile-Specific Adjustments
```css
@media (max-width: 576px) {
  .celebration-text {
    font-size: 1.25rem;
  }
  
  .modal-title, .rsvp-heading {
    font-size: 1.5rem;
  }
  
  .form-container {
    padding: 2rem;
  }
}
```

### Desktop-Specific Adjustments
```css
@media (min-width: 768px) {
  .celebration-text {
    font-size: 3rem;
  }
  
  .container {
    max-width: 1100px;
  }
}
```

## Implementation Notes

### Integration with Existing CSS
1. Add the CSS custom properties to the top of `rsvp_style.css`
2. Import the Beth Ellen font alongside the existing Lora import
3. Replace hardcoded hex values with CSS variables throughout existing styles
4. Apply Beth Ellen font specifically to celebration text elements

### Font Loading
```css
@import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600&family=Beth+Ellen&display=swap');
```

### CSS Variable Usage Example
```css
/* Instead of: */
color: #b22158;

/* Use: */
color: var(--primary-dark);
```

### Accessibility Considerations
- Maintain sufficient color contrast ratios
- Ensure text remains readable on all background combinations
- Test font legibility at various sizes, especially Beth Ellen for celebration text

## Quick Reference

### Most Common Elements
- **Main titles**: `color: var(--primary-dark)` + `font-family: 'Lora', serif`
- **Celebration text**: `color: var(--primary-medium)` + `font-family: 'Beth Ellen', cursive`
- **Subtitles**: `color: var(--primary-medium)` + `font-family: 'Lora', serif`
- **Form borders**: `border-color: var(--primary-medium)`
- **Buttons**: `background-color: var(--primary-light)`
- **Containers**: `background-color: var(--primary-pale)` or `var(--white)`

This style guide ensures consistent visual identity across the entire RSVP flow while providing flexibility for future development and maintenance.