from flask import Flask, render_template, send_file, redirect
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
import seaborn as sns


app = Flask(__name__)

# Define MySQL connection parameters
host = 'localhost'
database = 'student_data'
user = 'dev_user'
password = 'newuser123'
db_url = f'mysql+pymysql://{user}:{password}@{host}/{database}'

# Create MySQL engine
engine = create_engine(db_url)

file_path = "student-mat.csv"  # Update this with the correct file path
df = pd.read_csv(file_path, delimiter=";")

# Function to connect to MySQL database
def connect_to_mysql():
    return engine

# Function to create tables in MySQL database
def create_tables(conn):
    with conn.connect() as con:
        query = """
            CREATE TABLE IF NOT EXISTS student1 (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                school VARCHAR(2),
                sex CHAR(1),
                age INT,
                address CHAR(1),
                famsize CHAR(3),
                Pstatus CHAR(1),
                Medu INT,
                Fedu INT,
                Mjob VARCHAR(20),
                Fjob VARCHAR(20),
                reason VARCHAR(20),
                guardian VARCHAR(20),
                traveltime INT,
                studytime INT,
                failures INT,
                schoolsup CHAR(3),
                famsup CHAR(3),
                paid CHAR(3),
                activities CHAR(3),
                nursery CHAR(3),
                higher CHAR(3),
                internet CHAR(3),
                romantic CHAR(3),
                famrel INT,
                freetime INT,
                goout INT,
                Dalc INT,
                Walc INT,
                health INT,
                absences INT
            )
        """
        con.execute(text(query))
        print("Student table created successfully")

        query = """
            CREATE TABLE IF NOT EXISTS grade1 (
                student_id INT,
                course VARCHAR(20),
                G1 INT,
                G2 INT,
                G3 INT,
                PRIMARY KEY (student_id, course),
                FOREIGN KEY (student_id) REFERENCES student1(student_id)
            )
        """
        con.execute(text(query))
        print("Grade table created successfully")

# Function to perform data cleaning and validation for Student table
def clean_student_data(df):
    # Your data cleaning and validation code here
    return df

# Function to perform data cleaning and validation for Grade table
def clean_grade_data(df):
    # Your data cleaning and validation code here
    return df

# Function to load data into MySQL database for Student table
def load_student_data_to_mysql(conn, df):
    try:
        df.to_sql("student1", con=conn, if_exists='replace', index=False)
        print("Data inserted into Student table successfully")
    except Exception as e:
        print("Error while loading data to MySQL for Student table", e)

# Function to load data into MySQL database for Grade table
def load_grade_data_to_mysql(conn, df):
    try:
        df.to_sql("grade1", con=conn, if_exists='replace', index=False)
        print("Data inserted into Grade table successfully")
    except Exception as e:
        print("Error while loading data to MySQL for Grade table", e)

@app.route('/')
def index():
    # Render the index.html template
    return render_template('index.html')


@app.route('/histogram')
def histogram():
    plt.figure(figsize=(8, 6))
    sns.histplot(df['G1'], bins=10)
    plt.title('Histogram of G1 Grades')
    plt.xlabel('G1 Grade')
    plt.ylabel('Frequency')
    plt.savefig('static/histogram.png')  # Save plot as static image
    return render_template('histogram.html')

