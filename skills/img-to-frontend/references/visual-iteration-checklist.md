# Visual Iteration Checklist

Use this reference during image generation, detailed prompt writing, implementation, and screenshot comparison for high-fidelity website and page builds. The guidance is intentionally abstract: choose concrete visual decisions from the user's brief, not from this document's wording.

## Mandatory Image-First Gate

The workflow must start with actual image generation.

- Invoke `$imagegen` before writing any build prompt.
- Generate exactly four distinct website/page images unless the user requested a different count.
- Use built-in image generation by default, following the imagegen skill's default mode.
- Use one image-generation call per concept when possible so each direction can have a focused prompt.
- Present the four images to the user with short labels.
- Stop after the four images are shown.
- Ask the user which image to turn into the detailed build prompt.
- Do not continue to detailed prompt-writing or code until the user selects one.
- If image generation is unavailable, state the blocker and ask whether to proceed with text-only concepts. Do not silently downgrade.

## Four-Concept Generation Checklist

Each generated image direction must be meaningfully distinct and must grow from the user's brief. Do not treat this checklist as a menu of styles to copy. First infer what the site must help a visitor understand, feel, compare, choose, buy, join, learn, or do. Then create four directions that solve that communication problem through different visual systems.

For each direction, make deliberate choices across these axes:

- Structure: how the page organizes attention, sequence, navigation, hierarchy, and continuation beyond the first viewport.
- Content strategy: what information or artifact leads the experience, what supports it, and what can be delayed or compressed.
- Visual language: the relationship between imagery, interface elements, whitespace, rhythm, contrast, materiality, and brand signals.
- Typography system: the role of type in the concept, including scale, voice, hierarchy, texture, restraint, and readability.
- Color logic: how color communicates priority, mood, state, depth, affordance, and brand memory.
- Interaction model: how the page invites exploration, comparison, conversion, reading, browsing, or repeated use.
- Density and pacing: how much the user should see at once, where the layout should breathe, and where it should become efficient.
- Trust and specificity: what makes the experience credible, concrete, and fitted to this exact site rather than a generic template.

The four concepts should differ in several of these axes at once. Avoid versions that only change palette, button labels, image choices, or decorative surface treatment.

## Image Generation Prompt Pattern

Use the `$imagegen` skill's `ui-mockup` taxonomy for website and page design concepts.

Each image prompt should include:

- Use case: `ui-mockup`.
- Asset type: desktop website/page visual concept for the user's brief.
- Primary request: a complete page design for the user's purpose, audience, and goal.
- Composition/framing: straight-on desktop page view, 16:9, realistic UI, pixel-crisp.
- Style/medium: premium web design mockup with production-grade interface detail.
- Constraints: no generic template look, no crowded layout, no unreadable tiny text, no watermark.
- Differentiator: the core design decision that separates this concept from the other three, expressed as an intention rather than a copied style label.

Do not generate four prompts that only differ in adjectives. Change the underlying design strategy, hierarchy, content emphasis, interaction model, density, and brand behavior. Make them visually distinct from one another.

Refrain from creating cluttered, busy UIs with lots of SVGs and elements that will be difficult to replicate in prod.

## Detailed Build Prompt Template

When the user chooses a direction, produce a prompt with these sections:

```markdown
# Build Prompt: [Design Name]

## Goal
Build a production web page that closely matches the selected reference. This is real page UI, not a browser-window mockup and not a screenshot background.

## Canvas
- Target desktop screenshot: [width] x [height].
- Primary content max-width: [value].
- Outer padding: [value].
- Desktop composition: [major regions, proportions, and alignment relationships].
- Stack breakpoint: [value] before any overlap occurs.

## Visual Direction
[Concise art direction with tone, brand posture, and what the page should feel like.]

## Layout
[Precise grid, orientation alignment, first-read alignment, major content module placement, continuation hints, and vertical rhythm.]

## Typography
[Fonts, fallbacks, sizes, line heights, weights, tracking, uppercase rules, italic rules, and wrapping rules.]

## Color Tokens
[Named tokens with hex values and usage.]

## Components
[Inventory only the modules visible in the selected image. Describe each by purpose, hierarchy, content type, layout behavior, states, and relationship to surrounding modules.]

## Complex Visual Rules
[Rules for any structured, dense, spatial, data-rich, media-rich, or interactive visual system. Include anchors, scale behavior, state changes, stacking behavior, minimum readable sizes, and fallback layout.]

## Motion
[Specific, restrained animations and hover states.]

## Responsive Behavior
[Desktop, wide desktop, tablet, mobile rules. Include when dense modules stack or simplify.]

## Do Not
[No production browser chrome unless requested, no screenshot-as-background, no fake or flattened interface detail, no disconnected geometry, no overlapping modules, no generic template styling.]

## Acceptance Criteria
[Checklist that must be visually true before final.]
```

