# 🍎 Applytune Design System
**Apple-Inspired Minimalist Design**

---

## Philosophy

Applytune's design follows Apple's design principles:
- **Clarity**: Typography and interface elements are legible at every size
- **Deference**: Fluid motion and crisp interface help focus on content
- **Depth**: Visual layers and realistic motion convey hierarchy

---

## Color Palette

### Primary Colors
```css
--primary-900: #1d1d1f  /* Apple's signature dark - headings, icons */
--primary-800: #2d2d2f  /* Hover states */
--primary-700: #434343  /* Secondary text */
--primary-500: #666666  /* Body text */
--primary-300: #a4a4a4  /* Disabled states */
--primary-100: #e3e3e3  /* Borders, dividers */
--primary-50:  #f7f7f7  /* Subtle backgrounds */
```

### Accent Colors
```css
--accent-500: #0071e3   /* Apple blue - primary actions */
--accent-600: #0077ED   /* Hover state */
--accent-700: #006edb   /* Active state */
```

### Functional Colors
```css
--success: #10b981      /* Success states */
--warning: #f59e0b      /* Warnings */
--error:   #ef4444      /* Errors */
```

### Background Colors
```css
--background:     #ffffff    /* Main background */
--surface:        #fbfbfd    /* Elevated surfaces */
--surface-subtle: #f5f5f7    /* Subtle backgrounds */
```

---

## Typography

### Font Family
```css
font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 
             'Segoe UI', system-ui, sans-serif;
```

### Type Scale

| Style | Size | Weight | Line Height | Letter Spacing | Usage |
|-------|------|--------|-------------|----------------|-------|
| **Hero** | 3.5rem (56px) | 600 | 1.1 | -0.015em | Landing page headlines |
| **Display** | 2.5rem (40px) | 600 | 1.2 | -0.01em | Section headings |
| **Heading 1** | 2rem (32px) | 600 | 1.3 | -0.01em | Page titles |
| **Heading 2** | 1.5rem (24px) | 600 | 1.4 | -0.005em | Card titles |
| **Heading 3** | 1.25rem (20px) | 500 | 1.4 | 0 | Subsection titles |
| **Body Large** | 1.125rem (18px) | 400 | 1.6 | 0 | Lead paragraphs |
| **Body** | 1rem (16px) | 400 | 1.6 | 0 | Body text |
| **Body Small** | 0.875rem (14px) | 400 | 1.5 | 0 | Secondary text |
| **Caption** | 0.75rem (12px) | 400 | 1.4 | 0.02em | Labels, captions |
| **Overline** | 0.625rem (10px) | 500 | 1.2 | 0.1em | Uppercase labels |

### Font Weights
- **Light**: 300 - Descriptive text, subtle emphasis
- **Regular**: 400 - Body text
- **Medium**: 500 - Buttons, labels
- **Semibold**: 600 - Headings

---

## Spacing System

Apple uses generous whitespace. Our 8px base unit:

```
4px  = 0.25rem  = space-1
8px  = 0.5rem   = space-2
12px = 0.75rem  = space-3
16px = 1rem     = space-4
24px = 1.5rem   = space-6
32px = 2rem     = space-8
48px = 3rem     = space-12
64px = 4rem     = space-16
96px = 6rem     = space-24
```

### Common Spacing Patterns
- **Component padding**: 24px - 32px
- **Section padding**: 48px - 96px
- **Element gaps**: 16px - 24px
- **Line spacing**: 1.5 - 1.6 (generous)

---

## Border Radius

```css
--radius-sm:   0.5rem   (8px)   /* Small elements */
--radius-md:   0.75rem  (12px)  /* Cards, inputs */
--radius-lg:   1rem     (16px)  /* Large cards */
--radius-xl:   1.5rem   (24px)  /* Hero sections */
--radius-2xl:  2rem     (32px)  /* Special elements */
--radius-full: 9999px           /* Pills, buttons */
```

---

## Shadows

Subtle, elevated shadows following Apple's aesthetic:

```css
/* Apple shadow - subtle elevation */
--shadow-apple: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 
                0 2px 4px -1px rgba(0, 0, 0, 0.03);

/* Apple shadow large - cards */
--shadow-apple-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 
                   0 4px 6px -2px rgba(0, 0, 0, 0.03);

/* Apple shadow extra large - modals */
--shadow-apple-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 
                   0 10px 10px -5px rgba(0, 0, 0, 0.02);
```

---

## Buttons