# Route to render Age Distribution
@app.route('/age_distribution')
def age_distribution():
    # Generate plot
    plt.figure(figsize=(8, 6))
    df['age'].hist(bins=10, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title('Age Distribution of Students')
    plt.xlabel('Age')
    plt.ylabel('Frequency')
    plt.savefig('static/age_distribution.png')  # Save plot as static image
    
    return render_template('age_distribution.html')

@app.route('/parent_education')
def parent_education():
    # Generate plots
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Mother's education level
    df['Medu'].hist(bins=5, ax=axes[0], color='skyblue', edgecolor='black', alpha=0.7)
    axes[0].set_title("Mother's Education Level")
    axes[0].set_xlabel('Education Level')
    axes[0].set_ylabel('Frequency')

    # Father's education level
    df['Fedu'].hist(bins=5, ax=axes[1], color='skyblue', edgecolor='black', alpha=0.7)
    axes[1].set_title("Father's Education Level")
    axes[1].set_xlabel('Education Level')
    axes[1].set_ylabel('Frequency')

    plt.tight_layout()
    plt.savefig('static/parent_education.png')  # Save plot as static image

    # Pass the filename of the saved image to the template
    return render_template('parent_education.html', plot_image='static/parent_education.png')

# Route to render Reasons for Choosing School
@app.route('/reasons_for_school_choice')
def reasons_for_school_choice():
    # Generate plot
    plt.figure(figsize=(8, 6))
    df['reason'].value_counts().plot(kind='bar', color='skyblue')
    plt.title('Reasons for Choosing School')
    plt.xlabel('Reason')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/reasons_for_school_choice.png')  # Save plot as static image

    # Pass the filename of the saved image to the template
    return render_template('reasons_for_school_choice.html', plot_image='static/reasons_for_school_choice.png')

# Route to render Guardian Distribution
@app.route('/guardian_distribution')
def guardian_distribution():
    # Generate plot
    plt.figure(figsize=(8, 6))
    df['guardian'].value_counts().plot(kind='pie', autopct='%1.1f%%', colors=['skyblue', 'lightgreen', 'lightcoral'])
    plt.title('Guardian Distribution')
    plt.ylabel('')
    plt.tight_layout()
    plt.savefig('static/guardian_distribution.png')  # Save plot as static image

    # Pass the filename of the saved image to the template
    return render_template('guardian_distribution.html', plot_image='static/guardian_distribution.png')

@app.route('/travel_time')
def travel_time():
    # Generate plot
    plt.figure(figsize=(8, 6))
    df['traveltime'].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.title('Travel Time to School')
    plt.xlabel('Travel Time')
    plt.ylabel('Frequency')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('static/travel_time.png')  # Save plot as static image

    # Pass the filename of the saved image to the template
    return render_template('travel_time.html', plot_image='static/travel_time.png')

# Route to render Study Time
@app.route('/study_time')
def study_time():
    # Generate plot
    plt.figure(figsize=(8, 6))
    df['studytime'].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.title('Study Time Distribution')
    plt.xlabel('Study Time')
    plt.ylabel('Frequency')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('static/study_time.png')  # Save plot as static image

    # Pass the filename of the saved image to the template
    return render_template('study_time.html', plot_image='static/study_time.png')

# Route to render Family Relationship Quality
@app.route('/family_relationship')
def family_relationship():
    # Generate plot
    plt.figure(figsize=(8, 6))
    df['famrel'].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.title('Family Relationship Quality')
    plt.xlabel('Quality Rating')
    plt.ylabel('Frequency')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('static/family_relationship.png')  # Save plot as static image

    # Pass the filename of the saved image to the template
    return render_template('family_relationship.html', plot_image='static/family_relationship.png')

# Route to render Free Time After School
@app.route('/free_time')
def free_time():
    # Generate plot
    plt.figure(figsize=(8, 6))
    df['freetime'].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.title('Free Time After School')
    plt.xlabel('Free Time')
    plt.ylabel('Frequency')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig('static/free_time.png')  # Save plot as static image

    # Pass the filename of the saved image to the template
    return render_template('free_time.html', plot_image='static/free_time.png')

@app.route('/load_data')
def load_data():
    # Load data from CSV
    file_path = "student-mat.csv"  
    df = pd.read_csv(file_path, delimiter=";")

    # Clean and validate data for Student table
    student_df = clean_student_data(df)

    # Clean and validate data for Grade table
    grade_df = clean_grade_data(df)

    # Connect to MySQL
    conn = connect_to_mysql()

    if conn:
        # Create tables in MySQL
        create_tables(conn)

        # Load data into MySQL for Student table
        load_student_data_to_mysql(conn, student_df)

        # Load data into MySQL for Grade table
        load_grade_data_to_mysql(conn, grade_df)

        # Close connection
        conn.dispose()

    # Redirect to the index route after loading data
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
