import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def build_dark_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Premium Dark Technical Palette
    BG_COLOR = RGBColor(11, 16, 32)         # #0B1020 Deep Midnight Navy
    PANEL_BG = RGBColor(19, 27, 49)         # #131B31 Flat Dark Navy Panel
    PANEL_BORDER = RGBColor(37, 51, 77)     # #25334D Crisp subtle border
    CYAN = RGBColor(0, 229, 255)            # #00E5FF Electric Cyan accent
    TEAL = RGBColor(0, 201, 167)            # #00C9A7 Muted Teal / Positive Equilibrium
    INDIGO = RGBColor(100, 117, 255)        # #6475FF Restrained Indigo accent
    CORAL = RGBColor(244, 63, 94)           # #F43F5E Restrained Coral/Red for penalties
    WHITE = RGBColor(241, 245, 249)         # #F1F5F9 Soft White main text
    GREY = RGBColor(167, 177, 194)          # #A7B1C2 Cool Grey secondary text
    MUTED_DARK = RGBColor(71, 85, 105)      # #475569 Muted divider
    NASH_BG = RGBColor(6, 44, 38)           # #062C26 Dark Teal tint for Nash Cell
    NASH_BORDER = RGBColor(0, 201, 167)     # #00C9A7 Teal border for Nash Cell
    
    FONT_MAIN = "Arial"
    FONT_MONO = "Courier New"

    def add_dark_slide():
        slide = prs.slides.add_slide(blank_layout)
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = BG_COLOR
        
        # Solid background rectangle to guarantee dark canvas across all PPT viewers
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return slide

    def add_slide_header(slide, title_text, kicker="GAME THEORY ACADEMIC PROJECT // RESEARCH LAB"):
        # Kicker
        kb = slide.shapes.add_textbox(Inches(0.8), Inches(0.42), Inches(11.733), Inches(0.28))
        tf_k = kb.text_frame
        tf_k.word_wrap = True
        tf_k.margin_left = tf_k.margin_top = tf_k.margin_right = tf_k.margin_bottom = 0
        p_k = tf_k.paragraphs[0]
        r_k = p_k.add_run()
        r_k.text = kicker.upper()
        r_k.font.name = FONT_MAIN
        r_k.font.size = Pt(9.5)
        r_k.font.bold = True
        r_k.font.color.rgb = CYAN

        # Main Title
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.70), Inches(11.733), Inches(0.65))
        tf_t = tb.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        r_t = p_t.add_run()
        r_t.text = title_text
        r_t.font.name = FONT_MAIN
        r_t.font.size = Pt(22)
        r_t.font.bold = True
        r_t.font.color.rgb = WHITE

        # Subtle bottom line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.42), Inches(11.733), Inches(0.015))
        line.fill.solid()
        line.fill.fore_color.rgb = PANEL_BORDER
        line.line.fill.background()

        # Small cyan accent mark at the left of the divider
        accent = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.42), Inches(1.5), Inches(0.025))
        accent.fill.solid()
        accent.fill.fore_color.rgb = CYAN
        accent.line.fill.background()

    def add_panel(slide, left, top, width, height, bg_rgb=PANEL_BG, border_rgb=PANEL_BORDER, accent_strip=None):
        panel = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
        panel.fill.solid()
        panel.fill.fore_color.rgb = bg_rgb
        if border_rgb:
            panel.line.color.rgb = border_rgb
            panel.line.width = Pt(1)
        else:
            panel.line.fill.background()

        if accent_strip:
            strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.04))
            strip.fill.solid()
            strip.fill.fore_color.rgb = accent_strip
            strip.line.fill.background()

        return panel

    # ==============================================================
    # SLIDE 1: Title Slide (Cover)
    # ==============================================================
    s1 = add_dark_slide()

    # Network-node diffusion graphic on the right
    # Nodes coordinates
    nodes = [
        (Inches(9.2), Inches(2.2), CYAN, 0.16),
        (Inches(10.5), Inches(1.8), TEAL, 0.14),
        (Inches(11.8), Inches(2.5), INDIGO, 0.18),
        (Inches(9.8), Inches(3.4), CYAN, 0.22),
        (Inches(11.2), Inches(3.6), WHITE, 0.15),
        (Inches(12.3), Inches(4.2), TEAL, 0.14),
        (Inches(9.0), Inches(4.8), INDIGO, 0.16),
        (Inches(10.4), Inches(5.0), CYAN, 0.20),
        (Inches(11.9), Inches(5.5), TEAL, 0.15),
        (Inches(10.8), Inches(6.2), WHITE, 0.13),
    ]
    edges = [
        (0, 1), (1, 2), (0, 3), (1, 3), (1, 4), (2, 4),
        (2, 5), (3, 4), (3, 6), (4, 7), (4, 5), (5, 8),
        (6, 7), (7, 8), (7, 9), (8, 9)
    ]
    # Draw edges
    for e in edges:
        n1, n2 = nodes[e[0]], nodes[e[1]]
        x1, y1 = n1[0] + Inches(n1[3]/2), n1[1] + Inches(n1[3]/2)
        x2, y2 = n2[0] + Inches(n2[3]/2), n2[1] + Inches(n2[3]/2)
        connector = s1.shapes.add_connector(1, x1, y1, x2, y2) # 1 = msoConnectorStraight
        connector.line.color.rgb = RGBColor(30, 48, 78)
        connector.line.width = Pt(1)

    # Draw nodes
    for n in nodes:
        dot = s1.shapes.add_shape(MSO_SHAPE.OVAL, n[0], n[1], Inches(n[3]), Inches(n[3]))
        dot.fill.solid()
        dot.fill.fore_color.rgb = n[2]
        dot.line.color.rgb = BG_COLOR
        dot.line.width = Pt(1.5)

    # Left content area
    # Kicker
    k_box = s1.shapes.add_textbox(Inches(0.9), Inches(1.3), Inches(8.0), Inches(0.35))
    tf_k1 = k_box.text_frame
    tf_k1.word_wrap = True
    tf_k1.margin_left = tf_k1.margin_top = tf_k1.margin_right = tf_k1.margin_bottom = 0
    pk1 = tf_k1.paragraphs[0]
    rk1 = pk1.add_run()
    rk1.text = "B.TECH ACADEMIC CAPSTONE PROJECT  //  COURSE: GAME THEORY"
    rk1.font.name = FONT_MAIN
    rk1.font.size = Pt(11)
    rk1.font.bold = True
    rk1.font.color.rgb = CYAN

    # Title
    t_box = s1.shapes.add_textbox(Inches(0.9), Inches(1.8), Inches(7.8), Inches(2.0))
    tf_t1 = t_box.text_frame
    tf_t1.word_wrap = True
    tf_t1.margin_left = tf_t1.margin_top = tf_t1.margin_right = tf_t1.margin_bottom = 0
    pt1 = tf_t1.paragraphs[0]
    rt1 = pt1.add_run()
    rt1.text = "Game-Theoretic Analysis of Fake News Propagation and Platform Moderation Strategies"
    rt1.font.name = FONT_MAIN
    rt1.font.size = Pt(27)
    rt1.font.bold = True
    rt1.font.color.rgb = WHITE

    # Subtitle
    st_box = s1.shapes.add_textbox(Inches(0.9), Inches(3.9), Inches(7.8), Inches(0.45))
    tf_st1 = st_box.text_frame
    tf_st1.word_wrap = True
    tf_st1.margin_left = tf_st1.margin_top = tf_st1.margin_right = tf_st1.margin_bottom = 0
    pst1 = tf_st1.paragraphs[0]
    rst1 = pst1.add_run()
    rst1.text = "Game-Theoretic Contagion and Strategic Deterrence Analysis"
    rst1.font.name = FONT_MAIN
    rst1.font.size = Pt(14)
    rst1.font.color.rgb = GREY

    # Cyan divider line
    c_line = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(4.5), Inches(7.6), Inches(0.025))
    c_line.fill.solid()
    c_line.fill.fore_color.rgb = CYAN
    c_line.line.fill.background()

    # Authors panel card
    add_panel(s1, Inches(0.9), Inches(4.8), Inches(7.6), Inches(1.75), PANEL_BG, PANEL_BORDER, CYAN)
    
    ath_box = s1.shapes.add_textbox(Inches(1.15), Inches(4.95), Inches(7.1), Inches(1.45))
    tf_ath = ath_box.text_frame
    tf_ath.word_wrap = True
    tf_ath.margin_left = tf_ath.margin_top = tf_ath.margin_right = tf_ath.margin_bottom = 0

    p_a0 = tf_ath.paragraphs[0]
    r_a0 = p_a0.add_run()
    r_a0.text = "PROJECT AUTHORS & INVESTIGATORS"
    r_a0.font.name = FONT_MAIN
    r_a0.font.size = Pt(9.5)
    r_a0.font.bold = True
    r_a0.font.color.rgb = CYAN

    p_a1 = tf_ath.add_paragraph()
    p_a1.space_before = Pt(4)
    r_a1_1 = p_a1.add_run()
    r_a1_1.text = "• Shreshth Juneja  —  "
    r_a1_1.font.name = FONT_MAIN
    r_a1_1.font.size = Pt(12)
    r_a1_1.font.bold = True
    r_a1_1.font.color.rgb = WHITE
    r_a1_2 = p_a1.add_run()
    r_a1_2.text = "Registration Number: 2427030246"
    r_a1_2.font.name = FONT_MONO
    r_a1_2.font.size = Pt(11)
    r_a1_2.font.color.rgb = GREY

    p_a2 = tf_ath.add_paragraph()
    p_a2.space_before = Pt(3)
    r_a2_1 = p_a2.add_run()
    r_a2_1.text = "• Devaanshee Agarwal  —  "
    r_a2_1.font.name = FONT_MAIN
    r_a2_1.font.size = Pt(12)
    r_a2_1.font.bold = True
    r_a2_1.font.color.rgb = WHITE
    r_a2_2 = p_a2.add_run()
    r_a2_2.text = "Registration Number: 2427030504"
    r_a2_2.font.name = FONT_MONO
    r_a2_2.font.size = Pt(11)
    r_a2_2.font.color.rgb = GREY

    p_a3 = tf_ath.add_paragraph()
    p_a3.space_before = Pt(6)
    r_a3 = p_a3.add_run()
    r_a3.text = "Department of Computer Science & Engineering  |  Interactive Web-Native Architecture on Vercel"
    r_a3.font.name = FONT_MAIN
    r_a3.font.size = Pt(9.5)
    r_a3.font.color.rgb = TEAL

    # ==============================================================
    # SLIDE 2: Introduction & Problem Statement
    # ==============================================================
    s2 = add_dark_slide()
    add_slide_header(s2, "Introduction & Problem Statement: The Misinformation Dilemma", "GAME THEORY ACADEMIC PROJECT // 01 · FOUNDATIONS")

    # Two columns: Sharer Incentives vs Platform Dilemma
    col_w = Inches(5.72)
    top_pos = Inches(1.65)
    h_pos = Inches(4.25)

    # Left Column: Strategic Sharer
    add_panel(s2, Inches(0.8), top_pos, col_w, h_pos, PANEL_BG, PANEL_BORDER, CYAN)
    b_left = s2.shapes.add_textbox(Inches(1.05), top_pos + Inches(0.2), col_w - Inches(0.5), h_pos - Inches(0.35))
    tf_l = b_left.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0

    p_l0 = tf_l.paragraphs[0]
    r_l0 = p_l0.add_run()
    r_l0.text = "THE STRATEGIC SHARER (PLAYER 1)"
    r_l0.font.name = FONT_MAIN
    r_l0.font.size = Pt(12)
    r_l0.font.bold = True
    r_l0.font.color.rgb = CYAN

    items_l = [
        ("Virality & Attention Monetization:", "Content sharers and publishers optimize for social engagement, clicks, ad revenue, and peer influence, prioritizing emotional resonance over factual accuracy."),
        ("Asymmetric Transmission Advantage:", "Empirical network studies confirm fabricated narratives diffuse significantly faster, deeper, and more broadly than verified truth without incurrence of fact-checking friction."),
        ("Negative Spillover Externalities:", "Sharers internalize private engagement benefits (+5.0) while externalizing informational pollution and epistemic harm onto the public digital ecosystem."),
        ("Defensive Gaming:", "Sharers dynamically adapt dissemination tactics to circumvent passive rules, rendering static filtering policies ineffective.")
    ]
    for title, desc in items_l:
        p_t = tf_l.add_paragraph()
        p_t.space_before = Pt(8)
        r_t = p_t.add_run()
        r_t.text = "▸ " + title + " "
        r_t.font.name = FONT_MAIN
        r_t.font.size = Pt(10.5)
        r_t.font.bold = True
        r_t.font.color.rgb = WHITE

        r_d = p_t.add_run()
        r_d.text = desc
        r_d.font.name = FONT_MAIN
        r_d.font.size = Pt(10)
        r_d.font.color.rgb = GREY

    # Right Column: Platform Host
    add_panel(s2, Inches(6.81), top_pos, col_w, h_pos, PANEL_BG, PANEL_BORDER, INDIGO)
    b_right = s2.shapes.add_textbox(Inches(7.06), top_pos + Inches(0.2), col_w - Inches(0.5), h_pos - Inches(0.35))
    tf_r = b_right.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0

    p_r0 = tf_r.paragraphs[0]
    r_r0 = p_r0.add_run()
    r_r0.text = "THE PLATFORM OPERATOR (PLAYER 2)"
    r_r0.font.name = FONT_MAIN
    r_r0.font.size = Pt(12)
    r_r0.font.bold = True
    r_r0.font.color.rgb = INDIGO

    items_r = [
        ("Engagement vs. Ecosystem Trust:", "Social platforms face a fundamental trade-off: permissive viral reach maximizes short-term impressions but erodes long-term user retention and advertiser trust."),
        ("The Laissez-Faire Trap (Weak Moderation):", "Passive moderation saves operational compute costs but inflicts catastrophic brand damage (-4.0) when viral misinformation sparks advertiser boycotts and regulatory scrutiny."),
        ("Active Enforcement Overhead (Strong Moderation):", "Algorithmic downranking, reach dampening, and automated filtering require engineering investment, but defend platform health and advertiser safety (+3.0)."),
        ("Strategic Interdependence:", "Because payoffs depend directly on mutual actions, isolated technical filtering fails; the challenge must be resolved game-theoretically.")
    ]
    for title, desc in items_r:
        p_t = tf_r.add_paragraph()
        p_t.space_before = Pt(8)
        r_t = p_t.add_run()
        r_t.text = "▸ " + title + " "
        r_t.font.name = FONT_MAIN
        r_t.font.size = Pt(10.5)
        r_t.font.bold = True
        r_t.font.color.rgb = WHITE

        r_d = p_t.add_run()
        r_d.text = desc
        r_d.font.name = FONT_MAIN
        r_d.font.size = Pt(10)
        r_d.font.color.rgb = GREY

    # Bottom Callout Banner
    add_panel(s2, Inches(0.8), Inches(6.05), Inches(11.733), Inches(0.95), PANEL_BG, PANEL_BORDER, TEAL)
    b_bot = s2.shapes.add_textbox(Inches(1.05), Inches(6.12), Inches(11.233), Inches(0.8))
    tf_b = b_bot.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0

    p_b0 = tf_b.paragraphs[0]
    r_b0 = p_b0.add_run()
    r_b0.text = "CORE RESEARCH QUESTION & GAME-THEORETIC ALIGNMENT: "
    r_b0.font.name = FONT_MAIN
    r_b0.font.size = Pt(10)
    r_b0.font.bold = True
    r_b0.font.color.rgb = TEAL

    r_b1 = p_b0.add_run()
    r_b1.text = "How can the interaction between rational content creators and defensive platforms be mathematically modeled to identify stable equilibrium states? Can platform policy credible deterrence structurally eliminate viral fake news incentives at equilibrium without perpetual post-hoc censorship?"
    r_b1.font.name = FONT_MAIN
    r_b1.font.size = Pt(10)
    r_b1.font.color.rgb = WHITE

    # ==============================================================
    # SLIDE 3: Objectives and Academic Scope
    # ==============================================================
    s3 = add_dark_slide()
    add_slide_header(s3, "Objectives and Academic Scope: Research Framework", "GAME THEORY ACADEMIC PROJECT // 02 · RESEARCH FRAMEWORK")

    # 6 Compact Objective Panels (2 rows x 3 cols)
    obj_w = Inches(3.72)
    obj_h = Inches(2.05)
    xs = [Inches(0.8), Inches(4.81), Inches(8.81)]
    ys = [Inches(1.65), Inches(3.90)]

    objectives = [
        ("01 · STRATEGIC GAME FORMULATION", CYAN,
         "Model Content Sharers and Platforms as rational decision-makers in a 2-player non-cooperative game with calibrated action sets: {Spread, Do Not Spread} and {Weak, Strong Moderation}."),
        ("02 · 2×2 PAYOFF MATRIX", TEAL,
         "Construct a strategic normal-form matrix parameterizing virality rewards, brand damage (-4.0), operational moderation overhead, and compliance utilities under explicit ordering (u_Sharer, u_Platform)."),
        ("03 · EQUILIBRIUM & DOMINANCE PROOF", INDIGO,
         "Rigorously calculate player best-response correspondences, establish strict dominance of Strong Moderation (M ≻ W), and prove the unique pure-strategy Nash equilibrium at (N, M)."),
        ("04 · LOGISTIC CONTAGION COUPLING", CYAN,
         "Coupling microeconomic strategic payoffs with macroeconomic contagion via a discrete logistic recurrence with platform moderation damping factor (1 - m)."),
        ("05 · QUANTITATIVE METRICS EVALUATION", TEAL,
         "Measure cumulative exposure saturation, outbreak peak step shifting, total shielded users (4,044), and net percentage exposure reduction (40.5%)."),
        ("06 · PRODUCTION WEB-NATIVE LAB", INDIGO,
         "Deploy a zero-backend, client-side interactive simulation laboratory built in HTML5/CSS3/JavaScript (ES modules) with dual themes, hosted on Vercel edge infrastructure.")
    ]

    for idx, (title, accent, body) in enumerate(objectives):
        col = idx % 3
        row = idx // 3
        x, y = xs[col], ys[row]
        add_panel(s3, x, y, obj_w, obj_h, PANEL_BG, PANEL_BORDER, accent)

        box = s3.shapes.add_textbox(x + Inches(0.2), y + Inches(0.18), obj_w - Inches(0.4), obj_h - Inches(0.3))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        r0 = p0.add_run()
        r0.text = title
        r0.font.name = FONT_MAIN
        r0.font.size = Pt(11)
        r0.font.bold = True
        r0.font.color.rgb = accent

        p1 = tf.add_paragraph()
        p1.space_before = Pt(6)
        r1 = p1.add_run()
        r1.text = body
        r1.font.name = FONT_MAIN
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = GREY

    # Footer banner
    add_panel(s3, Inches(0.8), Inches(6.12), Inches(11.733), Inches(0.85), PANEL_BG, PANEL_BORDER)
    b_scope = s3.shapes.add_textbox(Inches(1.05), Inches(6.18), Inches(11.233), Inches(0.72))
    tf_sc = b_scope.text_frame
    tf_sc.word_wrap = True
    tf_sc.margin_left = tf_sc.margin_top = tf_sc.margin_right = tf_sc.margin_bottom = 0

    p_sc0 = tf_sc.paragraphs[0]
    r_sc0 = p_sc0.add_run()
    r_sc0.text = "ACADEMIC SCOPE & METHODOLOGICAL BOUNDARIES: "
    r_sc0.font.name = FONT_MAIN
    r_sc0.font.size = Pt(9.5)
    r_sc0.font.bold = True
    r_sc0.font.color.rgb = WHITE

    r_sc1 = p_sc0.add_run()
    r_sc1.text = "The project focuses rigorously on 2-player normal-form strategic deterrence and discrete logistic contagion. Excludes multi-stage stochastic games, dynamic network topology rewiring, and external third-party fact-checking debunking dynamics, maintaining a transparent and mathematically verifiable baseline."
    r_sc1.font.name = FONT_MAIN
    r_sc1.font.size = Pt(9.5)
    r_sc1.font.color.rgb = GREY

    # ==============================================================
    # SLIDE 4: Game-Theoretic Formulation: Players and Strategies
    # ==============================================================
    s4 = add_dark_slide()
    add_slide_header(s4, "Game-Theoretic Formulation: Players and Strategy Spaces", "GAME THEORY ACADEMIC PROJECT // 03 · FORMAL MODELING")

    col_w = Inches(5.72)
    top_pos = Inches(1.65)
    h_pos = Inches(5.35)

    # Left Column: Player 1
    add_panel(s4, Inches(0.8), top_pos, col_w, h_pos, PANEL_BG, PANEL_BORDER, CYAN)
    b_p1 = s4.shapes.add_textbox(Inches(1.05), top_pos + Inches(0.2), col_w - Inches(0.5), h_pos - Inches(0.35))
    tf_p1 = b_p1.text_frame
    tf_p1.word_wrap = True
    tf_p1.margin_left = tf_p1.margin_top = tf_p1.margin_right = tf_p1.margin_bottom = 0

    p_p1_0 = tf_p1.paragraphs[0]
    r_p1_0 = p_p1_0.add_run()
    r_p1_0.text = "PLAYER 1: CONTENT SHARER (PUBLISHER)"
    r_p1_0.font.name = FONT_MAIN
    r_p1_0.font.size = Pt(13)
    r_p1_0.font.bold = True
    r_p1_0.font.color.rgb = CYAN

    p_p1_sub = tf_p1.add_paragraph()
    p_p1_sub.space_before = Pt(3)
    r_p1_sub = p_p1_sub.add_run()
    r_p1_sub.text = "Strategic Goal: Maximize viral attention, click monetization, and peer influence."
    r_p1_sub.font.name = FONT_MAIN
    r_p1_sub.font.size = Pt(10)
    r_p1_sub.font.color.rgb = GREY

    strat_p1 = [
        ("STRATEGY S — SPREAD FAKE NEWS", CYAN,
         "Actively publish, amplify, or share sensationalized, unverified claims to generate viral attention, maximize retweets, and monetize ad revenue without fact-checking delays.",
         "Utility Impact: Yields +5.0 under weak moderation; drops to -2.0 when strongly penalized."),
        ("STRATEGY N — DO NOT SPREAD", TEAL,
         "Post organic, verified content or voluntarily refrain from sharing unverified rumors, adhering strictly to platform community guidelines.",
         "Utility Impact: Yields baseline utility +1.0 under weak moderation, and standard compliance utility 0.0 under strong moderation.")
    ]
    for s_title, s_color, s_body, s_util in strat_p1:
        p_st = tf_p1.add_paragraph()
        p_st.space_before = Pt(12)
        r_st = p_st.add_run()
        r_st.text = s_title
        r_st.font.name = FONT_MAIN
        r_st.font.size = Pt(11)
        r_st.font.bold = True
        r_st.font.color.rgb = s_color

        p_sb = tf_p1.add_paragraph()
        p_sb.space_before = Pt(3)
        r_sb = p_sb.add_run()
        r_sb.text = s_body
        r_sb.font.name = FONT_MAIN
        r_sb.font.size = Pt(10)
        r_sb.font.color.rgb = WHITE

        p_su = tf_p1.add_paragraph()
        p_su.space_before = Pt(2)
        r_su = p_su.add_run()
        r_su.text = "▸ " + s_util
        r_su.font.name = FONT_MAIN
        r_su.font.size = Pt(9.5)
        r_su.font.color.rgb = GREY

    # Right Column: Player 2
    add_panel(s4, Inches(6.81), top_pos, col_w, h_pos, PANEL_BG, PANEL_BORDER, INDIGO)
    b_p2 = s4.shapes.add_textbox(Inches(7.06), top_pos + Inches(0.2), col_w - Inches(0.5), h_pos - Inches(0.35))
    tf_p2 = b_p2.text_frame
    tf_p2.word_wrap = True
    tf_p2.margin_left = tf_p2.margin_top = tf_p2.margin_right = tf_p2.margin_bottom = 0

    p_p2_0 = tf_p2.paragraphs[0]
    r_p2_0 = p_p2_0.add_run()
    r_p2_0.text = "PLAYER 2: SOCIAL MEDIA PLATFORM (OPERATOR)"
    r_p2_0.font.name = FONT_MAIN
    r_p2_0.font.size = Pt(13)
    r_p2_0.font.bold = True
    r_p2_0.font.color.rgb = INDIGO

    p_p2_sub = tf_p2.add_paragraph()
    p_p2_sub.space_before = Pt(3)
    r_p2_sub = p_p2_sub.add_run()
    r_p2_sub.text = "Strategic Goal: Protect long-term platform trust, brand safety, and network stability."
    r_p2_sub.font.name = FONT_MAIN
    r_p2_sub.font.size = Pt(10)
    r_p2_sub.font.color.rgb = GREY

    strat_p2 = [
        ("STRATEGY W — WEAK MODERATION", CORAL,
         "Passive, laissez-faire moderation relying solely on post-hoc user flags; minimizes real-time compute and moderation payroll overhead.",
         "Utility Impact: Suffers severe brand damage (-4.0) if fake news spreads; earns 0.0 baseline under organic sharing."),
        ("STRATEGY M — STRONG MODERATION", TEAL,
         "Proactive algorithmic downranking, automated fact-checking flags, reach throttling, and account strikes against repeat misinformation publishers.",
         "Utility Impact: Successfully deters spread and protects advertiser trust (+3.0); maintains trusted ecosystem (+2.0) under organic sharing.")
    ]
    for s_title, s_color, s_body, s_util in strat_p2:
        p_st = tf_p2.add_paragraph()
        p_st.space_before = Pt(12)
        r_st = p_st.add_run()
        r_st.text = s_title
        r_st.font.name = FONT_MAIN
        r_st.font.size = Pt(11)
        r_st.font.bold = True
        r_st.font.color.rgb = s_color

        p_sb = tf_p2.add_paragraph()
        p_sb.space_before = Pt(3)
        r_sb = p_sb.add_run()
        r_sb.text = s_body
        r_sb.font.name = FONT_MAIN
        r_sb.font.size = Pt(10)
        r_sb.font.color.rgb = WHITE

        p_su = tf_p2.add_paragraph()
        p_su.space_before = Pt(2)
        r_su = p_su.add_run()
        r_su.text = "▸ " + s_util
        r_su.font.name = FONT_MAIN
        r_su.font.size = Pt(9.5)
        r_su.font.color.rgb = GREY

    # ==============================================================
    # SLIDE 5: Strategic Normal-Form Payoff Matrix
    # ==============================================================
    s5 = add_dark_slide()
    add_slide_header(s5, "Strategic Normal-Form Payoff Matrix", "GAME THEORY ACADEMIC PROJECT // 04 · MATRIX ANALYSIS")

    # Left: 2x2 Matrix Grid
    # Header cells
    col_w_m = Inches(3.6)
    row_h_m = Inches(1.9)
    x_off = Inches(0.8)
    y_off = Inches(1.65)

    # Column Headers: Weak Moderation (W) vs Strong Moderation (M)
    add_panel(s5, x_off + Inches(1.8), y_off, col_w_m, Inches(0.55), PANEL_BG, PANEL_BORDER, CORAL)
    tb_ch1 = s5.shapes.add_textbox(x_off + Inches(1.8), y_off + Inches(0.1), col_w_m, Inches(0.35))
    tf_ch1 = tb_ch1.text_frame
    tf_ch1.word_wrap = True
    p = tf_ch1.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Platform: Weak Moderation (W)"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = WHITE

    add_panel(s5, x_off + Inches(1.8) + col_w_m + Inches(0.15), y_off, col_w_m, Inches(0.55), PANEL_BG, PANEL_BORDER, TEAL)
    tb_ch2 = s5.shapes.add_textbox(x_off + Inches(1.8) + col_w_m + Inches(0.15), y_off + Inches(0.1), col_w_m, Inches(0.35))
    tf_ch2 = tb_ch2.text_frame
    tf_ch2.word_wrap = True
    p = tf_ch2.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "Platform: Strong Moderation (M)"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = TEAL

    # Row Headers: Spread (S) vs Do Not Spread (N)
    add_panel(s5, x_off, y_off + Inches(0.7), Inches(1.65), row_h_m, PANEL_BG, PANEL_BORDER, CYAN)
    tb_rh1 = s5.shapes.add_textbox(x_off + Inches(0.1), y_off + Inches(1.2), Inches(1.45), Inches(1.0))
    tf_rh1 = tb_rh1.text_frame
    tf_rh1.word_wrap = True
    p = tf_rh1.paragraphs[0]
    r = p.add_run()
    r.text = "Spread Fake News\n(S)"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = CYAN

    add_panel(s5, x_off, y_off + Inches(0.7) + row_h_m + Inches(0.15), Inches(1.65), row_h_m, PANEL_BG, PANEL_BORDER, WHITE)
    tb_rh2 = s5.shapes.add_textbox(x_off + Inches(0.1), y_off + Inches(0.7) + row_h_m + Inches(0.65), Inches(1.45), Inches(1.0))
    tf_rh2 = tb_rh2.text_frame
    tf_rh2.word_wrap = True
    p = tf_rh2.paragraphs[0]
    r = p.add_run()
    r.text = "Do Not Spread\n(N)"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = WHITE

    # 4 Payoff Cells
    # Cell 1: (S, W)
    x1, y1 = x_off + Inches(1.8), y_off + Inches(0.7)
    add_panel(s5, x1, y1, col_w_m, row_h_m, PANEL_BG, PANEL_BORDER)
    tb_c1 = s5.shapes.add_textbox(x1 + Inches(0.2), y1 + Inches(0.2), col_w_m - Inches(0.4), row_h_m - Inches(0.4))
    tf1 = tb_c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    r = p.add_run()
    r.text = "( 5.0 , -4.0 )"
    r.font.name = FONT_MONO
    r.font.size = Pt(20)
    r.font.bold = True
    r.font.color.rgb = WHITE

    p2 = tf1.add_paragraph()
    p2.space_before = Pt(4)
    r2 = p2.add_run()
    r2.text = "VIRAL EXPLOITATION"
    r2.font.name = FONT_MAIN
    r2.font.size = Pt(10)
    r2.font.bold = True
    r2.font.color.rgb = CORAL

    p3 = tf1.add_paragraph()
    p3.space_before = Pt(2)
    r3 = p3.add_run()
    r3.text = "Publisher harvests high clicks (+5.0); Platform incurs catastrophic advertiser & brand erosion (-4.0)."
    r3.font.name = FONT_MAIN
    r3.font.size = Pt(9)
    r3.font.color.rgb = GREY

    # Cell 2: (S, M)
    x2, y2 = x_off + Inches(1.8) + col_w_m + Inches(0.15), y_off + Inches(0.7)
    add_panel(s5, x2, y2, col_w_m, row_h_m, PANEL_BG, PANEL_BORDER)
    tb_c2 = s5.shapes.add_textbox(x2 + Inches(0.2), y2 + Inches(0.2), col_w_m - Inches(0.4), row_h_m - Inches(0.4))
    tf2 = tb_c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    r = p.add_run()
    r.text = "( -2.0 ,  3.0 )"
    r.font.name = FONT_MONO
    r.font.size = Pt(20)
    r.font.bold = True
    r.font.color.rgb = WHITE

    p2 = tf2.add_paragraph()
    p2.space_before = Pt(4)
    r2 = p2.add_run()
    r2.text = "ACTIVE DETERRENCE"
    r2.font.name = FONT_MAIN
    r2.font.size = Pt(10)
    r2.font.bold = True
    r2.font.color.rgb = CYAN

    p3 = tf2.add_paragraph()
    p3.space_before = Pt(2)
    r3 = p3.add_run()
    r3.text = "Publisher penalized by throttling (-2.0); Platform preserves brand reputation & advertiser trust (+3.0)."
    r3.font.name = FONT_MAIN
    r3.font.size = Pt(9)
    r3.font.color.rgb = GREY

    # Cell 3: (N, W)
    x3, y3 = x_off + Inches(1.8), y_off + Inches(0.7) + row_h_m + Inches(0.15)
    add_panel(s5, x3, y3, col_w_m, row_h_m, PANEL_BG, PANEL_BORDER)
    tb_c3 = s5.shapes.add_textbox(x3 + Inches(0.2), y3 + Inches(0.2), col_w_m - Inches(0.4), row_h_m - Inches(0.4))
    tf3 = tb_c3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    r = p.add_run()
    r.text = "( 1.0 ,  0.0 )"
    r.font.name = FONT_MONO
    r.font.size = Pt(20)
    r.font.bold = True
    r.font.color.rgb = WHITE

    p2 = tf3.add_paragraph()
    p2.space_before = Pt(4)
    r2 = p2.add_run()
    r2.text = "LAISSEZ-FAIRE BASELINE"
    r2.font.name = FONT_MAIN
    r2.font.size = Pt(10)
    r2.font.bold = True
    r2.font.color.rgb = GREY

    p3 = tf3.add_paragraph()
    p3.space_before = Pt(2)
    r3 = p3.add_run()
    r3.text = "Publisher earns organic social utility (+1.0); Platform operates in passive neutral status quo (0.0)."
    r3.font.name = FONT_MAIN
    r3.font.size = Pt(9)
    r3.font.color.rgb = GREY

    # Cell 4: (N, M) - NASH EQUILIBRIUM
    x4, y4 = x_off + Inches(1.8) + col_w_m + Inches(0.15), y_off + Inches(0.7) + row_h_m + Inches(0.15)
    add_panel(s5, x4, y4, col_w_m, row_h_m, NASH_BG, NASH_BORDER, TEAL)
    tb_c4 = s5.shapes.add_textbox(x4 + Inches(0.2), y4 + Inches(0.15), col_w_m - Inches(0.4), row_h_m - Inches(0.3))
    tf4 = tb_c4.text_frame
    tf4.word_wrap = True
    p = tf4.paragraphs[0]
    r = p.add_run()
    r.text = "( 0.0 ,  2.0 )"
    r.font.name = FONT_MONO
    r.font.size = Pt(20)
    r.font.bold = True
    r.font.color.rgb = TEAL

    p2 = tf4.add_paragraph()
    p2.space_before = Pt(3)
    r2 = p2.add_run()
    r2.text = "★ UNIQUE NASH EQUILIBRIUM"
    r2.font.name = FONT_MAIN
    r2.font.size = Pt(10.5)
    r2.font.bold = True
    r2.font.color.rgb = CYAN

    p3 = tf4.add_paragraph()
    p3.space_before = Pt(2)
    r3 = p3.add_run()
    r3.text = "Publisher maintains baseline adherence (0.0); Platform sustains high-trust ecosystem (+2.0)."
    r3.font.name = FONT_MAIN
    r3.font.size = Pt(9)
    r3.font.color.rgb = WHITE

    # Right Side Panel: Payoff Conventions & Structural Properties
    r_panel_x = Inches(10.15)
    r_panel_w = Inches(2.38)
    add_panel(s5, r_panel_x, y_off, r_panel_w, Inches(4.5), PANEL_BG, PANEL_BORDER, CYAN)
    tb_rp = s5.shapes.add_textbox(r_panel_x + Inches(0.18), y_off + Inches(0.2), r_panel_w - Inches(0.36), Inches(4.1))
    tf_rp = tb_rp.text_frame
    tf_rp.word_wrap = True
    tf_rp.margin_left = tf_rp.margin_top = tf_rp.margin_right = tf_rp.margin_bottom = 0

    p = tf_rp.paragraphs[0]
    r = p.add_run()
    r.text = "NOTATION & RULES"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = CYAN

    notes = [
        ("Payoff Tuple:", "(u_Sharer, u_Platform)"),
        ("Non-Zero-Sum:", "Total payoffs range from +1.0 in (S,W) to +2.0 in (N,M)."),
        ("Strict Dominance:", "Platform strictly prefers M regardless of Sharer action."),
        ("Stability Property:", "Neither agent has a profitable unilateral deviation at (N, M).")
    ]
    for n_title, n_desc in notes:
        p_n = tf_rp.add_paragraph()
        p_n.space_before = Pt(8)
        r_nt = p_n.add_run()
        r_nt.text = n_title + "\n"
        r_nt.font.name = FONT_MAIN
        r_nt.font.size = Pt(9.5)
        r_nt.font.bold = True
        r_nt.font.color.rgb = WHITE

        r_nd = p_n.add_run()
        r_nd.text = n_desc
        r_nd.font.name = FONT_MAIN
        r_nd.font.size = Pt(9)
        r_nd.font.color.rgb = GREY

    # Bottom Full-Width Summary Banner
    add_panel(s5, Inches(0.8), Inches(6.25), Inches(11.733), Inches(0.75), PANEL_BG, PANEL_BORDER, TEAL)
    tb_b5 = s5.shapes.add_textbox(Inches(1.05), Inches(6.32), Inches(11.233), Inches(0.6))
    tf_b5 = tb_b5.text_frame
    tf_b5.word_wrap = True
    tf_b5.margin_left = tf_b5.margin_top = tf_b5.margin_right = tf_b5.margin_bottom = 0

    p_b5 = tf_b5.paragraphs[0]
    r_b5_0 = p_b5.add_run()
    r_b5_0.text = "STRATEGIC TAKEAWAY: "
    r_b5_0.font.name = FONT_MAIN
    r_b5_0.font.size = Pt(9.5)
    r_b5_0.font.bold = True
    r_b5_0.font.color.rgb = TEAL

    r_b5_1 = p_b5.add_run()
    r_b5_1.text = "In the absence of credible enforcement, publishers have strong private incentives to exploit virality (+5.0). Credible strong moderation enforces negative returns (-2.0), shifting the system equilibrium to voluntary compliance (0.0, 2.0)."
    r_b5_1.font.name = FONT_MAIN
    r_b5_1.font.size = Pt(9.5)
    r_b5_1.font.color.rgb = WHITE

    # ==============================================================
    # SLIDE 6: Best Responses & Nash Equilibrium Proof: IESDS
    # ==============================================================
    s6 = add_dark_slide()
    add_slide_header(s6, "Best Responses & Nash Equilibrium Proof: IESDS", "GAME THEORY ACADEMIC PROJECT // 05 · MATHEMATICAL PROOF")

    col_w = Inches(5.72)
    top_pos = Inches(1.65)
    h_pos = Inches(3.9)

    # Step 1 Panel
    add_panel(s6, Inches(0.8), top_pos, col_w, h_pos, PANEL_BG, PANEL_BORDER, CYAN)
    b_st1 = s6.shapes.add_textbox(Inches(1.05), top_pos + Inches(0.2), col_w - Inches(0.5), h_pos - Inches(0.35))
    tf_st1 = b_st1.text_frame
    tf_st1.word_wrap = True
    tf_st1.margin_left = tf_st1.margin_top = tf_st1.margin_right = tf_st1.margin_bottom = 0

    p = tf_st1.paragraphs[0]
    r = p.add_run()
    r.text = "STEP 1: PLATFORM STRICT DOMINANCE PROOF"
    r.font.name = FONT_MAIN
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = CYAN

    p_eq1 = tf_st1.add_paragraph()
    p_eq1.space_before = Pt(8)
    r = p_eq1.add_run()
    r.text = "Evaluate Platform's utility u_2 across all possible Sharer actions:"
    r.font.name = FONT_MAIN
    r.font.size = Pt(10)
    r.font.color.rgb = GREY

    p_in1 = tf_st1.add_paragraph()
    p_in1.space_before = Pt(6)
    r = p_in1.add_run()
    r.text = "• If Sharer plays Spread (S):\n  u_2(S, M) = 3.0  >  u_2(S, W) = -4.0   [Δ = +7.0]"
    r.font.name = FONT_MONO
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = TEAL

    p_in2 = tf_st1.add_paragraph()
    p_in2.space_before = Pt(4)
    r = p_in2.add_run()
    r.text = "• If Sharer plays Do Not Spread (N):\n  u_2(N, M) = 2.0  >  u_2(N, W) = 0.0    [Δ = +2.0]"
    r.font.name = FONT_MONO
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = TEAL

    p_res1 = tf_st1.add_paragraph()
    p_res1.space_before = Pt(8)
    r = p_res1.add_run()
    r.text = "Strict Dominance Conclusion:\n"
    r.font.name = FONT_MAIN
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = WHITE
    r_sub = p_res1.add_run()
    r_sub.text = "Strategy M strictly dominates W (M ≻ W). Weak Moderation is strictly dominated and eliminated via Iterated Elimination of Strictly Dominated Strategies (IESDS)."
    r_sub.font.name = FONT_MAIN
    r_sub.font.size = Pt(9.5)
    r_sub.font.color.rgb = GREY

    # Step 2 Panel
    add_panel(s6, Inches(6.81), top_pos, col_w, h_pos, PANEL_BG, PANEL_BORDER, INDIGO)
    b_st2 = s6.shapes.add_textbox(Inches(7.06), top_pos + Inches(0.2), col_w - Inches(0.5), h_pos - Inches(0.35))
    tf_st2 = b_st2.text_frame
    tf_st2.word_wrap = True
    tf_st2.margin_left = tf_st2.margin_top = tf_st2.margin_right = tf_st2.margin_bottom = 0

    p = tf_st2.paragraphs[0]
    r = p.add_run()
    r.text = "STEP 2: SHARER'S BEST RESPONSE IN REDUCED GAME"
    r.font.name = FONT_MAIN
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = INDIGO

    p_eq2 = tf_st2.add_paragraph()
    p_eq2.space_before = Pt(8)
    r = p_eq2.add_run()
    r.text = "Under common knowledge of rationality, Sharer eliminates column W:"
    r.font.name = FONT_MAIN
    r.font.size = Pt(10)
    r.font.color.rgb = GREY

    p_in3 = tf_st2.add_paragraph()
    p_in3.space_before = Pt(6)
    r = p_in3.add_run()
    r.text = "• In reduced game (Column M), Sharer compares:\n  u_1(S, M) = -2.0  (Throttling penalties)\n  u_1(N, M) =  0.0  (Standard compliance)"
    r.font.name = FONT_MONO
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = CYAN

    p_in4 = tf_st2.add_paragraph()
    p_in4.space_before = Pt(4)
    r = p_in4.add_run()
    r.text = "• Best Response Condition:\n  Since 0.0 > -2.0  ⇒  BR_1(M) = {N}"
    r.font.name = FONT_MONO
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = TEAL

    p_res2 = tf_st2.add_paragraph()
    p_res2.space_before = Pt(8)
    r = p_res2.add_run()
    r.text = "Best-Response Conclusion:\n"
    r.font.name = FONT_MAIN
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = WHITE
    r_sub = p_res2.add_run()
    r_sub.text = "Knowing that the platform will play M, the Sharer's unique optimal choice is N. Spreading is actively deterred."
    r_sub.font.name = FONT_MAIN
    r_sub.font.size = Pt(9.5)
    r_sub.font.color.rgb = GREY

    # Bottom Full-Width Highlight: Unique Pure-Strategy Nash Equilibrium
    add_panel(s6, Inches(0.8), Inches(5.7), Inches(11.733), Inches(1.35), NASH_BG, NASH_BORDER, TEAL)
    b_nash = s6.shapes.add_textbox(Inches(1.05), Inches(5.78), Inches(11.233), Inches(1.2))
    tf_n = b_nash.text_frame
    tf_n.word_wrap = True
    tf_n.margin_left = tf_n.margin_top = tf_n.margin_right = tf_n.margin_bottom = 0

    p = tf_n.paragraphs[0]
    r = p.add_run()
    r.text = "★ UNIQUE PURE-STRATEGY NASH EQUILIBRIUM: (N, M) = (Do Not Spread, Strong Moderation)"
    r.font.name = FONT_MAIN
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = CYAN

    p2 = tf_n.add_paragraph()
    p2.space_before = Pt(4)
    r = p2.add_run()
    r.text = "Equilibrium Payoffs: u*(N, M) = (0.0, 2.0)  |  Strictly Self-Enforcing"
    r.font.name = FONT_MONO
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = TEAL

    p3 = tf_n.add_paragraph()
    p3.space_before = Pt(3)
    r = p3.add_run()
    r.text = "Deterrence Theorem: Because the platform's threat of aggressive enforcement is strictly credible and self-interested (u_2(S,M) > u_2(S,W)), rational creators voluntarily withhold false narratives, establishing ex-ante deterrence without perpetual censorship."
    r.font.name = FONT_MAIN
    r.font.size = Pt(9.5)
    r.font.color.rgb = WHITE

    # ==============================================================
    # SLIDE 7: System Architecture: Modern Web-Native Pipeline
    # ==============================================================
    s7 = add_dark_slide()
    add_slide_header(s7, "System Architecture: Modern Web-Native Pipeline", "GAME THEORY ACADEMIC PROJECT // 06 · SYSTEM DESIGN")

    # 4 Horizontal Stages
    stage_w = Inches(2.65)
    stage_h = Inches(3.6)
    stage_xs = [Inches(0.8), Inches(3.82), Inches(6.84), Inches(9.86)]

    stages = [
        ("01 · PRESENTATION", CYAN, [
            ("UI Framework", "Semantic HTML5 Single Page"),
            ("Design Engine", "Modern CSS3 Variables & Flexbox"),
            ("Dual Themes", "Cyberpunk Dark & Editorial Light"),
            ("Visualizations", "Dynamic HTML5 Canvas & Inline SVG")
        ]),
        ("02 · CONTROLLER", TEAL, [
            ("Core Language", "Vanilla JavaScript (ES6+ Modules)"),
            ("State Store", "Reactive Single-Source-of-Truth"),
            ("Event Coordinator", "Decoupled Custom Event Dispatcher"),
            ("DOM Sync", "Real-Time < 2ms Reactive Mutator")
        ]),
        ("03 · COMPUTATION", INDIGO, [
            ("Equilibrium Solver", "Normal-Form Matrix Nash Engine"),
            ("Contagion Engine", "Discrete Logistic Recurrence Loop"),
            ("Complexity", "O(T) Constant Memory Footprint"),
            ("Zero Dependencies", "Pure Mathematical JS Implementation")
        ]),
        ("04 · DEPLOYMENT", WHITE, [
            ("Bundler", "Vite 6 Production Optimizer"),
            ("Hosting", "Vercel Global Edge CDN"),
            ("Serverless", "Zero Cloud Database / API Latency"),
            ("Availability", "100% Client-Side In-Browser Execution")
        ])
    ]

    for idx, (st_title, st_accent, items) in enumerate(stages):
        x = stage_xs[idx]
        add_panel(s7, x, Inches(1.65), stage_w, stage_h, PANEL_BG, PANEL_BORDER, st_accent)

        # Connector arrow
        if idx < 3:
            ar_box = s7.shapes.add_textbox(x + stage_w, Inches(3.2), Inches(0.37), Inches(0.5))
            tf_ar = ar_box.text_frame
            tf_ar.margin_left = tf_ar.margin_top = tf_ar.margin_right = tf_ar.margin_bottom = 0
            p = tf_ar.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            r = p.add_run()
            r.text = "→"
            r.font.name = FONT_MAIN
            r.font.size = Pt(20)
            r.font.bold = True
            r.font.color.rgb = CYAN

        box = s7.shapes.add_textbox(x + Inches(0.18), Inches(1.85), stage_w - Inches(0.36), stage_h - Inches(0.4))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = st_title
        r.font.name = FONT_MAIN
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = st_accent

        for label, val in items:
            p_i = tf.add_paragraph()
            p_i.space_before = Pt(8)
            r_l = p_i.add_run()
            r_l.text = label + "\n"
            r_l.font.name = FONT_MAIN
            r_l.font.size = Pt(9.5)
            r_l.font.bold = True
            r_l.font.color.rgb = WHITE

            r_v = p_i.add_run()
            r_v.text = val
            r_v.font.name = FONT_MAIN
            r_v.font.size = Pt(8.5)
            r_v.font.color.rgb = GREY

    # Bottom Execution Loop Card
    add_panel(s7, Inches(0.8), Inches(5.45), Inches(11.733), Inches(1.5), PANEL_BG, PANEL_BORDER, CYAN)
    b_loop = s7.shapes.add_textbox(Inches(1.05), Inches(5.55), Inches(11.233), Inches(1.3))
    tf_lp = b_loop.text_frame
    tf_lp.word_wrap = True
    tf_lp.margin_left = tf_lp.margin_top = tf_lp.margin_right = tf_lp.margin_bottom = 0

    p = tf_lp.paragraphs[0]
    r = p.add_run()
    r.text = "REACTIVE REAL-TIME EXECUTION LIFECYCLE"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = CYAN

    p2 = tf_lp.add_paragraph()
    p2.space_before = Pt(4)
    r = p2.add_run()
    r.text = "1. User Interaction: "
    r.font.bold = True
    r.font.color.rgb = WHITE
    r_sub = p2.add_run()
    r_sub.text = "Sliders for N, I₀, β, m or matrix input edits trigger standard DOM input events.\n"
    r_sub.font.color.rgb = GREY

    r = p2.add_run()
    r.text = "2. State Dispatch: "
    r.font.bold = True
    r.font.color.rgb = WHITE
    r_sub = p2.add_run()
    r_sub.text = "src/main.js intercepts inputs, updates single-state store, and broadcasts change notifications.\n"
    r_sub.font.color.rgb = GREY

    r = p2.add_run()
    r.text = "3. Pure Computation: "
    r.font.bold = True
    r.font.color.rgb = WHITE
    r_sub = p2.add_run()
    r_sub.text = "src/model.js evaluates the discrete logistic loop & Nash solver in < 2ms without network overhead.\n"
    r_sub.font.color.rgb = GREY

    r = p2.add_run()
    r.text = "4. DOM & Canvas Paint: "
    r.font.bold = True
    r.font.color.rgb = WHITE
    r_sub = p2.add_run()
    r_sub.text = "Real-time Canvas redraws diffusion curves and shaded prevention area; KPI cards update instantly."
    r_sub.font.color.rgb = GREY

    # ==============================================================
    # SLIDE 8: Discrete Logistic Propagation Model
    # ==============================================================
    s8 = add_dark_slide()
    add_slide_header(s8, "Discrete Logistic Propagation Model: Mathematical Formulation", "GAME THEORY ACADEMIC PROJECT // 07 · CONTAGION MECHANICS")

    # Large Equation Panel
    add_panel(s8, Inches(0.8), Inches(1.65), Inches(11.733), Inches(1.3), PANEL_BG, PANEL_BORDER, CYAN)
    b_eq = s8.shapes.add_textbox(Inches(1.05), Inches(1.75), Inches(11.233), Inches(1.1))
    tf_eq = b_eq.text_frame
    tf_eq.word_wrap = True
    tf_eq.margin_left = tf_eq.margin_top = tf_eq.margin_right = tf_eq.margin_bottom = 0

    p = tf_eq.paragraphs[0]
    r = p.add_run()
    r.text = "I_{t+1} = min( N , max( 0 , I_t + β · (1 - m) · I_t · ( 1 - I_t / N ) ) )"
    r.font.name = FONT_MONO
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = CYAN

    p_sub = tf_eq.add_paragraph()
    p_sub.space_before = Pt(4)
    r_sub = p_sub.add_run()
    r_sub.text = "Discrete Recurrence for Misinformation Contagion with Defensive Platform Moderation Damping (1 - m)"
    r_sub.font.name = FONT_MAIN
    r_sub.font.size = Pt(10.5)
    r_sub.font.color.rgb = GREY

    # 6 Compact Parameter Breakdown Panels (2 rows x 3 cols)
    pw = Inches(3.72)
    ph = Inches(1.85)
    xs = [Inches(0.8), Inches(4.81), Inches(8.81)]
    ys = [Inches(3.15), Inches(5.15)]

    params = [
        ("N · TOTAL POPULATION", "10,000 Users", CYAN,
         "Carrying capacity ceiling representing the finite susceptible digital community."),
        ("I_t · CURRENT EXPOSURE", "I_t ∈ [0, N]", TEAL,
         "Cumulative individuals exposed to or infected by the false narrative at observation step t."),
        ("I_0 · INITIAL SEEDS", "100 Nodes (1.0%)", INDIGO,
         "Patient-zero seed cohort introducing the fabricated claim into the network."),
        ("β · SHARING PROPENSITY", "0.35 per contact", CYAN,
         "Baseline peer-to-peer viral transmission probability in the absence of moderation friction."),
        ("m · MODERATION INTENSITY", "0.50 (m ∈ [0, 1])", TEAL,
         "Platform intervention effectiveness: downranking, algorithmic filtering, and warning tags."),
        ("β_eff · EFFECTIVE VIRALITY", "β · (1 - m) = 0.175", INDIGO,
         "Net transmission rate under active moderation policy (0.35 × 0.50 = 0.175).")
    ]

    for idx, (p_name, p_val, p_acc, p_desc) in enumerate(params):
        col = idx % 3
        row = idx // 3
        x, y = xs[col], ys[row]
        add_panel(s8, x, y, pw, ph, PANEL_BG, PANEL_BORDER, p_acc)

        box = s8.shapes.add_textbox(x + Inches(0.18), y + Inches(0.15), pw - Inches(0.36), ph - Inches(0.3))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = p_name
        r.font.name = FONT_MAIN
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = p_acc

        p_v = tf.add_paragraph()
        p_v.space_before = Pt(3)
        r_v = p_v.add_run()
        r_v.text = p_val
        r_v.font.name = FONT_MONO
        r_v.font.size = Pt(13)
        r_v.font.bold = True
        r_v.font.color.rgb = WHITE

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(3)
        r_d = p_d.add_run()
        r_d.text = p_desc
        r_d.font.name = FONT_MAIN
        r_d.font.size = Pt(9)
        r_d.font.color.rgb = GREY

    # ==============================================================
    # SLIDE 9: Simulation Results: Baseline vs. Moderated Contagion
    # ==============================================================
    s9 = add_dark_slide()
    add_slide_header(s9, "Simulation Results: Baseline vs. Moderated Contagion", "GAME THEORY ACADEMIC PROJECT // 08 · QUANTITATIVE FINDINGS")

    # Parameters Banner
    add_panel(s9, Inches(0.8), Inches(1.65), Inches(11.733), Inches(0.55), PANEL_BG, PANEL_BORDER)
    b_prm = s9.shapes.add_textbox(Inches(1.05), Inches(1.72), Inches(11.233), Inches(0.4))
    tf_prm = b_prm.text_frame
    tf_prm.word_wrap = True
    tf_prm.margin_left = tf_prm.margin_top = tf_prm.margin_right = tf_prm.margin_bottom = 0

    p = tf_prm.paragraphs[0]
    r = p.add_run()
    r.text = "SIMULATION PARAMETERS:  N = 10,000  ·  I₀ = 100  ·  β = 0.35  ·  m = 0.50  ·  T = 30 STEPS"
    r.font.name = FONT_MONO
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = CYAN

    # 4 Large KPI Cards
    kpi_w = Inches(2.75)
    kpi_h = Inches(2.15)
    kpi_xs = [Inches(0.8), Inches(3.79), Inches(6.78), Inches(9.78)]

    kpis = [
        ("BASELINE EXPOSURE", "9,981", CORAL, "99.8% Saturated", "Laissez-faire (m = 0.00) saturates almost entire population."),
        ("MODERATED EXPOSURE", "5,936", INDIGO, "59.4% Final Exposure", "Active policy (m = 0.50) successfully caps viral propagation."),
        ("USERS PROTECTED", "4,044", TEAL, "Infections Prevented", "Absolute individuals shielded from fake narrative exposure."),
        ("EXPOSURE REDUCTION", "40.5%", CYAN, "Calculated Reduction", "Empirical percentage decrease in cumulative narrative saturation.")
    ]

    for idx, (k_title, k_val, k_acc, k_sub, k_desc) in enumerate(kpis):
        x = kpi_xs[idx]
        add_panel(s9, x, Inches(2.35), kpi_w, kpi_h, PANEL_BG, PANEL_BORDER, k_acc)

        box = s9.shapes.add_textbox(x + Inches(0.18), Inches(2.5), kpi_w - Inches(0.36), kpi_h - Inches(0.3))
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = k_title
        r.font.name = FONT_MAIN
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = k_acc

        p_v = tf.add_paragraph()
        p_v.space_before = Pt(3)
        r_v = p_v.add_run()
        r_v.text = k_val
        r_v.font.name = FONT_MONO
        r_v.font.size = Pt(26)
        r_v.font.bold = True
        r_v.font.color.rgb = WHITE

        p_s = tf.add_paragraph()
        p_s.space_before = Pt(2)
        r_s = p_s.add_run()
        r_s.text = k_sub
        r_s.font.name = FONT_MAIN
        r_s.font.size = Pt(9.5)
        r_s.font.bold = True
        r_s.font.color.rgb = k_acc

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(3)
        r_d = p_d.add_run()
        r_d.text = k_desc
        r_d.font.name = FONT_MAIN
        r_d.font.size = Pt(8.5)
        r_d.font.color.rgb = GREY

    # Bottom Findings & Analysis Panel
    add_panel(s9, Inches(0.8), Inches(4.7), Inches(11.733), Inches(2.25), PANEL_BG, PANEL_BORDER, TEAL)
    b_find = s9.shapes.add_textbox(Inches(1.05), Inches(4.85), Inches(11.233), Inches(2.0))
    tf_f = b_find.text_frame
    tf_f.word_wrap = True
    tf_f.margin_left = tf_f.margin_top = tf_f.margin_right = tf_f.margin_bottom = 0

    p = tf_f.paragraphs[0]
    r = p.add_run()
    r.text = "KEY EMPIRICAL & ANALYTICAL TAKEAWAYS"
    r.font.name = FONT_MAIN
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = TEAL

    takeaways = [
        ("Sigmoidal Saturation Flattening:", "Laissez-faire baseline policy (m = 0.00) rapidly infects 9,981 individuals (99.8% saturation). Active moderation policy (m = 0.50) successfully dampens effective virality, capping final exposure at 5,936 individuals."),
        ("Inflection Point Shift & Response Latency:", "Maximum infection acceleration is significantly delayed from Step 14 (baseline) to Step 28 (moderated), buying critical operational response time for verification systems and public fact-checkers."),
        ("Defensive Intervention Delta:", "The green shaded region between the two simulated curves visualizes exactly 4,044 individuals completely shielded from narrative contact, representing a verified 40.5% exposure reduction.")
    ]
    for t_head, t_body in takeaways:
        p_t = tf_f.add_paragraph()
        p_t.space_before = Pt(5)
        r_h = p_t.add_run()
        r_h.text = "▸ " + t_head + " "
        r_h.font.name = FONT_MAIN
        r_h.font.size = Pt(9.5)
        r_h.font.bold = True
        r_h.font.color.rgb = WHITE

        r_b = p_t.add_run()
        r_b.text = t_body
        r_b.font.name = FONT_MAIN
        r_b.font.size = Pt(9)
        r_b.font.color.rgb = GREY

    # ==============================================================
    # SLIDE 10: Application Demonstration
    # ==============================================================
    s10 = add_dark_slide()
    add_slide_header(s10, "Application Demonstration: Interactive Web Interface", "GAME THEORY ACADEMIC PROJECT // 09 · SOFTWARE ARTIFACT")

    # Left & Right screenshot frames
    f_w = Inches(5.72)
    f_h = Inches(4.1)
    top_pos = Inches(1.65)

    # Frame 1: Payoff Matrix
    add_panel(s10, Inches(0.8), top_pos, f_w, f_h, PANEL_BG, PANEL_BORDER, CYAN)
    # Add screenshot image inside frame
    img_path1 = "screenshots/02_payoff_matrix.png"
    if os.path.exists(img_path1):
        s10.shapes.add_picture(img_path1, Inches(0.85), top_pos + Inches(0.1), Inches(5.62), Inches(3.95))

    # Caption 1 below
    add_panel(s10, Inches(0.8), Inches(5.9), f_w, Inches(1.15), PANEL_BG, PANEL_BORDER)
    b_c1 = s10.shapes.add_textbox(Inches(1.0), Inches(5.98), f_w - Inches(0.4), Inches(1.0))
    tf_c1 = b_c1.text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_top = tf_c1.margin_right = tf_c1.margin_bottom = 0
    p = tf_c1.paragraphs[0]
    r = p.add_run()
    r.text = "MODULE 01: STRATEGIC PAYOFF MATRIX & NASH EQUILIBRIUM"
    r.font.name = FONT_MAIN
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = CYAN
    p2 = tf_c1.add_paragraph()
    p2.space_before = Pt(3)
    r2 = p2.add_run()
    r2.text = "Interactive 2×2 payoff matrix with automated best-response computation, live Nash equilibrium detection (0.0, 2.0), interactive payoff editing, and scenario preset loading."
    r2.font.name = FONT_MAIN
    r2.font.size = Pt(8.5)
    r2.font.color.rgb = GREY

    # Frame 2: Diffusion Graph
    add_panel(s10, Inches(6.81), top_pos, f_w, f_h, PANEL_BG, PANEL_BORDER, TEAL)
    img_path2 = "screenshots/03_diffusion_graph.png"
    if os.path.exists(img_path2):
        s10.shapes.add_picture(img_path2, Inches(6.86), top_pos + Inches(0.1), Inches(5.62), Inches(3.95))

    # Caption 2 below
    add_panel(s10, Inches(6.81), Inches(5.9), f_w, Inches(1.15), PANEL_BG, PANEL_BORDER)
    b_c2 = s10.shapes.add_textbox(Inches(7.01), Inches(5.98), f_w - Inches(0.4), Inches(1.0))
    tf_c2 = b_c2.text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_top = tf_c2.margin_right = tf_c2.margin_bottom = 0
    p = tf_c2.paragraphs[0]
    r = p.add_run()
    r.text = "MODULE 02: DISCRETE LOGISTIC SIMULATOR & ANALYTICS"
    r.font.name = FONT_MAIN
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = TEAL
    p2 = tf_c2.add_paragraph()
    p2.space_before = Pt(3)
    r2 = p2.add_run()
    r2.text = "Interactive parameter sliders (N, I₀, β, m, T) powering dual-curve Canvas visualization, real-time exposure comparison, and instant calculation of infections prevented (4,044)."
    r2.font.name = FONT_MAIN
    r2.font.size = Pt(8.5)
    r2.font.color.rgb = GREY

    # ==============================================================
    # SLIDE 11: Conclusion and Future Scope
    # ==============================================================
    s11 = add_dark_slide()
    add_slide_header(s11, "Conclusion and Future Research Directions", "GAME THEORY ACADEMIC PROJECT // 10 · SYNTHESIS")

    col_w = Inches(5.72)
    top_pos = Inches(1.65)
    h_pos = Inches(5.35)

    # Left Column: Strategic Takeaways
    add_panel(s11, Inches(0.8), top_pos, col_w, h_pos, PANEL_BG, PANEL_BORDER, CYAN)
    b_c_left = s11.shapes.add_textbox(Inches(1.05), top_pos + Inches(0.2), col_w - Inches(0.5), h_pos - Inches(0.35))
    tf_cl = b_c_left.text_frame
    tf_cl.word_wrap = True
    tf_cl.margin_left = tf_cl.margin_top = tf_cl.margin_right = tf_cl.margin_bottom = 0

    p = tf_cl.paragraphs[0]
    r = p.add_run()
    r.text = "THREE CORE STRATEGIC TAKEAWAYS"
    r.font.name = FONT_MAIN
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = CYAN

    takeaways_c = [
        ("1. Strategic Deterrence Mechanism:", "Misinformation propagation is fundamentally driven by economic incentives; passive moderation inevitably induces viral exploitation (+5.0). Credible strong moderation enforces negative returns (-2.0), flipping the publisher's best response."),
        ("2. Spontaneous Equilibrium Compliance:", "Because Strong Moderation is strictly dominant (M ≻ W), the unique Nash equilibrium (N, M) achieves voluntary compliance, preventing misinformation ex-ante without perpetual manual post-hoc censorship."),
        ("3. Macro-Micro Quantitative Validation:", "Coupling game-theoretic utility to a discrete logistic contagion model demonstrates that moderate intervention (m = 0.50) achieves a verified 40.5% exposure reduction (4,044 protected users)."),
        ("4. Zero-Backend Production Tool:", "Delivered a lightweight, client-side web application in pure JavaScript/HTML5 deployed on Vercel, proving high accessibility for academic demonstration.")
    ]
    for t_head, t_body in takeaways_c:
        p_t = tf_cl.add_paragraph()
        p_t.space_before = Pt(8)
        r_h = p_t.add_run()
        r_h.text = "▸ " + t_head + "\n"
        r_h.font.name = FONT_MAIN
        r_h.font.size = Pt(10)
        r_h.font.bold = True
        r_h.font.color.rgb = WHITE

        r_b = p_t.add_run()
        r_b.text = t_body
        r_b.font.name = FONT_MAIN
        r_b.font.size = Pt(9)
        r_b.font.color.rgb = GREY

    # Right Column: Future Directions
    add_panel(s11, Inches(6.81), top_pos, col_w, h_pos, PANEL_BG, PANEL_BORDER, INDIGO)
    b_c_right = s11.shapes.add_textbox(Inches(7.06), top_pos + Inches(0.2), col_w - Inches(0.5), h_pos - Inches(0.35))
    tf_cr = b_c_right.text_frame
    tf_cr.word_wrap = True
    tf_cr.margin_left = tf_cr.margin_top = tf_cr.margin_right = tf_cr.margin_bottom = 0

    p = tf_cr.paragraphs[0]
    r = p.add_run()
    r.text = "ACADEMIC LIMITATIONS & FUTURE RESEARCH"
    r.font.name = FONT_MAIN
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = INDIGO

    future_c = [
        ("1. Network Topology Generalization:", "Extend the homogeneous well-mixed population model to heterogeneous scale-free (Barabási–Albert) contact graphs to analyze targeted hub moderation."),
        ("2. Bayesian Incomplete Information Games:", "Model uncertainty where the platform faces heterogeneous publisher types (e.g., financially motivated spammers vs. ideologically committed zealots)."),
        ("3. Dynamic Repeated Games with Reputation:", "Expand the static single-period interaction into an infinitely repeated game with discount factor δ, modeling publisher reputation histories and punishment strategies."),
        ("4. Adversarial Machine Learning Co-Evolution:", "Simulate multi-agent reinforcement learning where publishers dynamically evolve adversarial text evasion tactics against platform automated classifiers.")
    ]
    for t_head, t_body in future_c:
        p_t = tf_cr.add_paragraph()
        p_t.space_before = Pt(8)
        r_h = p_t.add_run()
        r_h.text = "▸ " + t_head + "\n"
        r_h.font.name = FONT_MAIN
        r_h.font.size = Pt(10)
        r_h.font.bold = True
        r_h.font.color.rgb = WHITE

        r_b = p_t.add_run()
        r_b.text = t_body
        r_b.font.name = FONT_MAIN
        r_b.font.size = Pt(9)
        r_b.font.color.rgb = GREY

    # ==============================================================
    # SLIDE 12: Completely Blank Slide (Requirement)
    # ==============================================================
    # "Slide 12 — MUST REMAIN COMPLETELY BLANK.
    # Do not add a title, footer, slide number, background graphics, or any other element to slide 12."
    s12 = prs.slides.add_slide(blank_layout)
    # Strictly NO shapes, NO text, NO background shape, NO lines. Exactly 0 shapes.

    out_file = "Game_Theory_Project_Dark_Theme.pptx"
    prs.save(out_file)
    print(f"Redesigned presentation generated successfully at: {out_file}")

if __name__ == "__main__":
    build_dark_presentation()
