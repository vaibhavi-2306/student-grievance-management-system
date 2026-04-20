import streamlit as st
from datetime import datetime
from ai_analysis import analyze_complaint
from database import (
    insert_complaint,
    fetch_filtered_complaints,
    update_complaint_status,
    DB_CONNECTED,
)
st.set_page_config(
    page_title="Student Grievance Portal",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
 
    html, body, .stApp, [data-testid="stAppViewContainer"],
    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background-color: #f5f6fa !important;
        font-family: 'Inter', sans-serif !important;
    }
 
    .stApp p, .stApp span, .stApp label, .stApp div,
    .stApp li, .stApp h1, .stApp h2, .stApp h3, .stApp h4,
    [data-testid="stMarkdownContainer"] * {
        color: #1c1c2e !important;
    }
 
    /* NAV */
    .top-nav {
        background: #0f172a;
        padding: 0 2.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 60px;
    }
    .nav-logo { width:34px; height:34px; background:#1d4ed8; border-radius:8px;
        display:inline-flex; align-items:center; justify-content:center;
        font-size:18px; margin-right:12px; vertical-align:middle; }
    .nav-name  { color:#ffffff !important; font-size:1rem; font-weight:700; }
    .nav-sub   { color:#94a3b8 !important; font-size:0.72rem; display:block; }
    .nav-date  { color:#64748b !important; font-size:0.8rem; }
 
    /* HERO */
    .hero {
        background: linear-gradient(105deg, #0f172a 0%, #1e3a5f 55%, #1d4ed8 100%);
        padding: 2.2rem 2.5rem 2rem;
        margin-bottom: 0;
    }
    .hero-crumb { color:#64748b !important; font-size:0.76rem; margin-bottom:8px; }
    .hero-crumb span { color:#93c5fd !important; }
    .hero h2 { color:#ffffff !important; font-size:1.55rem; font-weight:700; margin:0 0 6px; }
    .hero p  { color:#93c5fd !important; font-size:0.88rem; margin:0; max-width:620px; }
 
    /* TABS */
    .stTabs [data-baseweb="tab-list"] {
        background:#ffffff !important;
        border-bottom: 2px solid #e2e8f0 !important;
        border-radius:0 !important; padding:0 1.5rem !important;
        gap:0 !important; box-shadow:none !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius:0 !important; font-weight:600 !important;
        font-size:0.88rem !important; color:#64748b !important;
        padding:14px 22px !important;
        border-bottom:3px solid transparent !important;
        margin-bottom:-2px !important; background:transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color:#1d4ed8 !important;
        border-bottom:3px solid #1d4ed8 !important;
        background:transparent !important;
    }
 
    /* PANEL */
    .panel {
        background:#ffffff; border:1px solid #e2e8f0;
        border-radius:12px; padding:1.8rem 2rem;
        margin-bottom:1.5rem;
    }
    .panel-title { font-size:1rem; font-weight:700; color:#0f172a !important; margin:0 0 3px; }
    .panel-sub   { font-size:0.82rem; color:#64748b !important; margin:0 0 1.4rem; }
 
    /* INPUTS */
    .stTextInput > div > div > input {
        background:#f8fafc !important; color:#0f172a !important;
        border:1.5px solid #cbd5e1 !important; border-radius:8px !important;
        font-size:0.92rem !important; padding:11px 14px !important;
    }
    .stTextInput > div > div > input:focus {
        background:#fff !important; border-color:#1d4ed8 !important;
        box-shadow:0 0 0 3px rgba(29,78,216,.1) !important;
    }
    .stTextInput > div > div > input::placeholder { color:#94a3b8 !important; }
 
    .stTextArea > div > div > textarea {
        background:#f8fafc !important; color:#0f172a !important;
        border:1.5px solid #cbd5e1 !important; border-radius:8px !important;
        font-size:0.92rem !important; padding:11px 14px !important;
        line-height:1.65 !important;
    }
    .stTextArea > div > div > textarea:focus {
        background:#fff !important; border-color:#1d4ed8 !important;
        box-shadow:0 0 0 3px rgba(29,78,216,.1) !important;
    }
    .stTextArea > div > div > textarea::placeholder { color:#94a3b8 !important; }
 
    .stTextInput label, .stTextArea label, .stSelectbox label {
        color:#374151 !important; font-weight:600 !important;
        font-size:0.84rem !important; letter-spacing:.2px !important;
    }
 
    .stSelectbox > div > div {
        background:#f8fafc !important; color:#0f172a !important;
        border:1.5px solid #cbd5e1 !important; border-radius:8px !important;
    }
    .stSelectbox > div > div > div { color:#0f172a !important; }
 
    /* BUTTONS */
    .stButton > button[kind="primary"] {
        background:#1d4ed8 !important; color:white !important;
        border:none !important; border-radius:8px !important;
        padding:.65rem 2rem !important; font-weight:600 !important;
        font-size:.9rem !important;
    }
    .stButton > button[kind="primary"]:hover {
        background:#1e40af !important;
        box-shadow:0 4px 14px rgba(29,78,216,.35) !important;
    }
    .stButton > button {
        background:#fff !important; color:#374151 !important;
        border:1.5px solid #d1d5db !important; border-radius:8px !important;
        font-weight:500 !important;
    }
    .stButton > button:hover { border-color:#1d4ed8 !important; color:#1d4ed8 !important; }
 
    /* METRICS */
    [data-testid="metric-container"] {
        background:white !important; border:1px solid #e2e8f0 !important;
        border-radius:10px !important; padding:1rem 1.2rem !important;
    }
    [data-testid="metric-container"] label { color:#64748b !important; font-size:.78rem !important; }
    [data-testid="stMetricValue"] { color:#0f172a !important; font-weight:700 !important; }
 
    /* BADGES */
    .badge {
        display:inline-flex; align-items:center; gap:4px;
        padding:3px 10px; border-radius:20px;
        font-size:.77rem; font-weight:600; letter-spacing:.3px;
    }
    .bc { background:#fef2f2; color:#b91c1c !important; border:1px solid #fecaca; }
    .bh { background:#fff7ed; color:#c2410c !important; border:1px solid #fed7aa; }
    .bm { background:#fefce8; color:#854d0e !important; border:1px solid #fde68a; }
    .bl { background:#f0fdf4; color:#166534 !important; border:1px solid #bbf7d0; }
    .bn { background:#fef2f2; color:#b91c1c !important; border:1px solid #fecaca; }
    .bnu{ background:#f8fafc; color:#475569 !important; border:1px solid #cbd5e1; }
    .bp { background:#f0fdf4; color:#166534 !important; border:1px solid #bbf7d0; }
    .bpe{ background:#eff6ff; color:#1d4ed8 !important; border:1px solid #bfdbfe; }
    .bi { background:#fefce8; color:#854d0e !important; border:1px solid #fde68a; }
    .br { background:#f0fdf4; color:#166534 !important; border:1px solid #bbf7d0; }
 
    /* CONFIRMATION BOX */
    .confirm-box {
        background:#f0fdf4; border:1px solid #bbf7d0;
        border-left:5px solid #16a34a; border-radius:10px;
        padding:1.2rem 1.5rem; margin:1.2rem 0;
    }
    .confirm-box strong { color:#14532d !important; }
    .confirm-box p      { color:#166534 !important; margin:.4rem 0 0; font-size:.88rem; }
    .ref-id { font-family:monospace; font-size:.85rem; font-weight:700;
        color:#15803d !important; letter-spacing:1px; }
 
    /* ERROR BOX */
    .err-box {
        background:#fef2f2; border:1px solid #fecaca;
        border-left:5px solid #dc2626; border-radius:10px;
        padding:1.2rem 1.5rem; margin:1.2rem 0;
        color:#7f1d1d !important;
    }
 
    /* TABLE */
    .ct { width:100%; border-collapse:collapse; font-size:.85rem; border-radius:10px; overflow:hidden; }
    .ct thead tr  { background:#0f172a; }
    .ct thead th  { color:#e2e8f0 !important; padding:11px 14px; text-align:left;
        font-weight:600; font-size:.76rem; text-transform:uppercase; letter-spacing:.5px; }
    .ct tbody td  { padding:11px 14px; border-bottom:1px solid #f1f5f9;
        color:#1c1c2e !important; background:#fff; vertical-align:top; }
    .ct tbody td strong { color:#0f172a !important; font-size:.88rem; }
    .ct tbody td small  { color:#94a3b8 !important; font-size:.74rem; }
    .ct tbody tr:hover td { background:#f8fafc !important; }
    .ct tbody tr.crit td  { background:#fef2f2 !important; border-left:3px solid #dc2626; }
 
    /* MISC */
    hr { border:none; border-top:1px solid #e2e8f0 !important; margin:1.5rem 0; }
    .stCaption, small { color:#64748b !important; }
    .stAlert { border-radius:8px !important; }
    [data-testid="stNotification"] * { color:#1c1c2e !important; }
    [data-testid="stSpinner"] p { color:#374151 !important; }
    [data-testid="stVerticalBlock"] > div { background:transparent !important; }
    code { background:#f1f5f9 !important; color:#1e3a5f !important; border-radius:4px; padding:2px 5px; }
    .streamlit-expanderHeader { background:#f8fafc !important; color:#374151 !important;
        border-radius:8px !important; font-weight:600 !important; font-size:.85rem !important; }
    thead th { color:#e2e8f0 !important; }
    tbody td  { color:#1c1c2e !important; }
    footer { visibility:hidden; }
    #MainMenu { visibility:hidden; }
    [data-testid="stToolbar"] { display:none; }
</style>
""", unsafe_allow_html=True)
 
def pbadge(p):
    cls = {"Critical":"bc","High":"bh","Medium":"bm","Low":"bl"}.get(p,"bl")
    dot = {"Critical":"🔴","High":"🟠","Medium":"🟡","Low":"🟢"}.get(p,"⚪")
    return f'<span class="badge {cls}">{dot} {p}</span>'
 
def sbadge(s):
    cls = {"Negative":"bn","Neutral":"bnu","Positive":"bp"}.get(s,"bnu")
    sym = {"Negative":"↓","Neutral":"→","Positive":"↑"}.get(s,"→")
    return f'<span class="badge {cls}">{sym} {s}</span>'
 
def stbadge(s):
    cls = {"Pending":"bpe","In Progress":"bi","Resolved":"br"}.get(s,"bpe")
    sym = {"Pending":"●","In Progress":"◑","Resolved":"✓"}.get(s,"●")
    return f'<span class="badge {cls}">{sym} {s}</span>'
 
def fdt(d):
    try:
        dt = datetime.fromisoformat(d.replace("Z","+00:00"))
        return dt.strftime("%d %b %Y, %I:%M %p")
    except Exception:
        return d or "—"
 
today = datetime.now().strftime("%A, %d %B %Y")
st.markdown(f"""
<div class="top-nav">
    <div style="display:flex;align-items:center">
        <span class="nav-logo">🎓</span>
        <div style="display:inline-block">
            <span class="nav-name">GrievanceDesk</span>
            <span class="nav-sub">Student Services Division</span>
        </div>
    </div>
    <span class="nav-date">{today}</span>
</div>
""", unsafe_allow_html=True)
 
if not DB_CONNECTED:
    st.markdown("""
    <div class="err-box">
        <strong>⚠️ Service Unavailable</strong><br>
        The database connection could not be established.
        Please verify your <code>.env</code> credentials and try again.
    </div>
    """, unsafe_allow_html=True)
    st.stop()
 

tab1, tab2 = st.tabs(["   Submit a Grievance   ", "   Authority Panel   "])
 
with tab1:
 
    st.markdown("""
    <div class="hero">
        <div class="hero-crumb">Home &nbsp;›&nbsp; <span>Submit Grievance</span></div>
        <h2>Submit a Grievance</h2>
        <p>Use this portal to raise a concern or complaint with the college administration.
           All submissions are reviewed and responded to within the prescribed resolution timeline.</p>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("<br>", unsafe_allow_html=True)
    fc, ic = st.columns([3, 1], gap="large")
 
    with fc:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<p class="panel-title">Grievance Details</p>', unsafe_allow_html=True)
        st.markdown('<p class="panel-sub">All fields are mandatory. Please provide accurate information.</p>', unsafe_allow_html=True)
 
        title = st.text_input("Subject", placeholder="e.g. Result not updated after re-evaluation", max_chars=150)
 
        category = st.selectbox("Category", [
            "Select a category…",
            "Academic — Examination / Results",
            "Academic — Attendance / Leave",
            "Academic — Faculty / Teaching Quality",
            "Infrastructure — Hostel / Accommodation",
            "Infrastructure — Library / Lab / Facilities",
            "Administration — Fee / Scholarship",
            "Administration — Certificate / Documents",
            "Student Services — Transport / Canteen",
            "Disciplinary / Misconduct",
            "Other"
        ])
 
        description = st.text_area("Description", placeholder=(
            "Describe the issue in detail — include relevant dates, "
            "names of departments or persons involved, and any prior action taken."
        ), height=200)
 
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.button("Submit Grievance", type="primary")
 
        if submitted:
            if not title.strip():
                st.warning("Please enter the subject of your grievance.")
            elif category == "Select a category…":
                st.warning("Please select a category.")
            elif len(description.strip()) < 20:
                st.warning("Please provide a more detailed description.")
            else:
                with st.spinner("Submitting your grievance…"):
                    ai = analyze_complaint(title.strip(), f"{title} {category} {description}")
                    try:
                        saved = insert_complaint(
                            title=f"[{category}] {title.strip()}",
                            description=description.strip(),
                            sentiment=ai["sentiment"],
                            urgency=ai["urgency"],
                            priority=ai["priority"]
                        )
                        ref = str(saved.get("id",""))[:8].upper() if saved else "N/A"
                        ok = True
                    except Exception as ex:
                        ok, err = False, str(ex)
 
                if ok:
                    st.markdown(f"""
                    <div class="confirm-box">
                        <strong>✔ &nbsp; Grievance Submitted Successfully</strong>
                        <p>Your grievance has been recorded and forwarded to the concerned department.
                           You will be notified once it is reviewed by the authority.</p>
                        <p style="margin-top:.8rem">Reference ID &nbsp;
                            <span class="ref-id">GD-{ref}</span>
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
 
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.markdown("**Priority**")
                        st.markdown(pbadge(ai["priority"]), unsafe_allow_html=True)
                    with c2:
                        st.markdown("**Urgency**")
                        u = "🔴 High" if ai["urgency"] == "High" else "🟢 Normal"
                        st.markdown(f"<span style='font-weight:600;color:#1c1c2e!important'>{u}</span>", unsafe_allow_html=True)
                    with c3:
                        st.markdown("**Status**")
                        st.markdown(stbadge("Pending"), unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="err-box"><strong>Submission Failed</strong><br>{err}</div>', unsafe_allow_html=True)
 
        st.markdown('</div>', unsafe_allow_html=True)
 
    with ic:
        st.markdown("""
        <div class="panel">
            <p class="panel-title">Guidelines</p>
            <p class="panel-sub">Please read before submitting.</p>
            <ul style="font-size:.84rem;line-height:2;padding-left:1.1rem">
                <li>Submit one grievance per issue.</li>
                <li>Provide accurate, factual information.</li>
                <li>Avoid duplicate submissions.</li>
                <li>Use respectful and formal language.</li>
                <li>Grievances are reviewed within <strong>5–7 working days</strong>.</li>
            </ul>
        </div>
 
        <div class="panel">
            <p class="panel-title">Contact the Office</p>
            <p style="font-size:.83rem;line-height:2;color:#374151!important">
                <strong>Student Welfare Office</strong><br>
                Room 102, Administrative Block<br>
                Mon – Fri &nbsp;|&nbsp; 9:00 AM – 5:00 PM<br><br>
                ☎ &nbsp;1800-XXX-XXXX<br>
                ✉ &nbsp;grievance@college.edu
            </p>
        </div>
 
        <div class="panel">
            <p class="panel-title">Resolution Timeline</p>
            <table style="width:100%;font-size:.82rem;border-collapse:collapse">
                <tr>
                    <td style="padding:5px 0;color:#374151!important">🔴 Critical</td>
                    <td style="padding:5px 0;text-align:right;color:#374151!important"><strong>Within 24 hrs</strong></td>
                </tr>
                <tr>
                    <td style="padding:5px 0;color:#374151!important">🟠 High</td>
                    <td style="padding:5px 0;text-align:right;color:#374151!important"><strong>2 – 3 days</strong></td>
                </tr>
                <tr>
                    <td style="padding:5px 0;color:#374151!important">🟡 Medium</td>
                    <td style="padding:5px 0;text-align:right;color:#374151!important"><strong>5 days</strong></td>
                </tr>
                <tr>
                    <td style="padding:5px 0;color:#374151!important">🟢 Low</td>
                    <td style="padding:5px 0;text-align:right;color:#374151!important"><strong>7 days</strong></td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

with tab2:
 
    # ── PASSWORD GATE ──
    if "admin_auth" not in st.session_state:
        st.session_state.admin_auth = False
 
    if not st.session_state.admin_auth:
        st.markdown("""
        <div class="hero">
            <div class="hero-crumb">Home &nbsp;›&nbsp; <span>Authority Panel</span></div>
            <h2>Authority Panel — Restricted Access</h2>
            <p>This section is accessible to authorised college administration staff only.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        _, lc, _ = st.columns([1, 1.4, 1])
        with lc:
            st.markdown('<div class="panel">', unsafe_allow_html=True)
            st.markdown("""
            <div style="text-align:center;margin-bottom:1.5rem">
                <div style="font-size:2.4rem;margin-bottom:.6rem">🔒</div>
                <p class="panel-title" style="text-align:center;font-size:1.05rem">Admin Sign In</p>
                <p class="panel-sub" style="text-align:center">Enter your credentials to access the Authority Panel.</p>
            </div>
            """, unsafe_allow_html=True)
            pwd = st.text_input("Password", type="password", placeholder="Enter admin password")
            if st.button("Sign In", type="primary", use_container_width=True):
                if pwd == "admin123":
                    st.session_state.admin_auth = True
                    st.rerun()
                else:
                    st.markdown('<div class="err-box"><strong>Access Denied</strong><br>Incorrect password. Please try again.</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<p style="text-align:center;font-size:.78rem;color:#94a3b8!important;margin-top:.8rem">Forgot password? Contact <strong>it-support@college.edu</strong></p>', unsafe_allow_html=True)
        st.stop()
 
    # ── SIGN OUT ──
    _, so_col = st.columns([5.5, 1])
    with so_col:
        if st.button("🔓 Sign Out"):
            st.session_state.admin_auth = False
            st.rerun()
 
    st.markdown("""
    <div class="hero">
        <div class="hero-crumb">Home &nbsp;›&nbsp; <span>Authority Panel</span></div>
        <h2>Grievance Management — Authority Panel</h2>
        <p>Review, prioritise and update the resolution status of student grievances.
           Records are automatically sorted by priority level.</p>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    try:
        all_c = fetch_filtered_complaints("All", "All")
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        all_c = []
 
    total    = len(all_c)
    crit_n   = sum(1 for c in all_c if c.get("priority") == "Critical")
    high_n   = sum(1 for c in all_c if c.get("priority") == "High")
    pend_n   = sum(1 for c in all_c if c.get("status")   == "Pending")
    prog_n   = sum(1 for c in all_c if c.get("status")   == "In Progress")
    res_n    = sum(1 for c in all_c if c.get("status")   == "Resolved")
 
    m1,m2,m3,m4,m5,m6 = st.columns(6)
    with m1: st.metric("Total Records", total)
    with m2: st.metric("🔴 Critical", crit_n)
    with m3: st.metric("🟠 High", high_n)
    with m4: st.metric("⏳ Pending", pend_n)
    with m5: st.metric("🔄 In Progress", prog_n)
    with m6: st.metric("✅ Resolved", res_n)
 
    st.markdown("---")
 
    # Filters
    f1, f2, f3, f4 = st.columns([1.2, 1.2, 1.5, 0.8])
    with f1:
        pf = st.selectbox("Priority", ["All","Critical","High","Medium","Low"])
    with f2:
        sf = st.selectbox("Status", ["All","Pending","In Progress","Resolved"])
    with f3:
        cf = st.selectbox("Category", [
            "All Categories",
            "Academic — Examination / Results",
            "Academic — Attendance / Leave",
            "Academic — Faculty / Teaching Quality",
            "Infrastructure — Hostel / Accommodation",
            "Infrastructure — Library / Lab / Facilities",
            "Administration — Fee / Scholarship",
            "Administration — Certificate / Documents",
            "Student Services — Transport / Canteen",
            "Disciplinary / Misconduct",
            "Other"
        ])
    with f4:
        st.markdown("<br>", unsafe_allow_html=True)
        st.button("🔄 Refresh")
 
    try:
        complaints = fetch_filtered_complaints(pf, sf)
    except Exception as e:
        st.error(f"Error: {e}")
        complaints = []
 
    if cf != "All Categories":
        key = cf.split("—")[0].strip().lower()
        complaints = [c for c in complaints if key in c.get("title","").lower()]
 
    st.markdown(
        f"<p style='font-size:.82rem;color:#64748b!important;margin:.7rem 0'>"
        f"Showing <strong style='color:#0f172a!important'>{len(complaints)}</strong> record(s)</p>",
        unsafe_allow_html=True
    )
 
    if not complaints:
        st.markdown("""
        <div style="text-align:center;padding:4rem 2rem">
            <div style="font-size:2.5rem;margin-bottom:1rem">📭</div>
            <p style="font-size:.95rem;font-weight:600;color:#475569!important">No records found</p>
            <p style="font-size:.84rem;color:#94a3b8!important">No grievances match the current filters.</p>
        </div>
        """, unsafe_allow_html=True)
    else:

        rows = ""
        for c in complaints:
            pri = c.get("priority","Low")
            sen = c.get("sentiment","Neutral")
            sts = c.get("status","Pending")
            ttl = c.get("title","—")
            dsc = c.get("description","—")
            urg = c.get("urgency","Low")
            cdt = fdt(c.get("created_at",""))
            dsc_s = (dsc[:105]+"…") if len(dsc)>105 else dsc
            rcls = "crit" if pri=="Critical" else ""
            urg_html = (
                '<span style="color:#dc2626!important;font-weight:600;font-size:.8rem">● High</span>'
                if urg=="High" else
                '<span style="color:#16a34a!important;font-size:.8rem">● Normal</span>'
            )
            rows += f"""
            <tr class="{rcls}">
                <td><strong>{ttl}</strong><br><small>{cdt}</small></td>
                <td style="max-width:200px">{dsc_s}</td>
                <td>{sbadge(sen)}</td>
                <td>{urg_html}</td>
                <td>{pbadge(pri)}</td>
                <td>{stbadge(sts)}</td>
            </tr>"""
 
        st.markdown(f"""
        <table class="ct">
            <thead><tr>
                <th>Subject &amp; Date</th>
                <th>Description</th>
                <th>Sentiment</th>
                <th>Urgency</th>
                <th>Priority</th>
                <th>Status</th>
            </tr></thead>
            <tbody>{rows}</tbody>
        </table>
        """, unsafe_allow_html=True)
 

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown('<p class="panel-title">Update Grievance Status</p>', unsafe_allow_html=True)
        st.markdown('<p class="panel-sub">Select a record and assign the appropriate resolution status.</p>', unsafe_allow_html=True)
 
        opts = {
            f"{c.get('title','Untitled')}  ·  {fdt(c.get('created_at',''))}  [{c.get('status','Pending')}]": c.get("id")
            for c in complaints
        }
 
        u1, u2, u3 = st.columns([3, 1.4, 0.9])
        with u1:
            sel = st.selectbox("Select Record", list(opts.keys()), label_visibility="collapsed")
        with u2:
            new_s = st.selectbox("New Status", ["Pending","In Progress","Resolved"], label_visibility="collapsed")
        with u3:
            upd = st.button("Update", type="primary", use_container_width=True)
 
        if upd and sel:
            try:
                ok = update_complaint_status(opts[sel], new_s)
                if ok:
                    st.success(f"Status updated to **{new_s}**. Click Refresh to reflect changes.")
                else:
                    st.error("Update failed. Please try again.")
            except Exception as ex:
                st.error(f"Error: {ex}")
 
        st.markdown('</div>', unsafe_allow_html=True)
 
        # Legend
        with st.expander("Status & Priority Reference"):
            l1, l2, l3 = st.columns(3)
            with l1:
                st.markdown("**Priority Levels**")
                for p in ["Critical","High","Medium","Low"]:
                    st.markdown(pbadge(p), unsafe_allow_html=True)
            with l2:
                st.markdown("**Sentiment**")
                for s in ["Negative","Neutral","Positive"]:
                    st.markdown(sbadge(s), unsafe_allow_html=True)
            with l3:
                st.markdown("**Status**")
                for s in ["Pending","In Progress","Resolved"]:
                    st.markdown(stbadge(s), unsafe_allow_html=True)
st.markdown("""
<hr style="margin-top:3rem">
<p style="text-align:center;font-size:.76rem;color:#94a3b8!important;padding-bottom:1.5rem">
    GrievanceDesk &nbsp;·&nbsp; Student Services Division &nbsp;·&nbsp;
    For urgent matters, contact the Student Welfare Office directly.
</p>
""", unsafe_allow_html=True)