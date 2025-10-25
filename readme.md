
# 📸 Speed Camera System

A Python-based system for managing **violations**, **drivers**, **offenses**, and **speed cameras**. 
It uses **MySQL** for persistent data storage, **Poetry** for dependency management, and **Pytest** for testing. 
The project follows a clean architecture structure with separate layers for domain, service, and database. 
--- 

## 🧱 Project Structure
```
src/
├── config.py
├── database/
│ ├── connection.py
│ └── sql_file_executor.py
├── domain/
│ ├── entity.py
│ ├── repository.py
│ └── typed_dict.py
├── service/
│ ├── dto.py
│ └── violation_service.py
tests/
├── test_domain/
└── test_service/
```
## ⚙️ Requirements
 
- Python **3.13.2**
- MySQL (running instance) 
- Poetry (for managing dependencies)
- Docker & Docker Compose

--- 
## 🚀 Installation & Setup 
1️⃣ Clone the repository 
```bash
git clone https://github.com/DamianKowalczykDK/speed-camera-system.git
```
2️⃣ Create a virtual environment & install dependencies 
```bash
poetry install 
poetry shell 
```
3️⃣ Configure environment variables 

Create a .env file in the root directory with the following content:
```bash
DB_HOST=localhost 
DB_PORT=3307 
DB_NAME=db_1 
DB_USER=your_login 
DB_PASSWORD=your_password 
DB_POOL_SIZE=5 
```
4️⃣ Initialize the database (optional) You can execute SQL initialization scripts using the SqlFileExecutor class. 

## 🐳 Docker Setup
The project uses Docker Compose for easy setup of both the application and MySQL database.

1️⃣ Start the services From the root directory, run: 
```bash
docker-compose up -d  
```
## 🧩 Features 
The system provides a structured architecture for managing and analyzing traffic violations and related data using 
repositories and services.
### Core functionalities: 
- **Driver Management** – supports CRUD operations (create, read, update, delete) through the DriverRepository.
- **Speed Camera Management** – allows adding and retrieving speed camera data using the SpeedCameraRepository. 
- **Offense Management** – defines and manages traffic offenses including penalty points and fine amounts. 
- **Violation Registration** – records a violation that links a driver, a speed camera, and an offense. 
- **Driver Violation Lookup** – retrieves all offenses for a driver based on their registration number. 
- **Top Drivers by Penalty Points** – generates a ranking of drivers with the most accumulated penalty points. 
- **Popular Speed Cameras** – identifies speed cameras that have recorded the highest number of violations. 
- **Summary Statistics** – provides aggregated data such as total and average fines, total offenses, and penalty point summaries. 
- **SQL File Executor** – executes .sql files directly to initialize or update the database schema and data. 
- **Data Layers** – all data operations are organized into clear layers:
  - **repository** – direct database queries (CRUD + reports)
  - **service** – business logic orchestration
  - **dto** – data transfer between layers
  - **entity** – domain model representations
## 🧪 Tests & Coverage
Run all tests with coverage using:
- coverage 100% ✅
- View HTML coverage report online: https://damiankowalczykdk.github.io/speed-camera-system/
```bash
poetry run pytest --cov=src --cov-report=html 
poetry run poe test # Shortcut task defined in pyproject.toml to run tests
```
## 🧰 Tech Stack
- Python 3.13.2 
- MySQL 
- Poetry 
- Pytest 
- Inflection 
- Dotenv 
## 👤 Author 
Created by Damian Kowalczyk 
## 📝 License 
This project is licensed under the **MIT License**