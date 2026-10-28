# Multimodal Construction Intelligence Platform

**BuildWise AI** is an educational prototype for construction-site image review, preliminary cost planning, weather-aware advisories and a construction Q&A assistant.

## Features

- **Image review:** upload JPG/PNG/WebP images and inspect image dimensions, brightness, contrast and edge activity; download a CSV report.
- **Preliminary cost estimator:** calculate a base estimate, contingency and optional fees/tax allowance from editable assumptions.
- **Weather advisory:** receive general planning reminders using forecast values entered by the user. This does not fetch live weather.
- **Site assistant:** rule-based guidance works without a key. Add a Gemini API key to enable AI-generated responses.

## Run locally

1. Install Python 3.11 or newer.
2. Clone this repository and open its folder.
3. Create and activate a virtual environment.
4. Install dependencies:

   \`pip install -r requirements.txt\`

5. Start the app:

   \`streamlit run app.py\`

## Optional Gemini API key

Create \`.streamlit/secrets.toml\` locally:

\`\`\`toml
GEMINI_API_KEY = "your-api-key"
\`\`\`

Never commit API keys. On Streamlit Community Cloud, add \`GEMINI_API_KEY\` in the app's **Settings → Secrets** panel.

## Deploy

1. Push this repository to GitHub.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Create an app and select this repository, branch \`main\`, and main file \`app.py\`.
4. Deploy; wait for the build to complete and test each module.
5. Paste the resulting app URL into the Skill Wallet Demo Link field and this repository URL into its GitHub Link field.

## Limitations and responsible use

This is a portfolio prototype, not a certified construction system. It does **not** currently contain a trained computer-vision model for PPE detection or structural crack diagnosis. Image metrics are general image heuristics and must not be interpreted as safety or defect classifications. Cost outputs depend entirely on user-entered assumptions. Weather advice depends on manually entered forecast data. AI output can be wrong and must be reviewed.

Do not use this prototype to certify worker PPE compliance, structural integrity, construction costs, or site safety. Escalate safety-critical decisions to qualified professionals and follow applicable codes and project procedures.

## Suggested next milestones

- Add a labelled, ethically sourced dataset and evaluate a trained PPE/object-detection model.
- Add a validated crack-segmentation/classification pipeline with clear uncertainty reporting.
- Add authenticated access, role-based permissions, audit logging and test coverage before handling real project data.
- Evaluate the assistant against reviewed construction questions and document its limitations.
