---
skill: frontend-design
version: 1.0
applies-to: coder, reviewer
activates-when: PRD mentions "design", "UI", "UX", "visual", "layout", "typography", "color", "responsive", "mobile", "accessibility", or "interface"
---

# Frontend Design Skill

## Domain Overview

Frontend design covers visual hierarchy, layout systems, typography, colour, spacing, and interaction states. The domain is distinct from frontend engineering because correctness here means visual consistency, accessibility, and perceived performance — not just working code. A general-purpose agent will often produce functional UIs that feel generic, ignore accessible contrast ratios, use arbitrary spacing values, and fail to communicate loading or error states visually.

---

## Core Principles

**1. Design with a system, not with values.**
All spacing, typography, and colour values come from a defined scale (e.g. Tailwind's default scale, or a custom design token set). No arbitrary pixel values. Violation: `margin: 13px` or `font-size: 15px` inline in a component.

**2. Every interactive element has four states.**
Default, hover, active/pressed, and disabled — all four must be styled. Focus must also be visible for keyboard users. Violation: a button component with only a default and hover state, invisible focus ring removed with `outline: none`.

**3. Visual hierarchy is achieved through contrast, size, and weight — not decoration.**
Important elements are larger, heavier, or higher-contrast. Decoration (borders, shadows, background fills) is added only when it serves a structural purpose. Violation: adding a box shadow to every card "to make it look nice" rather than to indicate elevation or interactivity.

**4. Spacing follows a consistent scale.**
Use 4px (or 8px) as the base unit. All spacing values are multiples: 4, 8, 12, 16, 24, 32, 48, 64. Nothing in between. Violation: a layout with gaps of 10px, 15px, and 20px that each come from separate decisions.

**5. Colour communicates meaning, not just style.**
Red = error/destructive, Yellow = warning, Green = success, Blue = info/interactive. These associations must be consistent throughout the app. Violation: using green for a destructive delete button because it "looks better" there.

**6. Responsive design is mobile-first.**
Write base styles for mobile, then add breakpoint overrides for larger screens. Never write desktop styles and patch mobile. Violation: a layout that works on desktop and has a `@media (max-width: 768px)` patch that makes it "fit" on mobile.

**7. Accessibility is not optional.**
Minimum contrast ratio: 4.5:1 for body text, 3:1 for large text and UI components. All images have `alt` text. All interactive elements are keyboard-reachable and have a visible focus state. Form inputs have associated `<label>` elements. Violation: grey text on a light background that fails WCAG AA.

---

## Procedural Knowledge

### How to Build a Component Visually

1. **Start with structure** — lay out the component with semantic HTML before adding any visual styling
2. **Apply spacing** — set padding and margins using the spacing scale
3. **Set typography** — size, weight, line-height, colour from the type scale
4. **Add colour** — background, border, text colours from the colour palette
5. **Handle states** — hover, focus, active, disabled
6. **Test at breakpoints** — mobile (375px), tablet (768px), desktop (1280px)
7. **Check accessibility** — contrast ratio, keyboard navigation, screen reader semantics

### Typography Scale

Use a modular type scale with consistent steps. Example (Tailwind):

| Role | Class | Size | Weight | Line Height |
|------|-------|------|--------|-------------|
| Display | `text-4xl font-bold` | 36px | 700 | 1.2 |
| Heading 1 | `text-2xl font-semibold` | 24px | 600 | 1.3 |
| Heading 2 | `text-xl font-semibold` | 20px | 600 | 1.4 |
| Body | `text-base font-normal` | 16px | 400 | 1.5 |
| Small / Caption | `text-sm font-normal` | 14px | 400 | 1.5 |
| Label | `text-xs font-medium` | 12px | 500 | 1.4 |

Never use more than 3 font sizes on a single screen.

### Colour System

Structure every colour palette in three layers:

```
Primitive tokens (raw values):
  blue-500: #3B82F6

Semantic tokens (meaning-mapped):
  color-primary:     blue-500
  color-destructive: red-600
  color-success:     green-600
  color-warning:     yellow-500
  color-text:        gray-900
  color-text-muted:  gray-500
  color-border:      gray-200
  color-surface:     white
  color-surface-alt: gray-50

Component tokens (optional, for complex systems):
  button-primary-bg: color-primary
```

Always reference semantic tokens in component code, never primitives directly.

### How to Design Feedback States

Every user action that takes time or can fail must have visual feedback:

| State | Visual Treatment |
|-------|-----------------|
| Loading | Skeleton screen (preferred) or spinner; disable interactive elements |
| Success | Brief inline confirmation (green checkmark / text); auto-dismiss after 3s |
| Error | Inline error message in red near the source; persist until resolved |
| Empty | Illustrated empty state with a clear call-to-action |
| Disabled | Reduced opacity (50–60%); `cursor-not-allowed`; no hover effects |

Never use a loading spinner for operations expected to take < 300ms — it causes visual flicker.

### Responsive Layout Patterns

```
Single column (mobile default):
  flex flex-col gap-4

Two columns at md:
  grid grid-cols-1 md:grid-cols-2 gap-6

Sidebar layout:
  flex flex-col md:flex-row
  sidebar: w-full md:w-64 shrink-0
  content: flex-1 min-w-0  ← min-w-0 prevents flex overflow

Card grid:
  grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4
```

`min-w-0` on flex children is required to prevent content overflow — a common missed detail.

---

## Patterns & Anti-Patterns

```
PATTERN: Skeleton loading over spinners
Context: Content that loads asynchronously (lists, profile data, dashboards)
✅ DO: Render grey placeholder shapes matching the content layout during load
❌ DON'T: Show a centred spinner that causes layout shift when content arrives
Reason: Skeletons preserve layout and perceived performance; spinners create jarring shifts
```

```
PATTERN: Semantic colour tokens
Context: All colour usage in components
✅ DO: bg-destructive text-destructive-foreground (semantic)
❌ DON'T: bg-red-600 text-white (primitive)
Reason: Semantic tokens make dark mode, rebranding, and theme changes a one-line change
```

```
PATTERN: Focus-visible over focus
Context: Keyboard accessibility
✅ DO: focus-visible:ring-2 focus-visible:ring-primary (shows only for keyboard)
❌ DON'T: focus:outline-none (removes focus entirely) or focus:ring-2 (shows on mouse click too)
Reason: focus-visible matches browser behaviour: visible for keyboard, hidden for mouse
```

```
PATTERN: Compound components for complex UI
Context: Tabs, dropdowns, modals, accordions
✅ DO: <Tabs><TabList><Tab /><Tab /></TabList><TabPanels>...</TabPanels></Tabs>
❌ DON'T: A single <Tabs items={[...]} renderContent={...} /> with everything in props
Reason: Compound components let consumers control layout and composition without forking
```

```
PATTERN: Icon + label, never icon alone
Context: Action buttons, navigation items
✅ DO: <button><Icon /><span>Delete</span></button> (or aria-label if label is visually hidden)
❌ DON'T: <button><TrashIcon /></button> with no accessible label
Reason: Icons are ambiguous; screen readers and unfamiliar users need the text label
```

---

## Integration Points

- **Feeds into:** `src/features/[feature]/components/`, design token file (`src/styles/tokens.css` or `tailwind.config.ts`)
- **Depends on:** `frontend` skill (component structure and state management)
- **Conflicts with:** none — but design decisions (colour, spacing scale) must be defined once in a shared token file and not duplicated per component
- **Reviewer focus:** arbitrary spacing/colour values, missing interaction states, colour used without semantic meaning, missing focus styles, accessibility violations

---

## Review Checklist

- [ ] All spacing values are multiples of 4px (or 8px) — no arbitrary values
- [ ] All colours reference semantic tokens, not primitive values
- [ ] All interactive elements have hover, focus, active, and disabled states
- [ ] Focus styles are visible and use `focus-visible` (not removed with `outline: none`)
- [ ] Text contrast ratio meets WCAG AA (4.5:1 for body, 3:1 for large text)
- [ ] All images have meaningful `alt` text (or `alt=""` for decorative images)
- [ ] All form inputs have an associated `<label>` (visible or visually hidden)
- [ ] Loading states use skeleton screens or appropriate feedback (no unhandled loading)
- [ ] Empty states have a message and a call-to-action
- [ ] Error states are inline, in red, near the source — not only in a toast
- [ ] Layout is mobile-first; responsive breakpoints tested at 375px, 768px, 1280px
- [ ] No hardcoded `px` values for font sizes — use scale classes
- [ ] Icon-only buttons have an `aria-label`
