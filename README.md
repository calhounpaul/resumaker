# Resume Generator

## Introduction

This repository generates customized resumes in PDF format using data from JSON files. It allows you to tailor your resume for different job categories and locations, emphasizing relevant skills, experiences, and projects for each position.

## Features

- **Customizable Content**: Combine personal, common, and job-specific data to create targeted resumes.
- **Multiple Locations**: Generate resumes for multiple base locations specified in your personal data.
- **Professional Formatting**: Uses the ReportLab library to produce well-formatted PDF resumes.
- **Easy Configuration**: Adjust global spacing, fonts, and styles directly in the script.

## Prerequisites

- Python 3.x
- [ReportLab](https://www.reportlab.com/) library (`pip install reportlab`)
- Fonts (SIL Open Font License v1.1):
  - `LibreBaskerville-Regular.ttf`
  - `LibreBaskerville-Bold.ttf`
  - `LibreBaskerville-Italic.ttf`

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/calhounpaul/resumaker
   cd resumaker
   ```

2. **Install Dependencies**

   ```bash
   pip3 install -r requirements.txt
   ```

3. **Add Fonts**

   Place the required font files in the `fonts/` directory.

## Directory Structure

- `generate.py`: Main script to generate resumes.
- `static_personal.json`: Your personal information and base locations.
- `static_common.json`: Common data like education, references, skills, and projects.
- `jobs_data/`: Directory containing job-specific JSON files.
- `fonts/`: Directory containing font files.
- `outputs/`: Generated resumes will be saved here.

## Data Preparation

### 1. Personal Data (`static_personal.json`)

Contains your personal information and preferred locations.

```json
{
  "personal_info": {
    "name": "John Doe",
    "email": "john.doe@example.com"
  },
  "base_locations": [
    "New York, NY",
    "San Francisco, CA"
  ]
}
```

### 2. Common Data (`static_common.json`)

Holds data shared across all resumes.

```json
{
  "education": [
    {
      "degree": "B.Sc. in Computer Science",
      "institution": "University of Example",
      "location": "Example City",
      "date": "2015 - 2019",
      "details": [
        "Graduated with honors",
        "Dean's List for all semesters"
      ]
    }
  ],
  "references": [
    {
      "name": "Jane Smith",
      "relationship": "Former Manager",
      "contact_info": "jane.smith@example.com"
    }
  ],
  "common_skills": [
    "Python",
    "JavaScript",
    "SQL"
  ],
  "common_certifications": [
    "Certified Scrum Master"
  ],
  "common_experience": {
    "exp_key_1": {
      "title": "Software Engineer",
      "date": "2019 - Present",
      "location": "Tech Corp",
      "duties": [
        "Developed scalable web applications",
        "Led a team of 5 junior developers"
      ]
    }
  },
  "all_projects": {
    "proj_key_1": {
      "name": "Open Source Contributor",
      "date": "2020",
      "description": "Contributed to open-source projects on GitHub",
      "link": "https://github.com/johndoe"
    }
  }
}
```

### 3. Job-Specific Data (`jobs_data/*.json`)

Create a JSON file for each job category in the `jobs_data/` directory.

Example (`jobs_data/software_engineer.json`):

```json
{
  "category": "Software Engineer",
  "emphasis": "Passionate software engineer with a focus on backend development and cloud technologies.",
  "skills": [
    "Django",
    "RESTful APIs"
  ],
  "certifications": [
    "AWS Certified Solutions Architect"
  ],
  "experience_keys": [
    "exp_key_1"
  ],
  "project_keys": [
    "proj_key_1"
  ]
}
```

## Usage

1. **Prepare Data Files**

   Ensure all JSON files are correctly set up as per the examples.

2. **Run the Script**

   ```bash
   python generate.py
   ```

3. **Find Your Resumes**

   Resumes will be generated in the `outputs/{timestamp}/` directory.

   Example output:

   ```
   Created outputs/20231020_123456/Software_Engineer_New_York,_NY/John Doe - Resume.pdf
   Generated 2 resumes in the 'outputs/20231020_123456' directory.
   ```

## Customization

- **Adjust Spacing and Fonts**

  Modify the global variables at the beginning of `generate.py` to tweak spacing, margins, and fonts.

- **Styles**

  Update the `styles` in the script to change font sizes, alignment, and other text properties.

## Contributing

Please open an issue or submit a pull request with improvements or bug fixes.