## Implementation Rules

- Use one canonical implementation path in the app. Do not leave duplicate pages or dead alternate components.
- Prefer CSS variables or existing token systems for all repeated values.
- Keep primary content and primary visual systems in real responsive layouts, not absolute-positioned against the viewport unless an element is intentionally decorative.
- Build marks, icons, controls, and visual details as inline SVG, CSS, HTML, or existing component primitives. Keep stroke widths, opacity, and alignment consistent.
- Build structured visuals as real UI rather than pasted screenshots.
- If the selected design includes linked or anchored elements, do not place relationship geometry in a separate fixed-size layer while the related elements move with fluid layout.
- When using SVG for spatial systems, use a stable `viewBox`, percentage-aware positions, and coordinates derived from the same layout model.
- If a visual system mixes HTML elements with SVG geometry, either make the whole system a scaled coordinate plane or calculate anchors from the rendered elements.
- Use `clamp()` for large text and complex visual scale where it preserves readability.
- Use container queries or breakpoints so dense modules shrink before they stack.
- Stack or simplify dense modules before their internal elements overlap.
- Prefer earlier stacking over unreadable or colliding UI.

## Screenshot Comparison Loop

At each loop, capture the current page and compare it against the target reference.

Check in this order:

- Page frame: background tone, outer padding, content max-width, viewport balance, and continuation beyond the first view.
- Global structure: navigation or orientation system, primary action placement, section boundaries, and alignment between major regions.
- Primary message: first-read content alignment, scale, line breaks, rhythm, supporting copy width, and relationship to action elements.
- Credibility and context: proof, metadata, attribution, status, or reassurance modules with the right weight, spacing, and proximity.
- Primary visual system: size, crop, aspect ratio, containment, border treatment, depth, internal spacing, and relationship to surrounding content.
- Repeated modules: item sizing, media ratio, text grouping, metadata placement, state treatment, and consistent rhythm.
- Input or transaction modules: control sizing, affordance clarity, validation states, supporting details, and trust cues.
- Dense or spatial systems: shell size, internal hierarchy, relationship geometry, labels, anchors, states, and legibility.
- Responsive states: wide desktop, reference desktop, constrained desktop, tablet, mobile.

Only change one major mismatch category per iteration when possible. Re-screenshot after structural changes.

## Responsive Complex-UI Rules

For dense, spatial, repeated, media-rich, data-rich, or task-heavy modules:

- Wide desktop: use available horizontal space without stretching typography beyond the reference mood.
- Standard desktop: maintain multi-column or side-by-side layout only if the visual module remains readable and internal elements do not overlap.
- Constrained desktop: shrink module scale, label size, media ratio, and padding within readable bounds.
- Before overlap: stack or simplify the module earlier than usual. Do not wait until mobile if geometry breaks around tablet or small desktop widths.
- Mobile: simplify the module, stack items vertically, reduce density, or replace an unreadable complex visual with a readable summary when needed.

Minimum complex-visual standards:

- Anchored geometry touches the elements it belongs to when anchors are present.
- Markers, labels, and relationship cues sit on the intended path or target rather than drifting as the layout changes.
- Curved, routed, or spatial relationships scale with the elements they describe.
- Text remains readable at the smallest supported multi-column width.
- No labels truncate unless intentionally abbreviated.

## Common Corrections

- If everything feels bunched, reduce component scale, module padding, font sizes, or internal gaps before increasing the whole section size.
- If the primary visual system feels too small on a large monitor, increase the relevant container or module width rather than only enlarging text.
- If a layout region leaves an unintended gap before the main visual focus, adjust region proportions and primary typography together.
- If first-read text becomes too large after a scale correction, back it off halfway rather than returning to the original small size.
- If orientation elements feel detached, align their container to the same max-width and edges as the page content.
- If a small marker or label causes misalignment, remove it or account for it with a separate non-layout decoration.
- If repeated module content feels separated by a hole, tighten the primary grouping, then place secondary information in a consistent supporting position.
- If state or metadata rows are noisy, reduce repetition and make the primary signal easier to scan.

## Final QA

Before closing out:

- The page is real UI, not an embedded screenshot.
- The browser chrome from a design mockup is not implemented unless explicitly requested.
- The selected reference direction is clearly recognizable.
- Layout aligns at the target viewport.
- Wide desktop does not waste most of the screen.
- Dense modules do not overlap while resizing.
- Connectors, anchors, labels, and other relationship geometry stay attached while resizing when those elements exist.
- Mobile has a deliberate stacked or simplified layout.
- Fonts load correctly or have intentional fallbacks.
- Buttons and controls are clickable and accessible.
- Color contrast is acceptable for core text and controls.
- Build/lint/typecheck or the closest available checks were run.
