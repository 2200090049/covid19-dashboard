# COVID-19 Data Analysis & Visualization Dashboard

## Project Overview
A comprehensive COVID-19 data analysis and visualization dashboard built with Streamlit, showcasing global pandemic trends, country comparisons, and interactive visualizations.

## Features
- 📊 Real-time COVID-19 data from Our World in Data
- 🌍 Global statistics and trends
- 🔄 Interactive country comparisons
- 💉 Vaccination progress tracking
- ⚠️ Case fatality rate analysis
- 📱 Responsive dashboard design
- 📥 Data export functionality

## Technologies Used
- **Python**: Core programming language
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **Plotly**: Interactive data visualization
- **NumPy**: Numerical computing

## Data Source
- Our World in Data COVID-19 Dataset: https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- PyCharm IDE
- Git (for version control)

### Running the Application
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

3. Open your browser and navigate to `http://localhost:8501`

## Project Structure
```
covid19-dashboard/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation

```

## Dashboard Features

### Global Statistics
- Total confirmed cases
- Total deaths
- Total vaccinations
- Case fatality rate
- Daily new cases and deaths

### Interactive Visualizations
- Global trend charts
- Country comparison line charts
- Top countries bar charts
- Vaccination progress charts
- Case fatality rate analysis

### User Controls
- Date range selector
- Country selection for comparisons
- Metric selection (cases, deaths, etc.)
- Data filtering options

## Deployment
This application is configured for deployment on Streamlit Community Cloud with automatic updates from GitHub.

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request



## Acknowledgments
- Our World in Data for providing comprehensive COVID-19 datasets
- Streamlit team for the excellent web framework
- Plotly for interactive visualization capabilities
