import os
import json
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListItem, ListFlowable, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Global spacing factors (adjust these to control spacing)
LINE_SPACING_FACTOR = 1.4
SECTION_GAP = 2  # Control the gap between major sections
SUBSECTION_GAP = 8  # Control the gap between subsections
INDENTATION_LEVEL = 3  # Control the indentation level for job role bullets
NAME_GAP = 2  # Gap between name and location
LOCATION_GAP = 0  # Gap between location and first section title

# Global page margin variables
RIGHT_MARGIN = 64
LEFT_MARGIN = 64
TOP_MARGIN = 64
BOTTOM_MARGIN = 32

# Font configuration
FONT_NAME = 'LibreBaskerville'
FONT_FILE = 'fonts/LibreBaskerville-Regular.ttf'
FONT_BOLD_FILE = 'fonts/LibreBaskerville-Bold.ttf'
FONT_ITALIC_FILE = 'fonts/LibreBaskerville-Italic.ttf'

# Register the font
pdfmetrics.registerFont(TTFont(f'{FONT_NAME}', FONT_FILE))
pdfmetrics.registerFont(TTFont(f'{FONT_NAME}-Bold', FONT_BOLD_FILE))
pdfmetrics.registerFont(TTFont(f'{FONT_NAME}-Italic', FONT_ITALIC_FILE))

pdfmetrics.registerFontFamily(FONT_NAME, normal=FONT_NAME, bold=f'{FONT_NAME}-Bold', italic=f'{FONT_NAME}-Italic')


