"""
CertLedger Presentation Deck Generator
Generates an executive, highly-styled 16:9 widescreen PowerPoint presentation (.pptx)
for the Academic Certificate Verification System.
"""

import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path="CertLedger_Academic_Presentation.pptx"):
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette Definitions
    C_NAVY_DARK    = RGBColor(15, 23, 42)     # #0F172A (Deep Slate/Navy)
    C_CARD_DARK    = RGBColor(30, 41, 59)     # #1E293B (Dark Slate Card)
    C_BG_LIGHT     = RGBColor(248, 250, 252)  # #F8FAFC (Ultra light slate bg)
    C_WHITE        = RGBColor(255, 255, 255)  # #FFFFFF
    C_BORDER_LIGHT = RGBColor(226, 232, 240)  # #E2E8F0 (Subtle border)
    C_BORDER_DARK  = RGBColor(51, 65, 85)     # #334155
    C_BLUE_PRIMARY = RGBColor(37, 99, 235)    # #2563EB (Vibrant Ethereum Blue)
    C_BLUE_LIGHT   = RGBColor(239, 246, 255)  # #EFF6FF (Soft Blue)
    C_INDIGO       = RGBColor(79, 70, 229)    # #4F46E5 (Indigo)
    C_EMERALD      = RGBColor(16, 185, 129)   # #10B981 (Verified Green)
    C_EMERALD_BG   = RGBColor(236, 253, 245)  # #ECFDF5 (Soft Green)
    C_AMBER        = RGBColor(245, 158, 11)   # #F59E0B (Warning/Notice)
    C_AMBER_BG     = RGBColor(254, 243, 199)  # #FEF3C7
    C_ROSE         = RGBColor(239, 68, 68)    # #EF4444 (Revoked/Alert)
    C_ROSE_BG      = RGBColor(254, 242, 242)  # #FEF2F2
    C_TEXT_DARK    = RGBColor(15, 23, 42)     # #0F172A
    C_TEXT_BODY    = RGBColor(51, 65, 85)     # #334155
    C_TEXT_MUTED   = RGBColor(100, 116, 139)  # #64748B
    C_TEXT_LIGHT   = RGBColor(241, 245, 249)  # #F1F5F9

    def set_slide_background(slide, color):
        bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = color
        bg_shape.line.color.rgb = color
        return bg_shape

    def add_header(slide, title, category="ACADEMIC PROJECT DEFENSE • BLOCKCHAIN VERIFICATION", is_dark=False):
        # Category Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf = cat_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = category.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = C_BLUE_PRIMARY if not is_dark else RGBColor(96, 165, 250)

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.7), Inches(0.65))
        tf2 = title_box.text_frame
        tf2.word_wrap = True
        tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
        p2 = tf2.paragraphs[0]
        p2.text = title
        p2.font.size = Pt(22)
        p2.font.bold = True
        p2.font.color.rgb = C_TEXT_LIGHT if is_dark else C_TEXT_DARK

        # Top Accent Divider Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.42), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = C_BORDER_DARK if is_dark else C_BORDER_LIGHT
        line.line.color.rgb = C_BORDER_DARK if is_dark else C_BORDER_LIGHT

    def add_card(slide, left, top, width, height, bg_color=C_WHITE, border_color=C_BORDER_LIGHT):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1)
        return shape

    def set_speaker_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        text_frame = notes_slide.notes_text_frame
        text_frame.text = notes_text

    # =========================================================================
    # SLIDE 1: Title Slide (Dark Theme)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, C_NAVY_DARK)

    # Decorative background glow accents
    accent_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(0.15), Inches(3.8))
    accent_bar.fill.solid()
    accent_bar.fill.fore_color.rgb = C_BLUE_PRIMARY
    accent_bar.line.color.rgb = C_BLUE_PRIMARY

    # Badge: System Tag
    badge = add_card(s1, Inches(1.2), Inches(1.8), Inches(3.2), Inches(0.4), bg_color=RGBColor(30, 41, 59), border_color=C_BLUE_PRIMARY)
    tf = badge.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.text = "DECENTRALIZED CREDENTIAL SYSTEM"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(147, 197, 253)
    p.alignment = PP_ALIGN.CENTER

    # Title & Subtitle Box
    t_box = s1.shapes.add_textbox(Inches(1.2), Inches(2.35), Inches(11.0), Inches(2.2))
    tf = t_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p = tf.paragraphs[0]
    p.text = "CertLedger"
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    p2 = tf.add_paragraph()
    p2.text = "Blockchain-Based Academic Certificate Verification System"
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = RGBColor(96, 165, 250)

    p3 = tf.add_paragraph()
    p3.text = "A Tamper-Evident Hybrid Platform Combining Ethereum Smart Contracts, Deterministic SHA-256 Fingerprinting & Zero-PII Architecture"
    p3.font.size = Pt(13)
    p3.font.color.rgb = RGBColor(148, 163, 184)
    p3.space_before = Pt(8)

    # 3 Key Architecture Highlights
    col_w = Inches(3.64)
    c1 = add_card(s1, Inches(1.2), Inches(4.8), col_w, Inches(1.8), bg_color=C_CARD_DARK, border_color=C_BORDER_DARK)
    tf1 = c1.text_frame
    tf1.margin_left = tf1.margin_right = Inches(0.2)
    tf1.margin_top = Inches(0.2)
    p = tf1.paragraphs[0]
    p.text = "⛓️ Hybrid On-Chain Design"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p_sub = tf1.add_paragraph()
    p_sub.text = "Solidity Smart Contract on Ethereum EVM anchors cryptographic digests with zero student PII on public ledgers."
    p_sub.font.size = Pt(10.5)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_before = Pt(4)

    c2 = add_card(s1, Inches(5.04), Inches(4.8), col_w, Inches(1.8), bg_color=C_CARD_DARK, border_color=C_BORDER_DARK)
    tf2 = c2.text_frame
    tf2.margin_left = tf2.margin_right = Inches(0.2)
    tf2.margin_top = Inches(0.2)
    p = tf2.paragraphs[0]
    p.text = "🛡️ Cryptographic Integrity"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p_sub = tf2.add_paragraph()
    p_sub.text = "SHA-256 avalanche effect guarantees single-byte tamper detection. Instant zero-gas public verification in <2 seconds."
    p_sub.font.size = Pt(10.5)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_before = Pt(4)

    c3 = add_card(s1, Inches(8.88), Inches(4.8), col_w, Inches(1.8), bg_color=C_CARD_DARK, border_color=C_BORDER_DARK)
    tf3 = c3.text_frame
    tf3.margin_left = tf3.margin_right = Inches(0.2)
    tf3.margin_top = Inches(0.2)
    p = tf3.paragraphs[0]
    p.text = "🚀 Production Tech Stack"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p_sub = tf3.add_paragraph()
    p_sub.text = "Solidity ^0.8.20, Hardhat, FastAPI, ReportLab Vector Engine, Web3.py, React 18 & Tailwind CSS."
    p_sub.font.size = Pt(10.5)
    p_sub.font.color.rgb = RGBColor(203, 213, 225)
    p_sub.space_before = Pt(4)

    # Footer Metadata
    ft_box = s1.shapes.add_textbox(Inches(1.2), Inches(6.8), Inches(11.0), Inches(0.4))
    tf = ft_box.text_frame
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "Academic Capstone Project • Final Technical Defense & System Demonstration"
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(148, 163, 184)

    set_speaker_notes(s1,
        "Good morning respected evaluators and examiners. Today I am presenting CertLedger, "
        "a decentralized, tamper-evident academic certificate verification system. "
        "Academic credential fraud is a multi-billion dollar worldwide challenge that harms universities and employers. "
        "Our system addresses this through a hybrid on-chain/off-chain architecture using Ethereum EVM smart contracts, "
        "Python FastAPI, ReportLab deterministic PDF generation, and a modern React dashboard. "
        "Crucially, our system achieves complete tamper-proofing while maintaining 100% Zero-PII compliance with privacy laws like GDPR and FERPA."
    )

    # =========================================================================
    # SLIDE 2: Problem Statement & Motivation
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, C_BG_LIGHT)
    add_header(s2, "The Problem: Flaws in Modern Academic Credential Verification")

    card_w = Inches(5.66)
    card_h = Inches(2.4)

    # Card 1: Degree Mills & Forgery
    p1 = add_card(s2, Inches(0.8), Inches(1.7), card_w, card_h)
    tf = p1.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "❌ 1. Credential Forgery & Degree Mills"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_ROSE
    bullets = [
        "Millions of counterfeit degrees and altered transcripts circulate globally.",
        "High-resolution digital graphics tools (Photoshop) enable undetectable paper & PDF forgery.",
        "Damages the academic reputation of accredited institutions and misleads employers."
    ]
    for b in bullets:
        bp = tf.add_paragraph()
        bp.text = "• " + b
        bp.font.size = Pt(11)
        bp.font.color.rgb = C_TEXT_BODY
        bp.space_before = Pt(4)

    # Card 2: Manual Friction & Delays
    p2 = add_card(s2, Inches(6.86), Inches(1.7), card_w, card_h)
    tf = p2.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "⏳ 2. Slow, Costly Manual Background Checks"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    bullets = [
        "Traditional verification takes 2 to 4 weeks via phone calls, postal mail, and emails.",
        "Commercial clearinghouses charge steep administrative fees ($15 - $50 per lookup).",
        "Imposes heavy administrative bottlenecks on university registrar departments."
    ]
    for b in bullets:
        bp = tf.add_paragraph()
        bp.text = "• " + b
        bp.font.size = Pt(11)
        bp.font.color.rgb = C_TEXT_BODY
        bp.space_before = Pt(4)

    # Card 3: The Blockchain Privacy Trap
    p3 = add_card(s2, Inches(0.8), Inches(4.35), card_w, card_h)
    tf = p3.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "🔒 3. The Public Blockchain Privacy Dilemma"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_PRIMARY
    bullets = [
        "Naive blockchain solutions store student names, grades, and IDs directly on-chain.",
        "Public ledgers are immutable, directly violating GDPR Article 17 ('Right to Erasure').",
        "Permanent exposure of educational records violates FERPA student privacy regulations."
    ]
    for b in bullets:
        bp = tf.add_paragraph()
        bp.text = "• " + b
        bp.font.size = Pt(11)
        bp.font.color.rgb = C_TEXT_BODY
        bp.space_before = Pt(4)

    # Card 4: Impossible Revocation
    p4 = add_card(s2, Inches(6.86), Inches(4.35), card_w, card_h)
    tf = p4.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "🚫 4. Permanent Fraud After Issuance (No Revocation)"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_ROSE
    bullets = [
        "Once a physical diploma or static PDF is handed to a graduate, it cannot be recalled.",
        "If degrees are later revoked due to plagiarism, fraud, or error, the revoked diploma still circulates.",
        "No decentralized registry exists where verifiers can query real-time validity status."
    ]
    for b in bullets:
        bp = tf.add_paragraph()
        bp.text = "• " + b
        bp.font.size = Pt(11)
        bp.font.color.rgb = C_TEXT_BODY
        bp.space_before = Pt(4)

    set_speaker_notes(s2,
        "To appreciate the need for CertLedger, we examine the four critical flaws in existing systems. "
        "First, fake degrees are everywhere due to photo editing tools. "
        "Second, background checks are painfully slow, taking weeks and costing tens of dollars per query. "
        "Third, many recent academic papers propose putting student records on Ethereum, but that is illegal under GDPR and FERPA "
        "because public blockchains cannot erase data. "
        "Fourth, traditional paper degrees cannot be dynamically revoked if an institution discovers academic misconduct post-graduation. "
        "CertLedger specifically solves all four problems simultaneously."
    )

    # =========================================================================
    # SLIDE 3: The CertLedger Solution & Value Proposition
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, C_BG_LIGHT)
    add_header(s3, "The CertLedger Solution: Hybrid Architecture & Zero-PII Trust")

    # Banner overview
    b_card = add_card(s3, Inches(0.8), Inches(1.65), Inches(11.733), Inches(1.15), bg_color=C_BLUE_LIGHT, border_color=C_BLUE_PRIMARY)
    tf = b_card.text_frame
    tf.margin_left = tf.margin_right = Inches(0.3)
    tf.margin_top = Inches(0.18)
    p = tf.paragraphs[0]
    p.text = "💡 Core Paradigm: Decentralized Cryptographic Fingerprinting"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_PRIMARY
    p2 = tf.add_paragraph()
    p2.text = "CertLedger anchors degrees to an Ethereum EVM smart contract by storing ONLY a 32-byte SHA-256 cryptographic digest of the canonical PDF, the verified university wallet address, block timestamp, and a revocation flag. Student PII remains 100% off-chain."
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_TEXT_BODY
    p2.space_before = Pt(4)

    # 4 Pillar Cards
    pillars = [
        ("🔐 Cryptographic Integrity", "SHA-256 Avalanche Effect", "Modifying even a single character or pixel in the PDF changes the entire hash digest, immediately triggering an INVALID verdict on-chain.", C_EMERALD),
        ("🛡️ Zero-PII Privacy by Design", "GDPR & FERPA Compliant", "Zero student names, roll numbers, or GPA records are stored on the blockchain ledger. Observers see only a one-way hexadecimal hash.", C_BLUE_PRIMARY),
        ("⚡ 3-Way Instant Verification", "< 2-Second Turnaround", "Verifiers can authoritatively check credentials via direct PDF drag-and-drop, Certificate ID lookup, or scanning the embedded dynamic QR code.", C_INDIGO),
        ("🔄 Dynamic On-Chain Revocation", "Authorized Issuer Control", "Universities can revoke fraudulent or errant diplomas on-chain. Verifiers are immediately alerted globally with zero delay.", C_ROSE),
    ]

    col_w = Inches(2.78)
    for idx, (title, sub, desc, color) in enumerate(pillars):
        x = Inches(0.8 + idx * 2.98)
        card = add_card(s3, x, Inches(3.05), col_w, Inches(3.8))
        tf = card.text_frame
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.25)
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = color
        
        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(10)
        p_sub.font.bold = True
        p_sub.font.color.rgb = C_TEXT_MUTED
        p_sub.space_before = Pt(2)

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(10.5)
        p_desc.font.color.rgb = C_TEXT_BODY
        p_desc.space_before = Pt(8)

    set_speaker_notes(s3,
        "Here is the core value proposition of CertLedger. Instead of treating the blockchain as a database, "
        "we treat it as an immutable trust anchor. "
        "We combine four pillars: "
        "First, cryptographic integrity through SHA-256, where altering 1 byte causes a completely different hash. "
        "Second, Zero-PII privacy design, guaranteeing compliance with data protection laws. "
        "Third, 3-way instant verification that takes under two seconds without requiring verifiers to sign transactions or pay gas. "
        "Fourth, authorized on-chain revocation, giving universities the power to invalidate credentials if fraud is detected."
    )

    # =========================================================================
    # SLIDE 4: System Architecture (3-Tier Hybrid Blueprint)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, C_BG_LIGHT)
    add_header(s4, "System Architecture: Hybrid On-Chain / Off-Chain Architecture")

    # 3 Architecture Tier Cards
    tier_w = Inches(3.72)
    tier_h = Inches(5.3)

    # Tier 1: Client
    t1 = add_card(s4, Inches(0.8), Inches(1.65), tier_w, tier_h)
    tf = t1.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "1. PRESENTATION LAYER"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_PRIMARY
    p_sub = tf.add_paragraph()
    p_sub.text = "React 18 + Vite + Tailwind CSS"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = C_TEXT_MUTED
    p_sub.space_before = Pt(2)

    items1 = [
        ("Registrar Dashboard", "Role-protected portal for university admins to issue & revoke diplomas."),
        ("Drag-and-Drop Dropzone", "Client-side candidate PDF file dropzone for instant zero-trust verification."),
        ("Dynamic QR Scanner", "Instant mobile redirection to authoritative verification audit reports."),
        ("Tamper Demonstration", "Interactive laboratory tool showing live hash discrepancies."),
        ("Responsive UX", "Designed with Lucide icons, glassmorphism, and instant toast notifications.")
    ]
    for h, b in items1:
        hp = tf.add_paragraph()
        hp.text = "• " + h
        hp.font.size = Pt(11)
        hp.font.bold = True
        hp.font.color.rgb = C_TEXT_DARK
        hp.space_before = Pt(8)
        bp = tf.add_paragraph()
        bp.text = "   " + b
        bp.font.size = Pt(10)
        bp.font.color.rgb = C_TEXT_BODY

    # Tier 2: Backend
    t2 = add_card(s4, Inches(4.8), Inches(1.65), tier_w, tier_h)
    tf = t2.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "2. APPLICATION & ENGINE"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_INDIGO
    p_sub = tf.add_paragraph()
    p_sub.text = "Python 3.10+ FastAPI & ReportLab"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = C_TEXT_MUTED
    p_sub.space_before = Pt(2)

    items2 = [
        ("REST API Gateway", "High-performance async FastAPI backend with OpenAPI Swagger docs."),
        ("Deterministic PDF Engine", "ReportLab vector generator rendering borders, seals, and QR codes."),
        ("Cryptographic Hasher", "FIPS 180-4 SHA-256 byte-stream hashing engine."),
        ("Web3 Integration", "Web3.py client signing transactions using institution private keys."),
        ("Relational Metadata", "SQLAlchemy + SQLite/PostgreSQL managing institutional logins & metadata.")
    ]
    for h, b in items2:
        hp = tf.add_paragraph()
        hp.text = "• " + h
        hp.font.size = Pt(11)
        hp.font.bold = True
        hp.font.color.rgb = C_TEXT_DARK
        hp.space_before = Pt(8)
        bp = tf.add_paragraph()
        bp.text = "   " + b
        bp.font.size = Pt(10)
        bp.font.color.rgb = C_TEXT_BODY

    # Tier 3: Blockchain
    t3 = add_card(s4, Inches(8.8), Inches(1.65), tier_w, tier_h)
    tf = t3.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "3. IMMUTABLE LEDGER"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p_sub = tf.add_paragraph()
    p_sub.text = "Solidity ^0.8.20 & Ethereum EVM"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = C_TEXT_MUTED
    p_sub.space_before = Pt(2)

    items3 = [
        ("Smart Contract", "AcademicCertificateRegistry.sol deployed on Ethereum EVM / Hardhat."),
        ("State Mappings", "Stores bytes32 certificateHash, issuer address, block timestamp, revoked bool."),
        ("Role-Based Security", "Contract Owner authorizes universities; only authorized issuers can mint."),
        ("Zero-Gas Queries", "Public view functions execute off-chain without spending ETH or gas."),
        ("Tamper-Proof Audit", "Immutable event logs (CertificateIssued, CertificateRevoked).")
    ]
    for h, b in items3:
        hp = tf.add_paragraph()
        hp.text = "• " + h
        hp.font.size = Pt(11)
        hp.font.bold = True
        hp.font.color.rgb = C_TEXT_DARK
        hp.space_before = Pt(8)
        bp = tf.add_paragraph()
        bp.text = "   " + b
        bp.font.size = Pt(10)
        bp.font.color.rgb = C_TEXT_BODY

    set_speaker_notes(s4,
        "Slide 4 presents our architectural blueprint. We divide the system into three well-defined layers. "
        "Layer 1 is the modern React 18 user interface featuring dark/light aesthetic, instant drag-and-drop dropzones, and mobile QR landing. "
        "Layer 2 is our FastAPI backend in Python. It handles JWT authentication, generates high-resolution PDF diplomas using ReportLab, "
        "calculates the SHA-256 binary hash, and interfaces with Web3.py. "
        "Layer 3 is the on-chain Ethereum EVM smart contract. Notice how clean the contract is: it holds no names, no roll numbers, and no grades. "
        "It stores only the 32-byte hash, the issuer wallet address, the timestamp, and a revocation flag."
    )

    # =========================================================================
    # SLIDE 5: Smart Contract Engineering (Solidity & EVM)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, C_BG_LIGHT)
    add_header(s5, "Smart Contract Engineering: AcademicCertificateRegistry.sol")

    # Left: Data Structure & Logic
    card_l = add_card(s5, Inches(0.8), Inches(1.65), Inches(6.2), Inches(5.3))
    tf = card_l.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "📜 Smart Contract State & Functions"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_PRIMARY

    funcs = [
        ("struct Certificate", "bytes32 certificateHash, address issuer, uint256 issuedAt, bool revoked."),
        ("authorizeIssuer(address _issuer)", "Restricted to contract owner. Enrolls accredited university wallet addresses."),
        ("revokeIssuer(address _issuer)", "Removes issuing privileges if an institution loses accreditation."),
        ("issueCertificate(string certId, bytes32 hash)", "Mints a certificate record on-chain. Reverts if duplicate certId or unauthorized caller."),
        ("verifyCertificate(string certId, bytes32 hash)", "View function returning (exists, hashMatches, revoked, issuer, issuedAt) in a single zero-gas call."),
        ("revokeCertificate(string certId)", "Enforces that ONLY the original issuing university can revoke a diploma.")
    ]
    for title, desc in funcs:
        tp = tf.add_paragraph()
        tp.text = "▶ " + title
        tp.font.size = Pt(10.5)
        tp.font.bold = True
        tp.font.color.rgb = C_TEXT_DARK
        tp.space_before = Pt(6)
        dp = tf.add_paragraph()
        dp.text = "   " + desc
        dp.font.size = Pt(9.5)
        dp.font.color.rgb = C_TEXT_BODY

    # Right: Code Snippet & Gas Optimization
    card_r = add_card(s5, Inches(7.3), Inches(1.65), Inches(5.233), Inches(5.3), bg_color=C_NAVY_DARK, border_color=C_BORDER_DARK)
    tf = card_r.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "⚡ Solidity Implementation Highlight"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(147, 197, 253)

    code_text = (
        "// Gas-Efficient Custom Errors (Solidity 0.8.20)\n"
        "error UnauthorizedIssuer(address caller);\n"
        "error CertificateAlreadyExists(string certId);\n"
        "error NotOriginalIssuer(address caller);\n\n"
        "struct Certificate {\n"
        "    bytes32 certificateHash;\n"
        "    address issuer;\n"
        "    uint256 issuedAt;\n"
        "    bool revoked;\n"
        "}\n\n"
        "mapping(bytes32 => Certificate) private certificates;\n"
        "mapping(address => bool) public authorizedIssuers;\n\n"
        "function verifyCertificate(\n"
        "    string calldata _certificateId,\n"
        "    bytes32 _certificateHash\n"
        ") external view returns (\n"
        "    bool exists, bool hashMatches, bool revoked,\n"
        "    address issuer, uint256 issuedAt\n"
        ") { ... }"
    )
    cp = tf.add_paragraph()
    cp.text = code_text
    cp.font.size = Pt(8.5)
    cp.font.name = "Consolas"
    cp.font.color.rgb = RGBColor(226, 232, 240)
    cp.space_before = Pt(6)

    # Bullet points on gas
    gp = tf.add_paragraph()
    gp.text = "Gas Optimization & EVM Security:"
    gp.font.size = Pt(10.5)
    gp.font.bold = True
    gp.font.color.rgb = C_EMERALD
    gp.space_before = Pt(8)

    gas_pts = [
        "Custom errors replace require strings, saving ~2,100 gas on reverts.",
        "Calldata used for string parameters to eliminate memory allocation.",
        "View functions run via local node RPC with 0 gas cost to verifiers."
    ]
    for pt in gas_pts:
        pp = tf.add_paragraph()
        pp.text = "✔ " + pt
        pp.font.size = Pt(9)
        pp.font.color.rgb = RGBColor(203, 213, 225)
        pp.space_before = Pt(3)

    set_speaker_notes(s5,
        "On Slide 5, we look at the smart contract engineering in Solidity 0.8.20. "
        "The contract is called AcademicCertificateRegistry. "
        "Notice the access control: only the contract owner can authorize an issuer, "
        "only an authorized issuer can issue certificates, and critically, "
        "only the original issuing institution wallet can revoke that specific diploma. "
        "We also implemented custom errors like UnauthorizedIssuer and CertificateAlreadyExists. "
        "In modern Solidity, custom errors save substantial gas compared to verbose revert strings. "
        "Finally, verifyCertificate is declared as external view, meaning employers can verify certificates "
        "infinitely without paying a single wei of gas or signing any MetaMask transaction."
    )

    # =========================================================================
    # SLIDE 6: Cryptographic Engine & Tamper Detection
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, C_BG_LIGHT)
    add_header(s6, "Cryptographic Engine: SHA-256 & The Avalanche Effect")

    # Left: The Math & Mechanism
    c_left = add_card(s6, Inches(0.8), Inches(1.65), Inches(5.7), Inches(5.3))
    tf = c_left.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "🔬 The SHA-256 Avalanche Effect"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_PRIMARY

    bullets = [
        ("Deterministic Vector PDF", "The diploma PDF is generated via ReportLab using fixed coordinates, fonts, anti-counterfeit guilloche borders, and an embedded dynamic QR code."),
        ("Cryptographic Stream Hashing", "The complete binary stream is digested using SHA-256 (FIPS 180-4), yielding a 256-bit (32-byte) collision-resistant hexadecimal fingerprint."),
        ("The Avalanche Property", "A strict mathematical requirement of secure hash functions: flipping a single bit in the input causes approximately 50% of the output bits to flip at random."),
        ("Collision Resistance", "Finding two different certificates that produce the same hash requires computing 2^128 operations, which is computationally impossible with modern supercomputers.")
    ]
    for title, desc in bullets:
        tp = tf.add_paragraph()
        tp.text = "• " + title
        tp.font.size = Pt(11)
        tp.font.bold = True
        tp.font.color.rgb = C_TEXT_DARK
        tp.space_before = Pt(8)
        dp = tf.add_paragraph()
        dp.text = "   " + desc
        dp.font.size = Pt(10)
        dp.font.color.rgb = C_TEXT_BODY

    # Right: Live Tamper Experiment Comparison
    c_right = add_card(s6, Inches(6.8), Inches(1.65), Inches(5.733), Inches(5.3))
    tf = c_right.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "🧪 Live Empirical Tamper Experiment"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_INDIGO

    # Box 1: Genuine
    b1 = add_card(s6, Inches(7.05), Inches(2.25), Inches(5.2), Inches(2.1), bg_color=C_EMERALD_BG, border_color=C_EMERALD)
    tf1 = b1.text_frame
    tf1.margin_left = tf1.margin_right = Inches(0.2)
    tf1.margin_top = Inches(0.15)
    p = tf1.paragraphs[0]
    p.text = "AUTHENTIC DIPLOMA (ORIGINAL PDF)"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(6, 95, 70)
    p2 = tf1.add_paragraph()
    p2.text = "• Binary Hash: 0x7f4a9b2c8d1e...a3f4\n• On-Chain Hash: 0x7f4a9b2c8d1e...a3f4\n• Hash Comparison: EXACT MATCH (TRUE)\n• Smart Contract Verdict: ✅ VALID & AUTHORITATIVE"
    p2.font.size = Pt(9.5)
    p2.font.name = "Consolas"
    p2.font.color.rgb = RGBColor(6, 78, 59)
    p2.space_before = Pt(4)

    # Box 2: Tampered
    b2 = add_card(s6, Inches(7.05), Inches(4.55), Inches(5.2), Inches(2.1), bg_color=C_ROSE_BG, border_color=C_ROSE)
    tf2 = b2.text_frame
    tf2.margin_left = tf2.margin_right = Inches(0.2)
    tf2.margin_top = Inches(0.15)
    p = tf2.paragraphs[0]
    p.text = "ALTERED DIPLOMA (10 BYTES MODIFIED)"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(153, 27, 27)
    p2 = tf2.add_paragraph()
    p2.text = "• Tamper: 'Grade A' altered to 'Grade A+' (10 bytes)\n• Altered Hash: 0x19e34c9f7a02...bb12\n• On-Chain Hash: 0x7f4a9b2c8d1e...a3f4\n• Smart Contract Verdict: ❌ TAMPERED / FORGED"
    p2.font.size = Pt(9.5)
    p2.font.name = "Consolas"
    p2.font.color.rgb = RGBColor(127, 29, 29)
    p2.space_before = Pt(4)

    set_speaker_notes(s6,
        "Slide 6 explains our cryptographic tamper detection engine. "
        "We rely on the SHA-256 cryptographic hash function, which exhibits the cryptographic avalanche effect. "
        "As demonstrated in our empirical testing shown on the right: "
        "When an authentic diploma is checked, its binary hash exactly matches the on-chain digest, returning VALID. "
        "However, if an attacker alters even 10 bytes—such as editing 'Grade A' to 'Grade A+'—the SHA-256 hash "
        "completely changes to an entirely different string. "
        "When compared to the immutable blockchain ledger, the hash mismatch is instantly caught, returning TAMPERED. "
        "This completely eliminates Photoshop and PDF editor forgery."
    )

    # =========================================================================
    # SLIDE 7: Privacy by Design & Regulatory Compliance (Zero-PII)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, C_BG_LIGHT)
    add_header(s7, "Privacy by Design: Zero-PII On-Chain & Legal Compliance")

    # 3 Column Cards
    col_w = Inches(3.72)
    col_h = Inches(5.3)

    # Col 1: GDPR Compliance
    c1 = add_card(s7, Inches(0.8), Inches(1.65), col_w, col_h)
    tf = c1.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "🇪🇺 GDPR Compliance"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_PRIMARY
    p_sub = tf.add_paragraph()
    p_sub.text = "Article 17: Right to Erasure"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = C_TEXT_MUTED
    p_sub.space_before = Pt(2)

    gdpr_pts = [
        ("The Legal Trap", "If student names/grades are stored on Ethereum, they cannot be deleted, permanently violating GDPR Article 17."),
        ("CertLedger Solution", "Only non-invertible hashes reside on-chain. Off-chain database records can be fully deleted or anonymized upon request."),
        ("Data Minimization", "Complies with GDPR Article 5(1)(c) by storing strictly the bare minimum verification anchor.")
    ]
    for h, b in gdpr_pts:
        hp = tf.add_paragraph()
        hp.text = "• " + h
        hp.font.size = Pt(11)
        hp.font.bold = True
        hp.font.color.rgb = C_TEXT_DARK
        hp.space_before = Pt(8)
        bp = tf.add_paragraph()
        bp.text = "   " + b
        bp.font.size = Pt(10)
        bp.font.color.rgb = C_TEXT_BODY

    # Col 2: FERPA Compliance
    c2 = add_card(s7, Inches(4.8), Inches(1.65), col_w, col_h)
    tf = c2.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "🏛️ FERPA Compliance"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_INDIGO
    p_sub = tf.add_paragraph()
    p_sub.text = "Educational Rights & Privacy Act"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = C_TEXT_MUTED
    p_sub.space_before = Pt(2)

    ferpa_pts = [
        ("Confidentiality Mandate", "FERPA prohibits the disclosure of student educational records without prior written consent."),
        ("Public Explorers Safe", "Anyone inspecting the blockchain via Etherscan or block explorers sees only meaningless 64-hex characters."),
        ("Zero Grade Leakage", "GPA, coursework, majors, and disciplinary histories never touch the mempool or ledger.")
    ]
    for h, b in ferpa_pts:
        hp = tf.add_paragraph()
        hp.text = "• " + h
        hp.font.size = Pt(11)
        hp.font.bold = True
        hp.font.color.rgb = C_TEXT_DARK
        hp.space_before = Pt(8)
        bp = tf.add_paragraph()
        bp.text = "   " + b
        bp.font.size = Pt(10)
        bp.font.color.rgb = C_TEXT_BODY

    # Col 3: Mathematical One-Way Proof
    c3 = add_card(s7, Inches(8.8), Inches(1.65), col_w, col_h)
    tf = c3.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "🔒 Cryptographic Proof"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p_sub = tf.add_paragraph()
    p_sub.text = "Irreversibility & Pre-image Resistance"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = C_TEXT_MUTED
    p_sub.space_before = Pt(2)

    crypto_pts = [
        ("One-Way Function", "Given hash H = SHA-256(PDF), finding the original PDF or student name from H alone is mathematically infeasible."),
        ("Immense Keyspace", "The search space is 2^256 possible outputs (~1.15 x 10^77 combinations, more than atoms in the observable universe)."),
        ("Rainbow Table Immune", "Because each PDF contains a unique certificate ID, issue date, and random vector elements, rainbow tables fail.")
    ]
    for h, b in crypto_pts:
        hp = tf.add_paragraph()
        hp.text = "• " + h
        hp.font.size = Pt(11)
        hp.font.bold = True
        hp.font.color.rgb = C_TEXT_DARK
        hp.space_before = Pt(8)
        bp = tf.add_paragraph()
        bp.text = "   " + b
        bp.font.size = Pt(10)
        bp.font.color.rgb = C_TEXT_BODY

    set_speaker_notes(s7,
        "Slide 7 covers a common exam trap and major research distinction: privacy and regulatory compliance. "
        "Many projects naively store student details in smart contracts. In the real world, this is illegal. "
        "Under GDPR Article 17, students have the Right to be Forgotten. If data is in an immutable block, it cannot be deleted. "
        "CertLedger solves this: student names and grades live solely in our off-chain database and on the student's physical/digital diploma. "
        "The blockchain holds only the one-way 32-byte SHA-256 hash. "
        "If a student requests erasure, we purge their off-chain record. The on-chain hash becomes an un-linkable orphan string, "
        "fully complying with both GDPR and FERPA regulations."
    )

    # =========================================================================
    # SLIDE 8: Certificate Issuance Lifecycle (5-Stage Workflow)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, C_BG_LIGHT)
    add_header(s8, "Certificate Issuance Lifecycle: From Enrollment to On-Chain Minting")

    # 5 Sequential Step Cards
    steps = [
        ("Step 1", "Registrar Auth", "University admin authenticates via JWT / Bcrypt credentials into the secure portal.", C_BLUE_PRIMARY),
        ("Step 2", "Data Ingestion", "Admin enters student name, roll ID, degree title, department, and graduation year.", C_INDIGO),
        ("Step 3", "PDF Rendering", "ReportLab draws deterministic vector canvas with university seal & dynamic QR code.", C_EMERALD),
        ("Step 4", "SHA-256 Digest", "Complete PDF binary stream is hashed into 32-byte cryptographic fingerprint.", C_AMBER),
        ("Step 5", "EVM Minting", "Web3 signs issueCertificate() tx; mined into Ethereum block with immutable timestamp.", C_BLUE_PRIMARY),
    ]

    card_w = Inches(2.2)
    card_h = Inches(3.2)
    for idx, (step_num, title, desc, color) in enumerate(steps):
        x = Inches(0.8 + idx * 2.38)
        c = add_card(s8, x, Inches(1.7), card_w, card_h)
        tf = c.text_frame
        tf.margin_left = tf.margin_right = Inches(0.15)
        tf.margin_top = Inches(0.2)
        p = tf.paragraphs[0]
        p.text = step_num
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = color

        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = C_TEXT_DARK
        p_t.space_before = Pt(4)

        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(9.5)
        p_d.font.color.rgb = C_TEXT_BODY
        p_d.space_before = Pt(6)

    # Lower Info Box: Technical Guarantees
    info = add_card(s8, Inches(0.8), Inches(5.15), Inches(11.733), Inches(1.8), bg_color=C_BLUE_LIGHT, border_color=C_BLUE_PRIMARY)
    tf = info.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.18)
    p = tf.paragraphs[0]
    p.text = "⚙️ Cryptographic Issuance Invariants & Smart Contract Guardrails"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_PRIMARY

    bullets = [
        "Anti-Replay Protection: If an admin attempts to issue an existing Certificate ID, the contract reverts with CertificateAlreadyExists.",
        "Deterministic Vector PDF: ReportLab uses fixed canvas geometry, so generating the PDF from source data produces the exact same binary stream.",
        "Atomic Storage: The generated PDF, transaction hash, block number, and gas used are linked together in the off-chain database."
    ]
    for b in bullets:
        bp = tf.add_paragraph()
        bp.text = "✔ " + b
        bp.font.size = Pt(10.5)
        bp.font.color.rgb = C_TEXT_BODY
        bp.space_before = Pt(4)

    set_speaker_notes(s8,
        "Slide 8 illustrates the end-to-end issuance lifecycle. "
        "The workflow has five distinct stages. "
        "First, the registrar logs in. "
        "Second, student metadata is submitted. "
        "Third, our ReportLab engine programmatically constructs a high-resolution vector PDF diploma, embedding university seals and a QR code. "
        "Fourth, the complete PDF binary is hashed into a 32-byte SHA-256 digest. "
        "Fifth, the university's Web3 wallet signs and broadcasts issueCertificate to the blockchain. "
        "The smart contract enforces that the certificate ID has not been used before, stores the hash and block timestamp, "
        "and emits the CertificateIssued event for indexing."
    )

    # =========================================================================
    # SLIDE 9: 3-Way Zero-Trust Verification Engine
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, C_BG_LIGHT)
    add_header(s9, "3-Way Zero-Trust Verification: Dropzone, ID Query & QR Scanning")

    col_w = Inches(3.72)
    col_h = Inches(5.3)

    # Mode 1: PDF Dropzone
    m1 = add_card(s9, Inches(0.8), Inches(1.65), col_w, col_h)
    tf = m1.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "MODE 1: PDF DROPZONE"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p_sub = tf.add_paragraph()
    p_sub.text = "Zero-Trust Document Verification"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = C_TEXT_MUTED
    p_sub.space_before = Pt(2)

    pts1 = [
        ("Action", "Employer drags & drops candidate's PDF file directly into the browser dropzone."),
        ("Under the Hood", "System hashes the uploaded PDF via SHA-256 and compares it to the on-chain hash stored under its Certificate ID."),
        ("Verdict", "If hashes match and revoked == false -> AUTHORITATIVE & VALID. If altered by even 1 byte -> TAMPERED.")
    ]
    for h, b in pts1:
        hp = tf.add_paragraph()
        hp.text = "• " + h
        hp.font.size = Pt(11)
        hp.font.bold = True
        hp.font.color.rgb = C_TEXT_DARK
        hp.space_before = Pt(8)
        bp = tf.add_paragraph()
        bp.text = "   " + b
        bp.font.size = Pt(10)
        bp.font.color.rgb = C_TEXT_BODY

    # Mode 2: ID Lookup
    m2 = add_card(s9, Inches(4.8), Inches(1.65), col_w, col_h)
    tf = m2.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "MODE 2: CERTIFICATE ID"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_PRIMARY
    p_sub = tf.add_paragraph()
    p_sub.text = "Direct On-Chain Registry Query"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = C_TEXT_MUTED
    p_sub.space_before = Pt(2)

    pts2 = [
        ("Action", "Verifier inputs Certificate ID (e.g., CERT-2026-0001) into the search portal."),
        ("Under the Hood", "Queries verifyCertificate() view function on EVM via JSON-RPC."),
        ("Verdict", "Returns existence status, issuing university wallet address, block timestamp, and live revocation status with 0 gas.")
    ]
    for h, b in pts2:
        hp = tf.add_paragraph()
        hp.text = "• " + h
        hp.font.size = Pt(11)
        hp.font.bold = True
        hp.font.color.rgb = C_TEXT_DARK
        hp.space_before = Pt(8)
        bp = tf.add_paragraph()
        bp.text = "   " + b
        bp.font.size = Pt(10)
        bp.font.color.rgb = C_TEXT_BODY

    # Mode 3: QR Code Mobile Scan
    m3 = add_card(s9, Inches(8.8), Inches(1.65), col_w, col_h)
    tf = m3.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "MODE 3: QR CODE SCAN"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_INDIGO
    p_sub = tf.add_paragraph()
    p_sub.text = "Frictionless Mobile Inspection"
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = C_TEXT_MUTED
    p_sub.space_before = Pt(2)

    pts3 = [
        ("Action", "Auditor or recruiter scans the QR code printed on physical/digital diploma using any smartphone camera."),
        ("Under the Hood", "Redirects to direct verification endpoint /verify/{cert_id}."),
        ("Verdict", "Presents a full cryptographic audit report: university name, degree title, tx hash, block confirmation, and status.")
    ]
    for h, b in pts3:
        hp = tf.add_paragraph()
        hp.text = "• " + h
        hp.font.size = Pt(11)
        hp.font.bold = True
        hp.font.color.rgb = C_TEXT_DARK
        hp.space_before = Pt(8)
        bp = tf.add_paragraph()
        bp.text = "   " + b
        bp.font.size = Pt(10)
        bp.font.color.rgb = C_TEXT_BODY

    set_speaker_notes(s9,
        "Slide 9 demonstrates our three zero-trust verification modalities. "
        "First, the PDF dropzone. A recruiter doesn't need to believe what the student claimed on their resume. "
        "They drop the PDF into the portal, the hash is computed locally in the client/backend, and compared to the blockchain. "
        "Second, direct ID search, querying the smart contract view function directly. "
        "Third, mobile QR scanning. Every PDF has a dynamic QR code that opens our direct verification route, "
        "giving employers an instant audit report on their phone in two seconds with zero software installation."
    )

    # =========================================================================
    # SLIDE 10: Dynamic On-Chain Revocation Mechanism
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, C_BG_LIGHT)
    add_header(s10, "Dynamic Revocation: Solving the Permanent Fraud Problem")

    # Left: The Mechanics & Security Rule
    c_left = add_card(s10, Inches(0.8), Inches(1.65), Inches(5.7), Inches(5.3))
    tf = c_left.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "🛡️ Cryptographic Revocation Governance"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_ROSE

    rev_pts = [
        ("The Critical Vulnerability in Paper", "When paper degrees or static PDFs are given to graduates, an institution has no technical means to recall them if fraud or plagiarism is discovered later."),
        ("Issuer-Only Authorization Rule", "In AcademicCertificateRegistry.sol, revokeCertificate() checks: msg.sender == cert.issuer. Another institution or malicious party CANNOT revoke someone else's degree."),
        ("Atomic State Transition", "The contract flips revoked = true and emits CertificateRevoked(certId, issuer, block.timestamp)."),
        ("Global Instant Propagation", "The moment the block is confirmed, any employer verifying the diploma is immediately warned that the credential has been revoked.")
    ]
    for h, b in rev_pts:
        hp = tf.add_paragraph()
        hp.text = "• " + h
        hp.font.size = Pt(11)
        hp.font.bold = True
        hp.font.color.rgb = C_TEXT_DARK
        hp.space_before = Pt(8)
        bp = tf.add_paragraph()
        bp.text = "   " + b
        bp.font.size = Pt(10)
        bp.font.color.rgb = C_TEXT_BODY

    # Right: Revocation Life Cycle Box
    c_right = add_card(s10, Inches(6.8), Inches(1.65), Inches(5.733), Inches(5.3), bg_color=C_ROSE_BG, border_color=C_ROSE)
    tf = c_right.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "⚠️ Real-Time Revocation Simulation"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(153, 27, 27)

    sim_text = (
        "// 1. Initial State (Block #1)\n"
        "status = verifyCertificate('CERT-2026-0001', hash);\n"
        ">> exists: true, hashMatches: true, revoked: FALSE\n"
        ">> Verdict: ✅ VALID\n\n"
        "// 2. University Discovers Plagiarism & Calls Revoke\n"
        "registry.revokeCertificate('CERT-2026-0001');\n"
        ">> Tx mined in Block #2 | Gas: ~29,000\n"
        ">> Event emitted: CertificateRevoked(...)\n\n"
        "// 3. Verifier Re-Checks Certificate (Block #2+)\n"
        "status = verifyCertificate('CERT-2026-0001', hash);\n"
        ">> exists: true, hashMatches: true, revoked: TRUE\n"
        ">> Verdict: 🚫 REVOKED (Discredited)"
    )
    sp = tf.add_paragraph()
    sp.text = sim_text
    sp.font.size = Pt(9.5)
    sp.font.name = "Consolas"
    sp.font.color.rgb = RGBColor(127, 29, 29)
    sp.space_before = Pt(8)

    sub_box = add_card(s10, Inches(7.05), Inches(5.35), Inches(5.2), Inches(1.35), bg_color=C_WHITE, border_color=C_ROSE)
    tf_sub = sub_box.text_frame
    tf_sub.margin_left = tf_sub.margin_right = Inches(0.2)
    tf_sub.margin_top = Inches(0.12)
    p = tf_sub.paragraphs[0]
    p.text = "Legal & Institutional Guarantee"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_ROSE
    p2 = tf_sub.add_paragraph()
    p2.text = "Protects the university's academic brand by ensuring fake or discredited credentials cannot circulate undetected in the job market."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_TEXT_BODY
    p2.space_before = Pt(2)

    set_speaker_notes(s10,
        "Slide 10 highlights revocation, an area where standard paper and PDF systems completely fail. "
        "If a university revokes a degree due to fraud, an alumnus can still show their printed paper diploma to an unsuspecting employer. "
        "In CertLedger, the issuing university calls revokeCertificate on the smart contract. "
        "Our contract strictly verifies that the caller address matches the original issuer address. "
        "Once mined, the revocation flag is permanent on-chain. "
        "Whenever anyone checks that diploma in the future, the system immediately returns a bright red REVOKED banner."
    )

    # =========================================================================
    # SLIDE 11: Technology Stack & Implementation Matrix
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, C_BG_LIGHT)
    add_header(s11, "Technology Stack & Implementation Matrix")

    # Table of Technologies
    rows = [
        ("Layer", "Technology", "Version", "Key Responsibilities"),
        ("Blockchain Core", "Solidity", "^0.8.20", "Smart contract registry, access control, revocation state"),
        ("EVM Development", "Hardhat & Ethers.js", "v2.22 / v6", "Local Ethereum node (port 8545), compilation, deployment scripts"),
        ("Security Standards", "OpenZeppelin Contracts", "v5.0.0", "Battle-tested Ownable and access control primitives"),
        ("Backend Framework", "Python & FastAPI", "v3.10+ / 0.110+", "High-speed asynchronous REST API, OpenAPI docs, routing"),
        ("Web3 Client", "Web3.py", "v6.15+", "EVM RPC interface, raw transaction signing, event filtering"),
        ("PDF Vector Engine", "ReportLab", "v4.1+", "Deterministic coordinate-based diploma rendering & guilloche borders"),
        ("Database & ORM", "SQLAlchemy + SQLite/Postgres", "v2.0+", "Relational metadata storage, institution auth, transaction receipts"),
        ("Frontend UI", "React 18 & Vite", "v18.2 / v5", "Component-based SPA, client dropzone, route guards"),
        ("Styling & Icons", "Tailwind CSS & Lucide React", "v3.4+", "Responsive styling, modern glassmorphic dashboard aesthetic")
    ]

    table_shape = s11.shapes.add_table(len(rows), 4, Inches(0.8), Inches(1.65), Inches(11.733), Inches(5.3))
    table = table_shape.table
    table.columns[0].width = Inches(2.2)
    table.columns[1].width = Inches(3.0)
    table.columns[2].width = Inches(1.5)
    table.columns[3].width = Inches(5.033)

    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.margin_left = Inches(0.12)
            tf.margin_right = Inches(0.12)
            tf.margin_top = Inches(0.06)
            tf.margin_bottom = Inches(0.06)
            p = tf.paragraphs[0]
            p.font.size = Pt(10.5 if r_idx > 0 else 11)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_NAVY_DARK
            else:
                p.font.color.rgb = C_TEXT_DARK if c_idx < 2 else C_TEXT_BODY
                if c_idx == 0:
                    p.font.bold = True
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_WHITE if r_idx % 2 == 1 else RGBColor(241, 245, 249)

    set_speaker_notes(s11,
        "Slide 11 summarizes our complete technology stack matrix. "
        "We selected each component for performance, security, and production readiness. "
        "On the blockchain side, we use Solidity 0.8.20 with Hardhat and OpenZeppelin v5. "
        "On the backend, Python FastAPI provides asynchronous high throughput, "
        "ReportLab provides deterministic vector PDF generation, and Web3.py interacts with the EVM. "
        "On the frontend, React 18 with Vite and Tailwind CSS offers a lightning-fast user experience."
    )

    # =========================================================================
    # SLIDE 12: Testing Strategy & Automated Validation
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12, C_BG_LIGHT)
    add_header(s12, "Testing Strategy: 100% Automated Test Passing & E2E Validation")

    # 3 Stat Cards
    c1 = add_card(s12, Inches(0.8), Inches(1.65), Inches(3.72), Inches(2.2), bg_color=C_EMERALD_BG, border_color=C_EMERALD)
    tf = c1.text_frame
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "17 / 17 PASSING"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = RGBColor(6, 95, 70)
    p2 = tf.add_paragraph()
    p2.text = "Smart Contract Mocha/Chai Tests"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = C_TEXT_DARK
    p3 = tf.add_paragraph()
    p3.text = "Validates issuer authorization, minting idempotency, zero-gas queries, revocation security, and custom error reverts."
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = C_TEXT_BODY
    p3.space_before = Pt(4)

    c2 = add_card(s12, Inches(4.8), Inches(1.65), Inches(3.72), Inches(2.2), bg_color=C_BLUE_LIGHT, border_color=C_BLUE_PRIMARY)
    tf = c2.text_frame
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "12 / 12 PASSING"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_PRIMARY
    p2 = tf.add_paragraph()
    p2.text = "Backend Pytest Integration Suite"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = C_TEXT_DARK
    p3 = tf.add_paragraph()
    p3.text = "Validates FastAPI endpoints, JWT auth, ReportLab PDF rendering consistency, SHA-256 byte hashing, and database transactions."
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = C_TEXT_BODY
    p3.space_before = Pt(4)

    c3 = add_card(s12, Inches(8.8), Inches(1.65), Inches(3.72), Inches(2.2), bg_color=RGBColor(245, 243, 255), border_color=C_INDIGO)
    tf = c3.text_frame
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "11 STAGES"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = C_INDIGO
    p2 = tf.add_paragraph()
    p2.text = "End-to-End Live Integration Demo"
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = C_TEXT_DARK
    p3 = tf.add_paragraph()
    p3.text = "Autonomous script (e2e_demo.py) running all 11 lifecycle stages on the live blockchain with automated verification."
    p3.font.size = Pt(9.5)
    p3.font.color.rgb = C_TEXT_BODY
    p3.space_before = Pt(4)

    # Lower Breakdown Box: The 11 Stages of e2e_demo.py
    box_e2e = add_card(s12, Inches(0.8), Inches(4.1), Inches(11.733), Inches(2.85))
    tf = box_e2e.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.2)
    p = tf.paragraphs[0]
    p.text = "📋 Automated 11-Stage End-to-End Lifecycle Execution (scripts/e2e_demo.py)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_DARK

    stages = [
        "1. Blockchain Connectivity: Verifies EVM JSON-RPC connection & deployed contract address.",
        "2. Admin Authentication: Logs in university registrar and acquires Bearer JWT token.",
        "3. Certificate Issuance: Renders canonical diploma, hashes SHA-256, and mines mint transaction.",
        "4. PDF Retrieval: Downloads canonical generated PDF file from backend repository.",
        "5. Verification by ID: Smart contract view call confirms valid on-chain record.",
        "6. Verification by PDF: Uploaded PDF hash matches blockchain digest exactly.",
        "7. Live Tamper Simulation: Injects 10 corrupted bytes into PDF; system correctly flags TAMPERED.",
        "8. On-Chain Revocation: Authorized institution wallet executes revokeCertificate() on EVM.",
        "9. Post-Revocation Check: Verifier re-queries diploma; system authoritatively reports REVOKED.",
        "10. Unknown Certificate Check: Queries non-existent ID; system cleanly returns NOT_FOUND.",
        "11. Blockchain Explorer Inspector: Inspects block numbers, gas used, and transaction confirmation."
    ]
    for s in stages:
        sp = tf.add_paragraph()
        sp.text = "✔ " + s
        sp.font.size = Pt(9.5)
        sp.font.color.rgb = C_TEXT_BODY
        sp.space_before = Pt(1.5)

    set_speaker_notes(s12,
        "Slide 12 presents our quality assurance and testing results. "
        "We have achieved 100% automated test coverage across all layers. "
        "Our smart contract suite has 17 out of 17 tests passing in Mocha and Chai. "
        "Our backend API has 12 out of 12 tests passing in Pytest. "
        "Furthermore, we built an end-to-end automated testing script called e2e_demo.py. "
        "It autonomously tests the entire 11-stage lifecycle against the live blockchain: "
        "from login and issuance, to hash matching, live tampering injection, on-chain revocation, "
        "and transaction block receipts. Everything executes without manual intervention."
    )

    # =========================================================================
    # SLIDE 13: Comparative Analysis (The Competitive Advantage)
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13, C_BG_LIGHT)
    add_header(s13, "Comparative Analysis: Traditional vs. Centralized vs. CertLedger")

    matrix = [
        ("Evaluation Dimension", "Traditional Paper", "Centralized SQL Portal", "Naive Blockchain", "CertLedger (Our System)"),
        ("Trust Model", "Institutional paper stamp", "Trust in single server / DB admin", "Consensus miners", "Decentralized EVM Consensus"),
        ("Verification Speed", "2 - 4 Weeks (Manual)", "Minutes (Requires API/Login)", "Seconds (Gas required)", "< 2 Seconds (Instant & Free)"),
        ("Tamper Resistance", "❌ Low (Photoshop forgery)", "⚠️ Moderate (Insider DB edit)", "✅ Immutable", "✅ 100% Tamper-Proof (SHA-256)"),
        ("Privacy & GDPR", "⚠️ Paper records leaked", "⚠️ Server breach risk", "❌ VIOLATION (Data on-chain)", "✅ 100% Zero-PII Compliant"),
        ("Revocation Support", "❌ Impossible after print", "✅ Mutable DB update", "⚠️ Complex / Gas heavy", "✅ Instant On-Chain Revocation"),
        ("Single Point of Failure", "❌ University closure halts", "❌ Server outage halts lookup", "✅ Distributed ledger", "✅ Resilient Distributed Ledger"),
        ("Verification Cost", "High ($15 - $50 clearinghouse)", "Subscription / Server hosting", "Transaction Gas fee", "Free (0 Gas View Calls)")
    ]

    t_shape = s13.shapes.add_table(len(matrix), 5, Inches(0.8), Inches(1.65), Inches(11.733), Inches(5.3))
    t = t_shape.table
    t.columns[0].width = Inches(2.5)
    t.columns[1].width = Inches(2.2)
    t.columns[2].width = Inches(2.3)
    t.columns[3].width = Inches(2.2)
    t.columns[4].width = Inches(2.533)

    for r_idx, row in enumerate(matrix):
        for c_idx, val in enumerate(row):
            cell = t.cell(r_idx, c_idx)
            cell.text = val
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.margin_left = Inches(0.1)
            tf.margin_right = Inches(0.1)
            tf.margin_top = Inches(0.06)
            tf.margin_bottom = Inches(0.06)
            p = tf.paragraphs[0]
            p.font.size = Pt(10 if r_idx > 0 else 10.5)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = C_WHITE
                cell.fill.solid()
                cell.fill.fore_color.rgb = C_NAVY_DARK
            else:
                if c_idx == 4:
                    p.font.bold = True
                    p.font.color.rgb = RGBColor(6, 95, 70)
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = C_EMERALD_BG
                else:
                    p.font.color.rgb = C_TEXT_DARK if c_idx == 0 else C_TEXT_BODY
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = C_WHITE if r_idx % 2 == 1 else RGBColor(248, 250, 252)

    set_speaker_notes(s13,
        "Slide 13 provides a comprehensive comparative evaluation matrix. "
        "Examiners frequently ask: 'Why not just use an SQL database with digital signatures?' "
        "As shown in column 3, a centralized database has a single point of failure and suffers from insider threats; "
        "a rogue database administrator can alter records or delete logs. "
        "On the other hand, naive blockchain projects (column 4) violate GDPR by placing student identities permanently on-chain. "
        "CertLedger (column 5) combines the best of all worlds: "
        "decentralized immutability, sub-two-second verification, zero gas cost for verifiers, "
        "and absolute privacy protection."
    )

    # =========================================================================
    # SLIDE 14: Gas Economics & Layer-2 Scalability
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14, C_BG_LIGHT)
    add_header(s14, "Gas Economics & Production Scaling: Layer-2 Networks")

    # Left: Gas Breakdown
    c_left = add_card(s14, Inches(0.8), Inches(1.65), Inches(5.7), Inches(5.3))
    tf = c_left.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "⛽ On-Chain Gas Cost Analysis"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_PRIMARY

    bullets = [
        ("Deployment Cost", "~620,000 gas (one-time deployment of AcademicCertificateRegistry.sol)."),
        ("Certificate Issuance", "~85,000 gas per minted certificate (writing struct to mapping & emitting event)."),
        ("Certificate Revocation", "~29,000 gas per revoked certificate (updating boolean flag & emitting event)."),
        ("Certificate Verification", "0 GAS! Executed as an off-chain eth_call view query against an RPC node.")
    ]
    for h, b in bullets:
        hp = tf.add_paragraph()
        hp.text = "• " + h
        hp.font.size = Pt(11)
        hp.font.bold = True
        hp.font.color.rgb = C_TEXT_DARK
        hp.space_before = Pt(8)
        bp = tf.add_paragraph()
        bp.text = "   " + b
        bp.font.size = Pt(10)
        bp.font.color.rgb = C_TEXT_BODY

    # Right: Layer-2 Deployment & Merkle Trees
    c_right = add_card(s14, Inches(6.8), Inches(1.65), Inches(5.733), Inches(5.3))
    tf = c_right.text_frame
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.25)
    p = tf.paragraphs[0]
    p.text = "🌐 Layer-2 Rollups & Mass Batching"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_INDIGO

    # Box: L2 Comparison
    b_l2 = add_card(s14, Inches(7.05), Inches(2.25), Inches(5.2), Inches(2.1), bg_color=C_BLUE_LIGHT, border_color=C_BLUE_PRIMARY)
    tf_l2 = b_l2.text_frame
    tf_l2.margin_left = tf_l2.margin_right = Inches(0.2)
    tf_l2.margin_top = Inches(0.15)
    p = tf_l2.paragraphs[0]
    p.text = "COST COMPARISON ACROSS NETWORKS"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = C_BLUE_PRIMARY
    p2 = tf_l2.add_paragraph()
    p2.text = (
        "• Ethereum Mainnet: ~$3.50 - $15.00 / certificate (prohibitive)\n"
        "• Polygon PoS: ~$0.005 / certificate (99.9% cheaper)\n"
        "• Arbitrum / Base L2: ~$0.01 / certificate\n"
        "• Merkle Batch Tree: <$0.0001 / certificate (10,000 in 1 tx)"
    )
    p2.font.size = Pt(9.5)
    p2.font.name = "Consolas"
    p2.font.color.rgb = C_TEXT_DARK
    p2.space_before = Pt(4)

    # Box: Merkle Tree Batching
    b_m = add_card(s14, Inches(7.05), Inches(4.55), Inches(5.2), Inches(2.1), bg_color=C_EMERALD_BG, border_color=C_EMERALD)
    tf_m = b_m.text_frame
    tf_m.margin_left = tf_m.margin_right = Inches(0.2)
    tf_m.margin_top = Inches(0.15)
    p = tf_m.paragraphs[0]
    p.text = "ENTERPRISE SCALING: MERKLE TREES"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(6, 95, 70)
    p2 = tf_m.add_paragraph()
    p2.text = (
        "• University constructs cryptographic Merkle Tree of graduating cohort.\n"
        "• Only 32-byte Merkle Root is stored on-chain in 1 transaction.\n"
        "• Each graduate receives Merkle proof path (~500 bytes).\n"
        "• Verifier validates root in O(log N) operations with zero gas."
    )
    p2.font.size = Pt(9.5)
    p2.font.name = "Consolas"
    p2.font.color.rgb = RGBColor(6, 78, 59)
    p2.space_before = Pt(4)

    set_speaker_notes(s14,
        "Slide 14 addresses gas economics and production scalability. "
        "In our smart contract, issuing a certificate consumes approximately 85,000 gas. "
        "On Ethereum L1, gas volatility makes single minting expensive. "
        "However, because our contract is standard EVM bytecode, it deploys seamlessly to Layer-2 networks "
        "like Polygon, Arbitrum, or Base, dropping issuance costs to less than a single penny. "
        "For massive graduating classes of ten thousand students, we can implement Merkle Tree batch minting: "
        "the university commits just one 32-byte Merkle Root to the blockchain, enabling all 10,000 certificates "
        "to be verified via cryptographic Merkle proofs for the cost of a single transaction."
    )

    # =========================================================================
    # SLIDE 15: Future Innovations & Extension Roadmap
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15, C_BG_LIGHT)
    add_header(s15, "Future Roadmap: Next-Generation Decentralized Credentials")

    # 4 Roadmap Cards
    items = [
        ("1. Soulbound Tokens (SBT - ERC-5192)", "Non-Transferable Identity", "Bind certificates directly to a graduate's verified wallet address as non-transferable Soulbound NFTs, preventing credential sale or unauthorized loaning.", C_BLUE_PRIMARY),
        ("2. W3C Verifiable Credentials & DIDs", "Global Academic Portability", "Implement W3C Decentralized Identifiers (DIDs) allowing credentials to be interoperable across international universities and digital identity wallets.", C_INDIGO),
        ("3. Decentralized Storage (IPFS / Filecoin)", "Decentralized Document Persistence", "Store encrypted diploma PDFs on IPFS clusters with cryptographic Content Identifiers (CIDs), eliminating centralized web hosting dependency.", C_EMERALD),
        ("4. Zero-Knowledge Proofs (zk-SNARKs)", "Selective Attribute Disclosure", "Enable graduates to prove qualifications (e.g. 'GPA > 3.5' or 'Degree from Top 10 University') without disclosing their exact transcript or grades.", C_AMBER)
    ]

    card_w = Inches(5.66)
    card_h = Inches(2.4)
    for idx, (title, sub, desc, color) in enumerate(items):
        col = idx % 2
        row = idx // 2
        x = Inches(0.8 + col * 6.06)
        y = Inches(1.7 + row * 2.65)
        c = add_card(s15, x, y, card_w, card_h)
        tf = c.text_frame
        tf.margin_left = tf.margin_right = Inches(0.25)
        tf.margin_top = Inches(0.2)
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = color

        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(10)
        p_sub.font.bold = True
        p_sub.font.color.rgb = C_TEXT_MUTED
        p_sub.space_before = Pt(2)

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(10.5)
        p_desc.font.color.rgb = C_TEXT_BODY
        p_desc.space_before = Pt(6)

    set_speaker_notes(s15,
        "Slide 15 presents our future innovation roadmap. "
        "There are four exciting directions for future research: "
        "First, Soulbound Tokens (ERC-5192) to lock credentials into student web3 wallets. "
        "Second, W3C Verifiable Credentials and DIDs for international standard compliance. "
        "Third, decentralized storage using IPFS and Filecoin. "
        "And fourth, Zero-Knowledge Proofs (zk-SNARKs), allowing students to selectively prove qualifications—"
        "such as demonstrating they graduated with first class honors—without showing their entire transcript."
    )

    # =========================================================================
    # SLIDE 16: Conclusion & Viva Voce Defense (Dark Theme)
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16, C_NAVY_DARK)

    # Header
    cat_box = s16.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(0.35))
    tf = cat_box.text_frame
    p = tf.paragraphs[0]
    p.text = "PROJECT SUMMARY & TECHNICAL DEFENSE"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = RGBColor(96, 165, 250)

    t_box = s16.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.7), Inches(0.65))
    tf = t_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Conclusion: CertLedger Impact & Takeaways"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

    # 3 Summary Cards
    col_w = Inches(3.72)
    s_c1 = add_card(s16, Inches(0.8), Inches(1.8), col_w, Inches(3.6), bg_color=C_CARD_DARK, border_color=C_BORDER_DARK)
    tf1 = s_c1.text_frame
    tf1.margin_left = tf1.margin_right = Inches(0.2)
    tf1.margin_top = Inches(0.2)
    p = tf1.paragraphs[0]
    p.text = "🎯 Objective Achieved"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(96, 165, 250)
    pts = [
        "Eliminates academic diploma forgery.",
        "Reduces background check time from weeks to < 2 seconds.",
        "Zero-gas cost for public verifiers.",
        "Dynamic on-chain revocation mechanism."
    ]
    for pt in pts:
        pp = tf1.add_paragraph()
        pp.text = "✔ " + pt
        pp.font.size = Pt(10.5)
        pp.font.color.rgb = RGBColor(226, 232, 240)
        pp.space_before = Pt(6)

    s_c2 = add_card(s16, Inches(4.8), Inches(1.8), col_w, Inches(3.6), bg_color=C_CARD_DARK, border_color=C_BORDER_DARK)
    tf2 = s_c2.text_frame
    tf2.margin_left = tf2.margin_right = Inches(0.2)
    tf2.margin_top = Inches(0.2)
    p = tf2.paragraphs[0]
    p.text = "🛡️ Privacy Architecture"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    pts2 = [
        "100% Zero-PII on public blockchain ledger.",
        "Fully compliant with GDPR Article 17 (Right to Erasure).",
        "Strictly adheres to FERPA student educational privacy.",
        "Cryptographically collision-resistant SHA-256 digests."
    ]
    for pt in pts2:
        pp = tf2.add_paragraph()
        pp.text = "✔ " + pt
        pp.font.size = Pt(10.5)
        pp.font.color.rgb = RGBColor(226, 232, 240)
        pp.space_before = Pt(6)

    s_c3 = add_card(s16, Inches(8.8), Inches(1.8), col_w, Inches(3.6), bg_color=C_CARD_DARK, border_color=C_BORDER_DARK)
    tf3 = s_c3.text_frame
    tf3.margin_left = tf3.margin_right = Inches(0.2)
    tf3.margin_top = Inches(0.2)
    p = tf3.paragraphs[0]
    p.text = "⚡ Engineering Rigor"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(167, 139, 250)
    pts3 = [
        "17/17 Smart contract tests passing.",
        "12/12 Pytest backend tests passing.",
        "11-Stage automated E2E demo script verified on EVM.",
        "Production-ready React 18 & FastAPI integration."
    ]
    for pt in pts3:
        pp = tf3.add_paragraph()
        pp.text = "✔ " + pt
        pp.font.size = Pt(10.5)
        pp.font.color.rgb = RGBColor(226, 232, 240)
        pp.space_before = Pt(6)

    # Defense Callout Box
    q_box = add_card(s16, Inches(0.8), Inches(5.65), Inches(11.733), Inches(1.3), bg_color=RGBColor(30, 41, 59), border_color=RGBColor(96, 165, 250))
    tf_q = q_box.text_frame
    tf_q.margin_left = tf_q.margin_right = Inches(0.25)
    tf_q.margin_top = Inches(0.15)
    p = tf_q.paragraphs[0]
    p.text = "🎓 Ready for Questions & Viva Voce Technical Defense"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(96, 165, 250)
    p2 = tf_q.add_paragraph()
    p2.text = "Prepared to demonstrate live certificate minting, tamper detection, on-chain revocation, and explain smart contract opcode execution & cryptographic primitives."
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = RGBColor(226, 232, 240)
    p2.space_before = Pt(3)

    set_speaker_notes(s16,
        "In conclusion, CertLedger successfully demonstrates how blockchain technology and cryptographic hashing "
        "can be applied to solve the real-world diploma fraud crisis while respecting strict privacy regulations. "
        "We have validated every single function through unit tests, integration tests, and an 11-stage automated E2E demonstration. "
        "Thank you for your time and attention. I am now pleased to invite your questions and begin the technical defense."
    )

    prs.save(output_path)
    print(f"Presentation saved successfully to: {os.path.abspath(output_path)}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "CertLedger_Academic_Presentation.pptx"
    create_deck(out_file)
