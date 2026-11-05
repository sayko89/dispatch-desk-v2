---
name: Nocturnal Dispatch Console
colors:
  surface: '#051131'
  surface-dim: '#051131'
  surface-bright: '#2d3859'
  surface-container-lowest: '#010c2c'
  surface-container-low: '#0e1a3a'
  surface-container: '#131e3e'
  surface-container-high: '#1e2849'
  surface-container-highest: '#293355'
  on-surface: '#dbe1ff'
  on-surface-variant: '#e6bcbd'
  inverse-surface: '#dbe1ff'
  inverse-on-surface: '#242f50'
  outline: '#ad8888'
  outline-variant: '#5d3f40'
  surface-tint: '#ffb3b5'
  primary: '#ffb3b5'
  on-primary: '#680019'
  primary-container: '#ff5167'
  on-primary-container: '#5b0015'
  inverse-primary: '#be0036'
  secondary: '#a3eeff'
  on-secondary: '#00363e'
  secondary-container: '#02daf7'
  on-secondary-container: '#005b68'
  tertiary: '#f7be36'
  on-tertiary: '#402d00'
  tertiary-container: '#b88900'
  on-tertiary-container: '#382700'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdada'
  primary-fixed-dim: '#ffb3b5'
  on-primary-fixed: '#40000c'
  on-primary-fixed-variant: '#920027'
  secondary-fixed: '#a3eeff'
  secondary-fixed-dim: '#02daf7'
  on-secondary-fixed: '#001f25'
  on-secondary-fixed-variant: '#004e5a'
  tertiary-fixed: '#ffdea0'
  tertiary-fixed-dim: '#f7be36'
  on-tertiary-fixed: '#261900'
  on-tertiary-fixed-variant: '#5c4300'
  background: '#051131'
  on-background: '#dbe1ff'
  surface-variant: '#293355'
  bg: '#030920'
  bg-subtle: '#06102C'
  panel: '#0A1636'
  panel-elevated: '#0F1E47'
  border-subtle: '#1A2C60'
  border-strong: '#27438A'
  text-primary: '#E9F1FF'
  text-muted: '#8598C8'
  text-dim: '#50659A'
  neon-red: '#FF2D55'
  neon-cyan: '#25E2FF'
  neon-amber: '#FFC53D'
  neon-green: '#22F0A3'
  neon-violet: '#AE8FFF'
typography:
  headline-xl:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 38px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 30px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 26px
    letterSpacing: 0em
  headline-sm:
    fontFamily: Space Grotesk
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 22px
    letterSpacing: 0.01em
  body-lg:
    fontFamily: IBM Plex Sans
    fontSize: 16px
    fontWeight: '500'
    lineHeight: 24px
  body-md:
    fontFamily: IBM Plex Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: IBM Plex Sans
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  telemetry-lg:
    fontFamily: JetBrains Mono
    fontSize: 18px
    fontWeight: '700'
    lineHeight: 22px
    letterSpacing: 0.02em
  telemetry-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: 0.01em
  telemetry-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.04em
  label-code:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '700'
    lineHeight: 12px
    letterSpacing: 0.08em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 0.75rem
  margin: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1rem
  space-xl: 1.5rem
---

# DESIGN.md · Dispatch Desk

## Concept
A hospital monitor at night. Dispatch console during a Friday night shift. Deep navy background (#030920), cards (#0A1636), neon red (#FF2D55) reserved strictly for alarms, red-code patients and primary action buttons. Cyan (#25E2FF) for system state and stations, amber (#FFC53D) for warnings/tasks, green (#22F0A3) for green codes and success. Single column, 390px mobile layout.

## Colors
- --bg: #030920
- --bg-2: #06102C
- --panel: #0A1636
- --panel-2: #0F1E47
- --line: #1A2C60
- --line-2: #27438A
- --fg: #E9F1FF
- --muted: #8598C8
- --dim: #50659A
- --red: #FF2D55
- --cyan: #25E2FF
- --amber: #FFC53D
- --green: #22F0A3
- --violet: #AE8FFF

## Typography
- Display: Chakra Petch (600, 700)
- Body: IBM Plex Sans (400, 500, 600)
- Data/Mono: JetBrains Mono (400, 500, 700)