def create_resume(data, timestamp=None):
    # Extract data from the JSON structure
    category = data['category']
    emphasis = data['emphasis']
    content = data['content']
    skills = data['skills']
    certifications = data['certifications']
    projects = data['projects']
    location = data['location']
    name = data['name']
    email = data['email']
    education = data.get('education', [])
    references = data.get('references', [])

    # Create output directory with timestamp
    if timestamp is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Use os.path.join for all path operations to ensure cross-platform compatibility
    output_dir = os.path.join('outputs', timestamp, category.replace('/', '_').replace(" ", "_") + "_" + location.replace('/', '_').replace(" ", "_"))

    # Create all necessary directories
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.join(output_dir, f"{name} - Resume.pdf")

    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=RIGHT_MARGIN, leftMargin=LEFT_MARGIN,
                            topMargin=TOP_MARGIN, bottomMargin=BOTTOM_MARGIN)

    styles = getSampleStyleSheet()

    # Update styles to use the same font and increased line height
    for style_name, style in styles.byName.items():
        if hasattr(style, 'fontName'):
            style.fontName = FONT_NAME
        if hasattr(style, 'fontSize') and hasattr(style, 'leading'):
            style.leading = style.fontSize * LINE_SPACING_FACTOR

    # Define custom styles
    base_style = ParagraphStyle('Base', fontName=FONT_NAME, fontSize=11, leading=11 * LINE_SPACING_FACTOR)
    styles.add(ParagraphStyle('Justify', parent=base_style, alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle('LeftAlign', parent=base_style, fontSize=11, alignment=TA_LEFT))
    styles.add(ParagraphStyle('LeftAlignTwoColList', parent=base_style, fontSize=10, alignment=TA_LEFT, leading=11 * 1.2))
    styles.add(ParagraphStyle('Center', parent=base_style, alignment=TA_CENTER))
    styles.add(ParagraphStyle('Name', parent=base_style, alignment=TA_CENTER, fontSize=16, leading=16 * LINE_SPACING_FACTOR))
    styles.add(ParagraphStyle('JobTitle', parent=base_style, fontSize=12, leading=12 * LINE_SPACING_FACTOR, spaceAfter=4, keepWithNext=True))
    styles.add(ParagraphStyle('JobDetails', parent=base_style, fontSize=10, leading=10 * LINE_SPACING_FACTOR, spaceAfter=2, keepWithNext=True))
    styles.add(ParagraphStyle('SectionTitle', parent=styles['Heading2'], spaceAfter=SUBSECTION_GAP, keepWithNext=True))
    styles.add(ParagraphStyle('ProjectHeader', parent=styles['LeftAlign'], keepWithNext=True))
    styles.add(ParagraphStyle('EducationTitle', parent=styles['LeftAlign'], keepWithNext=True))
    styles.add(ParagraphStyle('ReferenceName', parent=styles['LeftAlign'], keepWithNext=True))

    story = []

    # Name and personal info
    story.append(Paragraph(name, styles['Name']))
    story.append(Spacer(1, NAME_GAP))
    story.append(Paragraph(f"{location}", styles['Center']))
    story.append(Paragraph(email, styles['Center']))
    story.append(Spacer(1, LOCATION_GAP))

    # Summary
    story.append(Paragraph("Summary", styles['SectionTitle']))
    story.append(Paragraph(emphasis, styles['Justify']))
    story.append(Spacer(1, SECTION_GAP))

    # Core Competencies
    story.append(Paragraph("Core Competencies", styles['SectionTitle']))

    # Build pairs of skills
    skills_pairs = []
    skills = list(set(skills))
    for i in range(0, len(skills), 2):
        skill1 = skills[i]
        if i + 1 < len(skills):
            skill2 = skills[i + 1]
        else:
            skill2 = ''
        skills_pairs.append((skill1, skill2))

    # Build and append each pair of skills as a separate two-cell table
    for skill1, skill2 in skills_pairs:
        row = [Paragraph(f"• {skill1}", styles['LeftAlignTwoColList']),
            Paragraph(f"• {skill2}", styles['LeftAlignTwoColList']) if skill2 else Paragraph('', styles['LeftAlignTwoColList'])]
        table = Table([row], colWidths=[225, 225])
        table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(table)

    story.append(Spacer(1, SECTION_GAP))

    # Professional Experience
    if content:
        story.append(Paragraph("Professional Experience", styles['SectionTitle']))

        for job in content:
            # Job header
            story.append(Paragraph(f"<b>{job['title']}</b>", styles['JobTitle']))
            story.append(Paragraph(f"{job['date']} | {job['location']}", styles['JobDetails']))

            # Duties
            for duty in job['duties']:
                indented_duty = f"{'&nbsp;' * INDENTATION_LEVEL}• {duty}"
                story.append(Paragraph(indented_duty, styles['LeftAlign']))

            story.append(Spacer(1, SUBSECTION_GAP))
    else:
        # If no content, just add the section title
        story.append(Paragraph("Professional Experience", styles['SectionTitle']))

    # Projects
    if projects:
        story.append(Paragraph("Selected Projects", styles['SectionTitle']))

        for project in projects:
            # Project Header
            story.append(Paragraph(f"<b>{project['name']}</b> ({project['date']})", styles['ProjectHeader']))

            # Description and link
            story.append(Paragraph(project['description'], styles['LeftAlign']))
            if 'link' in project:
                story.append(Paragraph(f"Link: {project['link']}", styles['LeftAlign']))
            story.append(Spacer(1, SUBSECTION_GAP))

    # Certifications
    if certifications:
        story.append(Paragraph("Certifications", styles['SectionTitle']))
        cert_list = [ListItem(Paragraph(cert, styles['LeftAlign'])) for cert in certifications]
        story.append(ListFlowable(cert_list, bulletType='bullet'))
        story.append(Spacer(1, SECTION_GAP))

    # Education
    if education:
        story.append(Paragraph("Education", styles['SectionTitle']))

        for edu in education:
            # Education entry
            story.append(Paragraph(f"<b>{edu['degree']}</b>", styles['EducationTitle']))
            story.append(Paragraph(f"{edu['institution']}, {edu['location']} ({edu['date']})", styles['LeftAlign']))
            if 'details' in edu:
                for detail in edu['details']:
                    story.append(Paragraph(detail, styles['LeftAlign']))
            story.append(Spacer(1, SUBSECTION_GAP))

    # Professional References
    story.append(Paragraph("Professional References", styles['SectionTitle']))
    if references:
        for ref in references:
            story.append(Paragraph(f"<b>{ref['name']}</b>", styles['ReferenceName']))
            story.append(Paragraph(f"{ref['relationship']}, {ref['contact_info']}", styles['LeftAlign']))
            story.append(Spacer(1, SUBSECTION_GAP))
    else:
        story.append(Paragraph("Available upon request", styles['Normal']))

    doc.build(story)
    print(f"Created {filename}")


if __name__ == "__main__":
    # Load personal data
    with open('static_personal.json', 'r') as f:
        personal_data = json.load(f)

    # Load common data
    with open('static_common.json', 'r') as f:
        common_data = json.load(f)

    # Ensure 'jobs_data' directory exists
    if not os.path.exists('jobs_data'):
        os.makedirs('jobs_data')

    # Get list of job data files
    job_files = [f for f in os.listdir('jobs_data') if f.endswith('.json')]

    if not job_files:
        print("No job data files found in 'jobs_data' directory.")
        exit(1)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    total_resumes = 0

    # Generate resumes for each job category and location
    for job_file in job_files:
        with open(os.path.join('jobs_data', job_file), 'r') as f:
            job_input = json.load(f)

        for loc in personal_data['base_locations']:
            job_data = {
                "category": job_input["category"],
                "emphasis": job_input["emphasis"],
                "location": loc,
                "name": personal_data["personal_info"]["name"],
                "email": personal_data["personal_info"]["email"],
                "education": common_data.get("education", []),
                "references": personal_data.get("references", [])  # References now from static_personal.json
            }

            # Combine skills using categories
            skills_list = []
            category_keys = job_input.get('skill_categories', [])
            for key in category_keys:
                skills_from_category = common_data['common_skills'].get(key, [])
                skills_list.extend(skills_from_category)
            job_specific_skills = job_input.get('skills', [])
            skills_list.extend(job_specific_skills)
            job_data["skills"] = list(set(skills_list))

            # Combine certifications
            job_data["certifications"] = list(set(job_input.get("certifications", []) + common_data.get("common_certifications", [])))

            # Get content from experience_keys
            job_data["content"] = []
            for key in job_input.get("experience_keys", []):
                if key in common_data.get("common_experience", {}):
                    job_data["content"].append(common_data["common_experience"][key])
                else:
                    print(f"Warning: experience key '{key}' not found in common_experience")

            # Get projects from project_keys
            job_data["projects"] = []
            for key in job_input.get("project_keys", []):
                if key in common_data.get("all_projects", {}):
                    job_data["projects"].append(common_data["all_projects"][key])
                else:
                    print(f"Warning: project key '{key}' not found in all_projects")

            create_resume(job_data, timestamp=timestamp)
            total_resumes += 1

    print(f"Generated {total_resumes} resumes in the 'outputs/{timestamp}' directory.")
    if os.path.exists('latest_output'):
        os.system('rm -rf latest_output')
    os.system(f'cp -r outputs/{timestamp} latest_output')
    print("Copied the generated resumes to 'latest_output' folder.")