# HW7-TravelGuide-AI-Project

# Travel Guide AI – Homework 6  
**Author:** Zafar Adil  

---

## 📌 Project Purpose

The **Travel Guide AI** project is an AI-assisted travel planning application designed to help users explore the world more effectively during vacations or trips. Planning travel often requires juggling multiple variables such as budget, interests, accessibility needs, weather conditions, and daily scheduling. This project solves that problem by generating a **personalized, structured travel itinerary** through an intelligent, rule-driven workflow.

Rather than relying on manual research or static guides, this application dynamically assembles trip plans based on user preferences and constraints, making travel planning faster, more inclusive, and more data-informed.

### Relationship to AI & AI-Assisted Workflows
While the application does not rely on a large language model API, it demonstrates **AI-assisted design principles**, including:
- Decision logic that adapts outputs based on user inputs (interests, guardrails, budget)
- Automated itinerary generation using structured reasoning
- Simulated intelligence (weather forecasting, value scoring, activity selection)
- Assistive automation (PDF generation and summarization)

This mirrors real-world AI systems that combine heuristics, probabilistic data, and automation to enhance user decision-making.

---

## ⚙️ What the Code Does (High-Level Overview)

The project is implemented as an interactive **Streamlit web application** that performs the following tasks:

### Core Features
- **User Input Collection:**  
  Users enter destination, departure location, travel dates, budget range, interests, and accessibility or lifestyle guardrails.

- **AI-Assisted Itinerary Generation:**  
  The system dynamically creates a multi-day itinerary by selecting activities that align with the user's interests, constraints, and budget level.

- **Weather Forecast Simulation:**  
  Generates a 14-day mock weather forecast to help travelers anticipate conditions.

- **Value Score Analysis:**  
  Calculates an overall destination value score based on cost, exchange rate, and estimated daily expenses.

- **Accessibility & Safety Guardrails:**  
  Supports constraints such as wheelchair accessibility, dietary requirements, family-friendliness, and activity intensity.

- **PDF Travel Guide Generation:**  
  Produces a professional, downloadable PDF containing:
  - Cover page
  - Trip overview
  - Weather summary
  - Value score analysis
  - Detailed daily itinerary
  - Packing checklist

### AI-Related Logic
- Rule-based decision systems emulate intelligent planning behavior
- Context-aware activity filtering based on guardrails
- Automated summarization and document generation
- Session-based state management to preserve user workflows
pip install streamlit reportlab pillow requests

## ▶️ How to Run or Use the Project

### Prerequisites
Ensure Python 3.9+ is installed.

### Installation
Install the required dependencies:
--- bash 
pip install streamlit reportlab pillow requests

Run the Application
From the project directory:

streamlit run travel_guide_python.py

Usage Flow
Open the Streamlit app in your browser
Enter travel details (destination, dates, budget)
Select interests and accessibility guardrails
Click Generate Itinerary
Review the generated travel plan
Download the complete PDF travel guide

=============================================================================================

🔐 Security & Safe Sharing Instructions (Required)

To ensure safe use and responsible sharing of this project:
No API Keys Stored:
The application does not store or transmit API keys, credentials, or personal authentication data.

No Persistent Personal Data:
User inputs are handled only in memory via Streamlit session state and are not saved to disk or databases.

Safe to Share Publicly:
The project can be shared on GitHub or academic platforms without exposing sensitive information.

PDF Content Awareness:
Generated PDFs may contain user-entered travel details. Users should review documents before sharing them externally.

Dependency Security:
Always install dependencies from trusted sources (PyPI) and keep packages updated to avoid vulnerabilities.


✅ Educational Value
This project demonstrates:
Applied AI-assisted system design
User-centric automation
Ethical handling of user data
Practical use of Python for intelligent applications
It is suitable for coursework, portfolio presentation, and foundational AI workflow demonstrations.

---


```bash