### Primary Button
```css
.btn-primary {
  background: #1d1d1f;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 980px;  /* Pill shape */
  font-weight: 500;
  font-size: 1rem;
  letter-spacing: -0.01em;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-primary:hover {
  background: #2d2d2f;
  transform: translateY(-1px);
}
```

### Secondary Button
```css
.btn-secondary {
  background: transparent;
  color: #0071e3;
  padding: 0.75rem 1.5rem;
  border-radius: 980px;
  border: 1.5px solid #0071e3;
  font-weight: 500;
}

.btn-secondary:hover {
  background: #0071e3;
  color: white;
}
```

---

## Cards

### Standard Card
```css
.card {
  background: white;
  border: 1px solid #e3e3e3;
  border-radius: 1.5rem;  /* 24px */
  padding: 2rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.04);
}
```

### Glass Effect (Header)
```css
.glass {
  background: rgba(255, 255, 255, 0.72);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
}
```

---

## Inputs

### Text Input
```css
.input {
  width: 100%;
  padding: 0.875rem 1rem;
  border-radius: 0.75rem;  /* 12px */
  border: 1px solid #e3e3e3;
  background: white;
  color: #1d1d1f;
  font-weight: 300;  /* Light */
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.input:hover {
  border-color: #c8c8c8;
}

.input:focus {
  outline: 2px solid #1d1d1f;
  outline-offset: 3px;
  border-color: transparent;
}

.input::placeholder {
  color: #a4a4a4;
}
```

---

## Animation

### Timing Functions
```css
--ease-apple: cubic-bezier(0.4, 0, 0.2, 1);  /* Standard */
--ease-in: cubic-bezier(0.4, 0, 1, 1);       /* Entering */
--ease-out: cubic-bezier(0, 0, 0.2, 1);      /* Exiting */
```

### Animation Durations
```css
--duration-fast: 200ms;     /* Small interactions */
--duration-base: 300ms;     /* Standard transitions */
--duration-slow: 500ms;     /* Page transitions */
```

### Common Animations
```css
/* Fade in */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

/* Slide up */
@keyframes slideUp {
  from { 
    transform: translateY(30px);
    opacity: 0;
  }
  to { 
    transform: translateY(0);
    opacity: 1;
  }
}

/* Scale in */
@keyframes scaleIn {
  from {
    transform: scale(0.95);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}
```

---

## Layout

### Container Widths
```css
--container-sm: 640px   /* Mobile-first */
--container-md: 768px   /* Tablet */
--container-lg: 1024px  /* Desktop */
--container-xl: 1280px  /* Wide desktop */
--container-2xl: 1536px /* Ultra wide */
```

### Content Max Width
```
Main content: 1152px (max-w-6xl)
Reading content: 672px (max-w-2xl)
Form content: 768px (max-w-3xl)
```

### Padding
```css
/* Mobile */
padding: 1.5rem;  /* 24px */

/* Desktop */
padding: 2rem;    /* 32px */
```

---

## Icons

- **Size**: 16px, 20px, 24px (consistent with 4px grid)
- **Stroke width**: 2px (medium)
- **Style**: Lucide icons (clean, minimal)
- **Color**: Inherit from parent or use primary-900

---

## Best Practices

### Do's ✅
- Use generous whitespace
- Keep interfaces clean and minimal
- Use subtle shadows and transitions
- Stick to the type scale
- Use pill-shaped buttons (border-radius: 980px)
- Maintain 1.5-1.6 line height for readability
- Use font-weight: 300 (light) for body text
- Keep animations smooth (300ms default)

### Don'ts ❌
- Don't use bright, saturated colors
- Avoid heavy drop shadows
- Don't use multiple accent colors
- Avoid decorative elements
- Don't use complex gradients
- Avoid small, cramped spacing
- Don't use font sizes outside the scale
- Avoid fast, jarring animations

---

## Component Examples

### Hero Section
```tsx
<section className="py-24 px-6">
  <h1 className="text-hero font-semibold text-primary-900 mb-6 tracking-tight">
    Land more interviews with<br />
    <span className="text-gray-600">AI-optimized resumes</span>
  </h1>
  <p className="text-xl text-gray-500 font-light leading-relaxed">
    Fine-tune your resume for every job.
  </p>
</section>
```

### Card
```tsx
<div className="bg-white rounded-3xl shadow-apple-lg border border-gray-100 p-10">
  <h3 className="text-2xl font-semibold text-primary-900 mb-3 tracking-tight">
    Card Title
  </h3>
  <p className="text-gray-500 font-light">
    Card description goes here.
  </p>
</div>
```

---

**This design system ensures Applytune maintains Apple's premium, minimalist aesthetic throughout the application.** 🍎
