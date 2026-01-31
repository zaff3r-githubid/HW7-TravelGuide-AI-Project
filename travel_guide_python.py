"""
Travel Guide - AI-Powered Trip Planner
A comprehensive travel planning application with weather forecasts, value scores, and PDF generation.

Installation:
pip install streamlit reportlab pillow requests

Run:
streamlit run travel_guide.py
"""

import streamlit as st
import datetime
from datetime import timedelta
import random
from io import BytesIO
import traceback

# PDF imports with error handling
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER
    PDF_AVAILABLE = True
except ImportError as e:
    PDF_AVAILABLE = False
    st.error(f"⚠️ PDF generation not available. Install reportlab: pip install reportlab")

# Page configuration
st.set_page_config(
    page_title="Travel Guide AI",
    page_icon="✈️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #4F46E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    .activity-card {
        background-color: #F9FAFB;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #4F46E5;
        margin-bottom: 1rem;
    }
    .weather-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .value-score {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = None
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = None
if 'value_score' not in st.session_state:
    st.session_state.value_score = None
if 'pdf_error' not in st.session_state:
    st.session_state.pdf_error = None
if 'form_key' not in st.session_state:
    st.session_state.form_key = 0

# Interest options
INTERESTS = {
    '🎨 Museums & Art': 'museums',
    '🍽️ Food & Cuisine': 'food',
    '🏛️ Historic Sites': 'historic',
    '🌙 Nightlife': 'nightlife',
    '🌲 Nature & Outdoors': 'nature',
    '🛍️ Shopping': 'shopping',
    '🧗 Adventure Sports': 'adventure',
    '💆 Wellness & Spa': 'wellness',
    '📷 Photography': 'photography',
    '🎭 Local Culture': 'culture',
    '🏖️ Beach Activities': 'beach'
}

# Guardrail options
GUARDRAILS = {
    'Accessibility': [
        'wheelchair_accessible',
        'stroller_accessible',
        'no_stairs',
        'elevator_required'
    ],
    'Activity Level': [
        'no_walking_tours',
        'limited_walking',
        'indoor_only',
        'outdoor_only'
    ],
    'Family & Age': [
        'kids_friendly',
        'family_friendly',
        'teen_appropriate',
        'senior_friendly'
    ],
    'Dietary': [
        'vegetarian_required',
        'vegan_required',
        'halal_available',
        'kosher_available',
        'gluten_free'
    ],
    'Comfort & Safety': [
        'english_speaking_staff',
        'well_lit_areas',
        'high_safety_rating',
        'lgbtq_friendly'
    ],
    'Transportation': [
        'public_transit_accessible',
        'walking_distance',
        'parking_available'
    ],
    'Budget': [
        'free_activities_only',
        'low_cost_preferred',
        'no_premium_experiences'
    ]
}

def generate_weather_forecast(days=14):
    """Generate mock weather data"""
    weather_conditions = ['sunny', 'partly_cloudy', 'cloudy', 'rainy']
    forecast = []
    
    for i in range(days):
        temp = random.randint(65, 85)
        condition = random.choice(weather_conditions)
        precipitation = random.randint(0, 30) if condition == 'rainy' else random.randint(0, 10)
        
        forecast.append({
            'day': i + 1,
            'temp': temp,
            'condition': condition,
            'precipitation': precipitation,
            'uv_index': random.randint(3, 10)
        })
    
    return forecast

def calculate_value_score(destination, budget):
    """Calculate value score for destination"""
    return {
        'overall': round(random.uniform(7.0, 9.5), 1),
        'cost_of_living': round(random.uniform(6.5, 9.0), 1),
        'exchange_rate': round(random.uniform(7.0, 9.5), 1),
        'value_rating': round(random.uniform(7.5, 9.5), 1),
        'avg_daily_cost': {
            'budget': 75,
            'moderate': 150,
            'luxury': 300,
            'ultra': 500
        }.get(budget, 150)
    }

def generate_itinerary(destination, days, interests, guardrails, budget):
    """Generate complete trip itinerary"""
    itinerary_days = []
    
    # Activity templates based on interests
    morning_activities = {
        'museums': ('Local Art Museum', 'Explore contemporary and classical art collections', 15, 'culture'),
        'nature': ('National Park Exploration', 'Scenic trails and wildlife viewing', 0, 'nature'),
        'historic': ('Historical Walking Tour', 'Discover ancient architecture and stories', 10, 'historic'),
        'food': ('Food Market Tour', 'Sample local delicacies and fresh produce', 20, 'food'),
        'wellness': ('Morning Yoga Session', 'Beach-side meditation and stretching', 25, 'wellness')
    }
    
    afternoon_activities = {
        'shopping': ('Artisan Market Visit', 'Local crafts and unique souvenirs', 0, 'shopping'),
        'beach': ('Beach Time & Water Sports', 'Relax or try snorkeling/surfing', 30, 'beach'),
        'culture': ('Cultural Center Tour', 'Traditional performances and exhibits', 12, 'culture'),
        'adventure': ('Adventure Activity', 'Zip-lining or rock climbing experience', 50, 'adventure'),
        'photography': ('Photo Walk Tour', 'Capture stunning vistas and street scenes', 15, 'photography')
    }
    
    evening_activities = {
        'nightlife': ('Rooftop Bar Experience', 'Panoramic views with cocktails', 40, 'nightlife'),
        'food': ('Fine Dining Experience', 'Local specialties in authentic setting', 60, 'food'),
        'culture': ('Traditional Show', 'Music and dance performance', 25, 'culture')
    }
    
    free_only = 'free_activities_only' in guardrails
    kids_friendly = 'kids_friendly' in guardrails
    no_walking = 'no_walking_tours' in guardrails
    
    for day_num in range(1, days + 1):
        activities = []
        
        # Morning activity
        morning_choices = [k for k in morning_activities.keys() if k in interests or not interests]
        if morning_choices:
            choice = random.choice(morning_choices)
            title, desc, cost, activity_type = morning_activities[choice]
            if free_only:
                cost = 0
            if no_walking and 'walking' in title.lower():
                title = title.replace('Walking', 'Bus')
            
            activities.append({
                'time': '9:00 AM - 11:30 AM',
                'title': title,
                'description': desc,
                'cost': cost,
                'type': activity_type,
                'energy': 'medium'
            })
        
        # Lunch
        lunch_cost = 15 if budget == 'budget' else 25 if budget == 'moderate' else 45
        if free_only:
            lunch_cost = 15
        
        activities.append({
            'time': '12:00 PM - 1:30 PM',
            'title': 'Vegetarian Café' if 'vegetarian_required' in guardrails else 'Local Cuisine Restaurant',
            'description': 'Authentic local flavors and regional specialties',
            'cost': lunch_cost,
            'type': 'food',
            'energy': 'low'
        })
        
        # Afternoon activity
        afternoon_choices = [k for k in afternoon_activities.keys() if k in interests or not interests]
        if afternoon_choices:
            choice = random.choice(afternoon_choices)
            title, desc, cost, activity_type = afternoon_activities[choice]
            if free_only:
                cost = 0
            
            activities.append({
                'time': '2:00 PM - 5:00 PM',
                'title': title,
                'description': desc,
                'cost': cost,
                'type': activity_type,
                'energy': 'medium'
            })
        
        # Dinner
        dinner_cost = 20 if budget == 'budget' else 35 if budget == 'moderate' else 65
        if free_only:
            dinner_cost = 20
        
        activities.append({
            'time': '6:30 PM - 8:00 PM',
            'title': 'Dinner at Local Restaurant',
            'description': 'Traditional dishes in cozy atmosphere',
            'cost': dinner_cost,
            'type': 'food',
            'energy': 'low'
        })
        
        # Evening activity
        if not kids_friendly and 'nightlife' in interests:
            choice = 'nightlife'
        else:
            evening_choices = [k for k in evening_activities.keys() if k in interests or not interests]
            choice = random.choice(evening_choices) if evening_choices else 'culture'
        
        if choice in evening_activities:
            title, desc, cost, activity_type = evening_activities[choice]
            if free_only or kids_friendly:
                title = 'Evening Stroll'
                desc = 'Family-friendly walk along waterfront'
                cost = 0
                activity_type = 'nature'
            
            activities.append({
                'time': '8:30 PM - 10:00 PM',
                'title': title,
                'description': desc,
                'cost': cost,
                'type': activity_type,
                'energy': 'low'
            })
        
        total_cost = sum(a['cost'] for a in activities)
        walking_dist = '0.5 km' if no_walking else f'{random.randint(3, 8)} km'
        
        theme = 'Arrival & Orientation' if day_num == 1 else \
                'Farewell & Departure' if day_num == days else \
                f'Day {day_num} Exploration'
        
        itinerary_days.append({
            'day': day_num,
            'theme': theme,
            'activities': activities,
            'total_cost': total_cost,
            'walking_distance': walking_dist
        })
    
    return itinerary_days

def generate_pdf(destination, departure, start_date, days, itinerary, weather_data, value_score, interests, guardrails):
    """Generate comprehensive PDF travel guide"""
    try:
        if not PDF_AVAILABLE:
            raise ImportError("ReportLab not installed")
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        story = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#4F46E5'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1F2937'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Cover Page
        story.append(Spacer(1, 2*inch))
        story.append(Paragraph(f"Your Travel Guide to {destination}", title_style))
        story.append(Paragraph(f"{days}-Day Personalized Itinerary", styles['Normal']))
        story.append(Spacer(1, 0.5*inch))
        story.append(Paragraph(f"Departing from: {departure}", styles['Normal']))
        story.append(Paragraph(f"Travel Dates: {start_date}", styles['Normal']))
        story.append(PageBreak())
        
        # Trip Overview
        story.append(Paragraph("Trip Overview", heading_style))
        overview_data = [
            ['Destination', destination],
            ['Duration', f'{days} days'],
            ['Departure', departure],
            ['Budget Level', f"${value_score['avg_daily_cost']}/day"],
            ['Total Activities', str(sum(len(day['activities']) for day in itinerary))],
            ['Estimated Total Cost', f"${sum(day['total_cost'] for day in itinerary)}"]
        ]
        overview_table = Table(overview_data, colWidths=[2.5*inch, 3.5*inch])
        overview_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(overview_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Weather Forecast Summary
        story.append(Paragraph("14-Day Weather Forecast", heading_style))
        avg_temp = sum(w['temp'] for w in weather_data[:14])//14
        rainy_days = sum(1 for w in weather_data[:14] if w['condition'] == 'rainy')
        weather_summary = f"Average Temperature: {avg_temp} F | Rainy Days: {rainy_days}"
        story.append(Paragraph(weather_summary, styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Value Score
        story.append(Paragraph("Value Score Analysis", heading_style))
        value_data = [
            ['Overall Value', f"{value_score['overall']}/10"],
            ['Cost of Living', f"{value_score['cost_of_living']}/10"],
            ['Exchange Rate', f"{value_score['exchange_rate']}/10"],
            ['Est. Daily Cost', f"${value_score['avg_daily_cost']}"]
        ]
        value_table = Table(value_data, colWidths=[3*inch, 3*inch])
        value_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F0FDF4')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#22C55E')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('PADDING', (0, 0), (-1, -1), 8)
        ]))
        story.append(value_table)
        story.append(PageBreak())
        
        # Daily Itinerary
        story.append(Paragraph("Detailed Daily Itinerary", heading_style))
        
        for day in itinerary:
            story.append(Paragraph(f"Day {day['day']}: {day['theme']}", heading_style))
            story.append(Paragraph(f"Walking Distance: {day['walking_distance']} | Daily Cost: ${day['total_cost']}", styles['Italic']))
            story.append(Spacer(1, 0.1*inch))
            
            # Activities table
            activity_data = [['Time', 'Activity', 'Cost']]
            for act in day['activities']:
                activity_data.append([
                    act['time'],
                    f"{act['title']}\n{act['description']}",
                    f"${act['cost']}" if act['cost'] > 0 else "Free"
                ])
            
            activity_table = Table(activity_data, colWidths=[1.5*inch, 3.5*inch, 1*inch])
            activity_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F9FAFB')),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('PADDING', (0, 0), (-1, -1), 6)
            ]))
            story.append(activity_table)
            story.append(Spacer(1, 0.3*inch))
        
        # Packing List
        story.append(PageBreak())
        story.append(Paragraph("Packing List", heading_style))
        packing_items = [
            "Passport & Travel Documents",
            "Travel Insurance Information",
            "Credit Cards & Cash",
            "Phone Charger & Power Adapter",
            "Comfortable Walking Shoes",
            "Weather-appropriate Clothing",
            "Sunscreen & Sunglasses",
            "Camera & Accessories",
            "Medications & First Aid",
            "Reusable Water Bottle"
        ]
        for item in packing_items:
            story.append(Paragraph(f"☐ {item}", styles['Normal']))
            story.append(Spacer(1, 0.05*inch))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        st.session_state.pdf_error = str(e)
        st.error(f"PDF Generation Error: {str(e)}")
        st.error(f"Full traceback: {traceback.format_exc()}")
        return None

