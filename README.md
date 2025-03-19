# DigiBANKER

## About the Project

DigiBANKER is a virtual AI-based Bank Manager that streamlines the banking experience. The platform guides users through:

1. Complete KYC process step-by-step
2. Video and optional text responses for loan applications
3. Automated processing of financial requests

Developed at the Standard Chartered Hackathon 2025.

## Features

- Guided KYC verification
- Video-based loan application processing
- AI-powered decision making
- Secure document handling
- Real-time application status

## Getting Started

### Prerequisites

- Node.js (v18 or higher)
- Python 3.9+
- MongoDB

### Frontend Setup

```bash
# Clone the repository
git clone https://github.com/nabhpatodi10/sc-hack.git

# Navigate to frontend directory
cd sc-hack

# Install dependencies
npm install

# Run the development server
npm run start
```

### Backend Setup

```bash
# Navigate to backend directory
cd digibanker/backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API server
python app.py
```

## Architecture

The application uses a microservices architecture:
- Frontend: React.js
- Backend: Python FastAPI
- AI Processing: TensorFlow/PyTorch
- Database: MongoDB

## Developed By

- [Tanmay Agrawal]
- [Tuhina Tripathi]
- [Pratyush Kumar Singh]
- [Nabh Patodi]
- [Kratika Dariyani]
- [Akanksha Rathore]

Created during Standard Chartered Hackathon 2025.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
