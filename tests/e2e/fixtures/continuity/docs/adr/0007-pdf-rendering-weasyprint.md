# ADR-0007: Render quote PDFs with WeasyPrint, A4, RTL-aware

Status: accepted

## Context
Customers need quotes as PDF. Arabic quotes must render right-to-left with an embedded Arabic font.

## Decision
Use WeasyPrint with HTML templates. Page size A4. Templates set `dir="rtl"` when the quote
language is Arabic. Fonts are embedded, never referenced from the system.

## Consequences
WeasyPrint is a system dependency in the container image. Font files ship in `app/fonts/`.
