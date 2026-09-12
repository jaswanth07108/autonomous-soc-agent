import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def create_submission_pdf(output_filename="Tech_Zephyr_4_Problem9_AegisSOC_Submission.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#3b82f6'),
        spaceAfter=12
    )
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        spaceAfter=4
    )
    callout_style = ParagraphStyle(
        'Callout',
        parent=body_style,
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor('#1e40af'),
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("AegisSOC — Autonomous SOC Investigation & Response Agent", title_style))
    story.append(Paragraph("Tech Zephyr 4.0 — Agentic AI Hackathon, IIT Bhubaneswar &bull; Problem Statement 9", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#3b82f6'), spaceAfter=12))

    # Key Links Table
    link_data = [
        [Paragraph("<b>GitHub Repository:</b>", body_style), Paragraph("<a href='https://github.com/jaswanth07108/autonomous-soc-agent'><u>https://github.com/jaswanth07108/autonomous-soc-agent</u></a>", body_style)],
        [Paragraph("<b>Demo Video (Google Drive):</b>", body_style), Paragraph("<a href='https://drive.google.com/file/d/1WFjr_cEy7Ov5L1GSmViUykJf2-T9e-j4/view?usp=drive_link'><font color='#2563eb'><u>Click Here to Watch Demo Video (Google Drive)</u></font></a>", body_style)],
        [Paragraph("<b>Direct Video URL:</b>", body_style), Paragraph("<font size='7.5' color='#475569'>https://drive.google.com/file/d/1WFjr_cEy7Ov5L1GSmViUykJf2-T9e-j4/view?usp=drive_link</font>", body_style)],
        [Paragraph("<b>Live Demo Port:</b>", body_style), Paragraph("FastAPI Backend: <code>http://127.0.0.1:8000</code> &bull; React UI: <code>http://localhost:5173</code>", body_style)]
    ]
    t_links = Table(link_data, colWidths=[160, 370])
    t_links.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_links)
    story.append(Spacer(1, 10))

    # Deliverable 1: Problem & Solution Brief
    story.append(Paragraph("1. Problem & Solution Brief", h2_style))
    story.append(Paragraph("<b>The Problem:</b> Modern Security Operations Centers face overwhelming alert fatigue (thousands of alerts daily, >70% false positives) and rely on brittle, rigid playbooks. Generic GenAI chatbots merely summarize text and cannot investigate, verify ground truth, or execute actions.", body_style))
    story.append(Paragraph("<b>Our Solution (AegisSOC):</b> An autonomous Agentic AI SOC system operating inside a local sandbox. Instead of predetermined pipelines or static LLM prompts, AegisSOC follows a closed-loop ReAct decision trajectory:", body_style))
    
    trajectory_box = [
        [Paragraph("<b>GOAL &rarr; OBSERVE &rarr; HYPOTHESIZE &rarr; DYNAMIC PLAN &rarr; TOOL EXECUTION &rarr; DECIDE &rarr; ACT &rarr; VERIFY &rarr; ADAPT</b>", ParagraphStyle('P_Center', parent=body_style, fontName='Helvetica-Bold', alignment=1, textColor=colors.HexColor('#1e40af')))]
    ]
    t_traj = Table(trajectory_box, colWidths=[530])
    t_traj.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#eff6ff')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#bfdbfe')),
        ('PADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(t_traj)
    story.append(Spacer(1, 8))

    # Deliverable 2: Key Capabilities & Differentiators
    story.append(Paragraph("2. System Innovations & Agentic Capabilities", h2_style))
    story.append(Paragraph("&bull; <b>Dynamic Planning Engine:</b> Evaluates evolving hypotheses and selectively picks tools (early termination on benign health checks after 2 tools vs. deep multi-tool escalation on credential breaches).", bullet_style))
    story.append(Paragraph("&bull; <b>Closed-Loop Action Verification:</b> Executes simulated perimeter blocks (<code>block_ip</code>) and immediately re-checks the sandbox (<code>verify_firewall</code>) to ensure enforcement.", bullet_style))
    story.append(Paragraph("&bull; <b>Real-time Contradiction Adaptation:</b> Ingests contradictory Duo MFA tokens mid-flight, queries corporate IAM directories for change tickets, and adapts conclusions to <code>LEGITIMATE_ADMIN_ACTIVITY</code>.", bullet_style))
    story.append(Paragraph("&bull; <b>Autonomous Failure Recovery:</b> Automatically recovers from simulated perimeter firewall timeouts via backup isolation routes and verifies enforcement.", bullet_style))
    story.append(Paragraph("&bull; <b>Interactive Step-by-Step UI:</b> Allows analysts and judges to step through the agent's internal hypothesis and tool selection reasoning one action at a time.", bullet_style))
    story.append(Spacer(1, 8))

    # Deliverable 3: Evaluation Benchmark Results
    story.append(Paragraph("3. Evaluation Benchmark Results (100% Passing)", h2_style))
    benchmark_data = [
        [Paragraph("<b>Evaluation Metric</b>", body_style), Paragraph("<b>Score</b>", body_style), Paragraph("<b>Verification Finding</b>", body_style)],
        [Paragraph("Investigation Accuracy", body_style), Paragraph("<b>100.0%</b>", body_style), Paragraph("All 5 controlled scenarios correctly diagnosed", body_style)],
        [Paragraph("False Positive Handling", body_style), Paragraph("<b>100.0%</b>", body_style), Paragraph("Benign Prometheus telemetry spared from blocking", body_style)],
        [Paragraph("Adaptation Success Rate", body_style), Paragraph("<b>100.0%</b>", body_style), Paragraph("Contradictory MFA tokens resolved via IAM directory", body_style)],
        [Paragraph("Action Verification Rate", body_style), Paragraph("<b>100.0%</b>", body_style), Paragraph("Perimeter firewall state actively verified", body_style)],
        [Paragraph("Tool Failure Recovery Rate", body_style), Paragraph("<b>100.0%</b>", body_style), Paragraph("Firewall timeout recovered via fallback route", body_style)],
        [Paragraph("Evidence Sufficiency Rate", body_style), Paragraph("<b>100.0%</b>", body_style), Paragraph("All required auth logs, CVEs, and assets retrieved", body_style)]
    ]
    t_bench = Table(benchmark_data, colWidths=[150, 70, 310])
    t_bench.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_bench)
    story.append(Spacer(1, 10))

    # Deliverable 4: 5 Controlled Demo Scenarios
    story.append(Paragraph("4. The 5 Hackathon Demo Scenarios", h2_style))
    story.append(Paragraph("&bull; <b>Scenario 1 (Successful Attack):</b> SSH brute force &rarr; root escalation &rarr; <code>ATTACK_SUCCESSFUL</code> &rarr; <code>BLOCK_IP</code> &rarr; verified.", bullet_style))
    story.append(Paragraph("&bull; <b>Scenario 2 (False Positive):</b> Port scan &rarr; benign Prometheus health check &rarr; early termination &rarr; <code>FALSE_POSITIVE</code> &rarr; no block.", bullet_style))
    story.append(Paragraph("&bull; <b>Scenario 3 (Attack Failed):</b> SQLi exploit attempt &rarr; WAF 403 Forbidden &rarr; target CVE patched &rarr; <code>ATTACK_FAILED</code> &rarr; monitor.", bullet_style))
    story.append(Paragraph("&bull; <b>Scenario 4 (Adaptation):</b> Suspicious external login &rarr; Duo MFA token injected &rarr; IAM ticket verified &rarr; <code>LEGITIMATE_ADMIN_ACTIVITY</code>.", bullet_style))
    story.append(Paragraph("&bull; <b>Scenario 5 (Failure Recovery):</b> Ransomware C2 &rarr; firewall timeout &rarr; autonomous fallback &rarr; <code>BLOCK_IP_RECOVERED</code> &rarr; verified.", bullet_style))
    story.append(Spacer(1, 8))

    # Deliverable 5: Security Statement & Execution
    story.append(Paragraph("5. Security Statement & How to Run", h2_style))
    story.append(Paragraph("<b>Security / Sandboxing:</b> All security operations operate strictly within an isolated local SQLite sandbox (<code>soc_sandbox.db</code>). Zero API keys, passwords, or tokens exist in the repository.", body_style))
    story.append(Paragraph("<b>How to Run:</b> Clone repository &rarr; Start Backend: <code>py main.py</code> (port 8000) &rarr; Start Frontend: <code>npm run dev</code> (port 5173).", body_style))

    doc.build(story)
    print(f"Submission PDF successfully generated at: {output_filename}")

if __name__ == "__main__":
    create_submission_pdf()
