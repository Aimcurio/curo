---
name: curo-simulation-builder
description: Multi-agent orchestration pattern for Curo WebGL physics simulations.
---

# Curo Simulation Builder Pattern

## Orchestration Flow
When executing a Curo WebGL / 3D physics simulation kickoff brief, coordinate 4 specialized subagents concurrently:

1. **Subagent Alpha (Scaffolding & Environment):**
   - Setup Vite, TypeScript, `three`, `lil-gui`, `@types/three`.
   - Configure `tsconfig.json` (ES2020 target, bundler resolution, strict mode).
   - Create `index.html` full-screen container with inline WebGL context-lost fallback modal.

2. **Subagent Beta (Contracts & Symplectic Engine):**
   - Define canonical data contracts (`src/contracts.ts`): `Vector3D`, `CelestialBody`, `SimulationConfig`, `Preset`, `SimulationState`.
   - Implement symplectic numerical integrator (`src/physics.ts`): Velocity Verlet with fixed-timestep sub-stepping and Plummer gravitational softening.
   - Enforce zero heap allocation in tight physics loops.

3. **Subagent Gamma (GLSL Shaders & VFX):**
   - Author custom GLSL vertex & fragment shaders (`src/shaders.ts`) for GPU-based mesh displacement along the Y-axis.
   - Implement zero-allocation `Float32Array` ring-buffer trajectory trails (`src/trails.ts`) with additive blending.

4. **Subagent Delta (Presets, Scene & HUD):**
   - Formulate verified stable orbital presets (`src/presets.ts`): Sun-Earth-Moon, Binary Star, Figure-8 Choreography.
   - Assemble Three.js scene, `PerspectiveCamera`, lights, `OrbitControls` with damping, and `lil-gui` parameter panel (`src/main.ts`).
   - Implement delta time clamp ($\le 0.1\text{s}$) in the animation accumulator to eliminate tab-throttling artifacts.

## Validation & Observability
- **Validation Gate:** Execute `npm run build` to verify 0 TypeScript and bundling errors.
- **Observability Requirement:** All subagents must route execution traces, build logs, and validation artifacts to the Curo observability layer at `E:\curo`.
