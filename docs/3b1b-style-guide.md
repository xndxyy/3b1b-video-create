# 3Blue1Brown Visual Style Guide

Adopt 3B1B's look: dark canvas, restrained color, geometric clarity, motion that *explains* rather than decorates.

## Canvas & color

- Background `#111111` (or `#171717`), never pure black for the whole frame.
- Faint `GREY_E #222222` panels for grouping.
- Text `#DDDDDD` primary, `#BBBBBB` secondary. Avoid pure white.
- Connectors / axes `#888888` at 0.35–0.7 alpha.
- Strong semantic colors (≤3 on screen at once):
  - `BLUE #58C4DD` — primary concept, neuron, main curve
  - `GOLD #F0AC5F` — key conclusion, highlighted path
  - `GREEN #83C167` — correct / activated / pass
  - `RED #FC6255` — error / limit / counter-example
  - `PURPLE #9A72AC` — hidden layer / intermediate
  - `TEAL #5CD0B3` — auxiliary / data flow

## Motion principles

1. **Motion = meaning.** Animate the math itself: numbers transform, lines rotate, decision boundaries sweep.
2. **One idea at a time.** Don't pile 5 animations. Reveal sequentially.
3. **Easing.** Use smooth ease-in-out; avoid linear jumps for conceptual reveals.
4. **Glow over saturation.** Give key objects a subtle stroke / semi-transparent duplicate rather than cranking saturation.
5. **Hold & breathe.** After a reveal, hold 0.5–1.0s before the next beat so the viewer parses it.
6. **Labels follow objects.** When a node moves, its label tracks it (Manim `always_redraw` / updaters).

## Composition patterns that work well here

- **Neuron → math**: show a stylized biological neuron, then morph it into the artificial `Σ → threshold` box.
- **Formula → geometry**: take `w·x + b = 0` and animate it as a sweeping line in a 2D plane.
- **Truth table → points**: map logic-gate inputs to plotted points; draw the separating line.
- **Network growth**: start with 1 perceptron, sprout layers, end on a dense abstract net (the "3B1B shot").
- **Build-up chains**: NAND → NOT → AND → half-adder → ALU → CPU, each node spawning the next.

## Anti-patterns

- Static "PPT" slides with one image held 10s. Every beat should move or transform.
- More than 3 strong colors competing.
- Pure white text on pure black (harsh, not 3B1B).
- Decorative motion with no explanatory payload.