# Header
st.markdown('<div class="main-header">✈️ Travel Guide AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Your Personalized Trip Planner</div>', unsafe_allow_html=True)

# Display PDF status
if not PDF_AVAILABLE:
    st.warning("⚠️ PDF export not available. Please install: `pip install reportlab`")

# Main Form
with st.container():
    st.markdown("### 📋 Plan Your Trip")
    
    col1, col2 = st.columns(2)
    
    with col1:
        destination = st.text_input("🌍 Destination", placeholder="e.g., Paris, Tokyo, Bali", key=f"destination_{st.session_state.form_key}")
        start_date = st.date_input("📅 Start Date", datetime.date.today(), key=f"start_date_{st.session_state.form_key}")
        days = st.slider("📆 Number of Days", 1, 30, 7, key=f"days_{st.session_state.form_key}")
        budget = st.selectbox("💰 Budget Range", 
                             ['budget', 'moderate', 'luxury', 'ultra'],
                             format_func=lambda x: {
                                 'budget': 'Budget-Friendly ($50-100/day)',
                                 'moderate': 'Moderate ($100-200/day)',
                                 'luxury': 'Luxury ($200-400/day)',
                                 'ultra': 'Ultra-Luxury ($400+/day)'
                             }[x],
                             key=f"budget_{st.session_state.form_key}")
    
    with col2:
        departure = st.text_input("🛫 Departing From", placeholder="e.g., New York, London", key=f"departure_{st.session_state.form_key}")
        end_date = st.date_input("📅 End Date", start_date + timedelta(days=days-1), key=f"end_date_{st.session_state.form_key}")
        st.info(f"💡 End date is automatically calculated as {days} days from start date")
        
    st.markdown("### 🎯 Select Your Interests")
    interest_cols = st.columns(4)
    selected_interests = []
    
    for idx, (label, value) in enumerate(INTERESTS.items()):
        with interest_cols[idx % 4]:
            if st.checkbox(label, key=f"interest_{value}_{st.session_state.form_key}"):
                selected_interests.append(value)
    
    # Guardrails
    with st.expander("🛡️ Guardrails & Accessibility Options"):
        guardrail_selections = []
        
        for category, options in GUARDRAILS.items():
            st.markdown(f"**{category}**")
            cols = st.columns(3)
            for idx, option in enumerate(options):
                with cols[idx % 3]:
                    label = option.replace('_', ' ').title()
                    if st.checkbox(label, key=f"guard_{option}_{st.session_state.form_key}"):
                        guardrail_selections.append(option)

