# 📋 Student Grievence Portal
### A College Project | Built with Streamlit + Supabase + NLTK

---

## 📁 Project Folder Structure

```
complaint_management/
│
├── app.py              ← Main file
├── ai_analysis.py      ← AI logic: sentiment, urgency, priority
├── database.py         ← Supabase connection and queries
├── requirements.txt    ← Python libraries to install
├── .env                ← Your secret Supabase credentials
└── README.md           ← This guide
```

---

## 🗂️ PART 1: SUPABASE SETUP

### STEP 1: Create a New Project

1. After logging in, you'll see the Supabase dashboard
2. Click the **"New Project"** button
3. Fill in the details:
   - **Organization**: Select your personal account (or create one if prompted)
   - **Project Name**: Type `complaint-portal` (or any name you like)
   - **Database Password**: Create a strong password and **SAVE IT SOMEWHERE SAFE**
     ⚠️ You'll need this if you ever want to access the database directly
   - **Region**: Choose the region closest to you (e.g., South Asia for India)
   - **Pricing Plan**: Make sure **Free** is selected (it should be by default)
4. Click **"Create new project"**
5. ⏳ Wait about 1-2 minutes while Supabase sets up your project
   (You'll see a loading screen — this is normal!)

---

### STEP 2: Create the "complaints" Table

This is where ALL your complaint data will be stored.

1. In your Supabase project dashboard, look at the **left sidebar**
2. Click **"Table Editor"** (it has a table/grid icon)
3. Click the green **"Create a new table"** button
4. In the "Name" field, type exactly: `complaints`
5. ✅ Make sure **"Enable Row Level Security (RLS)"** is **UNCHECKED** (turned off)
6. Now add columns. By default, `id` and `created_at` are already there.
   Here's what each column should look like:

---

#### Column Setup :

The table already has:
| Column Name | Type |
|-------------|------|
| `id` | uuid (auto-generated — leave as is) |
| `created_at` | timestamptz (auto-set — leave as is) |

Now click **"Add column"** to add these NEW columns:

**Column 1:**
- Name: `title`
- Type: `text`
- Default Value: (leave empty)
- Nullable: ✅ (unchecked — meaning required)

**Column 2:**
- Name: `description`
- Type: `text`
- Nullable: ✅

**Column 3:**
- Name: `sentiment`
- Type: `text`
- Nullable: ✅

**Column 4:**
- Name: `urgency`
- Type: `text`
- Nullable: ✅

**Column 5:**
- Name: `priority`
- Type: `text`
- Nullable: ✅

**Column 6:**
- Name: `status`
- Type: `text`
- Default Value: `Pending`  ← Type this exactly
- Nullable: ✅

7. Click **"Save"** (green button at the bottom)
8. ✅ Your `complaints` table is now created!

---

#### 🖥️ Alternative: Use SQL Editor Instead

Instead of adding columns manually, you can run this SQL:

1. In the left sidebar, click **"SQL Editor"**
2. Click **"New query"**
3. Paste this SQL code:

```sql
CREATE TABLE complaints (
  id          uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  title       text NOT NULL,
  description text NOT NULL,
  sentiment   text,
  urgency     text,
  priority    text,
  status      text DEFAULT 'Pending',
  created_at  timestamptz DEFAULT now()
);
```

4. Click the **"Run"** button (or press Ctrl+Enter)
5. You should see: `Success. No rows returned`
6. ✅ Table created!

---

## 🔧 PART 2: PYTHON ENVIRONMENT SETUP

### STEP 3: Create Project Folder & Open Terminal

1. Create a folder somewhere on your computer, e.g.:
   - Windows: `C:\Users\YourName\Desktop\complaint_management`
   - Mac/Linux: `~/Desktop/complaint_management`

2. Copy all the project files into this folder:
   - `app.py`
   - `ai_analysis.py`
   - `database.py`
   - `requirements.txt`
   - `.env.example`

3. Open **Terminal** (Mac/Linux) or **Command Prompt** (Windows) in that folder:
   - Windows: Right-click inside the folder → "Open in Terminal" or type `cmd` in the address bar
   - Mac: Right-click folder → "New Terminal at Folder"


---

### STEP 4: Install Required Libraries

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` — The web UI framework
- `supabase` — Python library to connect to Supabase
- `python-dotenv` — To read your .env file
- `nltk` — Natural Language Toolkit (for sentiment analysis)
- `pandas` — For data handling in tables

---

## 🔑 PART 3: CONFIGURE CREDENTIALS

### STEP 5: Create Your .env File

1. In your project folder, create a new file called exactly: `.env`
   - ⚠️ Note: The filename starts with a dot. On Windows, you may need to create it via Notepad.
   - In Notepad: File → Save As → type `.env` → Save as type: "All Files (*.*)"
2. Open `.env` and add your Supabase credentials
3. Save the file
4. ✅ Done! Your credentials are now secured.

---

## 🚀 PART 4: RUNNING THE APP

### STEP 6: Start the Streamlit App

## 🛠️ PART 5: ADMIN DASHBOARD USAGE

1. Click the **"📊 Admin Dashboard"** tab
2. You'll see:
   - Summary metrics (total, critical, pending, resolved)
   - Filter dropdowns for Priority and Status
   - Full complaints table with color-coded badges
3. To update a status:
   - Use the dropdown to select a complaint
   - Select the new status (Pending / In Progress / Resolved)
   - Click "💾 Update Status"
4. Click "🔄 Refresh Data" to see latest changes

---

## 📊 How the AI Logic Works

### Sentiment Analysis (VADER)
VADER (Valence Aware Dictionary and sEntiment Reasoner) is a pre-built tool in the NLTK library.
It gives every word a sentiment score, then combines them for an overall score.
- Compound score > 0.05 → Positive
- Compound score < -0.05 → Negative
- In between → Neutral internet or API key needed — it runs completely on your computer!

### Urgency Detection
Simple keyword matching. We have a list of ~40 urgency-related words.
If ANY of those words appear in the complaint text, urgency = "High".

### Priority Matrix
```
IF  (Sentiment == Negative) AND (Urgency == High)  →  Critical
IF  (Urgency == High)                               →  High
IF  (Sentiment == Negative)                         →  Medium
ELSE                                                →  Low
```

---

*Built for college project demonstration. Runs 100% locally.*
