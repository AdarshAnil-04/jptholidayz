import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from apps.core.models import SiteSettings

def generate_booking_itinerary_pdf(booking):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    settings_obj = SiteSettings.load()
    elements = []
    
    styles = getSampleStyleSheet()
    
    # Custom Brand Palette (Derived from JPT Holidays Official Logo)
    PLUM = colors.HexColor('#732E4E')
    SKY_BLUE = colors.HexColor('#8BB8C7')
    NAVY = colors.HexColor('#0F172A')
    CHARCOAL = colors.HexColor('#334155')
    LIGHT_BG = colors.HexColor('#F8FAFC')
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PLUM
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=SKY_BLUE
    )
    
    heading_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=NAVY,
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=CHARCOAL
    )
    
    bold_body_style = ParagraphStyle(
        'BoldBodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=NAVY
    )

    # 1. Header
    elements.append(Paragraph(f"<b>JPT HOLIDAYS</b>", title_style))
    elements.append(Paragraph(f"{settings_obj.tagline} | Contact: {settings_obj.contact_email}", subtitle_style))
    elements.append(Spacer(1, 10))
    elements.append(HRFlowable(width="100%", thickness=2.5, color=PLUM, spaceAfter=15))

    # 2. Document Title
    elements.append(Paragraph(f"CONFIRMED TRAVEL ITINERARY & RESERVATION VOUCHER", heading_style))
    elements.append(Spacer(1, 8))

    # 3. Booking Details Grid Table
    details_data = [
        [
            Paragraph("<b>Booking Reference:</b>", bold_body_style),
            Paragraph(booking.reference_code, body_style),
            Paragraph("<b>Booking Status:</b>", bold_body_style),
            Paragraph(booking.get_status_display(), bold_body_style),
        ],
        [
            Paragraph("<b>Lead Passenger:</b>", bold_body_style),
            Paragraph(booking.guest_name, body_style),
            Paragraph("<b>Travel Date:</b>", bold_body_style),
            Paragraph(booking.travel_date.strftime('%B %d, %Y'), body_style),
        ],
        [
            Paragraph("<b>Email Address:</b>", bold_body_style),
            Paragraph(booking.guest_email, body_style),
            Paragraph("<b>No. of Travelers:</b>", bold_body_style),
            Paragraph(f"{booking.adults_count} Adults, {booking.children_count} Children", body_style),
        ],
        [
            Paragraph("<b>Destination:</b>", bold_body_style),
            Paragraph(booking.package.destination.name, body_style),
            Paragraph("<b>Duration:</b>", bold_body_style),
            Paragraph(f"{booking.package.duration_days} Days / {booking.package.duration_nights} Nights", body_style),
        ],
    ]

    t = Table(details_data, colWidths=[120, 150, 110, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 15))

    # 4. Package Summary & Financial Summary
    elements.append(Paragraph("Package Information & Pricing Breakdown", heading_style))
    financial_data = [
        [Paragraph("<b>Package Title:</b>", bold_body_style), Paragraph(booking.package.title, body_style)],
        [Paragraph("<b>Total Quoted Price:</b>", bold_body_style), Paragraph(f"${booking.total_quoted_price:,.2f}", bold_body_style)],
        [Paragraph("<b>Amount Paid to Date:</b>", bold_body_style), Paragraph(f"${booking.amount_paid:,.2f}", body_style)],
        [Paragraph("<b>Balance Due:</b>", bold_body_style), Paragraph(f"${booking.amount_due:,.2f}", bold_body_style)],
    ]
    t2 = Table(financial_data, colWidths=[150, 380])
    t2.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(t2)
    elements.append(Spacer(1, 15))

    # 5. Day-by-Day Itinerary Breakdown
    elements.append(Paragraph("Day-by-Day Itinerary", heading_style))
    itinerary_days = booking.package.itinerary_days.all().order_by('day_number')
    
    if itinerary_days.exists():
        for day in itinerary_days:
            elements.append(Paragraph(f"<b>Day {day.day_number}: {day.title}</b>", bold_body_style))
            elements.append(Paragraph(day.description, body_style))
            if day.accommodation or day.meals or day.activities:
                details_text = []
                if day.meals: details_text.append(f"Meals: {day.meals}")
                if day.accommodation: details_text.append(f"Hotel: {day.accommodation}")
                if day.transport: details_text.append(f"Transport: {day.transport}")
                elements.append(Paragraph(f"<i>{ ' | '.join(details_text) }</i>", body_style))
            elements.append(Spacer(1, 8))
    else:
        elements.append(Paragraph(booking.package.overview, body_style))
        elements.append(Spacer(1, 10))

    # 6. Inclusions & Exclusions
    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Inclusions & Exclusions", heading_style))
    inc_exc_data = [
        [
            Paragraph("<b>Included Services:</b>", bold_body_style),
            Paragraph("<b>Excluded Services:</b>", bold_body_style)
        ],
        [
            Paragraph("<br/>".join([f"• {item}" for item in booking.package.inclusions_list]), body_style),
            Paragraph("<br/>".join([f"• {item}" for item in booking.package.exclusions_list]), body_style)
        ]
    ]
    t3 = Table(inc_exc_data, colWidths=[265, 265])
    t3.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('BACKGROUND', (0,0), (-1,0), LIGHT_BG),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(t3)
    elements.append(Spacer(1, 15))

    # 7. Terms & Footer Disclaimer
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=10))
    disclaimer = (
        "<b>Important Notice:</b> This document serves as an itinerary voucher for JPT Holidays. "
        "Specific airline tickets, hotel check-in keys, or local tour vouchers will be provided prior to departure. "
        "Passport validity must be at least 6 months beyond intended departure date. For urgent assistance, contact "
        f"{settings_obj.contact_phone} or email {settings_obj.contact_email}."
    )
    elements.append(Paragraph(disclaimer, ParagraphStyle('Disc', parent=body_style, fontSize=8, leading=11, textColor=colors.HexColor('#64748B'))))

    doc.build(elements)
    buffer.seek(0)
    return buffer