# Action Buttons
col1, col2, col3 = st.columns([3, 1, 1])

with col1:
    if st.button("🎯 Generate Itinerary", type="primary", use_container_width=True):
        if not destination or not departure:
            st.error("Please enter both destination and departure location!")
        else:
            with st.spinner("Generating your perfect trip... ✨"):
                # Generate data
                st.session_state.weather_data = generate_weather_forecast(14)
                st.session_state.value_score = calculate_value_score(destination, budget)
                st.session_state.itinerary = generate_itinerary(
                    destination, days, selected_interests, 
                    guardrail_selections, budget
                )
                st.session_state.pdf_error = None
                st.success("✅ Itinerary generated successfully!")
                st.rerun()

with col2:
    if st.button("🔄 Reset Form", use_container_width=True):
        st.session_state.itinerary = None
        st.session_state.weather_data = None
        st.session_state.value_score = None
        st.session_state.pdf_error = None
        st.session_state.form_key += 1  # Increment to reset all form fields
        st.rerun()

# Display Results
if st.session_state.weather_data and st.session_state.value_score:
    st.markdown("---")
    
    # Weather Forecast
    st.markdown("### 🌤️ 14-Day Weather Forecast")
    weather_cols = st.columns(7)
    for idx, day in enumerate(st.session_state.weather_data[:14]):
        with weather_cols[idx % 7]:
            icon = {'sunny': '☀️', 'partly_cloudy': '⛅', 'cloudy': '☁️', 'rainy': '🌧️'}[day['condition']]
            st.markdown(f"""
            <div class="weather-box">
                <div style="font-size: 2rem;">{icon}</div>
                <div><strong>Day {day['day']}</strong></div>
                <div style="font-size: 1.5rem;">{day['temp']}°F</div>
                <div style="font-size: 0.8rem;">{day['precipitation']}% rain</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # Value Score
    st.markdown("### 💎 Value Score Analysis")
    score_cols = st.columns(4)
    score_data = [
        ("Overall Value", st.session_state.value_score['overall'], "⭐"),
        ("Cost of Living", st.session_state.value_score['cost_of_living'], "🏠"),
        ("Exchange Rate", st.session_state.value_score['exchange_rate'], "💱"),
        ("Daily Cost", f"${st.session_state.value_score['avg_daily_cost']}", "💰")
    ]
    
    for idx, (label, value, icon) in enumerate(score_data):
        with score_cols[idx]:
            st.markdown(f"""
            <div class="value-score">
                <div style="font-size: 2rem;">{icon}</div>
                <div style="font-size: 2rem; font-weight: bold;">{value}</div>
                <div>{label}</div>
            </div>
            """, unsafe_allow_html=True)

# Display Itinerary
if st.session_state.itinerary:
    st.markdown("---")
    st.markdown(f"### 🗺️ Your {days}-Day Itinerary")
    
    # Download PDF button
    if PDF_AVAILABLE:
        try:
            pdf_buffer = generate_pdf(
                destination, departure, str(start_date), days,
                st.session_state.itinerary, st.session_state.weather_data,
                st.session_state.value_score, selected_interests, guardrail_selections
            )
            
            if pdf_buffer:
                st.download_button(
                    label="📥 Download Complete PDF Guide",
                    data=pdf_buffer,
                    file_name=f"travel_guide_{destination.replace(' ', '_').lower()}.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=False
                )
                st.success("✅ PDF ready for download!")
            else:
                st.error("❌ PDF generation failed. Check error messages above.")
        except Exception as e:
            st.error(f"❌ PDF Error: {str(e)}")
            st.code(traceback.format_exc())
    else:
        st.info("💡 Install reportlab to enable PDF download: `pip install reportlab`")
    
    st.markdown("")
    
    # Display each day
    for day in st.session_state.itinerary:
        with st.expander(f"**Day {day['day']}: {day['theme']}** - ${day['total_cost']} | {day['walking_distance']}", expanded=day['day']==1):
            for activity in day['activities']:
                st.markdown(f"""
                <div class="activity-card">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <div style="color: #4F46E5; font-weight: bold; margin-bottom: 0.5rem;">
                                {activity['time']} • {activity['type'].upper()}
                            </div>
                            <div style="font-size: 1.1rem; font-weight: bold; margin-bottom: 0.3rem;">
                                {activity['title']}
                            </div>
                            <div style="color: #6B7280;">
                                {activity['description']}
                            </div>
                            <div style="margin-top: 0.5rem; font-size: 0.9rem; color: #9CA3AF;">
                                Energy Level: {activity['energy'].title()}
                            </div>
                        </div>
                        <div style="text-align: right; margin-left: 1rem;">
                            <div style="font-size: 1.5rem; font-weight: bold; color: #1F2937;">
                                {'FREE' if activity['cost'] == 0 else f"${activity['cost']}"}
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # Trip Summary
    st.markdown("### 📊 Trip Summary")
    summary_cols = st.columns(4)
    total_cost = sum(day['total_cost'] for day in st.session_state.itinerary)
    total_activities = sum(len(day['activities']) for day in st.session_state.itinerary)
    
    summary_cols[0].metric("Total Days", days)
    summary_cols[1].metric("Total Cost", f"${total_cost}")
    summary_cols[2].metric("Avg Daily Cost", f"${total_cost//days}")
    summary_cols[3].metric("Total Activities", total_activities)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6B7280; padding: 2rem;">
    <p><strong>Travel Guide AI</strong> - Making your dream trips a reality</p>
    <p>Built with ❤️ for adventurers worldwide</p>
</div>
""", unsafe_allow_html=True)