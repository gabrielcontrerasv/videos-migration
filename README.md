Webex to Azure Blob Migration App

This application is designed to migrate data from Webex to Azure Blob using Python, Docker, MySQL, and remote connections. The application utilizes Python to connect to Webex and MySQL to extract data from the Webex database. The extracted data is then uploaded to Azure Blob using remote connections.
Prerequisites

Before running this application, the following components are required:

    Python
    Docker
    MySQL
    Azure Blob Storage account
    Webex credentials with read access to the desired data

Installation

To install and run this application, follow these steps:

    Clone the repository to your local machine.
    Configure the MySQL and Azure Blob Storage credentials in the config.json file.
    Build the Docker image using the following command: docker build -t webex-azure-migration .
    Run the Docker container using the following command: docker run webex-azure-migration

Usage

The application is designed to migrate the following data from Webex to Azure Blob:

    Meetings
    Participants
    Recordings

To initiate the migration, run the main.py file using the following command:

css

python main.py

The application will prompt you to select the data you wish to migrate. Once selected, the application will initiate the migration process.
Support

For any issues or questions regarding this application, please contact the developers at contact@example.com.
Contributing

We welcome contributions from the community. Please refer to the CONTRIBUTING.md file for instructions on how to contribute.
License

This project is licensed under the MIT License - see the LICENSE file for details.
